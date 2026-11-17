// WHAT THE BOOK IS, FOR EVERY LEGAL AND NEAR-LEGAL SURFACE.
//
// CT, 2026-11-17: "It's not intended to teach, predict, prescribe, or anything
// like that. It's just a book now, a novel, and should be treated as such."
//
// The disclaimer, the terms, the policies page, the footer and the reader all
// say this from here, so the site cannot call the book a novel on one page and
// "informational and educational" on another. That exact split existed until
// this file: the legal pages still described a nonfiction guide.
//
// NOT REVIEWED BY A LAWYER. A fiction notice shows intent; it does not by
// itself protect against a claim from a real person or company who can be
// recognised in the story (see the Authors Guild's "Libel in Fiction"
// analysis). The invented names below are the ones the Author's Note lists.
export const bookNotice = Object.freeze({
  // One line, for footers and small print.
  short: 'The book is a novel. It is not advice, a prediction to rely on, or a guide to follow.',

  fiction:
    'Surviving the Singularity is a work of fiction. Names, characters, ' +
    'businesses, places and events are products of the author’s ' +
    'imagination or are used fictitiously. Claypot, PorusAI, Silvana, Chat ' +
    'Horizon, Rod Code and Porchlight are invented, and so is every person ' +
    'in its pages. Any resemblance to actual persons, living or dead, or to ' +
    'actual companies or events, is coincidental.',

  realThings:
    'Real companies, products, publications and public events that the ' +
    'story mentions by name, such as the 2017 research paper “Attention ' +
    'Is All You Need”, appear as setting. No affiliation with, ' +
    'sponsorship by or endorsement from any of them is claimed or implied.',

  intent:
    'The book is not intended to teach, predict or prescribe. It is not a ' +
    'manual, a plan or a forecast, and nothing in it is professional advice ' +
    'of any kind.',

  story:
    'What characters do in the story, including welding, wiring, building, ' +
    'farming, living in a vehicle and taking a drug, is storytelling. It is ' +
    'not instruction, and it is not a recommendation.',

  opinion:
    'The Author’s Note and the Afterword are the author speaking for ' +
    'himself. They are his opinion, including his guess about when ' +
    'artificial general intelligence arrives. That guess is one person’s ' +
    'forecast and may be wrong; do not make decisions on it.',

  // Everything on the site that is not the novel: blog, checklist, the
  // countdown, the research feed, and the archived nonfiction draft.
  site:
    'The rest of this site (the blog, the checklist, the countdown, the ' +
    'research feed and the archived earlier draft) is the author’s ' +
    'commentary and general information. It is not professional advice.'
});
