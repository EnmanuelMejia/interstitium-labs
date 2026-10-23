"""Assemble IL-22 course JSON."""
import json, sys
sys.path.insert(0, "/home/hatch/workspace/apex-audit/docs/university/data/_build")
from il22_a import MODULES_A
from il22_b import MODULES_B

modules = MODULES_A + MODULES_B

DRILLS = [
 {"id": "drill-sefirot", "title": "Tree check", "prompt": "Which sefirah balances Chesed and Gevurah on the middle pillar?",
  "choices": ["Keter", "Tiferet", "Yesod", "Malkhut"], "answer": 1,
  "explain": "Tiferet (beauty/balance) harmonizes loving-kindness and judgment."},
 {"id": "drill-corresp", "title": "Hermetic check", "prompt": "'As above, so below' is the Principle of:",
  "choices": ["Mentalism", "Correspondence", "Vibration", "Rhythm"], "answer": 1,
  "explain": "Correspondence \u2014 the Emerald Tablet's formula."},
 {"id": "drill-nigredo", "title": "Alchemical check", "prompt": "The first color-stage of the Great Work:",
  "choices": ["Albedo", "Nigredo", "Rubedo", "Citrinitas"], "answer": 1,
  "explain": "Nigredo (blackening/putrefaction) begins the sequence."},
 {"id": "drill-tarot0", "title": "Tarot check", "prompt": "Major Arcana 0 and XXI:",
  "choices": ["Magician / Judgement", "Fool / World", "Hermit / Star", "Lovers / Sun"], "answer": 1,
  "explain": "The Fool opens; the World closes the sequence."},
 {"id": "drill-gd", "title": "Golden Dawn check", "prompt": "The Golden Dawn's grade 5=6 belongs to:",
  "choices": ["The Outer Order", "The Inner/Second Order", "The Third Order", "The O.T.O."], "answer": 1,
  "explain": "Adeptus Minor opens the R.R. et A.C."},
 {"id": "drill-nagham", "title": "Gnostic check", "prompt": "The Nag Hammadi library was discovered in:",
  "choices": ["1890", "1945", "1975", "1914"], "answer": 1,
  "explain": "1945, Egypt \u2014 thirteen codices."}
]

SCENARIOS = [
 {
  "id": "sc-tarot-reading", "title": "Tarot as Symbolic Exercise",
  "context": "A friend faces a career decision and asks for a three-card reading (situation / obstacle / counsel). You draw: VIII Strength, XVI The Tower, XVII The Star. This is a symbolic exercise \u2014 the cards are a mirror for reflection, not a prediction engine. Read them within the tradition's symbolism.",
  "steps": [
   {"prompt": "How do you read Strength in the 'situation' position?",
    "options": [
     {"text": "As the tradition's symbolism: courage, patience, and mastery of impulse \u2014 the querent's situation calls for steady inner strength", "correct": True, "why": "Strength (fortitude taming the lion) is the tradition's emblem of courage-through-gentleness \u2014 read emically, as the system intends."},
     {"text": "As a prediction that they will become physically strong", "correct": False, "why": "Literalism breaks the symbolic grammar \u2014 the card is an archetype, not a weather report."},
     {"text": "As meaningless \u2014 refuse to continue", "correct": False, "why": "The exercise's contract is symbolic reflection; contempt is as unhelpful as credulity."}]},
   {"prompt": "The Tower as 'obstacle', followed by the Star as 'counsel'. Your synthesis?",
    "options": [
     {"text": "The obstacle is sudden disruption of existing structures (Tower); the counsel is hope and renewed orientation after the fall (Star) \u2014 reflect on what structures are brittle and what renewal looks like", "correct": True, "why": "This follows the cards' traditional sequence: Tower (XVI) shatters, Star (XVII) follows with hope \u2014 the Fool's-journey logic applied as reflective prompts."},
     {"text": "Predict a building collapse, then a lucky break", "correct": False, "why": "Divination-as-prediction is not the exercise; the cards structure reflection, not forecasts."},
     {"text": "The Star cancels the Tower, so there is no obstacle", "correct": False, "why": "Positions have distinct roles; collapsing them flattens the reading into wishfulness."}]}
  ]
 },
 {
  "id": "sc-alchemical-emblem", "title": "Decoding an Alchemical Emblem",
  "context": "You are shown a classic emblem: a crowned king and queen standing in a vessel over fire, with the motto 'solve et coagula'. A companion insists it depicts a literal royal wedding. Decode it in the tradition's symbolic terms.",
  "steps": [
   {"prompt": "What do the king and queen represent in the alchemical reading?",
    "options": [
     {"text": "The coniunctio \u2014 sulfur and mercury (solar/masculine and lunar/feminine principles) united in the Work", "correct": True, "why": "The chemical wedding: opposites joined. The tradition reads royal couples as the union of contrary principles, not as history."},
     {"text": "An actual 16th-century marriage", "correct": False, "why": "Emblems are symbolic compositions; literal-historical reading misses the genre entirely."},
     {"text": "The alchemist and his patron", "correct": False, "why": "A sociological guess with no support in the emblem tradition's own vocabulary."}]},
   {"prompt": "And 'solve et coagula' over the fire?",
    "options": [
     {"text": "Dissolve the matter (and the self) to prima materia, then reconstitute it perfected \u2014 the fire is both furnace and trial", "correct": True, "why": "The master formula governs the emblem: analysis then synthesis, applied to substance and practitioner together."},
     {"text": "Instructions for cooking", "correct": False, "why": "The motto is the tradition's central operative formula, not kitchen advice."},
     {"text": "A warning that the vessel will break", "correct": False, "why": "Fire here is the agent of transformation \u2014 read symbolically within the system."}]}
  ]
 },
 {
  "id": "sc-chart-reading", "title": "Reading a Chart Symbolically",
  "context": "A study partner shares a natal chart: Mars in Aries in the 10th house, Saturn conjunct the Moon in the 4th. They ask what a traditional astrologer would make of it \u2014 as an interpretive exercise, not a life prediction. Apply the grammar: planet (what drive), sign (how), house (where).",
  "steps": [
   {"prompt": "Mars in Aries in the 10th house \u2014 the traditional reading?",
    "options": [
     {"text": "The drive planet (Mars) in its own sign (Aries: direct, forceful) in the house of career (10th): ambition expressed through direct action in public/professional life", "correct": True, "why": "Grammar applied correctly: Mars=drive, Aries=how (its domicile \u2014 strong), 10th=where (career). A synthesis, not a sentence."},
     {"text": "They will become a soldier", "correct": False, "why": "Vocational literalism \u2014 the chart describes modal qualities, not job titles."},
     {"text": "Mars causes aggression, so they are dangerous", "correct": False, "why": "Causal determinism is not the tradition's interpretive claim; this is also ethically reckless."}]},
   {"prompt": "Saturn conjunct the Moon in the 4th \u2014 and your framing to the partner?",
    "options": [
     {"text": "Saturn (restriction, structure) joined to the Moon (emotional life) in the house of home/roots (4th): themes of emotional reserve shaped by early environment \u2014 offered as reflective material, explicitly not a diagnosis", "correct": True, "why": "Correct synthesis with the essential disclaimer: symbolic mirror, not psychological or medical verdict."},
     {"text": "A prediction of family tragedy", "correct": False, "why": "Predictive fatalism violates both the exercise's contract and basic responsibility."},
     {"text": "Ignore it \u2014 only the Mars placement matters", "correct": False, "why": "Cherry-picking breaks the chart's holism; the tradition reads configurations together."}]}
  ]
 }
]

mock = []
qid = 0
for m in modules:
    for q in m["quiz"]:
        qid += 1
        if qid > 36: break
        mock.append({"id": f"mock-m22-{qid:02d}", "type": "choice",
                     "q": q["q"], "choices": q["choices"],
                     "answer": q["answer"], "explain": q["explain"]})
    if qid > 36: break

CHEAT_SHEETS = [
 {"title": "Tradition Timeline",
  "blocks": [
   {"h": "Ancient\u2013medieval", "body": "- Babylonian omen-lore (2nd mill. BCE)\n- Hellenistic: Corpus Hermeticum, Ptolemy (2nd\u20133rd c. CE)\n- Zohar: 13th c. Spain (de Le\u00f3n)\n- Grimoires: 14th\u201317th c. manuscripts"},
   {"h": "Early modern", "body": "- Fama/Confessio: 1614\u20131615\n- Dee & Kelley: 1582\u20131589\n- Casaubon redates Hermes: 1614"},
   {"h": "Modern", "body": "- Theosophical Society: 1875\n- Golden Dawn: 1888\u20131903\n- RWS tarot: 1909; AMORC: 1915\n- Nag Hammadi: 1945"}]},
 {"title": "Kabbalah & Hermetic Correspondences",
  "blocks": [
   {"h": "Ten sefirot", "body": "Keter, Chokhmah, Binah | Chesed, Gevurah, Tiferet | Netzach, Hod, Yesod | Malkhut \u2014 three pillars, 22 letter-paths"},
   {"h": "Seven Hermetic principles", "body": "Mentalism, Correspondence, Vibration, Polarity, Rhythm, Cause & Effect, Gender (Kybalion formulation)"},
   {"h": "Luria", "body": "Tzimtzum \u2192 shevirah \u2192 tikkun"}]},
 {"title": "Tarot & Astrology Grids",
  "blocks": [
   {"h": "Major Arcana 0\u201321", "body": "Fool, Magician, High Priestess, Empress, Emperor, Hierophant, Lovers, Chariot, Strength/Justice, Hermit, Wheel, Justice/Strength, Hanged Man, Death, Temperance, Devil, Tower, Star, Moon, Sun, Judgement, World"},
   {"h": "Suits \u00d7 elements", "body": "Wands\u2013fire, Cups\u2013water, Swords\u2013air, Pentacles\u2013earth; courts: Page, Knight, Queen, King"},
   {"h": "Houses", "body": "1st self, 4th home, 7th partnership, 10th career; planets: Sun\u2013Saturn classical + modern outer"}]},
 {"title": "Critical-Reading Toolkit",
  "blocks": [
   {"h": "Moves", "body": "- Emic vs. etic: label which you're doing\n- Source criticism: who, when, from what sources, for whom?\n- Claim sorting: historical / symbolic / experiential \u2014 each by its own standards"},
   {"h": "Red flags", "body": "- Claimed antiquity without evidence (Casaubon pattern)\n- Lineage claims without archives\n- The blank rune problem: modern inventions sold as ancient"}]}
]

ANSWER_BANK = [
 {"q": "How should I read a text that claims ancient secret origins?", "a": "Framework: (1) What does scholarship say about dating and authorship? (2) What did the tradition *do* with the antiquity claim \u2014 what work did it perform? (3) What is the text's internal logic, taken on its own terms? The Casaubon pattern (Hermetica, Zohar's attribution, tarot's Egypt) shows claims and findings can both be true at different levels: the text is younger than claimed *and* the tradition built something real on the claim."},
 {"q": "A friend asks for a tarot reading about a medical decision. What do I do?", "a": "Framework: the course's contract \u2014 symbolic mirror, not prediction engine, and never a substitute for professional advice. Offer the reflective exercise if welcome, with the disclaimer explicit; redirect medical, legal, and financial decisions to qualified professionals. Divination as contemplation: legitimate. Divination as counsel on high-stakes decisions: irresponsible."},
 {"q": "How do I tell a genuine lineage from a invented one?", "a": "Framework: ask for documentation \u2014 charters, membership rolls, dated publications, archival traces. Rosicrucian orders, Golden Dawn successors, and Wiccan lines all make continuity claims; the honest ones distinguish documented history from traditional narrative. 'Secret, so no records' is compatible with both genuine secrecy and invention \u2014 which is why the question stays open rather than being answered by fiat."},
 {"q": "What's the difference between studying alchemy and believing in transmutation?", "a": "Framework: emic vs. etic. Studying = learning the system's internal logic, history, and symbolism (what practitioners claimed and did). Believing = assenting to the physical claims. The course trains the first; the second is a personal matter the course neither requires nor endorses. Most historians of alchemy do not believe lead was transmuted \u2014 and still find the tradition inexhaustibly interesting."},
 {"q": "How do I engage Eastern esoteric concepts respectfully?", "a": "Framework: (1) Learn the concept in its home tradition first \u2014 tantra as initiatory discipline, not lifestyle branding. (2) Note what the tradition itself restricts (Vajrayana empowerment). (3) Attribute borrowings. (4) Watch for the orientalist pattern: East as mystic Other. Respect = contextual understanding plus honesty about what you're actually doing with the material."},
 {"q": "Someone cites 'quantum physics proves Hermetic Mentalism.' Response?", "a": "Framework: claim sorting. Quantum mechanics is a physical theory with precise mathematical content; Mentalism is a metaphysical principle in a 1908 occult text. The vocabularies sound alike ('observer,' 'mind') but the claims operate at different levels with different standards of evidence. Analogy is fine; identity is not \u2014 flag the category error kindly."}
]

SOURCE_LINKS = [
 {"name": "Wikipedia \u2014 Kabbalah", "url": "https://en.wikipedia.org/wiki/Kabbalah", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Hermeticism", "url": "https://en.wikipedia.org/wiki/Hermeticism", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Alchemy", "url": "https://en.wikipedia.org/wiki/Alchemy", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Astrology", "url": "https://en.wikipedia.org/wiki/Astrology", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Tarot", "url": "https://en.wikipedia.org/wiki/Tarot", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Enochian magic", "url": "https://en.wikipedia.org/wiki/Enochian_magic", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Rosicrucianism", "url": "https://en.wikipedia.org/wiki/Rosicrucianism", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Theosophy", "url": "https://en.wikipedia.org/wiki/Theosophy", "retrieved": "2026-10-07"},
 {"name": "Wikipedia \u2014 Hermetic Order of the Golden Dawn", "url": "https://en.wikipedia.org/wiki/Hermetic_Order_of_the_Golden_Dawn", "retrieved": "2026-10-07"},
 {"name": "Internet Sacred Text Archive", "url": "https://www.sacred-texts.com/", "retrieved": "2026-10-07"}
]

doc = {
 "schemaVersion": "1.0",
 "courseId": "il-22-esoteric-secret-knowledge",
 "code": "IL-22",
 "title": "The Deep Library \u2014 Esoteric & Secret Knowledge",
 "tagline": "Kabbalah, Hermeticism, alchemy, astrology, tarot, Enochian, Rosicrucianism, Theosophy, the Golden Dawn: the Western mystery traditions and their Eastern counterparts, studied as traditions.",
 "blurb": "Sixteen modules, one per tradition or practice: how to approach esoteric material, Kabbalah and the Tree of Life, Hermeticism, alchemy, astrology, tarot, Enochian magic, Rosicrucianism, Theosophy, the Golden Dawn, grimoires, Gnosticism and esoteric Christianity, Eastern esoteric traditions, divination systems, symbolism and sacred geometry, and the modern occult revival. Presented throughout **as the traditions present themselves** \u2014 scholarly and descriptive, never as verified science; no invented lineages, no fabricated revelations, no invented quotations. Quizzes test knowledge *of* the traditions: practitioner claims, established history, and the difference. Original instructional content; confers no certificate.",
 "hours": 58,
 "updatedAt": "2026-10-07",
 "objectives": [
  "Read esoteric traditions emically (their own logic) and etically (scholarly history), and keep the two distinct",
  "Map the core symbol systems: Tree of Life, Hermetic principles, alchemical stages, astrological grammar, tarot arcana",
  "Narrate each tradition's history honestly \u2014 including disputed origins and lineage claims",
  "Practice symbolic interpretation: tarot spreads, alchemical emblems, chart grammar as reflective exercises",
  "Apply source criticism and claim-sorting to esoteric texts",
  "Recognize orientalist distortion in Western borrowings of Eastern traditions"
 ],
 "arc": [
  {"phase": "Phase 1 \u2014 Foundations", "title": "Learn to read", "body": "How to approach the traditions, then Kabbalah, Hermeticism, and alchemy: the three great symbolic systems. Modules 1\u20134."},
  {"phase": "Phase 2 \u2014 The arts", "title": "Enter the practices", "body": "Astrology, tarot, Enochian magic, Rosicrucianism: divinatory and ritual systems with their histories. Modules 5\u20138."},
  {"phase": "Phase 3 \u2014 Orders & horizons", "title": "Orders, East, and critique", "body": "Theosophy, the Golden Dawn, grimoires, Gnosticism, Eastern traditions, divination, symbolism, and the modern revival with critical reading. Modules 9\u201316."}
 ],
 "priorities": [
  {"label": "Core systems: Kabbalah, Hermeticism, alchemy (modules 2\u20134)", "minutes": 480},
  {"label": "Divinatory arts: astrology, tarot, divination (modules 5\u20136, 14)", "minutes": 420},
  {"label": "Ritual orders: Enochian, Rosicrucianism, Golden Dawn, grimoires (7\u201310, 11)", "minutes": 480},
  {"label": "Horizons: Gnosticism, Eastern traditions, symbolism, revival (12\u201313, 15\u201316)", "minutes": 420},
  {"label": "Scenarios + framing module + mock", "minutes": 360}
 ],
 "battlePlan": [
  {"id": "bp22-1", "title": "Complete the framing module (1) \u2014 the contract governs everything after", "minutes": 120},
  {"id": "bp22-2", "title": "Complete core systems (modules 2\u20134): notes, cards, quizzes", "minutes": 480},
  {"id": "bp22-3", "title": "Complete the arts (modules 5\u20138)", "minutes": 420},
  {"id": "bp22-4", "title": "Complete orders & horizons (modules 9\u201316)", "minutes": 600},
  {"id": "bp22-5", "title": "Work all three interpretive scenarios as symbolic exercises", "minutes": 180},
  {"id": "bp22-6", "title": "Sit the 36-task timed mock; review misses against the cheat sheets", "minutes": 150}
 ],
 "modules": modules,
 "scriptLabs": [],
 "drills": DRILLS,
 "scenarios": SCENARIOS,
 "trainers": [],
 "mockMinutes": 120,
 "mockTasks": mock,
 "cheatSheets": CHEAT_SHEETS,
 "answerBank": ANSWER_BANK,
 "sourceLinks": SOURCE_LINKS,
 "honestyNote": "Original instructional content. Esoteric material is presented descriptively as the traditions present it \u2014 history, symbolism, and practice as claimed by practitioners \u2014 never as verified science. No invented lineages, revelations, or quotations. Confers no certificate."
}

out = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json"
with open(out, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", out, "modules:", len(modules), "mock:", len(mock))
