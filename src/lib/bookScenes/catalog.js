/** Editorial descriptions also provide the nonvisual equivalent of each scene. */
export const sceneCatalog = {
  'food-delivery': {
    title: 'One harvest, five doors',
    file: 'v101-scene-food-delivery.svg',
    chapter: 'chapter9',
    description: 'An illustrative neighborhood food route, from the garden through packing to five households. The buildings show relationships, not a map or a measured service area.',
    alt: 'Isometric neighborhood model: a garden supplies eight usable kilograms, a food partner adds two, people pack the produce, and a delivery route reaches five homes with two kilograms each. Growing, handling, transport, and confirmation all remain part of the job.',
    caption: 'One harvest, five doors. Eight kilograms from the garden and two from the food partner keep the five-household promise. The buildings and route are illustrative; the vegetables supplement meals.',
    headings: ['Place or handoff', 'What the example requires'],
    rows: [
      ['Garden', 'Inspect the crop and equipment; harvest and weigh eight usable kilograms after the stated loss.'],
      ['Food partner', 'Supply the missing two kilograms before calling the delivery a success.'],
      ['Packing and transport', 'People sort, pack, handle, and deliver the food through the partner’s existing arrangements.'],
      ['Five households', 'Each receives two kilograms, free. Confirm receipt and whether people can use the food. This is a contribution to meals, not five complete diets.']
    ],
    options: [
      { id: 'all', label: 'Whole route', text: 'Eight kilograms from the garden plus two from the partner make ten: five deliveries of two kilograms. The work at every handoff still counts.' },
      { id: 'garden', label: 'Grow and check', text: 'The controller opens a valve. People inspect the crop, harvest, sort, and record the usable amount.' },
      { id: 'partner', label: 'Cover the shortfall', text: 'After the illustrative two-kilogram loss, the partner supplies the missing two. The five promised boxes keep their full weight.' },
      { id: 'homes', label: 'Reach each door', text: 'The result is checked at the recipient’s end: delivery received and food usable. Access does not require owning equipment or paying for a share.' }
    ],
    labels: [['GARDEN', '8 kg usable'], ['FOOD PARTNER', '+ 2 kg'], ['PEOPLE', 'Pack, drive, confirm'], ['FIVE HOMES', '2 kg each, free']],
    note: 'Illustrative route. Vegetables supplement meals.'
  },
  'living-soil': {
    title: 'A growing bed has an outside',
    file: 'v101-scene-living-soil.svg',
    chapter: 'chapter15',
    description: 'A soil cutaway separates exchanges inside the bed from inputs and outputs across its boundary. It is a conceptual view, not a construction plan or a measured soil profile.',
    alt: 'Three-dimensional growing-bed cutaway with crop leaves above mulch, branching roots in soil, a watering pipe, compost, and a harvested crate outside the bed. Sunlight and water enter; nutrients need replenishment, and harvested food carries nutrients away.',
    caption: 'The bed is part of a larger system. Plants, soil life, and returning organic matter exchange nutrients; sunlight, water, replenishment, and the nutrients carried away in harvest still cross its boundary. Conceptual cutaway, not a measured soil profile.',
    headings: ['Connection', 'What crosses or stays within the boundary'],
    rows: [
      ['Sunlight and water', 'Inputs reach the plants and soil; water also leaves through plants, evaporation, and drainage.'],
      ['Roots and soil life', 'Plants supply sugars. Organisms transform and release nutrients; different partnerships do different jobs.'],
      ['Compost and other replenishment', 'Returning organic matter supports the soil. Actual replacement needs depend on the crop, soil, and harvest.'],
      ['Harvest', 'Food leaves the bed and carries nutrients with it. Recycling some material does not make the garden self-sufficient forever.']
    ],
    options: [
      { id: 'all', label: 'Whole bed', text: 'Follow both the exchanges inside the bed and the inputs and outputs outside it. The arrows describe relationships, not measured quantities.' },
      { id: 'roots', label: 'Below the surface', text: 'Roots occupy a volume of soil. A reading near the surface cannot stand in for conditions throughout the root zone; observations have to be checked where the roots are.' },
      { id: 'inputs', label: 'What comes in', text: 'Sunlight, water, and replenishment enter from outside. Compost can return organic matter, but the actual needs must be checked.' },
      { id: 'harvest', label: 'What leaves', text: 'Harvested food carries nutrients out. Water also leaves the system. A useful recycling loop still has an outside.' }
    ],
    labels: [['INPUTS', 'Sun, water, replenishment'], ['WITHIN THE BED', 'Roots and soil life'], ['HARVEST', 'Nutrients leave in food'], ['WATER OUT', 'Plants, air, drainage']],
    note: 'Conceptual cutaway. Arrows are not quantities.'
  },
  'shared-workshop': {
    title: 'What keeps a workshop useful',
    file: 'v101-scene-shared-workshop.svg',
    chapter: 'chapter17',
    description: 'An open workshop model brings shared tools together with people, materials, power, maintenance, and the repair that leaves the bench. The scene is not a wiring or fabrication plan.',
    alt: 'Isometric open workshop with a 3D printer, a metalworking bench, a shared walk-behind tractor, a materials rack, and two people. Colored connections lead between the tools, the people who use and maintain them, incoming stock and spares, and a repaired part leaving the shop.',
    caption: 'Shared tools need a working arrangement around them: trained people, suitable power and materials, maintenance, and parts. The useful result leaves the bench. Illustrative workshop, not a fabrication or wiring plan.',
    headings: ['Dependency', 'Why it belongs in the picture'],
    rows: [
      ['People', 'Training, safe operation, shared access, and time for the work remain necessary.'],
      ['Materials and power', 'Stock, suitable supplies, and energy come from real arrangements outside the tool.'],
      ['Maintenance and spares', 'Documentation, compatible replacement parts, and repair skill keep equipment useful over time.'],
      ['Useful output', 'Judge the whole job and what it enables: a repair, a working tool, or a part that meets its intended requirements.']
    ],
    options: [
      { id: 'all', label: 'Whole workshop', text: 'The machines share a room, but usefulness comes from the whole arrangement: people, materials, power, maintenance, and a result someone needs.' },
      { id: 'people', label: 'People and time', text: 'Trained operators and maintainers remain in the picture. Sharing equipment does not make their time disappear.' },
      { id: 'supplies', label: 'Stock and spares', text: 'Feedstock, replacement parts, and suitable power cross the workshop boundary. Open plans do not eliminate these dependencies.' },
      { id: 'output', label: 'Useful result', text: 'Follow the part off the bench. Compare the whole job, including setup, supervision, maintenance, and the work people still do.' }
    ],
    labels: [['PEOPLE', 'Skill, access, time'], ['SUPPLIES', 'Stock, power, spares'], ['SHARED TOOLS', 'Operate and maintain'], ['USEFUL RESULT', 'A repair leaves the bench']],
    note: 'Illustrative workshop. Not a fabrication plan.'
  }
};

export const sceneIds = Object.keys(sceneCatalog);
export const sceneSize = { width: 960, height: 800 };
