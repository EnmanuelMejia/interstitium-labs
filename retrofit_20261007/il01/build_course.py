#!/usr/bin/env python3
"""Retrofit IL-01 (Esoteric Foundations) to the Multicloud course template.

Safe rewrite: json.load BEFORE, write via temp file + os.replace, json.load AFTER.
Only touches docs/university/data/courses/il-01-esoteric-foundations.json.
"""
import json, os, re, tempfile

COURSE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-01-esoteric-foundations.json'

with open(COURSE, encoding='utf-8') as f:
    data = json.load(f)  # validate BEFORE
assert data['courseId'] == 'il-01-esoteric-foundations', 'wrong file!'
assert len(data['modules']) == 3

# ---------------------------------------------------------------- module 1
M1_SUMMARY = """Welcome to the Interstitium Labs Esoteric Foundations academy \u2014 IL-01. I\u2019m your instructor for this academy, and over the next three modules we\u2019re going to read the Western esoteric current the way historians read anything: primary sources first, every claim tiered honestly, and belief never required. This is Module 1: Hermetic Foundations \u2014 the current from Alexandria to the present: the Hermetic Corpus (Corpus Hermeticum, Asclepius, Nag Hammadi context, late-antique Alexandria), the Golden Dawn (1888\u20131903 order history, grade system, the LBRP as study object), Wicca and Thelema (Gardnerian origins, Crowley/A.\u2019.\u2019A.\u2019./O.T.O., the Book of the Law), chaos magic and Discordianism (Spare\u2019s sigilization, Carroll\u2019s paradigm shifting, the Principia), Hermetic Qabalah (the Tree of Life, correspondences, tarot), and alchemy (Alexandrian roots, Paracelsus, laboratory vs. spiritual readings) \u2014 every text read through the four epistemic tiers: DOCUMENTED, SCHOLARLY CONSENSUS, TRADITIONAL, CONTESTED."""

M1_NOTES = [
 {"title": "Concepts", "body": """- **Corpus Hermeticum** \u2014 the dialogues attributed to Hermes Trismegistus; late-antique Alexandrian texts, not primeval Egyptian scripture.
- **Asclepius** \u2014 the most complete single Hermetic text; read it first.
- **Nag Hammadi** \u2014 the 1945 find that reframed the world the Hermetic texts belong to.
- **Late-antique Alexandria** \u2014 the syncretic city where Greek philosophy, Egyptian religion, and emerging Christianity met; the Corpus is what happens when they share a city.
- **Casaubon (1614)** \u2014 dated the Corpus to late antiquity by philology; the founding act of esoteric historiography. Texts have dates, and dates have consequences.
- **Cipher Manuscripts** \u2014 the Golden Dawn\u2019s founding documents: DOCUMENTED as artifacts, CONTESTED as to origin; tier each claim separately.
- **Golden Dawn (1888\u20131903)** \u2014 the order of Westcott, Mathers, and Woodman, through the schisms; read its grade papers as a curriculum, not a mystery.
- **Grade system** \u2014 the ladder from 0=0 upward; a syllabus: what\u2019s taught, in what order, to what end.
- **LBRP** \u2014 the Lesser Banishing Ritual of the Pentagram; a Golden Dawn paper and our study object. Note what the papers say vs. what later books claim.
- **Gardnerian Wicca** \u2014 Wicca\u2019s documented origins; tier the origin claims as you meet them.
- **Thelema** \u2014 Crowley\u2019s current: A.\u2019.\u2019A.\u2019., O.T.O., and the Book of the Law.
- **Book of the Law** \u2014 primary text first, Crowley\u2019s commentaries second, others\u2019 opinions last.
- **Sigilization** \u2014 Austin Osman Spare\u2019s technique: DOCUMENTED as technique, CONTESTED as mechanism.
- **Paradigm shifting** \u2014 Peter Carroll\u2019s chaos-magical move: belief as instrument, a tool rather than a truth-claim.
- **Principia Discordia** \u2014 the Discordian scripture; chaos magic\u2019s irreverent cousin.
- **Tree of Life** \u2014 the Hermetic Qabalah\u2019s map; a memory palace organizing planets, elements, and tarot, whatever else it is.
- **Correspondences** \u2014 the Qabalistic system of linkages across planets, elements, and tarot.
- **Paracelsus** \u2014 iatrochemistry: alchemy as early chemistry and medicine; \u201cthe dose makes the poison\u201d is alchemy\u2019s most DOCUMENTED contribution to science.
- **DOCUMENTED** \u2014 primary sources, artifacts, dated texts: the bedrock tier.
- **SCHOLARLY CONSENSUS** \u2014 what historians agree on: provisional, cited.
- **TRADITIONAL** \u2014 what lineages claim about themselves: reported, not endorsed.
- **CONTESTED** \u2014 open questions and rival readings: where the seminar lives."""},
 {"title": "Hands-on procedure", "body": """Before we theorize, we practice the one reflex this academy exists to build: tiering a claim. You\u2019ll use the Tiering Engine lab (il01-lab-tier) \u2014 but the procedure is identical on paper.

1. **Choose one claim** from this module\u2019s readings \u2014 for example, \u201cThe Corpus Hermeticum preserves primeval Egyptian wisdom.\u201d
2. **Split it into atomic sub-claims:** (a) the manuscripts exist and date to late antiquity; (b) their content originates in primeval Egypt.
3. **Collect the evidence you actually hold** for each sub-claim: the manuscript tradition and Casaubon\u2019s 1614 philology for (a); lineage assertion for (b).
4. **Run each sub-claim** through the lab\u2019s tier_claim function with its evidence string, and read the (tier, justification) pairs it returns.
5. **Record every pair in your tiered reading journal** with the evidence cited \u2014 the justification matters more than the label.
6. **Circle the CONTESTED sub-claims.** Those are not failures; they are your seminar questions for the rest of the academy."""},
 {"title": "Project brief", "body": """The brief. Choose one text from this module \u2014 the Asclepius, a Golden Dawn grade paper, or a passage of the Book of the Law \u2014 and produce a tiered dossier a historian would respect.

Deliverables. (1) A claim inventory: every factual claim the text or its surrounding tradition makes about origins, authorship, and transmission. (2) A tier for each claim \u2014 DOCUMENTED, SCHOLARLY CONSENSUS, TRADITIONAL, or CONTESTED \u2014 with the evidence cited. (3) One CONTESTED question argued both ways, about 300 words per side. (4) A reading-order recommendation for the next student: what to read first, and why.

The standard. Your tiers must survive cross-examination: TRADITIONAL is never marked wrong for being traditional, and DOCUMENTED is never awarded without evidence. Assessments test whether your dossier holds up \u2014 never what you believe."""},
 {"title": "Honesty note", "body": """Original study material, written for this academy \u2014 the questions, labs, and scenarios here are authored, not transcribed from any order\u2019s papers. The four tier labels are our historiographic method, not verdicts on the traditions: TRADITIONAL means \u201cthe lineage claims this,\u201d reported accurately and labeled honestly \u2014 never endorsed, never mocked. \u201cThe lineage claims X\u201d is itself a DOCUMENTED fact about the claim, whatever X\u2019s own tier is. Interstitium Labs is not affiliated with any esoteric order and confers no credential; assessments test literacy \u2014 what the texts say, what tier applies, how scholars argue \u2014 never belief."""},
]

M1_EXPLAINS = [
 "Tier each claim separately \u2014 the manuscript\u2019s date is DOCUMENTED; the origin story is CONTESTED. (Concepts: the four tiers; Hands-on procedure, step 2.)",
 "1614: the texts are late-antique, not primeval \u2014 dates have consequences. (Concepts: Casaubon.)",
 "Artifacts: DOCUMENTED. Their origin story: CONTESTED. Separate tiers. (Concepts: Cipher Manuscripts.)",
 "Paradigm shifting \u2014 the chaos-magical technique, tiered as practice not metaphysics. (Concepts: paradigm shifting.)",
 "Whatever else: a memory palace organizing planets, elements, tarot. (Concepts: Tree of Life.)",
 "Paracelsus: iatrochemistry \u2014 the DOCUMENTED contribution. (Concepts: Paracelsus.)",
]

# ---------------------------------------------------------------- module 2
M2_SUMMARY = """Welcome back to IL-01 \u2014 Esoteric Foundations. I\u2019m your instructor, and in Module 2 we work a single life\u2019s paper trail: John Dee\u2019s. This is Module 2: Dee and the Enochian System \u2014 Dee\u2019s documented life (1527\u20131608/09: court mathematician, navigator, advisor; the Mortlake library), the Enochian alphabet (21 letters, received 6 May 1583), the Angelical Keys (the 48/49 Calls, the 1581/82\u20131589 diaries, Kelly and Dee\u2019s scrying partnership), the Monas Hieroglyphica (1564: the glyph as a synthesis of geometry, alchemy, and astronomy), and the scholarly reception (Casaubon\u2019s True and Faithful Relation, Yates and the modern recovery, current work, the open questions). Praxis here means literacy: the commonplace book, the tiered reading journal \u2014 no belief required."""

M2_NOTES = [
 {"title": "Concepts", "body": """- **John Dee (1527\u20131608/09)** \u2014 court mathematician, navigator, and advisor; the biographical record is DOCUMENTED throughout.
- **\u2018Brittany\u2019** \u2014 Dee\u2019s imperial-imagination concept; the British Empire idea carries his fingerprints.
- **Mortlake** \u2014 Dee\u2019s library, the largest in England; his power was bibliographic before it was anything else.
- **Enochian alphabet** \u2014 21 letters, received 6 May 1583; the date is DOCUMENTED, the reception narrative TRADITIONAL.
- **Angelical Keys** \u2014 the 48 (or 49) Calls; study their structure \u2014 the grammar claims \u2014 before their content.
- **The diaries (1581/82\u20131589)** \u2014 the day-by-day record; genuine 16th-century documents by SCHOLARLY CONSENSUS.
- **Kelly** \u2014 the scryer; Dee recorded. The division of labor shapes how the diaries must be read.
- **Scrying** \u2014 the working practice of the partnership; the diaries are its logbook.
- **Monas Hieroglyphica (1564)** \u2014 the glyph synthesizing geometry, alchemy, and astronomy; read it as a diagram that thinks.
- **True and Faithful Relation (1659)** \u2014 Casaubon\u2019s hostile edition of the diaries; the attack that preserved them.
- **Hostile transmission** \u2014 Casaubon\u2019s irony: the debunker preserved what he attacked; hostile transmission is still transmission.
- **Yates** \u2014 the 20th-century recovery of Dee; the \u2018Hermetic tradition\u2019 thesis, SCHOLARLY CONSENSUS with live CONTESTED edges.
- **Commonplace book** \u2014 the early-modern method: copy the striking passage, note the tier, add your question.
- **Tiered reading journal** \u2014 every session logged with what you read, what tier it is, and the evidence; the assessment artifact."""},
 {"title": "Hands-on procedure", "body": """Dee\u2019s diaries reward the slow reader. This procedure turns one dated entry into a tiered journal session \u2014 the same move you\u2019ll repeat across the corpus.

1. **Select one dated entry** from the 1581/82\u20131589 diaries \u2014 a short one; the boring entries are often the most DOCUMENTED.
2. **Copy the entry into your commonplace book** verbatim, with its date and archive reference.
3. **List the entry\u2019s atomic claims:** who was present, what was seen or received, what was recorded.
4. **Tier each claim separately:** the entry\u2019s existence and date are DOCUMENTED; the reception narrative is TRADITIONAL; interpretations of what happened are CONTESTED.
5. **Note the division of labor** in this entry \u2014 what Kelly saw versus what Dee wrote \u2014 and how it shapes your reading.
6. **Write one open question** the entry leaves you with, and one Monas theorem or passage it echoes, if any.
7. **Log the session** in your tiered journal: claim, tier, evidence, question. Coverage beats cherry-picking \u2014 read the boring parts."""},
 {"title": "Project brief", "body": """The brief. Build the Dee dossier \u2014 three parts, one standard: the document is tiered separately from its content.

Deliverables. (1) A documented timeline of Dee\u2019s life \u2014 mathematician, navigator, advisor, Mortlake \u2014 with a source for every event: letters, library catalogues, dated works. (2) A tiered reading of one Monas theorem or one Angelical Key: structure first (what the figure or the Call\u2019s grammar claims), content second, every claim tiered. (3) A reception comparison: Casaubon\u2019s 1659 True and Faithful Relation against Yates\u2019s 20th-century recovery \u2014 what each preserves, what each argues, and what tier each of their claims earns.

The standard. The diaries\u2019 genuineness is SCHOLARLY CONSENSUS; what they record is the open question \u2014 tier the document separately from its content, or the dossier fails. No belief is required or tested; precision is."""},
 {"title": "Honesty note", "body": """Dee the mathematician and Dee the magus are the same man \u2014 the split is a modern invention, and this module refuses it. \u2018Received 6 May 1583\u2019 is a DOCUMENTED date from the record; the reception narrative around it is TRADITIONAL; what the alphabet is remains CONTESTED \u2014 we keep those three apart at all times. The diaries are genuine 16th-century documents; genuineness is a fact about the paper, not about the angels. Original study material throughout; Interstitium Labs is affiliated with no order and confers no credential; assessments test whether you can read, tier, and argue \u2014 never what you affirm."""},
]

M2_EXPLAINS = [
 "Dee advised on the imperial imagination \u2014 DOCUMENTED advisory role. (Concepts: \u2018Brittany\u2019.)",
 "The division of labor: Kelly saw, Dee wrote \u2014 it shapes how we read the diaries. (Concepts: Kelly; Hands-on procedure, step 5.)",
 "The Angelical Keys: 48 (or 49) Calls \u2014 structure first, content second. (Concepts: Angelical Keys.)",
 "1564 \u2014 the synthetic glyph, early in Dee\u2019s career. (Concepts: Monas Hieroglyphica.)",
 "The 1659 hostile edition preserved what it attacked. (Concepts: hostile transmission.)",
 "Copy the passage, note the tier, add your question \u2014 praxis as literacy. (Concepts: commonplace book.)",
]

# ---------------------------------------------------------------- module 3
M3_SUMMARY = """Welcome to Module 3 \u2014 the seminar. I\u2019m your instructor, and for this final module we change register: from the archive to the argument. This is Module 3: The CCRU Seminar \u2014 Nick Land and the CCRU (the Warwick 1990s collective: who, where, what; the writings; primary texts in reading order; the archive itself as artifact), hyperstition (fiction as an engine, the hyperstitional circuit, examples and counter-examples \u2014 a CONTESTED theory, labeled as such), the numogram and syzygies (decimal sorcery, working the diagram, reading a technical diagram as a text), meme chaos-magic theory (Spare\u2019s sigilization in the network age, memes as hyperstitional objects, attention as a medium), and Project Cybersyn (Allende\u2019s Chile 1971\u201373, Stafford Beer and the viable system model, the operations room \u2014 what was actually built versus what has been mythologized). Read Land\u2019s 1990s corpus, then argue about what it means \u2014 with tiers."""

M3_NOTES = [
 {"title": "Concepts", "body": """- **CCRU** \u2014 the Cybernetic Culture Research Unit, Warwick University, mid-to-late 1990s: the collective, the texts, the legend.
- **Nick Land** \u2014 the 1990s writings are the seminar\u2019s spine; the later work is a separate question, out of scope.
- **Hyperstition** \u2014 fiction as an engine: ideas that make themselves real by being believed and circulated.
- **Hyperstitional circuit** \u2014 belief \u2192 action \u2192 reality \u2192 belief; the feedback loop is the theory\u2019s signature.
- **Theory status** \u2014 CONTESTED: provocative framework or mystified feedback loop is the live debate.
- **Numogram** \u2014 the decimal-sorcery diagram; treat it like an engineering drawing \u2014 precise about an imprecise thing.
- **Syzygies** \u2014 the numogram\u2019s currents and pairings; work the diagram, don\u2019t just admire it.
- **Meme chaos-magic** \u2014 Spare\u2019s sigilization, networked: memes as hyperstitional objects at internet scale.
- **Attention as a medium** \u2014 the economics of the circuit: what the loop runs on.
- **Stafford Beer** \u2014 management cybernetics; the serious theory under the Cybersyn legend.
- **Viable system model (VSM)** \u2014 Beer\u2019s model; study it before buying the chairs.
- **Project Cybersyn** \u2014 Allende\u2019s Chile, 1971\u20131973: the telex network, the VSM design, the operations room.
- **Mythologized Cybersyn** \u2014 the \u2018internet before the internet\u2019 claims; tier the hype separately from the build.
- **The archive as artifact** \u2014 how the CCRU texts survived (websites, samizdat, reissues) is part of the story; web-era texts vanish."""},
 {"title": "Hands-on procedure", "body": """Two exercises, one discipline: separate what was built from what was mythologized, and read a diagram as data.

1. **List the Cybersyn claims:** the telex network, the VSM design, the operations room with its chairs and screens, and the \u2018internet before the internet\u2019 gloss.
2. **Sort them:** DOCUMENTED build (telex network, VSM design, ops room, 1971\u201373) versus mythologized legacy (the gloss) \u2014 tier the hype separately.
3. **Run the Numogram Walker lab** (il01-lab-numogram): build the digit graph from the syzygy pairings, BFS from 0, and confirm connectivity \u2014 the diagram as data you can walk.
4. **Take one hyperstition candidate** from the corpus and test it against the circuit: did it change behavior before it was \u2018true\u2019? Record the counter-examples too \u2014 failed prophecies are data.
5. **Journal the session:** every claim tiered, every tier evidenced. The circuit needs the feedback to close; check whether it did."""},
 {"title": "Project brief", "body": """The brief. Choose one candidate hyperstition \u2014 from the Land/CCRU corpus or the meme layer \u2014 and build the case file.

Deliverables. (1) The circuit, documented: belief \u2192 action \u2192 reality \u2192 belief, with dated evidence at each arrow \u2014 or the dated evidence that the loop failed to close. (2) Counter-examples: at least two failed prophecies or stillborn circuits, tiered. (3) A verdict of about 500 words argued both ways: the strongest case that the circuit is real, and the strongest case that it is mystified feedback. (4) The Cybersyn contrast: one page on what honest tiering looks like when applied to a documented build versus its mythology.

The standard. The theory\u2019s CONTESTED status is not a defect to hide \u2014 it is the seminar\u2019s subject. You are graded on whether your tiers hold and your evidence is dated, never on which side you take."""},
 {"title": "Honesty note", "body": """Hyperstition is presented as a CONTESTED theory throughout \u2014 the seminar\u2019s job is to map the argument, not to settle it. Land\u2019s post-1990s work is a separate question and out of scope; we read the 1990s corpus. Cybersyn\u2019s documented build (telex network, VSM design, ops room, 1971\u201373) and its mythologized legacy are different tiers, and we never let the legend borrow the build\u2019s credibility. Meme chaos-magic is taught as hypothesis \u2014 the chaos-magic lineage is real, the network-age extension is argued, not asserted. Original study material; no credential conferred; assessments test whether you can map the circuit and tier the claims \u2014 never what you believe."""},
]

M3_EXPLAINS = [
 "The feedback loop \u2014 ideas bootstrapping themselves into reality. (Concepts: hyperstitional circuit.)",
 "The circuit\u2019s signature: behavioral effects preceding truth. (Hands-on procedure, step 4.)",
 "Precision about the imprecise thing \u2014 diagram literacy. (Concepts: numogram.)",
 "Real build; the mythology is the separate tier. (Concepts: Project Cybersyn; Hands-on procedure, step 2.)",
 "The serious theory under the Cybersyn legend. (Concepts: viable system model.)",
 "Sigils in the network age \u2014 the chaos-magic technique scaled. (Concepts: meme chaos-magic.)",
]

# ------------------------------------------------------- terminalSims (new)
TERMINAL_SIMS = [
 {"id": "il01-tiering-terminal",
  "title": "The Tiering Terminal",
  "brief": "Practice the tier discipline at the command line \u2014 query the academy\u2019s tiers, dates, and figures. Every answer restates this course\u2019s own material.",
  "prompt": "learner@il:tier$",
  "commands": [
   {"cmd": "help", "out": "commands: tiers | corpus | casaubon | dee | monas | cybersyn | hyperstition | journal | honesty"},
   {"cmd": "tiers", "out": "DOCUMENTED \u2014 primary sources, artifacts, dated texts. | SCHOLARLY CONSENSUS \u2014 what historians agree on, provisional and cited. | TRADITIONAL \u2014 what lineages claim about themselves, reported not endorsed. | CONTESTED \u2014 open questions and rival readings."},
   {"cmd": "corpus", "out": "Corpus Hermeticum + Asclepius: late-antique Alexandrian dialogues attributed to Hermes Trismegistus. Read the Asclepius first \u2014 the most complete single text."},
   {"cmd": "casaubon", "out": "Isaac Casaubon, 1614: dated the Corpus to late antiquity by philology. The founding act of esoteric historiography \u2014 dates have consequences."},
   {"cmd": "dee", "out": "John Dee, 1527\u20131608/09: court mathematician, navigator, advisor. Mortlake held the largest library in England."},
   {"cmd": "monas", "out": "Monas Hieroglyphica, 1564: one glyph synthesizing geometry, alchemy, and astronomy. Read it as a diagram that thinks."},
   {"cmd": "cybersyn", "out": "Project Cybersyn, Chile 1971\u201373: telex network, viable system model, operations room. DOCUMENTED build; mythologized legacy tiered separately."},
   {"cmd": "hyperstition", "out": "Fiction as an engine: belief \u2192 action \u2192 reality \u2192 belief. Theory status: CONTESTED."},
   {"cmd": "journal", "out": "Log every reading: claim, tier, evidence, open question. The journal is the assessment artifact."},
   {"cmd": "honesty", "out": "Assessments test literacy, never belief. Original study material; no credential conferred; no affiliation with any order."},
  ]},
]

# ------------------------------------------------------------------ apply
NEWMODS = {
 "il01-hermetic-foundations": (M1_SUMMARY, M1_NOTES, M1_EXPLAINS),
 "il01-dee-enochian": (M2_SUMMARY, M2_NOTES, M2_EXPLAINS),
 "il01-ccru-seminar": (M3_SUMMARY, M3_NOTES, M3_EXPLAINS),
}

COMPETITORS = ('aleks', 'brilliant', 'khan academy', 'coursera', 'udemy', 'edx')

def _brand_free(blob, where):
    for c in COMPETITORS:
        assert not re.search(r'\b' + re.escape(c) + r'\b', blob), f'competitor brand in {where}: {c}'

for m in data['modules']:
    summary, notes, explains = NEWMODS[m['id']]
    m['summary'] = summary
    m['weight'] = 1
    m['notes'] = notes
    assert len(notes) == 4, m['id']
    assert [n['title'] for n in notes] == ['Concepts', 'Hands-on procedure', 'Project brief', 'Honesty note']
    assert notes[0]['body'].count('\n- **') >= 5, 'concepts glossary too thin'
    assert len(m['quiz']) >= 4
    assert len(explains) == len(m['quiz'])
    for i, q in enumerate(m['quiz']):
        q['explain'] = explains[i]
        assert len(q['choices']) == 4, q['q']
        assert isinstance(q['answer'], int) and 0 <= q['answer'] < 4, q['q']
        assert q['explain'].strip(), q['q']
    assert len(m['cards']) >= 5
    blob = json.dumps(m).lower()
    _brand_free(blob, m['id'])

data['terminalSims'] = TERMINAL_SIMS

# course-level sanity: required keys exist
for k in ('arc', 'priorities', 'battlePlan', 'mockTasks', 'cheatSheets', 'answerBank', 'sourceLinks', 'honestyNote'):
    assert k in data and data[k], f'missing {k}'
assert isinstance(data['mockMinutes'], int)
for s in data['sourceLinks']:
    assert s.get('retrieved'), 'sourceLink missing retrieved date'

blob = json.dumps(data).lower()
_brand_free(blob, 'course-level')
assert 'palantir' not in blob

fd, tmp = tempfile.mkstemp(dir=os.path.dirname(COURSE), suffix='.tmp')
with os.fdopen(fd, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
with open(tmp, encoding='utf-8') as f:
    json.load(f)  # validate AFTER
os.replace(tmp, COURSE)
print('COURSE OK: 3 modules retrofitted, terminalSims added, JSON valid.')
