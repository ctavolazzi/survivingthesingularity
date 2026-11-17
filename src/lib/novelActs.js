// The four acts of the novel, described once for the homepage and the
// preorder page. Titles and chapter ranges are the manuscript's own
// (src/lib/data/novel/book.json). The descriptions are site copy written from
// the manuscript; they stop short of each act's ending on purpose.
//
// `opening` is the novel's first sentence and `premise` is from the Author's
// Note, both verbatim. If the manuscript changes either, change them here.
export const novel = Object.freeze({
  opening:
    'The night Elijah Madrone ended three careers, he was drinking a ' +
    'four-dollar beer and trying to teach himself JavaScript.',
  premise:
    'Their story follows a man who wants machines to make his friends more ' +
    'capable, helps set off something with very different consequences, and ' +
    'has to learn what responsibility looks like after the demonstration.',
  forecast:
    'My call, for the record, has not changed since I first made it years ' +
    'ago: AGI by Thanksgiving 2027.',
  forecastDoubt: 'You can doubt my forecast.'
});

export const acts = Object.freeze([
  Object.freeze({
    num: 'Act One',
    title: 'The Bar',
    range: 'Chapters 0 to 5',
    desc:
      'Elijah Madrone is a farm kid and bar musician who taught himself to ' +
      'code. One night he shows three realtors what a chatbot can do. A week ' +
      'later they raise a glass to him for the three people they let go. He ' +
      'starts writing down what comes next.'
  }),
  Object.freeze({
    num: 'Act Two',
    title: 'The City',
    range: 'Chapters 6 to 15',
    desc:
      'A four-minute video makes him known to strangers. He says yes to ' +
      'everyone: the conference, the dinner on the hill, the young ' +
      'billionaire with the talking lamp. Then the attention runs out, and ' +
      'he is living in his truck in Stockton.'
  }),
  Object.freeze({
    num: 'Act Three',
    title: 'The Farm',
    range: 'Chapters 16 to 31',
    desc:
      'Nineteen households past Cloverdale hand him a broom. A welder, a ' +
      'grower and a twice-retrained warehouse worker teach him what his ' +
      'notebooks left out: hands, soil, and asking first.'
  }),
  Object.freeze({
    num: 'Act Four',
    title: 'Home',
    range: 'Chapters 32 to 39, and an afterword',
    desc:
      'The thing he predicted arrives, and not the way he wrote it. He has ' +
      'to work out what is his to change and what is not. It ends at ' +
      'Thanksgiving, 2027.'
  })
]);
