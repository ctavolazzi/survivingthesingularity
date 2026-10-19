#!/usr/bin/env python3
"""Build the portable decision desk from the original matrix and dated updates."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'matrix.json').read_text())
updates = {
    'D01': ('Author decision', 'Technical baseline recommended: PR24 source, PR26 editorial documents and selective foreword transfer. CT chooses the public edition and timing.'),
    'D02': ('Author decision', 'Food-first copy reached the public page. Older individual-escape copy and conflicting access labels remain in the 07:29 observation.'),
    'D03': ('Open', 'Actual payment, email and protected-download delivery remain unverified. Passing browser checks do not clear this gate.'),
    'D06': ('Verified candidate', 'PR29 replaces obsolete sign-in tests and fixes checklist reload data loss. 54 local cases and 540 Linux WebKit cases passed on code commit 780c5d4. Publication is separate.'),
    'D07': ('Author decision', 'Opening and ending comparison plans are ready. Foreword existence and CT ownership of v0.12 are already settled.'),
    'D09': ('Ready to prepare', 'The $5 offer, bounded continuing access, future membership exemption, separate print discount and no-account model were already ratified. Reconcile those terms across surfaces.'),
    'D11': ('Ready to prepare', 'Collect primary-source evidence for the requested foreword before the remaining wording decisions.'),
    'D12': ('Ready to prepare', 'Chapter 9 is the recommended author-led pilot. Agents assemble source, proposed cuts and seam references; CT supplies the prose.'),
    'D22': ('Release gate', 'An interim digital release can precede the complete rewrite. Physical proofs apply to print; each edition needs its relevant checks.'),
    'D25': ('Later', 'Defer platform expansion and preserve the no-account ruling. An existing future membership benefit is not a decision to build a membership platform.'),
    'D27': ('Maintenance', 'Archive coverage is timestamped. Strategy work is uploaded through 235e572 and browser repairs through 5b12396; later edits need their own preservation receipt.'),
}
titles = {'D09': 'Reconcile the ratified paid-offer terms', 'D06': 'Review the verified browser repair for integration'}
for row in data['options']:
    default = 'Later' if row['phase'] in ['Defer', 'Later', 'After gates'] else 'Release gate' if row['phase'] == 'Release gate' else 'Open'
    row['current_status'], row['update'] = updates.get(row['id'], (default, 'No later status update recorded. Use the dated assessment and its prerequisites below.'))
    row['current_title'] = titles.get(row['id'], row['option'])

e = lambda value: html.escape(str(value), quote=True)
keys = [c['id'] for c in data['criteria']]
weights = data['presets']['Balanced']

def score(row):
    return sum(w * row['ratings'][k] for k, w in zip(keys, weights)) * 20 / sum(weights)

def render_row(row):
    links = ' '.join(f'<a href="{e(url)}" aria-label="{e(row["id"])} source {i+1}" target="_blank" rel="noopener noreferrer">Source {i+1}</a>' for i, url in enumerate(row['sources']))
    ratings = ' · '.join(f'{e(c["label"])} {row["ratings"][c["id"]]}/5' for c in data['criteria'])
    dependencies = ', '.join(row['dependencies']) or 'None listed'
    conditional = row.get('conditions', '')
    if conditional:
        dependencies += '; ' + (', '.join(conditional) if isinstance(conditional, list) else str(conditional))
    return f'''<tr data-id="{e(row['id'])}" data-score="{score(row):.2f}">
      <td class="score-cell"><strong class="score">{score(row):.0f}</strong><span>/100</span></td>
      <td><details class="option"><summary><span class="option-id">{e(row['id'])}</span><span class="option-title">{e(row['current_title'])}</span><span class="expand" aria-hidden="true">+</span><span class="row-status">{e(row['current_status'])}</span></summary>
      <div class="option-body"><p class="update">{e(row['update'])}</p><p><b>Prerequisites:</b> {e(dependencies)}</p>
      <h4>Original assessment · 06:47–06:57 PDT</h4><p>{e(row['evidence'])}</p>
      <p><b>First step then:</b> {e(row['first_step'])}</p><p><b>Completion criterion:</b> {e(row['acceptance'])}</p>
      <p class="small">{ratings}. Evidence confidence: {e(row['evidence_confidence'])}.</p><div class="source-links">{links}</div></div>
      </details></td><td class="effort-cell">{e(row['effort'])}<span>{e(row['owner'])}</span></td></tr>'''

rows = sorted(data['options'], key=lambda r: (-score(r), r['id']))
controls = ''.join(f'''<div class="weight"><label for="weight-{e(c['id'])}">{e(c['label'])}<output id="output-{e(c['id'])}" for="weight-{e(c['id'])}">{c['weight']}%</output></label><input id="weight-{e(c['id'])}" data-key="{e(c['id'])}" type="range" min="0" max="100" step="1" value="{c['weight']}" aria-describedby="weight-help"><p>{e(c['definition'])}</p></div>''' for c in data['criteria'])
presets = ''.join(f'<button type="button" data-preset="{e(name)}" aria-pressed="{str(name == "Balanced").lower()}">{e(name)}</button>' for name in data['presets'])
payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
template = (ROOT / 'dashboard.template.html').read_text()
rendered = template.replace('@@ROWS@@', ''.join(render_row(r) for r in rows)).replace('@@CONTROLS@@', controls).replace('@@PRESETS@@', presets).replace('@@DATA@@', payload)
assert '@@' not in rendered
assert '\u2014' not in rendered
out = ROOT / 'next-steps.html'
out.write_text(rendered)
assert out.read_text() == rendered
print(f'Built {out.name}: {len(rows)} options, {len(rendered.encode()):,} bytes; assets and data embedded.')
