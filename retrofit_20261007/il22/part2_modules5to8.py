#!/usr/bin/env python3
"""Retrofit IL-22 modules 5-8 (astrology, tarot, enochian, rosicrucianism)."""
import json, os

PATH = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json'
GL = '- **%s** \u2014 %s'

UPDATES = {

'm22-astrology': {
'summary': (
    "Welcome to Module 5 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we are "
    "taking up the oldest continuous symbolic language in this course: four thousand years of reading the sky, from Babylonian omen "
    "tablets to the modern natal chart. You'll learn astrology's real history \u2014 Babylon, Hellenistic Egypt, Ptolemy's Tetrabiblos, "
    "the Islamic, Indian, and medieval European transmissions \u2014 and its working grammar: planets, signs, houses, and aspects, and how "
    "practitioners combine them. We will be exact about what astrology claims and what the sciences found, because this module is the "
    "course's clearest case of a symbolic system with a vast history that is not verified science \u2014 and studying it honestly means "
    "holding both facts at once."
),
'glossary': [
    GL % ('Natal chart', 'the practitioner\u2019s basic document: planetary positions at birth mapped onto the houses for a location.'),
    GL % ('Planets (astrological)', 'Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn classically \u2014 plus Uranus, Neptune, Pluto in modern practice \u2014 each with significations (Mars: drive, conflict).'),
    GL % ('Signs', 'the twelve zodiacal divisions (Aries\u2013Pisces) read as modal qualities \u2014 *how* a planet acts.'),
    GL % ('Houses', 'twelve life-domains (1st: self, 7th: partnership, 10th: career) \u2014 *where* in life a planet acts.'),
    GL % ('Aspects', 'angular relationships between planets \u2014 conjunction, opposition, trine (120\u00b0, traditionally harmonious) \u2014 read as relationships between drives.'),
    GL % ('Tetrabiblos', "Ptolemy\u2019s 2nd-century CE systematization of Hellenistic horoscopic astrology \u2014 the classical statement of planetary significations."),
],
'proc_intro': (
    "Practitioners read a chart by synthesis, not by single factors. Run this six-step descriptive reading on any sample natal chart "
    "(use a published example chart from the source links, or the worked positions below) \u2014 the point is to learn the grammar from the inside."
),
'steps': [
    "**List the planets with sign and house.** For each planet write one line: planet \u2012 sign (*how* it acts) \u2012 house (*where* in life it acts). Use the seven classical planets plus the modern three.",
    "**Read each placement emically.** In the tradition's terms, what does the combination say? Example pattern: 'Mars in Aries in the 10th \u2014 drive expressed directly, in the domain of career.' Do all ten.",
    "**Map the aspects.** Note the major angular relationships \u2014 conjunctions, oppositions, trines (120\u00b0, harmonious in the tradition's reading). For each, state which two drives are in relationship.",
    "**Synthesize, don't stack.** Write three sentences that combine placements into a whole \u2014 the way practitioners claim meaning *emerges* from combination, not from adding isolated factors.",
    "**Add the history.** Which layer of the tradition are you using \u2014 Babylonian omen-logic, Hellenistic horoscopy (Tetrabiblos), or modern psychological astrology? Label it.",
    "**Close with the etic sentence.** Controlled studies have not found effects beyond chance; astrology was expelled from the sciences in the 17th\u201318th centuries. Write one sentence stating what you just did: a symbolic-interpretive exercise with four millennia of continuous use \u2014 not an astronomical measurement.",
],
'project': (
    "Write a 700-word 'grammar book' entry for one component of the astrological system \u2014 your choice of planets, signs, houses, or aspects. "
    "Part 1 (emic): define each item in the tradition's terms with its significations (e.g., for houses: 1st self, 7th partnership, 10th career). "
    "Part 2 (etic): trace the component's history on this module's arc \u2014 Babylonian omen literature (*Enuma Anu Enlil*, signs for king and "
    "state), Hellenistic invention of the horoscope, Ptolemy's *Tetrabiblos* (2nd c. CE), and transmission through Islamic, Indian (*jyotisha*), "
    "Chinese, and medieval European traditions. Part 3: one paragraph stating the modern scholarly status honestly, and why the course studies "
    "the system anyway \u2014 as a symbolic language with four millennia of continuous use."
),
'honesty': (
    "This module reports astrology's claims as the tradition's claims and reports the scientific record plainly: controlled studies have not "
    "found effects beyond chance, and astrology left the sciences in the 17th\u201318th centuries. Practitioners' distinction \u2014 symbolic "
    "interpretation of archetypal patterns, not astronomical claims about physical influence \u2014 is presented as the practitioners' own framing, "
    "not as a defense. Chart work in this course is a reflective, interpretive exercise; it is never presented as prediction or as a substitute "
    "for professional counsel."
),
'cards_add': [
    ("The twelve houses in brief?",
     "Life-domains: 1st self, 7th partnership, 10th career \u2014 *where* in life a planet acts, in the tradition's grammar."),
],
'quiz_add': [
    ("In the traditional grammar, Mars signifies:",
     ["Emotion and relationship", "Drive and conflict", "Material security", "Spiritual liberation"],
     1,
     "Each planet carries significations \u2014 Mars: drive, conflict \u2014 modified by sign (*how*) and house (*where*)."),
    ("The modern planets added to the classical seven are:",
     ["Uranus, Neptune, Pluto", "Earth, Ceres, Eris", "Vulcan, Lilith, Chiron", "None were added"],
     0,
     "The Concepts notes: seven classical planets plus the modern additions Uranus, Neptune, Pluto."),
    ("Hellenistic Egypt's distinctive contribution to astrology was:",
     ["The telescope", "The invention of the horoscope (2nd c. BCE\u20132nd c. CE)", "The zodiac's abolition", "Chinese transmission"],
     1,
     "Babylon gave omen-lore; Hellenistic Egypt invented the horoscope \u2014 the individual birth chart."),
    ("*Jyotisha* is:",
     ["The Chinese zodiac", "The Indian astrological tradition in astrology's transmission arc", "A Babylonian tablet", "A house system"],
     1,
     "The transmission arc runs through Islamic, Indian (jyotisha), Chinese, and medieval European traditions."),
    ("A conjunction, in the aspect grammar, is:",
     ["A 120\u00b0 harmonious angle", "Two planets at the same zodiacal longitude", "A house cusp", "A Babylonian omen"],
     1,
     "Aspects are angular relationships: conjunction (together), opposition, trine (120\u00b0, harmonious) \u2014 see the Concepts notes."),
    ("The honest reason this course studies astrology is that it is:",
     ["Scientifically proven", "A symbolic language with four millennia of continuous use, studied for structure and history \u2014 not as verified science", "Required for the certificate", "A predictive science"],
     1,
     "The Concepts notes close the module's contract: structure and history, never verified science; the course confers no certificate."),
],
},

'm22-tarot': {
'summary': (
    "Welcome to Module 6 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're taking "
    "apart the most misunderstood object in the occult world: the tarot. You'll learn what it actually was \u2014 a 15th-century Italian "
    "card game, *tarocchi*, three centuries before anyone read fortunes with it \u2014 how Antoine Court de G\u00e9belin invented its Egyptian "
    "origin story in 1781, how \u00c9liphas L\u00e9vi wired the 22 trumps to the Hebrew letters, and how the Golden Dawn built the Qabalistic-"
    "astrological engine that still drives modern decks. You'll sequence all 22 Major Arcana and meet the Rider-Waite-Smith deck that made "
    "the modern symbolic tarot. This module is a masterclass in the lineage problem \u2014 watch how a game became an oracle, and ask at every "
    "step what each generation *did* with the cards."
),
'glossary': [
    GL % ('Tarocchi', 'the 15th-century Italian trick-taking card game tarot descends from \u2014 22 trump cards (*trionfi*) plus four suited sequences.'),
    GL % ('Major Arcana', 'the 22 trumps, numbered 0\u201321 (Fool through World), read in the modern tradition as a symbolic journey \u2014 the \u201cFool\u2019s Journey.\u201d'),
    GL % ('Minor Arcana', '56 cards: four suits (Wands, Cups, Swords, Pentacles) of Ace\u201310 plus four court cards (Page, Knight, Queen, King) each.'),
    GL % ('Court de G\u00e9belin', 'Antoine Court de G\u00e9belin (1781) \u2014 began tarot\u2019s occult reinterpretation with the claimed (scholar-rejected) Egyptian origin.'),
    GL % ('\u00c9liphas L\u00e9vi', '1850s occultist who linked the 22 trumps to the Hebrew letters \u2014 the Qabalistic linkage that made modern occult tarot possible.'),
    GL % ('Rider-Waite-Smith', 'the 1909 deck: A. E. Waite\u2019s system with Pamela Colman Smith\u2019s fully illustrated minors \u2014 the modern standard.'),
],
'proc_intro': (
    "Tarot in this course is a symbolic instrument for reflection \u2014 the cards are a mirror, not a prediction engine. Run this seven-step "
    "three-card exercise (situation / obstacle / counsel) to learn the interpretive grammar from the inside."
),
'steps': [
    "**Frame a real question.** Write one sentence about a situation you genuinely face \u2014 the exercise only works on live material. This is reflection, not divination-as-prediction.",
    "**Draw three cards and name them precisely.** Situation / obstacle / counsel. Use the Major Arcana sequence from the Concepts notes (0 Fool \u2013 XXI World) and the suit-element mapping (Wands\u2013fire, Cups\u2013water, Swords\u2013air, Pentacles\u2013earth).",
    "**Read each card emically.** What does the card mean in the tradition's symbolism? Use the Golden Dawn correspondences where you know them (e.g., The Emperor\u2013Aries, The Moon\u2013Pisces) and the suit elements.",
    "**Read positionally.** The same card means something different as obstacle vs. counsel \u2014 state how the position reshapes the card's meaning in one sentence per card.",
    "**Synthesize the spread.** Write three sentences telling the story the three cards make together \u2014 situation complicated by obstacle, addressed by counsel.",
    "**Apply the honesty check.** Write one etic sentence: the cards did not predict anything; the spread's value was forcing structured reflection on a real question. Note the lineage honestly \u2014 this method is a 19th\u201320th-century synthesis, not an ancient inheritance.",
    "**File the method.** Record which deck-imagery you used (Rider-Waite-Smith scenes shape modern meanings) so your next reading is comparable.",
],
'project': (
    "Produce a 'deck dossier': choose any five Major Arcana (include at least one from 0\u2013VII and one from XIII\u2013XXI) and write a 150-word "
    "entry per card with three labeled parts: (1) the card's place in the sequence and its traditional symbolism; (2) its Golden Dawn "
    "correspondences \u2014 Hebrew letter/Tree-of-Life path and astrological attribution where the module's Concepts notes give them; "
    "(3) the lineage note \u2014 which layer of tarot's history produced this meaning (15th-century game, Court de G\u00e9belin's 1781 "
    "reinterpretation, L\u00e9vi's 1850s Qabalistic linkage, the Golden Dawn synthesis, or the 1909 Rider-Waite-Smith illustrations). "
    "Conclude with a 200-word reflection on what the lineage problem looks like inside a single deck."
),
'honesty': (
    "Tarot's Egyptian origin is Court de G\u00e9belin's 1781 invention \u2014 scholars reject it, and this module says so plainly. The "
    "Qabalistic-astrological correspondences are a 19th-century Golden Dawn synthesis, not an ancient inheritance. Card work here is "
    "presented as a symbolic exercise for reflection \u2014 the cards are a mirror, never a prediction engine and never a substitute for "
    "professional advice on medical, legal, or financial decisions. The deck's history is the honest part; the symbolism is the "
    "tradition's own."
),
'cards_add': [],
'quiz_add': [
    ("The Fool's Journey refers to:",
     ["A medieval pilgrimage", "The modern reading of the 22 Major Arcana as a symbolic sequence from Fool (0) to World (XXI)", "Court de G\u00e9belin's travels", "A Golden Dawn grade"],
     1,
     "The Concepts notes: the 0\u201321 sequence read as a symbolic journey \u2014 a modern interpretive frame."),
    ("Pamela Colman Smith's decisive contribution was:",
     ["Founding the Golden Dawn", "Fully illustrating all 56 minor cards \u2014 which is why the Rider-Waite-Smith deck dominates modern practice", "Inventing the suits", "Translating the Zohar"],
     1,
     "Waite's system + Smith's illustrated minors (1909) = the modern standard deck."),
    ("Card XI in the sequence given here is:",
     ["Strength (or Justice)", "Justice (or Strength)", "The Hermit", "The Hanged Man"],
     1,
     "The notes give VIII Strength (or Justice) and XI Justice (or Strength) \u2014 the two traditions swap them."),
    ("In the Golden Dawn system, the suit of Pentacles corresponds to:",
     ["Fire and will", "Water and emotion", "Air and intellect", "Earth: the material and practical"],
     3,
     "Wands\u2013fire, Cups\u2013water, Swords\u2013air, Pentacles\u2013earth \u2014 the standard elemental mapping."),
    ("How many court cards are in each suit?",
     ["Two", "Three", "Four \u2014 Page, Knight, Queen, King", "Ten"],
     2,
     "Four suits \u00d7 (Ace\u201310 + Page, Knight, Queen, King) = the 56 Minor Arcana."),
    ("The honest lineage of the tarot meanings used in modern readings is:",
     ["Ancient Egypt via secret transmission", "A 15th-century game reshaped by 1781, 1850s, Golden Dawn, and 1909 layers \u2014 a 19th\u201320th-century synthesis", "Medieval Cathar doctrine", "A single 1909 invention"],
     1,
     "The lineage problem applied: game \u2192 Court de G\u00e9belin \u2192 L\u00e9vi \u2192 Golden Dawn \u2192 Rider-Waite-Smith."),
],
},

'm22-enochian': {
'summary': (
    "Welcome to Module 7 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're opening "
    "the most extensive record of Renaissance ritual magic in existence: John Dee's diaries of the 'angelic conversations' of 1582\u20131589. "
    "You'll meet Dee \u2014 mathematician, astronomer, advisor to Elizabeth I \u2014 and the scryer Edward Kelley dictating from the shew-stone; "
    "you'll learn the system's architecture \u2014 the Great Table's four Watchtowers, the 48 Calls, the 30 Aethyrs \u2014 and you'll confront "
    "the Enochian language itself, which modern linguistics finds to be a genuine constructed language with consistent internal structure, "
    "whatever its claimed origin. Then we'll trace the system's strange afterlife: how the Golden Dawn absorbed it wholesale and handed it to "
    "Crowley and a century of ceremonial magic. Genuine 16th-century documents, a real linguistic puzzle, and a 19th-century revival \u2014 "
    "this module has all three layers at once."
),
'glossary': [
    GL % ('Mysteriorum Libri', "Dee's detailed diaries of the 1582\u20131589 angel workings \u2014 the primary source, among the most extensive records of Renaissance ritual magic."),
    GL % ('Shew-stone', 'the scrying crystal into which Kelley gazed while dictating the angels\u2019 communications; Dee questioned and recorded.'),
    GL % ('Great Table', 'the system\u2019s master diagram: four Watchtowers of elements and cardinal directions, each with its angel hierarchy.'),
    GL % ('Calls (Keys)', 'the 48 invocations in the angelic language \u2014 the operative utterances of the system, in the diaries\u2019 presentation.'),
    GL % ('Aethyrs', 'the 30 expansive spiritual regions explored via the Calls \u2014 the visionary territories Crowley later mapped in *The Vision and the Voice*.'),
    GL % ('Enochian language', 'the dictated tongue \u2014 vocabulary, grammar, script \u2014 that linguistic analysis finds structurally consistent: a real constructed language, whatever its claimed origin.'),
],
'proc_intro': (
    "You cannot 'practice' the Calls casually \u2014 and this course does not ask you to. What you *can* do is the scholar's hands-on work: "
    "a six-step structural analysis of the system as the diaries present it, which teaches you how to dissect any ritual system."
),
'steps': [
    "**Reconstruct the timeline.** 1582\u20131589: the workings. Note who did what \u2014 Kelley gazed into the shew-stone and dictated; Dee questioned and recorded. Write the division of labor in one sentence.",
    "**Map the architecture.** Draw the system's structure from the Concepts notes: the Great Table (four Watchtowers \u2014 elements/directions) \u2192 the 48 Calls \u2192 the 30 Aethyrs \u2192 the angel hierarchies. One diagram, labeled.",
    "**Separate the two language claims.** Claim A (practitioner): the operative angelic tongue, the language of Adam. Claim B (scholar): a structured constructed language \u2014 Kelley's remarkable linguistic production. Write both without merging them.",
    "**Trace the transmission.** Dee's diaries \u2192 the Golden Dawn's wholesale absorption (Watchtower rituals, grade ceremonies) \u2192 Crowley's *Vision and the Voice* \u2192 subsequent ceremonial magic. Mark which layer modern practice descends from most.",
    "**Apply the Casaubon question.** What did the Golden Dawn *do* with Dee's system \u2014 what work did the 'ancient angelic' framing perform for a 19th-century order? One paragraph.",
    "**Write the honesty verdict.** Genuine 16th-century documents? Yes. Structurally consistent language? Yes. Proven angelic origin? Unproven \u2014 and the course does not assert it.",
],
'project': (
    "Write a 700-word structural dossier on the Enochian system with four labeled sections: (1) the historical record \u2014 Dee (1527\u20131609), "
    "Kelley, the 1582\u20131589 workings, the *Mysteriorum Libri* as primary source; (2) the system's architecture \u2014 Great Table, four "
    "Watchtowers, 48 Calls, 30 Aethyrs, angel hierarchies, each defined in the diaries' terms; (3) the language question \u2014 the practitioner "
    "claim vs. the linguistic finding of consistent internal structure, held apart; (4) the afterlife \u2014 Golden Dawn absorption, Crowley's "
    "*Vision and the Voice*, and the honest assessment that modern Enochian practice descends more from the 19th-century revival than from "
    "Dee's own use. Conclude with one sentence applying the module's honesty verdict."
),
'honesty': (
    "The diaries are genuine 16th-century documents \u2014 that is history. The language's internal consistency is a linguistic finding \u2014 "
    "that is analysis. The claim that angels dictated it is the tradition's claim \u2014 reported emically, never asserted as fact. This module "
    "teaches the system's structure and history; it does not teach ritual operation of the Calls, and nothing here should be read as instruction "
    "in or endorsement of spirit evocation."
),
'cards_add': [
    ("Dee's dates and roles?",
     "1527\u20131609 \u2014 mathematician, astronomer, advisor to Elizabeth I; the questioner-recorder of the workings."),
],
'quiz_add': [
    ("The division of labor in the workings was:",
     ["Dee gazed, Kelley recorded", "Kelley gazed into the shew-stone and dictated; Dee questioned and recorded", "Both gazed together", "Kelley worked alone"],
     1,
     "The Concepts notes: Kelley the scryer dictated, Dee the scholar interrogated and wrote \u2014 hence the diaries' detail."),
    ("The Enochian system's angel hierarchies govern:",
     ["The tarot suits", "Each division of the Great Table's Watchtowers", "The 22 paths", "The zodiacal signs"],
     1,
     "Named angels govern each Watchtower division \u2014 the system's most elaborate angel-magic structure."),
    ("Crowley's *Vision and the Voice* is:",
     ["A biography of Dee", "His exploration of the 30 Aethyrs", "A Golden Dawn charter", "A translation of the Zohar"],
     1,
     "The afterlife layer: through the Golden Dawn, Enochian reached Crowley, who mapped the Aethyrs."),
    ("Modern Enochian practice descends primarily from:",
     ["Dee's own 16th-century use directly", "The 19th-century Golden Dawn revival and its successors", "Blavatsky's Mahatmas", "Medieval grimoires"],
     1,
     "The honest transmission assessment in the Concepts notes: the revival, not Dee's own use."),
    ("The scholarly view of the Enochian language's origin attributes it to:",
     ["Random syllables", "Kelley's linguistic production \u2014 while acknowledging its genuine internal structure", "Ancient Hebrew", "Dee's invention alone"],
     1,
     "Consistent structure (a real constructed language) + scholarly attribution to Kelley: both facts held together."),
    ("The Watchtower rituals of the Golden Dawn show:",
     ["Dee's rejection of the system", "The Golden Dawn's wholesale absorption of Enochian into its grade ceremonies", "A tarot innovation", "The Rosicrucian manifestos' influence"],
     1,
     "Absorption, not invention: the Golden Dawn built Dee's Tablets into its own ritual architecture."),
],
},

'm22-rosicrucianism': {
'summary': (
    "Welcome to Module 8 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're opening "
    "the case that made 'secret society' a European obsession: two anonymous pamphlets printed in Kassel in 1614 and 1615 \u2014 the *Fama* "
    "and *Confessio Fraternitatis* \u2014 announcing a hidden brotherhood, its founder Christian Rosenkreutz, and a program for the universal "
    "reformation of art, science, and religion. You'll learn what the manifestos said, who probably wrote them (and what he later said about "
    "his 'youthful jest'), how the 'Rosicrucian furor' swept the continent, and how claimed Rosicrucian descent runs \u2014 through 18th-century "
    "German orders to AMORC in 1915 \u2014 on traditional assertions rather than documented institutional histories. This is the lineage problem "
    "as a four-century case study."
),
'glossary': [
    GL % ('Fama Fraternitatis', '1614 Kassel pamphlet announcing the secret brotherhood of Christian Rosenkreutz \u2014 the spark of the Rosicrucian furor.'),
    GL % ('Confessio Fraternitatis', '1615 companion manifesto developing the call for universal reformation of arts, sciences, and religion.'),
    GL % ('Chymische Hochzeit', "'Chemical Wedding' (1616) \u2014 the alchemical-wedding allegory attached to the manifestos; Andreae later called it a youthful *ludibrium* (jest)."),
    GL % ('Christian Rosenkreutz', 'the Fama\u2019s pilgrim-founder whose intact tomb is discovered 120 years after his death \u2014 read by scholars as allegorical, by later orders as real or ascended.'),
    GL % ('Rosicrucian furor', 'the continent-wide pamphlet war and debate the 1614\u20131615 manifestos triggered across Europe.'),
    GL % ('AMORC', 'Ancient Mystical Order Rosae Crucis \u2014 founded 1915 by H. Spencer Lewis; the largest modern Rosicrucian body.'),
],
'proc_intro': (
    "Continuity claims are the lineage problem's favorite habitat. Run this six-step audit on any order's descent claim \u2014 Rosicrucian, "
    "Golden Dawn successor, or Wiccan line \u2014 using the Rosicrucian case as your worked example."
),
'steps': [
    "**State the claim precisely.** 'Order X descends from the 1614 fraternity.' Write the exact claim \u2014 vague descent ('in the spirit of') is a different, weaker claim.",
    "**Demand the documentation.** Charters, membership rolls, dated publications, archival traces: list what would have to exist for the claim to hold. For the 1614 fraternity itself, note there is no contemporary evidence of Rosenkreutz as a historical person.",
    "**Check the authorship layer.** Johann Valentin Andreae is the leading candidate for the manifestos \u2014 and he later called the *Chymische Hochzeit* a youthful jest. Record how that complicates, without settling, the question.",
    "**Map the actual institutions.** 18th-century German orders (Gold- und Rosenkreuzer) \u2192 19th-century occultism \u2192 AMORC (1915, H. Spencer Lewis) and smaller fraternities. Draw the chain with dates.",
    "**Mark the gaps.** Where the chain has traditional assertion instead of documentation, label it 'traditional assertion, not documented institutional history' \u2014 the module's honest formula.",
    "**Render the verdict in two sentences.** Sentence one (etic): what the documents support. Sentence two (emic): what the tradition claims about itself \u2014 because the claim itself is part of the history.",
],
'project': (
    "Write a 700-word 'manifesto audit' of the Rosicrucian case in three labeled parts. Part 1: the documents \u2014 *Fama* (1614), *Confessio* "
    "(1615), *Chymische Hochzeit* (1616); what each announced (the brotherhood, Rosenkreutz's pilgrimage and tomb, the call for universal "
    "reformation) and the furor that followed. Part 2: the authorship and context questions \u2014 Andreae as leading candidate, the 'ludibrium' "
    "remark, the early-17th-century reform hopes and the Thirty Years' War that crushed them, the networks that later fed the Royal Society. "
    "Part 3: the orders \u2014 Gold- und Rosenkreuzer, 19th-century occultism, AMORC (1915) \u2014 with every continuity claim labeled as "
    "traditional assertion or documented history, per the audit procedure. Conclude with the module's two-sentence verdict form."
),
'honesty': (
    "No contemporary evidence places Christian Rosenkreutz as a historical person \u2014 scholars read him as allegorical, and this module says "
    "so. Continuity between the 1614 fraternity and modern orders is reported as traditional assertion, not documented institutional history. "
    "Andreae's 'jest' remark is reported as complicating the authorship question, not settling it. The manifestos' *influence* \u2014 the furor, "
    "the reform networks, the four centuries of orders \u2014 is the solid historical ground; the founding myth is the interesting story built on it."
),
'cards_add': [
    ("The Thirty Years' War: relevance to the manifestos?",
     "The reform hopes of the manifestos' world were crushed by the war \u2014 context for why the 'universal reformation' never came."),
],
'quiz_add': [
    ("The *Chymische Hochzeit* (1616) is:",
     ["The first manifesto", "The alchemical-wedding allegory attached to the manifestos", "A Golden Dawn ritual", "AMORC's charter"],
     1,
     "1616: the allegorical third document \u2014 the one Andreae later called a youthful jest."),
    ("The 'Rosicrucian furor' was:",
     ["A war", "A continent-wide pamphlet debate triggered by the 1614\u20131615 manifestos", "A plague", "A papal bull"],
     1,
     "The manifestos invited Europe's learned to join a secret brotherhood \u2014 Europe answered with pamphlets."),
    ("The Gold- und Rosenkreuzer belong to:",
     ["The 1614 fraternity itself", "18th-century German Rosicrucian orders in the claimed descent chain", "The Golden Dawn", "The Royal Society"],
     1,
     "The descent chain runs through 18th-century German orders to 19th-century occultism and modern bodies."),
    ("The manifestos' call for 'universal reformation' resonated with networks that later fed:",
     ["The Inquisition", "The Royal Society", "The East India Company", "The Bauhaus"],
     1,
     "The Concepts notes: reform hopes, Paracelsian medicine, and the networks behind early modern science."),
    ("H. Spencer Lewis founded AMORC in:",
     ["1614", "1888", "1915", "1947"],
     2,
     "1915 \u2014 the largest modern Rosicrucian body, still active with its Supreme Grand Lodge."),
    ("The honest scholarly position on Rosenkreutz's tomb (discovered intact 120 years on) is that it is:",
     ["Archaeologically confirmed", "Part of the Fama's allegorical founding narrative \u2014 no contemporary evidence for the person", "Located in Kassel", "A Golden Dawn invention"],
     1,
     "The figure functions as founding myth; later orders variously treat him as real or ascended."),
],
},
}


def main():
    d = json.load(open(PATH))
    mods = {m['id']: m for m in d['modules']}
    for mid, u in UPDATES.items():
        m = mods[mid]
        m['summary'] = u['summary']
        preserved = ['### ' + n['title'] + '\n\n' + n['body'] for n in m['notes']]
        concepts = '\n'.join(u['glossary']) + '\n\n**From this module\u2019s study notes:**\n\n' + '\n\n'.join(preserved)
        proc = u['proc_intro'] + '\n\n' + '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(u['steps']))
        m['notes'] = [
            {'title': 'Concepts', 'body': concepts},
            {'title': 'Hands-on procedure', 'body': proc},
            {'title': 'Project brief', 'body': u['project']},
            {'title': 'Honesty note', 'body': u['honesty']},
        ]
        m['cards'] = m['cards'] + [{'front': f, 'back': b} for f, b in u['cards_add']]
        assert len(m['cards']) == 6, (mid, len(m['cards']))
        m['quiz'] = m['quiz'] + [{'q': q, 'choices': ch, 'answer': a, 'explain': e} for (q, ch, a, e) in u['quiz_add']]
        assert len(m['quiz']) == 10, (mid, len(m['quiz']))
        for qi, q in enumerate(m['quiz']):
            assert len(q['choices']) == 4, (mid, qi)
            assert isinstance(q['answer'], int) and 0 <= q['answer'] <= 3, (mid, qi)
            assert q['explain'], (mid, qi)
    tmp = PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    d2 = json.load(open(tmp))
    assert len(d2['modules']) == 16
    os.replace(tmp, PATH)
    print('part2 ok: modules 5-8 retrofitted')

if __name__ == '__main__':
    main()
