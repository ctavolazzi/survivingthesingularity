/**
 * Blueprint content data - The YouTube Shouse Blueprint
 * Each section maps to /blueprint/[section]
 */

export const sections = [
  {
    slug: 'economic-trap',
    number: '01',
    title: 'The Economic Trap',
    subtitle: 'The Death of the Old Dream & the Generational Wealth Gap',
    content: [
      {
        type: 'prose',
        text: `The 20th-century American Dream - characterized by a 30-year mortgage, corporate compliance, and status-seeking - is officially dead. The contemporary era is defined by a collapse in these traditional frameworks. The macro-economic landscape of 2026 is defined by a permanent reset of global purchasing power and a fundamental collapse of the post-war social contract.`
      },
      {
        type: 'prose',
        text: `Statistical data from the Bureau of Labor Statistics and the Federal Reserve confirms that the United States dollar has experienced a catastrophic erosion of value since early 2020. The cumulative inflation rate between January 2020 and early 2026 has reached approximately 25.23%, meaning that a dollar in 2026 retains only 79.8% of the purchasing power it held just six years prior.`
      },
      {
        type: 'table',
        title: 'Structural Erosion of Purchasing Power',
        headers: ['Economic Indicator', '2020 Baseline', '2026 Observation', 'Change'],
        rows: [
          ['Consumer Price Index (CPI-U)', '258.812', '324.122', '+25.23%'],
          ['Purchasing Power of $1.00', '$1.00', '$0.80', '-20.00%'],
          ['Home Price to Income Ratio', '3.5x (Boomer)', '6.3x (Millennial)', '+80.00%'],
          ['Gas Price (Avg/Gallon)', '$2.57', '$3.29', '+28.01%'],
          ['Electricity (per kWh)', '$0.13', '$0.19', '+46.15%'],
        ]
      },
      {
        type: 'table',
        title: 'Generational Wealth Distribution',
        headers: ['Generation', 'Population Share', 'Share of Total U.S. Wealth'],
        rows: [
          ['Silent/Earlier', '<10%', '12.1%'],
          ['Baby Boomers', '21%', '51.1%'],
          ['Generation X', '20%', '26.1%'],
          ['Millennials/Gen Z', '>40%', '10.7%'],
        ]
      },
      {
        type: 'prose',
        text: `This concentration is the result of liquidating the infrastructure - land and housing - that should have been the foundation for their descendants. Baby Boomers currently own 41% of all real estate in the United States, while Millennials hold only 21%, despite the latter cohort representing 34% of the home-owning aged population. Furthermore, one-third of Baby Boomers who own their homes report they will never sell.`
      },
      {
        type: 'prose',
        text: `The psychological impact of currency erosion is amplified by the "silent pay cut" phenomenon. For a household to maintain the same standard of living as in early 2020, nominal income must have increased by a minimum of 26%. Housing costs, which occupy approximately 34.9% of the average American household's spending, have increased by a staggering 43% since 2020, while food prices have risen by 31%.`
      },
      {
        type: 'callout',
        text: `The traditional path - mortgage, career ladder, retirement - is mathematically inaccessible. The new path requires building something different.`
      }
    ]
  },
  {
    slug: 'the-shouse',
    number: '02',
    title: 'The Shouse',
    subtitle: 'Steel Construction, the $8,000 Living Space, and Regulatory Navigation',
    content: [
      {
        type: 'prose',
        text: `The architectural manifestation of the shift away from traditional housing is the shouse - a portmanteau of "shop" and "house." Unlike the traditional suburban home, which prioritizes leisure and sleeping quarters, the shouse model flips the domestic hierarchy. It prioritizes the production space (the shop) as the primary engine of the property, with the living quarters reduced to a secondary, highly efficient partition.`
      },
      {
        type: 'table',
        title: 'Construction Cost Comparison',
        headers: ['Cost Component', 'Traditional Residential', 'YouTube Shouse Model'],
        rows: [
          ['Initial Acquisition/Build', '~$500,000', '~$100,000 - $175,000'],
          ['Building Material', 'Wood Frame / Drywall', 'Red Iron Steel / Metal Panels'],
          ['Foundation Cost', '~$14,500 (Standard)', '~$4 - $8 per sq. ft. (Slab)'],
          ['Cost per Square Foot', '~$150', '~$25 - $43 (Turnkey)'],
          ['Living Space Budget', 'Included in Total', '<$8,000 (Partition or RV)'],
          ['Primary Utility', 'Consumption / Leisure', 'Industrial Production'],
          ['Debt Service Term', '30 Years', '0 - 10 Years (Potential Cash Build)'],
        ]
      },
      {
        type: 'heading',
        text: 'Navigating the Regulatory Landscape'
      },
      {
        type: 'prose',
        text: `The primary obstacle to the shouse lifestyle is the complex intersection of state and local building regulations. For a shouse to be viable, it must navigate the definitions of occupancy groups. Group R-3 (Residential) applies to permanent residential occupancies. Group F (Factory Industrial) includes buildings used for fabricating and manufacturing. The challenge is that if the structure is attached to a commercial use, it requires full submittal of mechanical, plumbing, and electrical (MEP) plans.`
      },
      {
        type: 'table',
        title: 'RV Living Legality by Jurisdiction',
        headers: ['Jurisdiction Type', 'RV Living Status', 'Notes'],
        rows: [
          ['Urban (e.g., San Jose)', 'Prohibited (General)', 'Only allowed in "auto camps" or with 48-hour permits'],
          ['Rural (e.g., Lake County)', 'Temporary Only', 'Classified as vehicle, not residence'],
          ['Emergency (e.g., LA County)', 'Allowed (Restricted)', 'Specific to shelter crises or disaster recovery'],
          ['Private Land (Statewide)', 'Variable', 'Zoning laws often prohibit long-term use'],
        ]
      },
      {
        type: 'heading',
        text: 'The $8,000 Living Space'
      },
      {
        type: 'prose',
        text: `To stay within the $8,000 budget for a living space, the maker must adopt an industrial mindset. This is typically achieved by partitioning off a small corner of the shop, creating a "thermal envelope" within the larger structure. Insulation is the single most important investment.`
      },
      {
        type: 'table',
        title: 'Insulation Options',
        headers: ['Material', 'R-Value/Inch', 'Cost/Sq.Ft. (Installed)', 'Benefit'],
        rows: [
          ['Fiberglass Batts', '~3.5', '$0.50 - $2.50', 'Economical; easy to DIY'],
          ['Blown-in Cellulose', '~3.7', '$1.00 - $2.80', 'Superior ceiling coverage; fire resistant'],
          ['Closed-Cell Foam', '~7.0', '$3.00 - $8.00', 'Maximum R-value; acts as vapor barrier'],
          ['SIP Panels', 'Variable', '$5.00 - $10.00', 'Structural and insulated; fast assembly'],
        ]
      },
      {
        type: 'prose',
        text: `If choosing the travel trailer option, a used trailer can be purchased for under $5,000, leaving $3,000 for site preparation, a gravel pad, and a basic electrical hookup. The "pre-built" nature of the trailer handles most of the budget's requirements.`
      },
      {
        type: 'heading',
        text: 'The Community Shouse: Collective Property Ownership'
      },
      {
        type: 'prose',
        text: `The shouse model scales beyond the individual. A community shouse - sometimes called a "maker commons" or "cooperative homestead" - applies the same low-overhead industrial architecture to collective land ownership. Three to eight households pooling capital can acquire substantially more land per dollar and share the fixed costs of infrastructure: water well, solar array, septic system, and broadband. The individual unit cost drops by 40–60% while the total productive capacity multiplies.`
      },
      {
        type: 'table',
        title: 'Individual vs. Community Shouse Economics',
        headers: ['Variable', 'Solo Shouse (5 acres)', 'Community Shouse (30 acres / 6 units)'],
        rows: [
          ['Land acquisition', '~$30,000', '~$90,000 (~$15,000/unit)'],
          ['Infrastructure (well, septic, solar)', '~$35,000', '~$60,000 (~$10,000/unit)'],
          ['Per-unit steel shell build', '~$40,000', '~$35,000 (bulk material discount)'],
          ['All-in per household cost', '~$105,000', '~$60,000'],
          ['Productive food area (shared)', '0.25 acres', '4+ acres (~0.67 acres/unit)'],
          ['Monthly overhead per household', '~$600 - $900', '~$250 - $400'],
        ]
      },
      {
        type: 'heading',
        text: 'Legal Structures for Collective Ownership'
      },
      {
        type: 'prose',
        text: `Three structures dominate community land ownership in the current regulatory environment. Each trades governance complexity for different degrees of individual control and tax advantage.`
      },
      {
        type: 'table',
        title: 'Collective Ownership Structures',
        headers: ['Structure', 'Ownership Model', 'Exit Mechanism', 'Best For'],
        rows: [
          ['Tenancy in Common (TIC)', 'Fractional undivided interest', 'Sell individual share; buy-out required', 'Small groups (2-4), high trust'],
          ['LLC (Member-Managed)', 'Membership units = land rights', 'Operating agreement governs buyout', 'Flexibility; limits personal liability'],
          ['Community Land Trust (CLT)', 'Trust holds land; residents own improvements', 'Resale formula limits equity gain', 'Long-term affordability; mission-driven'],
          ['Agricultural Co-op', 'Member equity; patronage dividends', 'Share redemption per bylaws', 'Production-first; IRS 521 tax benefits'],
        ]
      },
      {
        type: 'prose',
        text: `The LLC model is the most common entry point for small groups. Draft an operating agreement that specifies: (1) decision rights by membership unit, (2) a right of first refusal if any member exits, (3) a formula for capital contributions and sweat equity conversion, and (4) minimum residency obligations to prevent absentee ownership drift. The Community Land Trust model is optimal when the primary goal is permanent affordability across generations - the trust retains ownership of the underlying land, permanently decoupling it from speculative markets.`
      },
      {
        type: 'callout',
        text: `The community shouse is not a commune. Each unit maintains a private living envelope and independent income streams. The shared layer is infrastructure and land - the most expensive and least movable assets. This is cooperative economics applied surgically to the parts of life where individual ownership is financially irrational.`
      }
    ]
  },
  {
    slug: 'content-engine',
    number: '03',
    title: 'The Content Engine',
    subtitle: 'YouTube, the One-Hour Rule, Faceless Channels, and Workshop Gear',
    content: [
      {
        type: 'prose',
        text: `The shouse lifestyle is not merely a cost-saving measure; it is a platform for the creation of a "Content Engine." Once the maker has suppressed their overhead, they must transition into the production phase.`
      },
      {
        type: 'heading',
        text: 'The One-Hour Rule'
      },
      {
        type: 'prose',
        text: `Teach ANY skill that you are good at that took you more than an hour to learn. This rule works because the most effective teacher for a beginner is often someone who has just mastered the skill themselves. An expert who has spent 30 years whittling spoons may have forgotten the initial frustrations; a maker who figured it out yesterday still understands exactly where the confusion lies.`
      },
      {
        type: 'callout',
        text: `The value of your content is directly proportional to the amount of time and frustration saved for the viewer. If it took you an afternoon to figure out, someone will pay to skip that frustration.`
      },
      {
        type: 'heading',
        text: 'The Faceless Advantage'
      },
      {
        type: 'prose',
        text: `In the faceless channel model, the brand is the maker's competence, not their personality. By pointing the lens at the workbench and clearly explaining the movements of the hands, the creator removes the pressure of "performing." Faceless channels are often more scalable because they focus entirely on the value of the information provided.`
      },
      {
        type: 'heading',
        text: 'Audio Engineering in a High-Noise Environment'
      },
      {
        type: 'prose',
        text: `Audio is the most critical element of educational content. In a workshop, the main challenge is signal-to-noise ratio. Dynamic microphones are preferred because they are less sensitive to ambient noise.`
      },
      {
        type: 'table',
        title: 'Microphone Selection',
        headers: ['Model', 'Connection', 'Type', 'Use Case'],
        rows: [
          ['Shure SM7B', 'XLR', 'Dynamic', 'Professional voiceover; best noise rejection'],
          ['Shure MV7', 'USB/XLR', 'Dynamic', 'Beginners; hybrid flexibility'],
          ['Rode PodMic', 'XLR', 'Dynamic', 'Budget-conscious; robust metal build'],
          ['Sennheiser MKE 600', 'XLR', 'Shotgun', 'Overhead mounting; out-of-frame audio'],
          ['DJI Mic 2', 'Wireless', 'Lav', 'Moving around large projects'],
        ]
      },
      {
        type: 'heading',
        text: 'The Overhead Camera Rig'
      },
      {
        type: 'table',
        title: 'Camera Rig Options',
        headers: ['Rig Type', 'Cost', 'Pros', 'Cons'],
        rows: [
          ['Standard Tripod', '~$15 - $100', 'Cheap; portable', 'Legs get in the shot'],
          ['C-Stand + Boom', '~$130 - $250', 'Rock-solid; professional', 'Takes up floor space'],
          ['Ceiling Rail', '~$300 - $600', 'Clean floor; max mobility', 'Permanent install'],
          ['Articulating Arm', '~$50 - $150', 'Precise; small footprint', 'Can vibrate on shaky surface'],
        ]
      },
      {
        type: 'heading',
        text: 'Camera Selection for 2026'
      },
      {
        type: 'prose',
        text: `DJI Osmo Pocket 3 is highly recommended for solo makers due to its 3-axis mechanical gimbal. The Sony ZV-E10 II is a mid-range powerhouse with shallow depth of field for cinematic workbench shots. The Panasonic Lumix GH7 is the professional choice with an internal cooling fan for filming heavy welding or machining.`
      }
    ]
  },
  {
    slug: 'digital-sovereignty',
    number: '04',
    title: 'Digital Sovereignty',
    subtitle: 'Local LLMs, VRAM Optimization, Llama 4, and the Sovereign Software Stack',
    content: [
      {
        type: 'prose',
        text: `Running Large Language Models locally is the ultimate privacy power move. By avoiding third-party APIs, individuals bypass the risk of their proprietary data being used for training or being subject to government subpoena. Local AI ensures that an individual's intelligence layer is as secure as their most sensitive database.`
      },
      {
        type: 'table',
        title: 'GPU Options for Local AI (2026)',
        headers: ['GPU Model', 'VRAM', 'Bandwidth', 'Ideal Workload'],
        rows: [
          ['NVIDIA RTX 3090', '24GB GDDR6X', '936 GB/s', 'Budget large VRAM; 7B-30B models'],
          ['NVIDIA RTX 4090', '24GB GDDR6X', '1,008 GB/s', 'Proven baseline; 30B models'],
          ['NVIDIA RTX 5090', '32GB GDDR7', '1,792 GB/s', 'Flagship; 70B models (quantized)'],
          ['Mac Studio M4 Ultra', '512GB (Shared)', '819 GB/s', 'Ultra-large models (up to 405B)'],
        ]
      },
      {
        type: 'heading',
        text: 'VRAM and Model Parameter Ratios'
      },
      {
        type: 'table',
        title: 'VRAM Requirements by Quantization',
        headers: ['Model Size', 'VRAM (FP16/Raw)', 'VRAM (Q4)', 'VRAM (Q2/IQ2)'],
        rows: [
          ['7B - 8B', '14GB - 16GB', '4GB - 5GB', '2GB - 3GB'],
          ['30B - 34B', '64GB+', '19GB - 20GB', '10GB - 12GB'],
          ['70B', '140GB+', '35GB - 40GB', '20GB - 22GB'],
          ['405B', '810GB+', '200GB+', '120GB+'],
        ]
      },
      {
        type: 'heading',
        text: 'Bandwidth and Throughput'
      },
      {
        type: 'table',
        title: 'Performance Benchmarks',
        headers: ['Setup', 'VRAM Total', 'Bandwidth', 'Speed (32B Q4)', 'Price (2026)'],
        rows: [
          ['Single RTX 5090', '32GB', '1,792 GB/s', '61 tok/s', '$2,500 - $3,800'],
          ['Dual RTX 3090 (Used)', '48GB', '936 GB/s', '30 tok/s', '$1,600 - $1,800'],
          ['Mac Studio M4 Max', '128GB', '400 GB/s', '40-60 tok/s', '$3,500 - $5,000'],
          ['DGX Spark / H100', '80GB', '2,000 GB/s', '150+ tok/s', '$25,000+'],
        ]
      },
      {
        type: 'heading',
        text: 'The Sovereign Software Stack'
      },
      {
        type: 'prose',
        text: `Engine Layer: Ollama or Llama.cpp for managing GGUF-quantized models. Interface Layer: Open WebUI or LM Studio for ChatGPT-like front-end. Workflow Builder: n8n for self-hosted RAG pipelines. Character Framework: WAFT for interactive world models and dynamic AI characters.`
      },
      {
        type: 'callout',
        text: `Recommended models: dolphin-3.0-llama-4-8b for instruction accuracy without refusal; qwen-2.5-coder-32b for superior coding performance.`
      },
      {
        type: 'heading',
        text: 'Offline AI for Healthcare'
      },
      {
        type: 'prose',
        text: `Healthcare is the most acute dependency most households have on corporate infrastructure. A single emergency room visit averages $2,200 out-of-pocket. Primary care is gated behind insurance, referral queues, and geographic access. Offline AI does not replace emergency medicine - it addresses the 80% of healthcare interactions that are informational: symptom triage, medication interactions, dosage guidance, chronic condition management, and mental health support.`
      },
      {
        type: 'prose',
        text: `A local medical RAG system combines a quantized LLM with a curated corpus of peer-reviewed literature (PubMed Open Access, Merck Manual, CDC guidelines) indexed into a local vector database. Queries never leave the hardware. The model has no financial incentive to upsell pharmaceuticals or procedures. For a rural shouse community 45 minutes from the nearest urgent care, this is the difference between a 3 AM panic spiral and a calibrated first-response decision.`
      },
      {
        type: 'table',
        title: 'Offline Healthcare AI Stack',
        headers: ['Layer', 'Tool', 'Purpose', 'Hardware Req.'],
        rows: [
          ['Inference engine', 'Ollama / llama.cpp', 'Run quantized medical LLM', 'RTX 3090 or M2 Pro+'],
          ['Medical knowledge base', 'PubMed OA + Merck Manual + UpToDate (offline export)', 'RAG source corpus', '~50GB SSD'],
          ['Vector database', 'ChromaDB or Qdrant (self-hosted)', 'Semantic search over corpus', '8GB RAM minimum'],
          ['RAG orchestration', 'Anything-LLM or Open WebUI (RAG mode)', 'Query routing + context injection', 'Same machine'],
          ['Wearable telemetry', 'Withings / Garmin local sync', 'Vital trends without cloud upload', 'Local WiFi only'],
          ['Emergency reference', 'Where There Is No Doctor (offline PDF + embedded)', 'Field-level triage guide', 'Offline-first'],
        ]
      },
      {
        type: 'table',
        title: 'Recommended Models for Medical Use Cases',
        headers: ['Model', 'Parameters', 'Strength', 'Use Case'],
        rows: [
          ['Med42-v2 (M42 Health)', '70B (Q4)', 'Clinical reasoning; trained on medical text', 'Symptom triage, DDx support'],
          ['BioMistral-7B', '7B (Q4)', 'Biomedical literature comprehension', 'Research summaries, drug interactions'],
          ['Llama 3.1-70B (uncensored)', '70B (Q4)', 'General reasoning; no refusals', 'Mental health support, frank discussion'],
          ['OpenBioLLM-70B', '70B (Q4)', 'USMLE-level medical knowledge', 'Detailed clinical questions'],
        ]
      },
      {
        type: 'prose',
        text: `Critical implementation notes: (1) All medical AI outputs are informational, not diagnostic. The stack must surface this disclaimer in the UI at every response. (2) The corpus must be version-controlled and updated quarterly - stale medical literature is worse than no literature. (3) For community deployments, run the stack on a dedicated machine accessible over local LAN - members can query from any device without internet. (4) Pair with a physical medical kit: tourniquets, wound closure strips, SAM splints, and a printed copy of "Where There Is No Doctor" - analog backup for power-out scenarios.`
      },
      {
        type: 'callout',
        text: `Medical sovereignty is not about avoiding doctors. It is about removing the information asymmetry between patient and system. When you can query 40 million peer-reviewed papers in 3 seconds on your own hardware, you walk into any clinical encounter as an equal.`
      }
    ]
  },
  {
    slug: 'physical-exit',
    number: '05',
    title: 'The Physical Exit',
    subtitle: 'Rural Land Acquisition, Butte County Zoning, Title 25, and RV Living',
    content: [
      {
        type: 'prose',
        text: `The goal of the digital cash engine is to fund an immediate physical exit from society's extractive grid. This involves purchasing marginal land, parking an RV, and dropping expenses to the bare minimum for survival.`
      },
      {
        type: 'heading',
        text: 'Land Acquisition in Butte County'
      },
      {
        type: 'prose',
        text: `Butte County, California, serves as a case study for strategic relocation. Median list prices for rural land sit around $199,000, but low-end farmland can be found for as little as $1,475 per acre. The primary driver for selection should be zoning accessibility and the ability to build independent structures.`
      },
      {
        type: 'table',
        title: 'Butte County Zoning Districts',
        headers: ['Zone', 'Primary Purpose', 'Key Provisions for Autonomy'],
        rows: [
          ['Agriculture (AG)', 'Support family farms', 'Min 20 acres; allows agritourism and farmstays'],
          ['Timber Mountain (TM)', 'Timber production', 'Allows Limited Density Owner-Built dwellings'],
          ['Rural Residential (RR)', 'Low-density residential', 'Conditionally permits public uses'],
          ['Foothill Residential (FR)', 'Large-lot sensitive settings', 'Allows small farmsteads and crops'],
        ]
      },
      {
        type: 'heading',
        text: 'Title 25: The Blueprint for Sovereign Dwellings'
      },
      {
        type: 'prose',
        text: `Butte County has adopted Title 25 (Limited Density Owner-Built Rural Dwellings), which provides an alternative building code pathway. This code substantially relaxes standard requirements, facilitating affordable shouse construction.`
      },
      {
        type: 'table',
        title: 'Title 24 vs. Title 25',
        headers: ['Requirement', 'Title 24 (Standard)', 'Title 25 (Owner-Built)'],
        rows: [
          ['Permit Duration', '1 Year', '3 Years'],
          ['Heating Source', 'Code-mandated capacity', 'Woodstove or pellet stove allowed'],
          ['Fire Sprinklers', 'Mandatory for all units', 'Not required under 1,250 sq. ft.'],
          ['Materials', 'Industrial/Standardized', 'Owner-generated (milled lumber, stone)'],
          ['Power Source', 'Two sources for off-grid', 'Generators/Solar allowed as sole source'],
        ]
      },
      {
        type: 'callout',
        text: `Title 25 empowers homeowners to construct homes using non-industrial methods. This is the literal cure - using one's own hands to build a home and workshop outside the permission of megalithic corporations.`
      }
    ]
  },
  {
    slug: 'robotics',
    number: '06',
    title: 'Robotics & Automation',
    subtitle: 'FarmBot, Mobile Aloha, Agricultural Autonomy, and Workshop Manipulators',
    content: [
      {
        type: 'prose',
        text: `The endgame of the Millennial Builder framework is the securing of independent resources through automation. This involves automating caloric production and manual labor, decoupling from the corporate grid.`
      },
      {
        type: 'heading',
        text: 'Agricultural Autonomy with FarmBot'
      },
      {
        type: 'prose',
        text: `Open-source robotics like FarmBot allow for the precise cultivation of food. The FarmBot Genesis XL (18 m²) is designed to grow enough vegetables to meet daily nutritional requirements. By using hexagonal packing, the bot can increase harvest volume by approximately 12% over traditional methods.`
      },
      {
        type: 'table',
        title: 'FarmBot Output by Model',
        headers: ['Bot Model', 'Growing Area', 'Avg. Cups/Month', 'Avg. Calories/Day', 'ROI'],
        rows: [
          ['Express', '3.6 m²', '108', '35 - 65 cal', '< 2 Years'],
          ['Genesis XL', '18.0 m²', '540', '175 - 328 cal', '< 1 Year'],
          ['Genesis MAX', '54.0 m²', '1,620', '525 - 984 cal', '6 Months'],
        ]
      },
      {
        type: 'table',
        title: 'Top Caloric Performers per m²',
        headers: ['Crop', 'Calories/m²/day'],
        rows: [
          ['Potatoes', '41.03'],
          ['Sweet Potatoes', '38.89'],
          ['Turnips', '24.16'],
          ['Carrots', '22.74'],
          ['Spinach', '22.65'],
        ]
      },
      {
        type: 'heading',
        text: 'The Workshop Manipulator: Mobile Aloha'
      },
      {
        type: 'prose',
        text: `The Mobile Aloha platform is a low-cost whole-body teleoperation system. A DIY version can be built for approximately $1,800, using four robotic arms and an AgileX Tracer base. It excels at tasks requiring mobility and dexterity.`
      },
      {
        type: 'prose',
        text: `Using the ACT (Action Chunking with Transformers) framework, the robot can be co-trained with existing datasets to autonomously perform tasks like sautéing, opening cabinets, or using a drill after just 50 demonstrations. Successful task execution rates increase by 90% after 50 demos.`
      },
      {
        type: 'prose',
        text: `Other open-source platforms include OpenMower (RTK GPS-guided lawn mowing via Raspberry Pi) and Acorn by Twisted Fields (autonomous solar-powered rover for farming at scale).`
      },
      {
        type: 'heading',
        text: 'Semi-Autonomous Community Supported Agriculture (CSA)'
      },
      {
        type: 'prose',
        text: `Community Supported Agriculture is a pre-purchase food subscription model: members pay upfront for a season's share of a farm's harvest, shifting financial risk from farmer to community. The conventional CSA relies on hand labor. The semi-autonomous CSA layers open-source robotics (FarmBot, Acorn, OpenMower) with a scheduling software layer so that most routine operations - seeding, watering, weeding, soil monitoring - run without daily human intervention. Labor input shifts from daily maintenance to weekly harvesting and equipment checks.`
      },
      {
        type: 'table',
        title: 'Semi-Autonomous CSA Configuration (20 Shares)',
        headers: ['Component', 'Role', 'Est. Cost', 'Automation Level'],
        rows: [
          ['FarmBot Genesis MAX (×2)', 'Precision planting, watering, weeding', '~$14,000', 'Full (seeding, irrigation, weeding)'],
          ['Acorn Rover (Twisted Fields)', 'Row cultivation, soil monitoring', '~$12,000', 'Supervised autonomous'],
          ['Raspberry Pi sensor network', 'Soil moisture, pH, temperature telemetry', '~$600', 'Continuous passive'],
          ['n8n self-hosted workflow', 'Schedule coordination + alert routing', '~$0 (self-hosted)', 'Automated'],
          ['Walk-in cold storage (DIY)', 'Post-harvest preservation', '~$3,000 - $5,000', 'Thermostat-controlled'],
          ['Share distribution app (Farmigo fork)', 'Member management + pickup scheduling', '~$0 (open-source)', 'Self-service'],
        ]
      },
      {
        type: 'prose',
        text: `A 20-share CSA at $600/share/season generates $12,000 in guaranteed pre-season revenue. With automated production reducing labor costs, a two-person operation managing the above stack can sustain 20–30 shares while holding day jobs. At 50 shares the operation becomes a primary income source. The cooperative overlay - where share members collectively own the land and equipment via an LLC or CLT - eliminates the single largest failure mode of traditional CSAs: land tenure insecurity.`
      },
      {
        type: 'table',
        title: 'CSA Scale Economics',
        headers: ['Scale', 'Shares', 'Annual Revenue', 'Robot Coverage', 'Human Hours/Week'],
        rows: [
          ['Starter', '10-15', '$6,000 - $9,000', '60%', '8-12 hrs'],
          ['Sustainable', '20-35', '$12,000 - $21,000', '75%', '12-18 hrs'],
          ['Livelihood', '50-80', '$30,000 - $48,000', '85%', '20-30 hrs'],
          ['Community Enterprise', '100+', '$60,000+', '90%+', 'Hired crew justified'],
        ]
      },
      {
        type: 'callout',
        text: `The semi-autonomous CSA is the agricultural equivalent of the content engine: build the machine once, then operate it at low marginal cost. The land trust provides the stable base. The automation stack handles the daily labor. The community provides the capital and the market simultaneously.`
      }
    ]
  },
  {
    slug: 'cash-engine',
    number: '07',
    title: 'The Cash Engine',
    subtitle: 'FogSift $20 Offers, Lemon Squeezy, and Content Automation Workflows',
    content: [
      {
        type: 'prose',
        text: `Material independence requires an independent digital revenue engine. The strategy involves weaponizing tech fluency to solve specific problems for direct cash, bypassing the "prestige" of corporate titles.`
      },
      {
        type: 'heading',
        text: 'The FogSift $20 Offer'
      },
      {
        type: 'prose',
        text: `Identify a high-value problem. Provide a custom video solution for a flat $20 fee. Deliver via processors like Lemon Squeezy to maintain digital sovereignty. The FogSift model utilizes a direct payment queue to deliver custom, unlisted video solutions.`
      },
      {
        type: 'heading',
        text: 'Content Methodology (A-E Structure)'
      },
      {
        type: 'prose',
        text: `Every digital product follows a hyper-efficient five-part structure: A) What is happening - raw data and diagnostic breakdown. B) What is happening next - projections and evidence-based forecasts. C) Why - underlying mechanisms and causal relationships. D) What important people are saying - expert insights. E) Speculation - original interpretations and second-order insights.`
      },
      {
        type: 'heading',
        text: 'The Lemon Squeezy Merchant Model'
      },
      {
        type: 'prose',
        text: `Lemon Squeezy acts as the "Merchant of Record," handling global sales tax and VAT compliance. They charge a fee of typically 5% + 50c per transaction. Key features include no-code checkout, AI fraud prevention, and unlisted video delivery via Make.com or Zapier.`
      },
      {
        type: 'heading',
        text: 'Content Automation Workflows'
      },
      {
        type: 'prose',
        text: `Scripting and Research: Use deep research tools or Perplexity for niche data. Synthesis: Feed brain-dumps into n8n workflows for structured output. Video Production: Use InVideo or Pictory for stock-asset visuals. Automation: Set up Zaps to auto-post to social, notify subscribers, and log performance.`
      },
      {
        type: 'callout',
        text: `The 2026 YouTube algorithm rewards high-frequency, unpolished, authentic content. Consistent output - making three videos to beat the 99% who never make more than two - is the key to establishing a digital flag.`
      }
    ]
  },
  {
    slug: 'execute',
    number: '08',
    title: 'Execute',
    subtitle: 'Final Directives for Immediate Action',
    content: [
      {
        type: 'prose',
        text: `Stop waiting for the perfect situation. Participate before the window closes. The opportunity exists to harvest one's own crops and build with one's own hands, outside the pleasure or permission of megalithic corporations. The time to act is now.`
      },
      {
        type: 'heading',
        text: 'The Five Directives'
      },
      {
        type: 'directive',
        number: '1',
        title: 'The YouTube Launch',
        text: 'Record a three-minute video about a skill you possess. Upload it today. Repeat until you have 100 videos, improving one thing each time.'
      },
      {
        type: 'directive',
        number: '2',
        title: 'Intellectual Audit',
        text: 'Identify what you can teach. If it took you an hour to learn, it is valuable to someone who hasn\'t spent that hour yet.'
      },
      {
        type: 'directive',
        number: '3',
        title: 'Communication Firewall',
        text: 'Disengage from anyone who uses your emotional energy as their primary regulator. Protect your build time.'
      },
      {
        type: 'directive',
        number: '4',
        title: 'Physical Search',
        text: 'Filter for land parcels under $40K. Map out your exit. Look at Butte County, Lake County, Mendocino County.'
      },
      {
        type: 'directive',
        number: '5',
        title: 'The Shop Build',
        text: 'Commit to a living space under $8,000 to escape the debt cycle. Steel shell. Thermal envelope. Wet wall. Done.'
      },
      {
        type: 'callout',
        text: `Real security is not found in a high-status zip code, but in a low-overhead environment that facilitates deep, focused work. The future of the American Dream is found in the insulated corner of a red-iron shop, where the noise of the world is filtered out, and the work of the hands is documented for a global audience.`
      },
      {
        type: 'prose',
        text: `Whether the medium is garden robots, custom furniture, or miniature painting, the blueprint remains the same: crush the overhead, build the shop, and reclaim the freedom to create. Hit record, speak with your full chest, and build the future with your own two hands.`
      }
    ]
  }
];

export function getSection(slug) {
  return sections.find(s => s.slug === slug);
}

export function getNextSection(slug) {
  const idx = sections.findIndex(s => s.slug === slug);
  return idx >= 0 && idx < sections.length - 1 ? sections[idx + 1] : null;
}

export function getPrevSection(slug) {
  const idx = sections.findIndex(s => s.slug === slug);
  return idx > 0 ? sections[idx - 1] : null;
}
