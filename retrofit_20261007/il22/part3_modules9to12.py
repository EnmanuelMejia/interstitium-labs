#!/usr/bin/env python3
"""Retrofit IL-22 modules 9-12 (theosophy, golden dawn, grimoires, gnosticism)."""
import json, os

PATH = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json'
GL = '- **%s** \u2014 %s'

UPDATES = {

'm22-theosophy': {
'summary': (
    "Welcome to Module 9 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're meeting "
    "the most consequential \u2014 and most contested \u2014 figure of the 19th-century occult revival: Helena Petrovna Blavatsky (1831\u20131891). "
    "You'll learn how she and Henry Steel Olcott founded the Theosophical Society in New York in 1875, what *Isis Unveiled* (1877) and *The "
    "Secret Doctrine* (1888) actually argue \u2014 root races, planetary rounds, the hidden *Book of Dzyan* \u2014 who the Masters were claimed "
    "to be, and what the 1885 Hodgson Report concluded (and what the Society for Psychical Research later withdrew). Then the influence "
    "question: the New Age, abstract art, Yeats, Indian nationalism \u2014 understanding modern esotericism is impossible without Theosophy, "
    "whatever you conclude about Blavatsky. This module is claim-sorting under maximum pressure: unproven phenomena, a contested documentary "
    "record, and undeniable historical influence, all at once."
),
'glossary': [
    GL % ('Theosophical Society', 'founded 1875 in New York by Blavatsky, Olcott, and associates; three objects: universal brotherhood, comparative religion/science study, investigation of unexplained natural laws and psychic powers.'),
    GL % ('Mahatmas (Masters)', 'the hidden adepts \u2014 notably Koot Hoomi and Morya \u2014 claimed to guide the Society; the \u201cMahatma Letters\u201d are the documentary core of the claim and the controversy.'),
    GL % ('Isis Unveiled (1877)', "Blavatsky\u2019s first major work: an attack on materialist science and Christian orthodoxy defending occult phenomena."),
    GL % ('The Secret Doctrine (1888)', 'the vast cosmology \u2014 seven root races cycling through planetary rounds, Fohat, cosmic evolution \u2014 allegedly drawn from the hidden *Book of Dzyan*.'),
    GL % ('Book of Dzyan', 'the hidden text the *Secret Doctrine* claims as its source; scholars read the work as Blavatsky\u2019s syncretic composition from 19th-century sources.'),
    GL % ('Hodgson Report', 'the Society for Psychical Research\u2019s 1885 investigation concluding fraud; the SPR partially withdrew criticisms in 1986 without endorsing the phenomena.'),
],
'proc_intro': (
    "Theosophy is where claim-sorting earns its keep. Apply this six-step controversy audit to the Blavatsky case \u2014 then reuse it on "
    "Crowley, Gardner, or any contested figure in this course."
),
'steps': [
    "**List the claims separately.** Phenomena claims (the Masters' letters, occult phenomena), source claims (the *Book of Dzyan*), historical claims (the Society's founding, 1875, New York). One list, three labels \u2014 never let a verdict on one bleed into another.",
    "**Check each against the record.** Hodgson Report (1885): fraud. SPR's 1986 partial withdrawal: criticisms retracted, phenomena not endorsed. The *Secret Doctrine*'s sources: 19th-century materials, per scholarship. Write what is established for each.",
    "**State the honest position in the module's formula.** 'The claims are unproven, the documentary record contested, the movement's influence undeniable.' Memorize this sentence \u2014 it is the etic verdict.",
    "**Now read emically.** In the Society's own terms: universal brotherhood, the Masters guiding humanity, the *Secret Doctrine* as ancient wisdom. Summarize the inside view fairly \u2014 charity first.",
    "**Trace the influence.** New Age thought, abstract art (Kandinsky, Mondrian), Yeats, Annie Besant's later leadership and Indian nationalism, the garbled-but-real transmission of Buddhist and Hindu concepts West. List five.",
    "**Ask the transmission question.** What did Theosophy *do* with 'Eastern wisdom' \u2014 what work did the claim of ancient Eastern sources perform for a 19th-century Western movement? This is the Casaubon question applied to 1875.",
],
'project': (
    "Write a 700-word controversy dossier on Blavatsky in three labeled parts. Part 1 (emic): the Society's founding (1875, New York, Blavatsky "
    "and Olcott), the three objects, the Masters and the Mahatma Letters, and the *Secret Doctrine*'s cosmology (root races, planetary rounds, "
    "*Book of Dzyan*) \u2014 all in the tradition's own terms. Part 2 (etic): the Hodgson Report (1885), the SPR's 1986 partial withdrawal, and "
    "the scholarly reading of the *Secret Doctrine* as syncretic 19th-century composition. Part 3: the influence audit \u2014 the modern New Age, "
    "Kandinsky, Mondrian, Yeats, Besant and Indian nationalism, the transmission of Eastern concepts West \u2014 with one paragraph on what the "
    "'ancient Eastern wisdom' claim *did* for the movement. Conclude with the module's honest-position formula, applied."
),
'honesty': (
    "This module asserts nothing about the reality of the Masters, the phenomena, or the *Book of Dzyan* \u2014 the claims are reported as the "
    "Society's claims, the investigations are reported as investigations, and the honest position is stated outright: claims unproven, record "
    "contested, influence undeniable. The SPR's 1986 move is reported precisely \u2014 criticisms partially withdrawn, phenomena not endorsed \u2014 "
    "not inflated into vindication. Theosophy's cultural influence is history; its metaphysics is the tradition's own teaching."
),
'cards_add': [
    ("Annie Besant: significance in this module?",
     "Later Theosophical leader whose work fed Indian nationalism \u2014 part of the movement's historical influence."),
],
'quiz_add': [
    ("Blavatsky's dates are:",
     ["1875\u20131947", "1831\u20131891", "1890\u20131946", "1884\u20131964"],
     1,
     "1831\u20131891 \u2014 the Society's founding (1875) falls mid-career; see the Concepts notes."),
    ("The Society's headquarters later moved to:",
     ["London", "Adyar, India", "Paris", "Cairo"],
     1,
     "Founded in New York (1875); headquarters later moved to Adyar \u2014 the India connection that fed Besant's nationalism work."),
    ("Fohat, in the *Secret Doctrine*'s cosmology, belongs to:",
     ["The three objects", "The cosmic-evolution vocabulary \u2014 alongside root races and planetary rounds", "The Hodgson Report", "The Mahatma Letters' signatories"],
     1,
     "The Concepts notes: root races, planetary rounds, Fohat and cosmic evolution \u2014 the *Secret Doctrine*'s system."),
    ("Koot Hoomi and Morya are presented as:",
     ["The Society's elected presidents", "Mahatmas \u2014 hidden adepts corresponding with early Theosophists", "Ancient Egyptian priests", "Fictional characters Blavatsky disowned"],
     1,
     "The Mahatma Letters are the documentary core of the Masters claim \u2014 and of the controversy."),
    ("The SPR's 1986 action on the Hodgson Report was to:",
     ["Fully vindicate Blavatsky", "Withdraw some criticisms without endorsing the phenomena", "Reaffirm every charge", "Dissolve the Society"],
     1,
     "Precision matters: partial withdrawal of criticisms, no endorsement of phenomena \u2014 the honesty note's formula."),
    ("Theosophy's transmission of Buddhist and Hindu concepts West is described as:",
     ["Perfectly accurate", "Garbled but real \u2014 however distorted, the concepts traveled", "Entirely fabricated", "A purely Indian initiative"],
     1,
     "The Concepts notes: 'however garbled' \u2014 influence and distortion together, honestly stated."),
],
},

'm22-golden-dawn': {
'summary': (
    "Welcome to Module 10 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're entering "
    "the order that rewired modern magic: the Hermetic Order of the Golden Dawn, London, 1888\u20131903. You'll learn the founding story \u2014 "
    "Westcott, Mathers, Woodman, the Cipher Manuscripts, and the mysterious Anna Sprengel of Nuremberg, whose existence scholars have never "
    "verified \u2014 the grade system climbing the Tree of Life from Neophyte 0=0 to Adeptus Minor 5=6, and the great synthesis itself: Qabalah, "
    "tarot, astrology, Enochian, and Egyptian-flavored ritual fused into one curriculum. Then the breakup \u2014 the Battle of Blythe Road, "
    "Mathers' autocracy, the exposed letters \u2014 and the legacy: Regardie's 1937\u20131940 publication, Crowley, Dion Fortune, and Wicca all "
    "drinking from this well. Nearly everything 'ceremonial magic' means today was assembled in these fifteen years."
),
'glossary': [
    GL % ('Cipher Manuscripts', 'the encoded rituals Westcott claimed came from a German adept \u2014 the Golden Dawn\u2019s founding documents; the manuscripts look like work of Westcott\u2019s era, possibly his own.'),
    GL % ('Anna Sprengel', 'the Nuremberg adept whose address the manuscripts supposedly supplied \u2014 her existence has never been verified by scholars.'),
    GL % ('Outer Order', 'the elemental curriculum: Neophyte 0=0 through Philosophus 4=7 \u2014 the Order as school, with examinations in the correspondences.'),
    GL % ('Inner (Second) Order', 'the *Rosae Rubeae et Aureae Crucis*: Adeptus Minor 5=6 and above, entered through the Vault of the Adepti ritual.'),
    GL % ('The synthesis', 'the Golden Dawn\u2019s fusion \u2014 Qabalah as filing system, tarot on the paths, astrology, Enochian Watchtower magic, Egyptian-flavored ritual, Middle Pillar, pentagram/hexagram rituals, tattva vision.'),
    GL % ('Battle of Blythe Road', 'the 1900 rupture: Mathers initiated Crowley into the Second Order against the London adepts\u2019 wishes \u2014 the break point of the Order.'),
],
'proc_intro': (
    "The Golden Dawn was a *system* \u2014 its power was the cross-referencing. This six-step exercise teaches you to work the correspondences "
    "the way an Outer Order student did: one symbol, traced through every grid."
),
'steps': [
    "**Pick one tarot trump.** Choose any Major Arcana card \u2014 e.g., The Emperor or The Moon, whose correspondences this course has given you.",
    "**Place it on the Tree.** Which of the 22 paths (Hebrew letters) does the Golden Dawn system assign it to? Write the path and letter.",
    "**Add the astrology.** What is its astrological correspondence (e.g., The Emperor\u2013Aries, The Moon\u2013Pisces)? Add it to the card's entry.",
    "**Add the Enochian layer.** Which Watchtower/elemental quarter does the card's elemental dignity belong to? (The Golden Dawn wired Enochian's Watchtowers into its elemental grade rituals.)",
    "**Write the synthesis sentence.** One sentence combining all four layers \u2014 Tree path, Hebrew letter, astrology, element \u2014 the way a Golden Dawn paper would file the symbol.",
    "**Label the invention.** Every correspondence you just wrote is a 19th-century synthesis, not an ancient inheritance. End with one etic sentence: who built this grid (Westcott, Mathers, Woodman, 1888), from what sources, and what the unverified Sprengel story did for the Order's authority.",
],
'project': (
    "Write a 700-word order dossier on the Golden Dawn in three labeled parts. Part 1: the founding \u2014 1888, London, Westcott, Mathers, "
    "Woodman; the Cipher Manuscripts and the Anna Sprengel address; the scholarly status of each (manuscripts look like Westcott's era's work; "
    "Sprengel never verified). Part 2: the machine \u2014 the grade system (Outer Order 0=0\u20134=7, Inner Order from 5=6, the Vault of the "
    "Adepti), the examinations, and the synthesis (Qabalah, tarot, astrology, Enochian, Egyptian-flavored ritual, Middle Pillar, pentagram/hexagram "
    "rituals, tattva vision). Part 3: the breakup and legacy \u2014 1900\u20131903, the Battle of Blythe Road, Mathers' autocracy, the exposed "
    "Sprengel letters; successor orders (Stella Matutina, Alpha et Omega); Regardie's 1937\u20131940 publication; Crowley, Dion Fortune, and Wicca. "
    "Conclude with the lineage verdict in the module's two-sentence form: what the documents support, and what the founding story did for the Order."
),
'honesty': (
    "Anna Sprengel's existence is unverified \u2014 this module states that plainly and does not launder the founding story into fact. The "
    "Cipher Manuscripts are reported as appearing to be work of Westcott's era, possibly his own composition. The correspondences are "
    "presented as the Golden Dawn's 19th-century synthesis \u2014 brilliant as a system, not ancient as a transmission. The Order's influence "
    "on a century of ceremonial magic is history; its charter myth is the tradition's own story, labeled as such."
),
'cards_add': [
    ("The Vault of the Adepti?",
     "The initiation ritual of the Second Order \u2014 entered at Adeptus Minor 5=6."),
],
'quiz_add': [
    ("The three founders were:",
     ["Westcott, Mathers, and Crowley", "Westcott, Mathers, and Woodman", "Blavatsky, Olcott, and Judge", "Dee, Kelley, and Ficino"],
     1,
     "1888, London: William Wynn Westcott, S. L. MacGregor Mathers, William Robert Woodman."),
    ("The grade Philosophus 4=7 belongs to:",
     ["The Inner Order", "The Outer Order's elemental grades", "The Third Order", "No order"],
     1,
     "Outer Order: Neophyte 0=0 through Philosophus 4=7; the Second Order begins at 5=6."),
    ("Tattva vision techniques in the Golden Dawn curriculum were:",
     ["Egyptian funerary rites", "Vision techniques adapted into the synthesis alongside the Middle Pillar and pentagram rituals", "A tarot spread", "The Enochian Calls"],
     1,
     "The Concepts notes list them among the synthesis components: Middle Pillar, pentagram/hexagram rituals, tattva vision."),
    ("Stella Matutina and Alpha et Omega were:",
     ["Golden Dawn successor orders after the 1900\u20131903 breakup", "Theosophical lodges", "Rosicrucian manifestos", "Tarot decks"],
     0,
     "Successor orders carried the system forward after the rupture \u2014 see the Concepts notes."),
    ("Israel Regardie's 1937\u20131940 publication did what?",
     ["Founded a new order", "Made the Golden Dawn's rituals public property", "Debunked the Cipher Manuscripts", "Translated the Zohar"],
     1,
     "Regardie's publication ended the secrecy \u2014 the system became public property."),
    ("The Golden Dawn's Enochian material came from:",
     ["Blavatsky's Masters", "Dee and Kelley's system, absorbed wholesale \u2014 Watchtower rituals and grade ceremonies", "The Cipher Manuscripts alone", "Medieval grimoires"],
     1,
     "Absorption: Dee's Tablets rebuilt into the Order's Watchtower rituals \u2014 the Enochian module's afterlife layer."),
],
},

'm22-grimoires': {
'summary': (
    "Welcome to Module 11 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're opening "
    "the handbooks of ritual magic themselves: the grimoires. You'll learn what these 14th\u201317th-century Solomonic manuals promise and "
    "how they work \u2014 the *Key of Solomon*'s machinery of purity, pentacles, and divine names; the *Ars Goetia*'s 72 demons in their "
    "hierarchy of kings, dukes, princes, marquises, and counts, each with seal, office, and appearance; and the ritual logic itself: the "
    "circle protects the operator, the triangle constrains the spirit, the divine names compel obedience. Then the honest reading: scholars' "
    "etic view of demonology as systematized cosmology and anxiety about power, practitioners' two modern readings \u2014 external entities vs. "
    "Jungian archetypes \u2014 and the course's rule that both are *readings*, not verdicts."
),
'glossary': [
    GL % ('Grimoire', 'a handbook of ritual magic \u2014 chiefly the Solomonic tradition, in manuscripts mainly 14th\u201317th c. (printed from the 17th), drawing on Jewish, Christian, and Arabic magical traditions.'),
    GL % ('Key of Solomon (*Clavicula Salomonis*)', 'the classic grimoire: preparations (fasting, prayer, vestments), pentacles, consecrated tools, conjuration by divine names.'),
    GL % ('Ars Goetia', 'first book of the *Lesser Key of Solomon*: 72 demons in hierarchy, each with office, appearance, and seal; revived for modern occultism by the 1904 Mathers/Crowley edition.'),
    GL % ('Circle / triangle / names', 'the ritual logic: the circle protects the operator, the triangle constrains the spirit, divine names compel obedience.'),
    GL % ('Pseudepigraphic frame', 'the Solomonic attribution \u2014 wisdom literature in King Solomon\u2019s legendary name, not his authorship.'),
    GL % ('Evocation', 'the ritual operation of calling a spirit to visible appearance within the triangle \u2014 commanded by divine names, not personal power.'),
],
'proc_intro': (
    "Grimoires are procedural texts \u2014 they can be analyzed like protocols. Run this six-step ritual-logic analysis on the Goetic operation "
    "as the Concepts notes describe it. You are dissecting the *logic*, not performing the rite."
),
'steps': [
    "**State the aim.** What does the operator want \u2014 knowledge, treasure, influence? Write the grimoire's promised outcome in one sentence.",
    "**List the preparations.** Fasting, prayer, vestments, pentacles, consecrated tools \u2014 the *Key of Solomon*'s purity requirements. Note how they frame the magic as religious operation.",
    "**Diagram the space.** Draw the circle (operator's protection), the triangle (the spirit's constraint), and the placement of seals and names. Label each element's function.",
    "**Identify the authority.** By what does the magician command? Divine names \u2014 not personal power. Write the sentence: 'The operator commands by ___ .'",
    "**Read the spirit two ways.** Reading A (traditional practitioner): an external entity with office and appearance. Reading B (Jungian-influenced, 20th c.): a psychological archetype. State what each reading explains and what it leaves out.",
    "**Place it etically.** Scholars read grimoires as religious literature reflecting their eras' cosmologies \u2014 demonology as systematized anxiety about power. Write the etic paragraph: 14th\u201317th-century manuscripts, Jewish/Christian/Arabic sources, the world that needed ranked spirits.",
],
'project': (
    "Write a 700-word grimoire dossier in three labeled parts. Part 1: the tradition \u2014 what grimoires are, the Solomonic pseudepigraphic "
    "frame, the manuscript dates (14th\u201317th c.) and sources (Jewish, Christian, Arabic magical traditions). Part 2: two worked systems \u2014 "
    "the *Key of Solomon* (preparations, pentacles, tools, conjuration by divine names) and the *Ars Goetia* (72 demons, the hierarchy of kings "
    "through counts, seals/offices/appearances, the 1904 Mathers/Crowley revival); include your labeled diagram of circle, triangle, and names "
    "with each element's function. Part 3: the honest reading \u2014 the scholarly etic view and the two practitioner readings, each labeled as "
    "a *reading*, with one paragraph on why the course refuses verdicts here."
),
'honesty': (
    "Nothing in this module instructs, encourages, or endorses the practice of spirit evocation \u2014 the operations are analyzed as historical "
    "ritual logic, never as how-to. The demons' reality is never asserted: the scholarly reading (religious literature, systematized cosmology) "
    "and the practitioner readings (external entities; Jungian archetypes) are presented side by side as *readings*. The Solomonic attribution "
    "is reported as a pseudepigraphic frame, not as history."
),
'cards_add': [
    ("The Lesser Key of Solomon: structure?",
     "A composite grimoire whose first book is the Ars Goetia (72 demons); the 1904 Mathers/Crowley edition revived it."),
],
'quiz_add': [
    ("Grimoire manuscripts date mainly from:",
     ["The 2nd\u20133rd centuries CE", "The 14th\u201317th centuries", "The 19th century", "Antiquity"],
     1,
     "14th\u201317th c. manuscripts (printed from the 17th) \u2014 drawing on older Jewish, Christian, and Arabic traditions."),
    ("The *Key of Solomon*'s pentacles are:",
     ["Demon seals", "Consecrated geometric figures used in the operations", "Coins", "Tarot cards"],
     1,
     "Pentacles, consecrated tools, vestments, fasting and prayer \u2014 the purity-preparation machinery."),
    ("In Goetic hierarchy, which ranks appear?",
     ["Only kings", "Kings, dukes, princes, marquises, counts", "Angels only", "No ranks"],
     1,
     "72 demons in full feudal hierarchy \u2014 each with office, appearance, and seal."),
    ("The triangle's function in the ritual logic is to:",
     ["Protect the operator", "Constrain the spirit", "Hold the incense", "Mark the compass points"],
     1,
     "Circle = operator's protection; triangle = the spirit's constraint; names = compulsion."),
    ("The Jungian-influenced reading of the Goetic spirits treats them as:",
     ["Proven external entities", "Psychological archetypes", "Literary frauds", "Alchemical stages"],
     1,
     "The 20th-century practitioner reading: archetypes \u2014 presented as a reading, not a verdict."),
    ("The 1904 Goetia edition's significance was:",
     ["Its debunking of the text", "Its revival of the Goetia for modern occultism (Mathers with Crowley)", "Its translation into Latin", "Its use by the Golden Dawn's Outer Order"],
     1,
     "Mathers/Crowley 1904: the edition that carried the Goetia into 20th-century magic."),
],
},

'm22-gnosticism': {
'summary': (
    "Welcome to Module 12 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're opening "
    "the sealed jar of 1945: thirteen codices from Nag Hammadi, Egypt \u2014 fifty-two texts that let the so-called heretics speak for "
    "themselves for the first time in sixteen centuries. You'll learn the classic Gnostic myth as scholars reconstruct it \u2014 the "
    "transcendent God, the fall that produces the demiurge, the flawed material world, the trapped sparks of light, and salvation through "
    "*gnosis*, direct experiential knowing \u2014 and what *gnosis* actually means (acquaintance with the divine, not information about it). "
    "Then the quieter current beside it: esoteric Christianity \u2014 Meister Eckhart on the Godhead beyond God, Jacob B\u00f6hme on the Ungrund, "
    "the Philokalia's hesychast inner prayer \u2014 contemplative practice at the edge of orthodoxy rather than an alternative cosmology. "
    "Before 1945 we knew Gnosticism through its enemies; now we read both sides."
),
'glossary': [
    GL % ('Nag Hammadi library', '1945, Egypt: 13 codices, 52 texts (Gospel of Thomas, Gospel of Philip, Apocryphon of John) \u2014 Gnostic voices in their own words.'),
    GL % ('Demiurge', "'craftsman-god' \u2014 in the reconstructed myth, the lesser creator responsible for flawed matter, often identified with the Old Testament creator."),
    GL % ('Gnosis', 'Greek: knowledge \u2014 salvific, transformative *acquaintance* with the divine, not information about it; the mechanism of salvation in these texts.'),
    GL % ('Apocryphon of John', 'a core Nag Hammadi text presenting the classic Gnostic myth in full \u2014 the fall, the demiurge, the sparks, the savior\u2019s revelation.'),
    GL % ('Meister Eckhart', 'c. 1260\u20131328 \u2014 Dominican mystic of the Godhead beyond God; the esoteric-Christian current within (and at the edge of) orthodoxy.'),
    GL % ('Hesychasm', 'the Orthodox inner-prayer tradition of the Philokalia \u2014 contemplative esotericism inside Christianity, not an alternative cosmology.'),
],
'proc_intro': (
    "Gnostic texts reward slow, structural reading. Run this six-step myth-mapping procedure on the reconstructed Gnostic myth from the "
    "Concepts notes \u2014 it works on any Nag Hammadi text you read afterward."
),
'steps': [
    "**Name the actors.** Transcendent God, the fall/error, the demiurge, the material world, the trapped sparks, the revealer. List them \u2014 every Gnostic text casts these roles, even when the names change.",
    "**Chart the fall.** What goes wrong, and at whose hands? Write the cosmogonic sequence in five short clauses: fullness \u2192 error \u2192 demiurge \u2192 flawed matter \u2192 trapped light.",
    "**Locate gnosis.** Where in the text does saving knowledge arrive \u2014 and what does it reveal? Note the Gospel of Thomas's formulation (saying 77): the kingdom 'inside of you, and it is outside of you.'",
    "**Ask the community question.** Do these texts describe historical communities' beliefs or literary theology? Report the debate from the Concepts notes \u2014 the course reports it, not a verdict.",
    "**Contrast the neighbor.** Place the myth beside the esoteric-Christian current: Eckhart's Godhead beyond God, B\u00f6hme's Ungrund and divine unfolding, hesychast inner prayer. What stays inside orthodoxy, and what breaks with it?",
    "**Write the before/after.** One paragraph on what 1945 changed: before, Gnosticism known through Irenaeus's *Against Heresies* (~180 CE); after, thirteen codices of first-person voices. That contrast is the module's historiographical lesson.",
],
'project': (
    "Write a 700-word 'two-libraries' essay. Part 1: the Nag Hammadi library \u2014 the 1945 discovery, the thirteen codices and fifty-two "
    "texts, and the reconstructed classic myth (transcendent God, demiurge, flawed matter, trapped sparks, salvation by gnosis) presented as "
    "the texts' teaching. Part 2: the *other* library \u2014 what was known before 1945 through Irenaeus's *Against Heresies* (~180 CE), and how "
    "the new texts changed scholarship's picture; include the debated question (historical communities vs. literary theology) reported as a "
    "debate. Part 3: the esoteric-Christian current \u2014 Eckhart (c. 1260\u20131328), B\u00f6hme (1575\u20131624) on the Ungrund, the Philokalia "
    "hesychasts \u2014 with one paragraph distinguishing contemplative practice at orthodoxy's edge from alternative cosmology. Close with a "
    "definition of gnosis in your own words."
),
'honesty': (
    "The Gnostic myth is presented as the texts' teaching \u2014 'this is what these writings claim' \u2014 never as history or metaphysics "
    "asserted by the course. Whether the texts describe real communities or literary theology is reported as a live scholarly debate, not "
    "settled. The Nag Hammadi codices are dated as scholarship dates them: 4th-century Coptic copies of earlier Greek works (roughly 2nd\u20134th "
    "centuries CE). Eckhart, B\u00f6hme, and the hesychasts are placed honestly at orthodoxy's edge \u2014 contemplatives, not Gnostics."
),
'cards_add': [
    ("The Gospel of Thomas, saying 77 (translators' rendering)?",
     "The kingdom is 'inside of you, and it is outside of you' \u2014 gnosis as direct acquaintance."),
],
'quiz_add': [
    ("The Nag Hammadi codices are, physically:",
     ["1st-century scrolls", "4th-century Coptic copies of earlier Greek works", "19th-century forgeries", "Medieval Latin manuscripts"],
     1,
     "Dated 2nd\u20134th c. CE in scholarship \u2014 4th-century Coptic copies preserving earlier Greek texts."),
    ("The *Apocryphon of John* is central because it:",
     ["Attacks Gnosticism", "Presents the classic Gnostic myth in full", "Is a tarot manual", "Dates to 1945"],
     1,
     "A core Nag Hammadi text: the fall, the demiurge, the sparks, the savior's revelation."),
    ("Irenaeus's *Against Heresies* (~180 CE) matters here as:",
     ["A Gnostic gospel", "The orthodox opponents' account \u2014 nearly all that was known before 1945", "A Nag Hammadi codex", "A modern commentary"],
     1,
     "Before the jar: Gnosticism known through its enemies. After: the heretics speak."),
    ("B\u00f6hme's *Ungrund* belongs to:",
     ["The Gnostic myth", "Esoteric Christianity \u2014 the divine unfolding at orthodoxy's edge", "The Enochian Aethyrs", "Alchemical stages"],
     1,
     "Jacob B\u00f6hme (1575\u20131624): the Ungrund \u2014 contemplative, at the edge of orthodoxy, not an alternative cosmology."),
    ("In these texts, the material world is presented as:",
     ["Perfect", "Flawed \u2014 the demiurge's compromised craftsmanship", "Irrelevant", "The highest good"],
     1,
     "The reconstructed myth: flawed matter, trapped sparks \u2014 hence salvation by gnosis, not by works."),
    ("The scholarly debate the course reports (not a verdict) is whether the texts describe:",
     ["Real events in Egypt", "Historical communities' beliefs or literary theology", "Alchemy", "The future"],
     1,
     "The Concepts notes: debated \u2014 the course reports the debate, and refuses the verdict."),
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
    print('part3 ok: modules 9-12 retrofitted')

if __name__ == '__main__':
    main()
