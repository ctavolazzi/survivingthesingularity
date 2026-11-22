// Planning an edit to the manuscript Doc, and checking it afterwards.
//
// Nothing here talks to Google. A chat reads the Doc with its Docs connector
// (`read_doc`), hands the saved result to these functions, and sends the
// request they return with the connector's `update_doc`. That keeps one safe
// way of editing for every chat, whatever tools it has.
//
// The rules built in here were each learned on the live Doc:
//   - Change words by exact match, never by position. The author and other
//     chats type in the Doc while you work, so positions go stale in seconds.
//   - The match must appear exactly once in the whole Doc.
//   - Suggestions are the default. A suggestion deletes the matched words and
//     types them again, which drops italics and links on them, so keep the
//     match short and plain.

const DASHES = /[\u2013\u2014]/;

function runsOf(paragraph) {
  return (paragraph.elements ?? [])
    .filter((el) => el.textRun)
    .map((el) => {
      const style = el.textRun.textStyle ?? {};
      return {
        text: el.textRun.content ?? '',
        italic: Boolean(style.italic),
        bold: Boolean(style.bold),
        link: Boolean(style.link),
        inserted: (el.textRun.suggestedInsertionIds ?? []).length > 0,
        deleted: (el.textRun.suggestedDeletionIds ?? []).length > 0
      };
    });
}

/** The Doc as a list of paragraphs, each knowing which part of the book it is in. */
export function docParagraphs(read) {
  const doc = read?.content ?? read;
  const body = doc?.tabs?.[0]?.documentTab?.body?.content ?? [];
  const out = [];
  let section = '';
  for (const el of body) {
    if (!el.paragraph) continue;
    const runs = runsOf(el.paragraph);
    const text = runs.map((r) => r.text).join('').replace(/\n$/, '');
    const style = el.paragraph.paragraphStyle?.namedStyleType ?? 'NORMAL_TEXT';
    // A heading names the part of the book for everything under it. A heading
    // that is only a pending suggestion does not count yet.
    if (style === 'HEADING_1' && text.trim() && runs.some((r) => !r.inserted)) section = text.trim();
    out.push({ start: el.startIndex ?? 0, style, section, text, runs });
  }
  return out;
}

/** Document id and revision, for the request and for the record. */
export function docIdentity(read) {
  const doc = read?.content ?? read;
  return { documentId: doc?.documentId ?? '', title: doc?.title ?? '', revisionId: doc?.revisionId ?? '' };
}

/** Every place the words appear: [{section, paragraph}]. */
export function findMatches(read, find) {
  const hits = [];
  if (!find) return hits;
  for (const paragraph of docParagraphs(read)) {
    let at = paragraph.text.indexOf(find);
    while (at >= 0) {
      hits.push({ section: paragraph.section, paragraph, at });
      at = paragraph.text.indexOf(find, at + find.length);
    }
  }
  return hits;
}

/**
 * Plan one change. Returns {ok, problems, warnings, where, request}.
 * `request` is ready for the Docs connector's update_doc when ok is true.
 *
 * @param {object} read  a saved read_doc result
 * @param {{find: string, replace: string, direct?: boolean}} change
 *   direct: true makes a direct edit. Only when the author has said so, in so
 *   many words, in this conversation.
 */
export function planEdit(read, { find, replace, direct = false }) {
  const problems = [];
  const warnings = [];
  const { documentId, title, revisionId } = docIdentity(read);

  if (!find) problems.push('Nothing to find. Give the words to change.');
  if (replace === undefined || replace === null) problems.push('Nothing to put in their place.');
  if (find && find === replace) problems.push('The new words are the same as the old ones.');
  if (find && find.includes('\n')) problems.push('The words to find run across two paragraphs. Match inside one paragraph.');
  if (replace && DASHES.test(replace)) problems.push('The new words have an en dash or an em dash. The book uses neither.');

  const hits = find ? findMatches(read, find) : [];
  if (find && hits.length === 0) {
    problems.push('Those words are not in the Doc. Read the Doc again: it may have changed since your copy was made.');
  }
  if (hits.length > 1) {
    const places = [...new Set(hits.map((h) => h.section || 'before the first heading'))].join('; ');
    problems.push(`Those words appear ${hits.length} times (${places}). Add a few more words so the match appears once.`);
  }

  let where = null;
  if (hits.length === 1) {
    const { paragraph, at, section } = hits[0];
    where = { section, paragraph: paragraph.text };
    // Which runs does the match touch?
    let pos = 0;
    const touched = [];
    for (const run of paragraph.runs) {
      const end = pos + run.text.length;
      if (end > at && pos < at + find.length) touched.push(run);
      pos = end;
    }
    if (touched.some((r) => r.italic || r.bold || r.link)) {
      warnings.push('The match includes italic, bold or linked words. A suggestion will drop that styling. Match fewer words if you can.');
    }
    if (paragraph.runs.some((r) => r.inserted || r.deleted)) {
      warnings.push('That paragraph already has a suggestion waiting. Check with the author before adding another on top of it.');
    }
    if (find.length > 240) warnings.push('The match is long. Shorter matches are safer.');
  }

  const ok = problems.length === 0;
  return {
    ok,
    problems,
    warnings,
    where,
    document: { documentId, title, readAtRevision: revisionId },
    request: ok
      ? {
          documentId,
          writeControl: { writeMode: direct ? 'EDIT' : 'SUGGEST' },
          requests: [{ replaceAllText: { containsText: { text: find, matchCase: true }, replaceText: replace } }]
        }
      : null
  };
}

/**
 * The suggestions waiting in the Doc, in reading order. Each is
 * {section, text}, with new words as [+...] and removed words as [-...].
 */
export function pendingSuggestions(read) {
  const out = [];
  for (const paragraph of docParagraphs(read)) {
    if (!paragraph.runs.some((r) => r.inserted || r.deleted)) continue;
    const text = paragraph.runs
      .map((r) => {
        const words = r.text.replace(/\n$/, '');
        if (r.inserted) return `[+${words}]`;
        if (r.deleted) return `[-${words}]`;
        return words;
      })
      .join('');
    out.push({ section: paragraph.section, text });
  }
  return out;
}

/**
 * After sending a planned edit: is it in the Doc? Give a fresh read.
 * Returns {found, as}: as is 'suggestion', 'text', or null.
 */
export function verifyEdit(readAfter, { replace }) {
  const lines = String(replace ?? '').split('\n').filter((line) => line.trim());
  if (!lines.length) return { found: false, as: null };
  const paragraphs = docParagraphs(readAfter);
  let asSuggestion = true;
  for (const line of lines) {
    const holder = paragraphs.find((p) => p.text.includes(line));
    if (!holder) return { found: false, as: null };
    const inserted = holder.runs.filter((r) => r.inserted).map((r) => r.text).join('');
    if (!inserted.includes(line.slice(0, Math.min(24, line.length)))) asSuggestion = false;
  }
  return { found: true, as: asSuggestion ? 'suggestion' : 'text' };
}
