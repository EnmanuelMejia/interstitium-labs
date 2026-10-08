#!/usr/bin/env python3
"""Retrofit IL-22 modules 1-4 to the Multicloud course template.
Loads the course JSON, rewrites summaries to instructor voice, restructures
notes into the four template sections (Concepts / Hands-on procedure /
Project brief / Honesty note) while preserving all existing factual content
verbatim, expands cards to 6 and quiz to 10 per module. Writes atomically
and re-validates with json.load.
"""
import json, os

PATH = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json'

GL = '- **%s** \u2014 %s'  # glossary bullet: "- **term** — definition"

UPDATES = {

'm22-approaching': {
'summary': (
    "Welcome to Module 1 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, "
    "and before we open a single grimoire or lay out a single tarot card, we are going to settle the most important thing "
    "in the whole course: how to study esoteric traditions honestly. You'll learn the difference between emic reading "
    "(taking a tradition's own categories seriously) and etic reading (standing outside with the scholar's tools), why "
    "claimed ancient lineages need scrutiny without contempt, and the framing contract this course keeps from here to the "
    "final module \u2014 traditions presented as the traditions present themselves, never as verified science. This is the "
    "module everything else stands on, so read it like a craftsman reads a level: everything we build later has to sit true to it."
),
'glossary': [
    GL % ('Emic', "reading from inside a tradition's own categories \u2014 e.g., what the Tree of Life *means* within Kabbalah."),
    GL % ('Etic', 'reading from outside the tradition \u2014 historical, sociological, or philological analysis, e.g., the social role of court alchemists.'),
    GL % ('Pseudepigraphy', 'attributing a text to a figure other than its actual author \u2014 e.g., the Zohar\u2019s attribution to the 2nd-century Shimon bar Yochai.'),
    GL % ('Lineage claim', 'a tradition\u2019s assertion of ancient or unbroken transmission; scholarship treats these as claims to be tested, not facts to be assumed.'),
    GL % ('Primary source', 'a document from within the period or tradition under study \u2014 Dee\u2019s diaries, manuscript copies of the Corpus Hermeticum \u2014 as distinct from later commentary about it.'),
    GL % ('Claim sorting', 'separating a historical claim (judged by archives) from a symbolic claim (judged by coherence) from an experiential claim (judged by phenomenology) before evaluating any of them.'),
],
'proc_intro': (
    "Whenever this course \u2014 or any book, video, or teacher \u2014 hands you an esoteric claim, run it through the four-question "
    "claim-sort before you decide what to do with it. Do this now with one claim from any later module's reading list; it takes ten minutes."
),
'steps': [
    "**Isolate the claim verbatim.** Copy the sentence exactly. Most confusion starts from paraphrasing a claim into something stronger or weaker than it was.",
    "**Sort the claim.** Is it historical ('this text dates to 1500 BCE'), symbolic ('the serpent means renewal'), or experiential ('this practice produces insight')? Write the label next to the quote.",
    "**Check the scholarship on dating and authorship.** What do historians actually accept? Use the module's study notes and source links \u2014 the Casaubon pattern from this module's notes is your model: claimed Mosaic antiquity, philological redating to the 2nd\u20133rd centuries CE.",
    "**Ask what the claim did.** If a tradition claims ancient origins, don't stop at true-or-false: ask what work the claim performed \u2014 authority, continuity, reform. Write one sentence.",
    "**Label your reading.** Note whether you are reading emically (the tradition's own logic) or etically (the scholar's outside view) right now \u2014 and switch deliberately, not by accident.",
],
'project': (
    "Write a 600-word source-critical dossier on the tradition of any one later module (Kabbalah, Hermeticism, alchemy, astrology, tarot, "
    "Enochian, Rosicrucianism, or Theosophy). The dossier has three labeled parts: (1) the tradition's central claims in its own terms \u2014 "
    "an emic summary of what practitioners say it is; (2) what scholarship says about its texts' dating, authorship, and lineage claims \u2014 "
    "an etic account; (3) what the tradition *did* with its claimed antiquity or authority \u2014 the lineage problem applied. Conclude with "
    "one sentence stating the course's framing contract as it applies to your dossier. This is the template for how every module's material "
    "should be handled."
),
'honesty': (
    "This module makes no supernatural claims and asks for no belief. It teaches a *method*: traditions described as the traditions describe "
    "themselves, scholarship reported where it is settled, and the two kept visibly distinct. The quizzes test knowledge *of* the traditions \u2014 "
    "what practitioners claim, what scholars have established, and the difference \u2014 never your personal spiritual attainment. If a later "
    "module's material ever reads as endorsement of the supernatural, return here: the contract is descriptive and scholarly throughout."
),
'cards_add': [
    ("Pseudepigraphy \u2014 definition and one course example?",
     "Attributing a text to someone other than its author; e.g., the Zohar's attribution to Shimon bar Yochai (2nd c.), while scholarship places it with Moses de Le\u00f3n in 13th-century Spain."),
    ("The three critical-reading moves?",
     "Source criticism (who wrote this, when, from what sources, for whom?); claim sorting (historical vs. symbolic vs. experiential, each by its own standards); charity (the strongest version first)."),
],
'quiz_add': [
    ("Pseudepigraphy is best illustrated in this course by:",
     ["The Zohar's attribution to Shimon bar Yochai, while scholarship places it with Moses de Le\u00f3n",
      "Dee writing his own diaries",
      "Court de G\u00e9belin painting a tarot deck",
      "The 1614 printing of the Fama Fraternitatis"],
     0,
     "Pseudepigraphy = false attribution; the Zohar case is this course's standard example, from the Kabbalah module's Concepts notes."),
    ("'What does tikkun mean in Lurianic teaching?' is an emic question because it:",
     ["Asks what scholars think of Luria",
      "Asks what the concept means inside the tradition's own categories",
      "Asks for the date of the Zohar",
      "Asks whether tikkun is scientifically real"],
     1,
     "Emic = inside the tradition's own categories; etic = the scholar's outside view. See the Concepts notes on emic vs. etic."),
    ("The 'Casaubon pattern' refers to:",
     ["Proving every old text is a fraud",
      "A claimed ancient origin meeting philological redating \u2014 and then asking what the tradition did with the claim",
      "Translating Greek into Latin",
      "Burning grimoires"],
     1,
     "Neither the claim nor the debunking is the whole story: study what the tradition built on its claimed antiquity."),
    ("Which of these is a primary source for the study of Renaissance angel magic?",
     ["A modern commentary on Dee",
      "Dee's Mysteriorum Libri \u2014 his contemporary diaries of the workings",
      "A 20th-century novel about Kelley",
      "This module's honesty note"],
     1,
     "Primary = from within the period under study; Dee's diaries are the Enochian module's core primary source."),
    ("The charity principle in critical reading means:",
     ["Believing the tradition's claims",
      "Addressing the strongest version of a claim before evaluating it",
      "Ignoring weak evidence",
      "Preferring debunking"],
     1,
     "Charity = strongest version first; it is one of the three critical-reading moves in the Concepts notes."),
    ("A claim that 'the Corpus Hermeticum was written in Moses\u2019 era' is best sorted as:",
     ["A symbolic claim",
      "An experiential claim",
      "A historical claim \u2014 judged by philology and dating, which placed it in the 2nd\u20133rd centuries CE",
      "Not sortable"],
     2,
     "Dating claims are historical claims; Casaubon's 1614 philology is the model for how they are judged."),
],
},

'm22-kabbalah': {
'summary': (
    "Welcome to Module 2 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and today "
    "we enter the central symbolic system of Jewish esotericism: Kabbalah. You'll learn to name and place the ten sefirot on the "
    "Tree of Life, meet the Zohar \u2014 the tradition's central text, wrapped in one of history's great authorship puzzles \u2014 and "
    "walk through Isaac Luria's cosmic drama of contraction, shattering, and repair. Everything here is presented as the tradition "
    "presents itself, with the scholarly record \u2014 dates, authorship, the difference between classical Kabbalah and its modern "
    "popularizations \u2014 kept honestly alongside. Master the Tree and you hold the filing system the rest of Western occultism borrowed."
),
'glossary': [
    GL % ('Sefirot', 'the ten divine emanations mapped on the Tree of Life: Keter, Chokhmah, Binah, Chesed, Gevurah, Tiferet, Netzach, Hod, Yesod, Malkhut.'),
    GL % ('Tree of Life', 'the diagram of ten sefirot in three pillars, joined by twenty-two paths associated with the Hebrew letters \u2014 simultaneously cosmology, psychology, and a map of the divine in the tradition\u2019s terms.'),
    GL % ('Zohar', "'Book of Splendor' \u2014 the central text of classical Kabbalah, appearing in 13th-century Spain through Moses de Le\u00f3n, attributed by the tradition to Shimon bar Yochai (2nd c.)."),
    GL % ('Tzimtzum', 'divine contraction \u2014 in Lurianic teaching, God\u2019s self-limitation that makes space for creation.'),
    GL % ('Shevirat ha-kelim', "'the shattering of the vessels' \u2014 the Lurianic catastrophe scattering holy sparks through creation."),
    GL % ('Tikkun', "'restoration' \u2014 the gathering of the scattered sparks through human ethical and ritual action, in Lurianic teaching."),
],
'proc_intro': (
    "The Tree of Life is a working instrument, not just a picture. Run this five-step mapping exercise with any ethical or psychological "
    "situation \u2014 your own or a case from history \u2014 to learn the Tree's internal logic from the inside, emically."
),
'steps': [
    "**State the situation in one sentence.** Pick something with tension: a decision, a conflict, a creative block. Write it down plainly.",
    "**Place the forces on the pillars.** Which elements belong to the right pillar of mercy (Chokhmah, Chesed, Netzach \u2014 expansion, kindness, endurance) and which to the left pillar of judgment (Binah, Gevurah, Hod \u2014 boundary, strength, form)? Assign at least one element to each.",
    "**Find the middle.** What would Tiferet (beauty/balance) look like here \u2014 the harmonizing center between Chesed and Gevurah? Write the balanced resolution in the tradition's terms.",
    "**Ground it.** Trace the resolution downward through Yesod (foundation) to Malkhut (kingship) \u2014 what concrete action in the world embodies it?",
    "**Step back and label your reading.** You just worked emically \u2014 inside Kabbalah's own categories. Now add one etic sentence: what kind of human situation does this exercise actually address, in scholarly terms?",
],
'project': (
    "Build a labeled diagram of the Tree of Life: the ten sefirot in their three pillars (right: Chokhmah, Chesed, Netzach; left: Binah, "
    "Gevurah, Hod; middle: Keter, Tiferet, Yesod, Malkhut), with the twenty-two paths noted as associated with the Hebrew letters. "
    "Accompany it with a 400-word commentary in two labeled parts: (1) an emic reading \u2014 what the Tree means within the tradition, "
    "including one Lurianic concept (tzimtzum, shevirah, or tikkun) placed on the diagram; (2) an etic note \u2014 the difference between "
    "classical Kabbalah (elite, textually demanding, historically restricted) and modern popularizations that borrow the diagram without "
    "its textual matrix. Cite the Zohar's dating and Luria's dates (1534\u20131572, Safed) from this module's Concepts notes."
),
'honesty': (
    "Everything in this module is presented as the Kabbalistic tradition presents it \u2014 history, symbolism, and practice as claimed by "
    "its practitioners \u2014 never as verified science. The tradition's own claims (divine emanation, the cosmic drama of the sparks) are "
    "reported emically; the scholarly record (the Zohar's 13th-century composition, the allegorical-vs.-historical reading of lineage claims) "
    "is reported etically, and the two are never blurred. Classical Kabbalah was a demanding textual discipline within Judaism; this course "
    "studies it, it does not initiate into it."
),
'cards_add': [
    ("The three pillars and the sefirot on each?",
     "Right (mercy): Chokhmah, Chesed, Netzach. Left (judgment): Binah, Gevurah, Hod. Middle (balance): Keter, Tiferet, Yesod, Malkhut."),
],
'quiz_add': [
    ("In which city did Isaac Luria teach?",
     ["Cordoba", "Safed", "Prague", "Cairo"],
     1,
     "Luria (1534\u20131572) taught in Safed; his disciples recorded the tzimtzum\u2013shevirah\u2013tikkun cosmology."),
    ("The Zohar is written largely in which language?",
     ["Biblical Hebrew", "Aramaic", "Greek", "Latin"],
     1,
     "The Zohar's Aramaic \u2014 a mystical Torah commentary \u2014 is part of why its 2nd-century attribution does not hold up."),
    ("Netzach sits on which pillar of the Tree?",
     ["The left pillar of judgment", "The middle pillar of balance", "The right pillar of mercy", "Outside the pillars"],
     2,
     "Right pillar: Chokhmah, Chesed, Netzach \u2014 expansion and endurance; see the Concepts notes."),
    ("Which sefirah is called 'kingship'?",
     ["Keter", "Yesod", "Malkhut", "Hod"],
     2,
     "Malkhut (kingship) is the lowest sefirah of the middle pillar \u2014 the divine as it touches the world."),
    ("Luria's teachings reached later Kabbalists through:",
     ["His own published books", "His disciples' records", "The Zohar directly", "19th-century occultists"],
     1,
     "Luria wrote little himself; the cosmic drama survives in his disciples' writings \u2014 a standard transmission pattern."),
    ("A 'diagram-only' borrowing of Kabbalah \u2014 the Tree without its textual and communal matrix \u2014 characterizes:",
     ["Classical Kabbalah", "The Zohar's original audience", "Modern popularizations", "Lurianic Safed"],
     2,
     "Classical Kabbalah was an elite textual discipline; popularizations often keep the diagram and discard the matrix."),
],
},

'm22-hermeticism': {
'summary': (
    "Welcome to Module 3 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we are meeting "
    "Hermes Trismegistus \u2014 the 'thrice-greatest,' the fusion of Greek Hermes and Egyptian Thoth \u2014 and the strange, beautiful body of "
    "Greek dialogues attributed to him. You'll learn what the Corpus Hermeticum actually contains, what Isaac Casaubon's 1614 philology did "
    "to its claimed antiquity, where the famous seven Hermetic principles really come from (spoiler: a 1908 book, not ancient Egypt), and how "
    "Marsilio Ficino's translation made Hermes a founding father of Renaissance thought. This is the Casaubon pattern in full color \u2014 the "
    "claim, the dating, and then the interesting part: what the Renaissance *did* with Hermes once it had him."
),
'glossary': [
    GL % ('Hermes Trismegistus', "'thrice-greatest Hermes' \u2014 the syncretic Graeco-Egyptian figure, fusing Hermes and Thoth, to whom the Hermetic writings are attributed."),
    GL % ('Corpus Hermeticum', 'the collection of Greek Hermetic dialogues (2nd\u20133rd c. CE, Hellenistic Egypt) \u2014 philosophical-religious conversations, not spellbooks.'),
    GL % ('Poimandres', 'the opening dialogue of the Corpus: a visionary account of creation and the soul\u2019s ascent revealed to Hermes.'),
    GL % ('Emerald Tablet', 'a short Hermetic text of uncertain date containing the formula \u201cas above, so below\u201d \u2014 the Principle of Correspondence in its classic wording.'),
    GL % ('Prisca theologia', "'ancient theology' \u2014 the Renaissance idea, carried by Ficino\u2019s translations, that Hermes and Plato transmitted a primeval divine wisdom."),
    GL % ('The Kybalion', 'the 1908 book, published anonymously as \u201cThree Initiates,\u201d that popularized the seven Hermetic principles in their modern formulation.'),
],
'proc_intro': (
    "The seven principles are the modern tradition's formulation \u2014 not the ancient corpus's. This six-step tracing exercise teaches you "
    "to separate the 1908 layer from the Hellenistic layer, which is exactly the dating discipline the whole course runs on."
),
'steps': [
    "**List the seven principles from the Concepts notes.** Mentalism, Correspondence, Vibration, Polarity, Rhythm, Cause and Effect, Gender \u2014 write them in your own words, one line each.",
    "**For each principle, ask: where would I look for its ancient analogue?** Correspondence \u2192 the Emerald Tablet's 'as above, so below'; the rest \u2192 the Corpus dialogues and the tradition's own explanations.",
    "**Note what is missing.** The ancient texts do not present a numbered sevenfold list \u2014 that packaging is the Kybalion's. Write down which principles have a clear ancient analogue and which do not.",
    "**Check the dating chain.** Corpus: 2nd\u20133rd c. CE (Casaubon, 1614). Ficino's Latin translation: 1463\u20131471 (commissioned by Cosimo de' Medici). The Kybalion: 1908. Place each fact on a timeline.",
    "**Ask what each layer did.** What did the Renaissance do with Hermes (prisca theologia)? What did 1908 do with him (the seven principles)? One sentence each.",
    "**Label the layers.** In your notes, tag every Hermetic claim you meet from here on as Hellenistic, Renaissance, or modern \u2014 the three strata of this module.",
],
'project': (
    "Write a 600-word comparative note titled 'Three Hermeses': the Hellenistic Hermes of the Corpus Hermeticum (what the 2nd\u20133rd-century "
    "dialogues actually contain, per the Concepts notes), the Renaissance Hermes of Ficino's translation (1463\u20131471, prisca theologia, "
    "read alongside Plato), and the modern Hermes of the Kybalion's seven principles (1908). For each, state (1) what the texts say, "
    "(2) what scholars say about their date, and (3) what that era's readers *did* with Hermes. Conclude by applying the module's honesty "
    "discipline: which of the three is oldest, and why does that matter less than what each did with him?"
),
'honesty': (
    "The seven principles are presented as the modern Hermetic tradition presents them \u2014 a 1908 formulation, not ancient Egyptian wisdom. "
    "The Corpus Hermeticum is presented as scholarship dates it: Hellenistic Egypt, 2nd\u20133rd centuries CE, whatever Renaissance readers "
    "believed. 'As above, so below' is reported as the tradition's hermeneutic principle (read one level through another), not as an empirical "
    "prediction. No part of this module asserts Hermetic metaphysics as verified fact."
),
'cards_add': [
    ("The Poimandres?",
     "The opening dialogue of the Corpus Hermeticum \u2014 a visionary revelation to Hermes of creation and the soul's ascent."),
],
'quiz_add': [
    ("The Kybalion was published:",
     ["In Hellenistic Egypt", "In 1908, anonymously as 'Three Initiates'", "By Marsilio Ficino", "In the Emerald Tablet"],
     1,
     "1908 \u2014 the seven-principles list is a modern formulation, per the Concepts notes."),
    ("Ficino's translation of the Corpus was commissioned by:",
     ["The Pope", "Cosimo de' Medici", "John Dee", "Isaac Casaubon"],
     1,
     "1463\u20131471: Cosimo de' Medici's commission made Hermes a Renaissance authority \u2014 the prisca theologia move."),
    ("The Principle of Mentalism states, in the tradition's terms:",
     ["'Nothing rests'", "'All is mind'", "'As above, so below'", "'Every cause has its effect'"],
     1,
     "Mentalism = all is mind; Vibration = nothing rests; Correspondence = as above, so below; Cause and Effect is its own principle."),
    ("Newton's extensive alchemical manuscripts show, for this module's argument:",
     ["That Newton was a Hermetic priest", "That the boundary between early science and alchemy was porous", "That gravity is Hermetic", "Nothing relevant"],
     1,
     "The Renaissance-revival note: Hermetic ideas flowed into alchemy and early science \u2014 the boundary was porous."),
    ("The Emerald Tablet's date, on the honest scholarly accounting used here:",
     ["Firmly 3000 BCE", "Uncertain", "1463", "1908"],
     1,
     "The Concepts notes give the Tablet as 'a short Hermetic text of uncertain date' \u2014 honesty means saying so."),
    ("Prisca theologia held that:",
     ["Hermes was a fraud", "Hermes and Plato transmitted a primeval divine wisdom", "Only the Kybalion matters", "Alchemy predates writing"],
     1,
     "Ficino's framing: Hermes read alongside Plato as ancient theology \u2014 what the Renaissance *did* with Hermes."),
],
},

'm22-alchemy': {
'summary': (
    "Welcome to Module 4 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're following "
    "the Great Work from Hellenistic Egypt to Paracelsus: the quest for the philosopher's stone, the color-stages of nigredo, albedo, "
    "citrinitas, and rubedo, and the master formula *solve et coagula* \u2014 dissolve and coagulate. You'll learn to read alchemy's symbolic "
    "language emically, as practitioners meant it \u2014 matter and spirit worked simultaneously \u2014 and to place it etically in history: the "
    "laboratory techniques chemistry inherited, and the moment quantitative science displaced transmutation theory. Alchemy is where this "
    "course's two readings meet most vividly, so bring both."
),
'glossary': [
    GL % ('Magnum Opus', "'the Great Work' \u2014 the alchemical program culminating in the philosopher's stone, in the tradition's terms."),
    GL % ('Philosopher\u2019s stone', 'the sought agent of transmutation of base metals into gold \u2014 and, in parallel, of bodily perfection via the elixir of life.'),
    GL % ('Prima materia', "'first matter' \u2014 the undifferentiated base to which the substance is reduced in the solve phase, before reconstitution."),
    GL % ('Nigredo / albedo / citrinitas / rubedo', 'the color-stages of the Work: blackening (putrefaction), whitening (purification), yellowing, reddening (completion).'),
    GL % ('Solve et coagula', "'dissolve and coagulate' \u2014 the master formula: break down to prima materia, reconstitute perfected; applied to matter and practitioner alike."),
    GL % ('Tria prima', "Paracelsus's three principles \u2014 sulfur, mercury, salt \u2014 the chemical triad of his iatrochemistry (medical chemistry)."),
],
'proc_intro': (
    "Alchemical emblems are meant to be *read*, not glanced at. Use this five-move procedure on the 'chemical wedding' image described in "
    "this module's quiz notes \u2014 a king and queen joining \u2014 or on any alchemical emblem you find in the source links."
),
'steps': [
    "**Describe literally.** What is depicted, with no interpretation? Two crowned figures joining hands, their attributes, the setting. Write only what you see.",
    "**Find the color-stage.** Which phase of nigredo \u2012 albedo \u2012 citrinitas \u2012 rubedo does the scene suggest? A wedding-union points toward conjunction and the reddening completion \u2014 note your reasoning, not just the label.",
    "**Apply solve et coagula.** What has been dissolved here (the separate king and queen, sulfur and mercury as opposites) and what is being reconstituted (their union)?",
    "**Read the two levels.** State the material reading (the joining of chemical opposites in the Work) and the spiritual reading (dissolution of the practitioner's divided self, reconstitution whole) side by side \u2014 practitioners held both at once.",
    "**Place it historically.** Which station of the arc does this emblem belong to \u2014 Hellenistic, Islamic, medieval European, or Renaissance? What does that placement tell you about who made it and why?",
],
'project': (
    "Produce a 500-word emblem reading of the 'chemical wedding' (king and queen joining) plus a one-paragraph historical placement. The "
    "reading follows the five-move procedure in this module's Hands-on procedure section: literal description, color-stage identification, "
    "solve-et-coagula analysis, the material and spiritual levels held together, and a labeled emic/etic split (what the tradition claims "
    "the image means vs. what scholarship says about its historical context). The historical paragraph places the emblem on the module's arc "
    "\u2014 Zosimos (~300 CE), Jabir's corpus (8th\u20139th c.), the 12th-century translations, Paracelsus (1493\u20131541) \u2014 and names "
    "what chemistry inherited from the laboratory side: distillation, sublimation, crystallization, apparatus."
),
'honesty': (
    "Transmutation of base metals into gold is presented as the alchemists' *aim*, never as an achieved or achievable fact \u2014 chemistry's "
    "quantitative program (Boyle, Lavoisier) displaced the theory in the 17th\u201318th centuries, and this module reports that displacement "
    "plainly. The spiritual reading of the stages (nigredo as ego-dissolution and the like) is reported as the tradition's own symbolic "
    "interpretation, not as psychology. What alchemy genuinely bequeathed \u2014 laboratory technique and the experimental habit \u2014 is stated as history."
),
'cards_add': [
    ("The tria prima?",
     "Sulfur, mercury, salt \u2014 Paracelsus's three principles, the chemical triad of his iatrochemistry."),
],
'quiz_add': [
    ("Paracelsus (1493\u20131541) is credited in this module with:",
     ["Discovering oxygen", "The tria prima and the founding of iatrochemistry", "Translating the Corpus Hermeticum", "The 1614 manifestos"],
     1,
     "Sulfur, mercury, salt \u2014 and alchemy turned toward medicine. See the Concepts notes."),
    ("Iatrochemistry means:",
     ["Star-medicine", "Medical chemistry \u2014 Paracelsus's application of alchemy to healing", "The study of poisons only", "Astrological medicine exclusively"],
     1,
     "Paracelsus founded iatrochemistry: the alchemical tradition redirected to medicine."),
    ("Zosimos of Panopolis (~300 CE) belongs to which station of alchemy's arc?",
     ["Renaissance Paracelsianism", "Hellenistic Egypt \u2014 the beginning of the arc", "Medieval Europe", "The Islamic golden age"],
     1,
     "The arc opens in Hellenistic Egypt with Zosimos, then the Islamic world (Jabir), medieval Europe, the Renaissance."),
    ("The 'elixir of life' in the Great Work is:",
     ["A poison", "The parallel of the stone for the body \u2014 the agent of bodily perfection", "A stage before nigredo", "A mistranslation"],
     1,
     "Stone: metals perfected. Elixir: the body perfected \u2014 the two aims run in parallel."),
    ("Citrinitas is the stage of:",
     ["Blackening", "Whitening", "Yellowing", "Reddening"],
     2,
     "Nigredo (blackening), albedo (whitening), citrinitas (yellowing), rubedo (reddening) \u2014 the color sequence."),
    ("Qualitative transmutation theory was displaced in the 17th\u201318th centuries by:",
     ["The Rosicrucian manifestos", "Chemistry's quantitative program \u2014 Boyle, Lavoisier", "The Royal Society's ban", "Newton's alchemy"],
     1,
     "The etic historical fact: quantitative chemistry replaced transmutation theory; the laboratory techniques survived."),
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
    print('part1 ok: modules 1-4 retrofitted')

if __name__ == '__main__':
    main()
