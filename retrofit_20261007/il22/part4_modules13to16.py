#!/usr/bin/env python3
"""Retrofit IL-22 modules 13-16 (eastern, divination, symbolism, modern revival)."""
import json, os

PATH = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json'
GL = '- **%s** \u2014 %s'

UPDATES = {

'm22-eastern-esoteric': {
'summary': (
    "Welcome to Module 13 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we are leaving "
    "the Western currents behind to meet the Eastern traditions Western occultism borrowed from \u2014 in their own contexts, on their own "
    "terms. You'll learn what tantra actually is (a rigorous initiatory discipline from the 6th century CE, not the popular Western "
    "reduction), how Daoist inner alchemy (*neidan*) turned the laboratory inward \u2014 jing refined to qi, qi to shen, the body as crucible "
    "\u2014 and how Vajrayana Buddhism structures its esoteric transmission through deity yoga, mantra, mandala, and required guru empowerment. "
    "Then the hard part: orientalism. Edward Said named the pattern in 1978 \u2014 the East constructed as mystic Other \u2014 and Western "
    "occultism's borrowings (chakras in Theosophy, 'tantra' in the New Age) are textbook cases. Study the traditions in their contexts first; "
    "borrow, if at all, with attribution and understanding."
),
'glossary': [
    GL % ('Tantra', 'Hindu and Buddhist esoteric traditions (from ~6th c. CE): ritual, mantra, mandala, and the subtle body \u2014 a rigorous initiatory discipline, in the traditions\u2019 own terms.'),
    GL % ('Chakras / nadis', 'the subtle body\u2019s centers and channels through which energy moves (*kundalini* in some systems) \u2014 initiatory anatomy, not lifestyle metaphor.'),
    GL % ('Neidan', "'inner alchemy' \u2014 Daoist internal alchemy (systematized from the Tang\u2013Song eras): refining jing \u2192 qi \u2192 shen through breath, meditation, and visualization."),
    GL % ('Microcosmic orbit', 'the neidan circulation of qi through the body\u2019s channels in meditation \u2014 the body worked as the crucible.'),
    GL % ('Vajrayana', "'diamond vehicle' \u2014 Tibetan Buddhism\u2019s esoteric stratum: deity yoga, mantra, mandala; guru empowerment/initiation required, samaya vows governing transmission."),
    GL % ('Orientalism', "Edward Said\u2019s term (1978) for the Western construction of the East as mystic Other \u2014 the distortion pattern in occultism\u2019s Eastern borrowings."),
],
'proc_intro': (
    "Borrowing without understanding is the failure mode this module exists to prevent. Run this six-step attribution audit on any Western "
    "use of an Eastern esoteric concept \u2014 a book, a class, a product \u2014 using the module's three traditions as your reference."
),
'steps': [
    "**Name the borrowed concept precisely.** 'Chakras,' 'tantra,' 'qi' \u2014 write the exact term as the borrower uses it.",
    "**Recover the home context.** What does the term mean in its tradition \u2014 tantra as initiatory discipline (not sexuality), neidan as jing\u2192qi\u2192shen refinement, Vajrayana as guru-transmitted deity yoga? Write the home meaning from the Concepts notes.",
    "**List what was stripped.** Initiatory structure? Ethical context? Required transmission (empowerment, samaya vows)? Textual lineage? Check off each element the borrowing keeps or drops.",
    "**Check the direction of travel.** Theosophy's chakras, New Age 'tantra,' energy-medicine qi \u2014 who carried the concept West, when, and through what intermediaries? One timeline.",
    "**Apply Said's test.** Does the borrowing present the East as mystic Other \u2014 timeless, exotic, available for extraction? Quote the borrower's framing and judge it.",
    "**Write the honest verdict.** Either: 'attributed, contextualized borrowing' (home meaning preserved, transmission acknowledged) or 'orientalist extraction' (stripped, decontextualized) \u2014 with the evidence for each. Then state the anti-orientalist minimum: study contexts first; attribute; understand before borrowing.",
],
'project': (
    "Write a 700-word borrowing audit of one Western use of an Eastern esoteric concept \u2014 your choice (e.g., chakras in a Theosophical text, "
    "'tantra' in a New Age book, qi in an energy-medicine manual). Part 1: the home tradition \u2014 the concept's meaning, initiatory structure, "
    "and ethical/transmission context from this module's Concepts notes (tantra's ritual-mandala-mantra complex, neidan's three refinements and "
    "microcosmic orbit, or Vajrayana's deity yoga and required empowerment). Part 2: the borrowing \u2014 what was kept, what was stripped, who "
    "carried it West and when. Part 3: the verdict \u2014 attributed borrowing or orientalist extraction, judged by the audit procedure, with "
    "Said's *Orientalism* (1978) applied to the borrower's framing. Close with one paragraph on what respectful engagement would require."
),
'honesty': (
    "Eastern traditions are presented in their own contexts and terms \u2014 tantra as initiatory discipline, neidan as internal refinement, "
    "Vajrayana as guru-transmitted practice \u2014 never as exotic decoration. The popular Western reductions (tantra-as-sexuality and the like) "
    "are named as distortions, not debated as interpretations. Vajrayana's transmission restrictions are reported as the tradition's own requirement, "
    "which this course respects by teaching *about* the systems rather than initiating into them. Nothing here authorizes decontextualized borrowing."
),
'cards_add': [
    ("The *Cantong qi* (2nd c. CE)?",
     "A Daoist alchemical classic of outer alchemy \u2014 the textual root later internalized by neidan manuals."),
],
'quiz_add': [
    ("In neidan, *shen* is:",
     ["Essence \u2014 the base to refine", "Vital energy", "Spirit \u2014 the final refinement of qi", "A breathing technique"],
     2,
     "Jing (essence) \u2192 qi (vital energy) \u2192 shen (spirit): the three refinements, body as crucible."),
    ("The *nadis* are:",
     ["Chakra centers", "The subtle body's channels through which energy moves", "Daoist scriptures", "Vajrayana vows"],
     1,
     "Chakras and channels (nadis): the subtle-body anatomy of the tantric systems."),
    ("Samaya, in Vajrayana, refers to:",
     ["A meditation posture", "The vows governing esoteric transmission", "A mandala pattern", "A root race"],
     1,
     "Restricted texts and samaya vows govern transmission \u2014 the tradition's own requirement."),
    ("The classical tantric claim for its methods is:",
     ["Wealth and power", "Accelerated liberation through ritual identification with the deity", "Physical immortality", "Political influence"],
     1,
     "The tradition's own claim \u2014 reported emically, not endorsed: liberation, sped by ritual identification."),
    ("Tantra's textual traditions begin around:",
     ["The 6th century CE", "The 2nd century BCE", "The 19th century", "1945"],
     0,
     "From ~6th c. CE \u2014 Hindu and Buddhist esoteric traditions with ritual, mantra, and mandala."),
    ("A borrowing that keeps a concept's home meaning and acknowledges transmission is, by this module's standard:",
     ["Still orientalist", "An attributed, contextualized borrowing \u2014 the honest kind", "Forbidden", "The same as extraction"],
     1,
     "The anti-orientalist minimum: study contexts first, attribute, understand before borrowing."),
],
},

'm22-divination': {
'summary': (
    "Welcome to Module 14 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're studying "
    "three complete divinatory grammars side by side: the *Yijing* (I Ching) with its 64 hexagrams of broken and solid lines, the runes \u2014 "
    "the Elder Futhark's 24 characters, an alphabet before it was ever an oracle \u2014 and geomancy, the most algorithmic of the divinatory "
    "arts, with its sixteen figures generated by deterministic reduction. You'll learn how each system generates its signs, structures them, "
    "and interprets them \u2014 and you'll learn the shared logic underneath all three: random generation plus fixed interpretive grammar "
    "equals a mirror for reflection. Presented throughout as symbolic instruments, never as prediction machines \u2014 and with the runes' "
    "modern history told honestly, blank rune and all."
),
'glossary': [
    GL % ('Hexagram', 'a six-line figure of broken (yin) or solid (yang) lines \u2014 64 in the Yijing, each with judgment, image, and line texts.'),
    GL % ('Changing lines', 'old yin/yang lines that transform into their opposite \u2014 generating a second hexagram that shows the situation\u2019s movement.'),
    GL % ('Ten Wings', 'the canonical commentaries on the Yijing, traditionally attributed to Confucius \u2014 the wisdom-text layer of the oracle.'),
    GL % ('Elder Futhark', 'the 24-rune Germanic alphabet (~2nd\u20138th c. CE) \u2014 memorial and inscriptional first; modern runic divination is largely a 20th-century construction.'),
    GL % ('Blank rune', 'the extra rune popularized by Ralph Blum\u2019s 1982 *Book of Runes* \u2014 no historical attestation; the honest account names it as modern.'),
    GL % ('Geomantic figures', 'sixteen figures (Via, Carcer, Amissio...) generated by reducing 16 rows of marks \u2014 Mothers, Daughters, Nieces, Witnesses, Judge \u2014 each with planetary and zodiacal attributions.'),
],
'proc_intro': (
    "Geomancy is the most procedural of the divinatory arts \u2014 which makes it the perfect hands-on exercise. Generate a complete geomantic "
    "chart by hand, exactly as the medieval procedure runs. All you need is paper and a pen."
),
'steps': [
    "**Make the sixteen rows.** Without counting, make sixteen rows of random dots or strokes \u2014 four rows per 'Mother.' Speed matters: don't count as you go.",
    "**Reduce by pairs.** For each row, pair off the marks; an even remainder gives two dots, an odd remainder one dot. Four reduced rows make one figure \u2014 a Mother. Repeat for all four Mothers.",
    "**Derive the Daughters.** Combine the Mothers' lines by the fixed algorithm (first lines of the four Mothers make the First Daughter, and so on) to get four Daughters.",
    "**Derive the Nieces, Witnesses, and Judge.** Combine Daughters into Nieces, Nieces into the two Witnesses, and the Witnesses into the single Judge \u2014 each step by the same fixed combination rule.",
    "**Read the figures.** Identify each figure among the sixteen (Via, Carcer, Amissio, and the rest) and note its planetary and zodiacal attributions from a standard table.",
    "**Interpret \u2014 then label.** Write the reflective reading (what does the Judge suggest about your question?), then the honesty sentence: random generation + fixed grammar = a mirror for reflection; the chart predicted nothing, and the value was structured self-examination.",
],
'project': (
    "Produce a comparative grammar chart of the three systems plus a 400-word analysis. The chart has four columns \u2014 I Ching, runes, "
    "geomancy \u2014 and rows for: sign inventory (64 hexagrams / 24+1 runes / 16 figures), generation method (yarrow stalks or coins with "
    "changing lines / cast and read positionally / 16-row reduction algorithm), structural unit (binary lines / discrete signs / four-line "
    "figures), interpretive layer (judgments, images, Ten Wings / positional meanings / planetary-zodiacal attributions), and historical "
    "honesty note (three millennia of continuous use / historical runology \u2260 modern divination, blank rune modern / medieval-Renaissance "
    "peak, most algorithmic). The analysis states the shared divinatory logic in your own words and defends the course's framing: symbolic "
    "instruments for reflection, not prediction machines \u2014 with one paragraph on where each system's modern form departs from its history."
),
'honesty': (
    "The I Ching's three millennia of continuous use is history; its power as an oracle is the tradition's claim, not the course's. Runic "
    "divination as modern books teach it is largely a 20th-century construction \u2014 the Elder Futhark was an alphabet, the blank rune is "
    "Blum's 1982 invention \u2014 and this module refuses to retroject the modern system onto Vikings. Geomancy's algorithm is genuinely "
    "medieval; its attributions are the medieval system's, not nature's. All three are presented as mirrors for reflection, never as "
    "prediction engines."
),
'cards_add': [
    ("Yarrow-stalk vs. coin method?",
     "Traditional yarrow-stalk manipulation, later simplified to three coins \u2014 both produce a hexagram plus changing lines."),
],
'quiz_add': [
    ("Each hexagram's judgment, image, and line texts are supplemented by:",
     ["The Ten Wings \u2014 commentaries traditionally attributed to Confucius", "The 16 geomantic figures", "The 22 paths", "The Emerald Tablet"],
     0,
     "The Ten Wings are the canonical commentary layer \u2014 the Yijing as wisdom text, not just oracle."),
    ("Old yin and old yang lines are 'changing' because they:",
     ["Are decorative", "Transform into their opposite, generating a second hexagram", "Cancel the reading", "Indicate a new question"],
     1,
     "Changing lines show the situation's movement \u2014 the I Ching reads dynamically, per the Concepts notes."),
    ("The Elder Futhark's 24 runes date approximately to:",
     ["The 15th century", "The 2nd\u20138th centuries CE", "1781", "1909"],
     1,
     "~2nd\u20138th c. CE: a Germanic alphabet for memorial and inscriptional use \u2014 not originally divinatory."),
    ("In geomancy, the Judge is:",
     ["The first figure cast", "The single final figure derived from the two Witnesses", "A planetary attribution", "The querent"],
     1,
     "Mothers \u2192 Daughters \u2192 Nieces \u2192 Witnesses \u2192 Judge: the deterministic derivation chain."),
    ("*Enuma Anu Enlil* is mentioned in this course as:",
     ["A geomantic figure", "Babylonian omen literature \u2014 the deep-history root of astrology's sign-reading", "A runic poem", "A Theosophical text"],
     1,
     "The astrology module's deep history: 2nd-millennium BCE celestial omens for king and state."),
    ("The shared divinatory logic across all three systems is:",
     ["Spirit contact", "Random generation + fixed interpretive grammar = a mirror for reflection", "Astronomical measurement", "Psychic power"],
     1,
     "The Concepts notes' formula \u2014 symbolic instruments, not prediction machines."),
],
},

'm22-symbolism': {
'summary': (
    "Welcome to Module 15 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this module, and we're studying "
    "the medium every tradition in this course thinks in: symbols. You'll learn the difference between a sign (points to one thing) and a "
    "symbol (participates in what it represents, inexhaustibly) \u2014 and why reducing a symbol to a single 'meaning' kills it. We'll walk "
    "the recurring images \u2014 serpent, tree, circle, cross \u2014 across traditions from Eden to the caduceus to kundalini, and then take up "
    "sacred geometry: the golden ratio \u03c6 (what it is, where it actually appears, and where the popular books lie about it), the vesica "
    "piscis, and the five Platonic solids from Plato's *Timaeus* to Kepler's gloriously wrong *Mysterium Cosmographicum* of 1596. The "
    "contemplative discipline is real; the hype is not \u2014 this module teaches you to keep them separate."
),
'glossary': [
    GL % ('Sign vs. symbol', 'a sign points to one thing (a stop sign); a symbol participates in its referent and carries inexhaustible meanings \u2014 the cross, the serpent, the tree.'),
    GL % ('Axis mundi', 'the world-axis joining underworld, earth, and heaven \u2014 the tree image (Yggdrasil, the Tree of Life, the Bodhi tree) in its cosmological role.'),
    GL % ('Ouroboros', 'the serpent eating its tail \u2014 cyclical renewal and wholeness, the unity of beginning and end in the traditions\u2019 reading.'),
    GL % ('Golden ratio (\u03c6)', '(1+\u221a5)/2 \u2248 1.618 \u2014 the self-similar rectangle ratio; genuinely in the pentagon and phyllotaxis, mythically in most claimed artworks.'),
    GL % ('Vesica piscis', 'the almond-shaped intersection of two overlapping equal circles \u2014 the generator of equilateral-triangle geometry.'),
    GL % ('Platonic solids', 'the five regular polyhedra (tetrahedron, cube, octahedron, dodecahedron, icosahedron) \u2014 proved complete by Euclid; cosmological speculation from the *Timaeus* to Kepler.'),
],
'proc_intro': (
    "Geometry as contemplative instrument is a genuine traditional practice \u2014 and it is done with a compass, not just read about. "
    "Construct the vesica piscis and its triangle by hand in six steps."
),
'steps': [
    "**Draw the first circle.** With a compass, draw a circle of any comfortable radius. Mark its center.",
    "**Draw the second.** Place the compass point on the first circle's circumference and draw a second circle of the *same* radius. The overlap is the vesica piscis \u2014 the almond shape at the center.",
    "**Find the triangle.** Mark the two points where the circles intersect, and the two centers. Connect them: the line between the centers and the lines to either intersection point form equilateral triangles.",
    "**Meditate the construction \u2014 the traditional use.** Spend five minutes contemplating the figure: two wholes overlapping to generate a third form. In the traditions' terms, this is geometry as contemplative instrument, not decoration.",
    "**Extend honestly.** The five Platonic solids (tetrahedron, cube, octahedron, dodecahedron, icosahedron \u2014 Euclid proved these are all) were used for cosmological speculation from Plato's *Timaeus* to Kepler's *Mysterium Cosmographicum* (1596), which nested them between planetary spheres. Note: Kepler's model was wrong \u2014 gloriously, instructively wrong.",
    "**Write the two-column ledger.** Column one: what you experienced doing the construction (the discipline is real). Column two: which \u03c6-claims about art and architecture you can actually verify (most are modern myth). Keep the columns separate \u2014 that separation *is* the module's lesson.",
],
'project': (
    "Produce a 'symbol dossier' on one recurring image \u2014 serpent, tree, circle, or cross \u2014 in 600 words with three labeled parts. "
    "Part 1: the image's core resonances from the Concepts notes (e.g., serpent: wisdom, renewal, danger \u2014 Eden, caduceus, kundalini; "
    "tree: axis mundi \u2014 Yggdrasil, Tree of Life, Bodhi tree). Part 2: two worked appearances in traditions from this course, each read "
    "emically (what the symbol means inside that tradition) with the sign-vs.-symbol distinction applied \u2014 show the meaning *exceeding* "
    "any single paraphrase. Part 3: the honesty ledger \u2014 one paragraph on a genuine contemplative use of the image, and one on a hyped or "
    "false claim about it that the module's discipline rejects. Conclude with your own one-sentence definition of how symbols differ from signs."
),
'honesty': (
    "The contemplative use of symbols and geometry is presented as a genuine traditional practice \u2014 the course respects the discipline. "
    "The *claims* made about \u03c6 \u2014 that it encodes the pyramids or governs all beauty \u2014 are reported as mostly modern myth, and "
    "debunking them is presented as not touching the practice. Kepler's 1596 nesting of the Platonic solids is admired and labeled wrong. "
    "Symbols are never reduced to single meanings here; the inexhaustibility is the point, and the course does not pretend otherwise."
),
'cards_add': [
    ("The caduceus and kundalini: what do they share, symbolically?",
     "The serpent image \u2014 wisdom, renewal (shedding skin), danger \u2014 working across Greek and Indian symbolic vocabularies."),
],
'quiz_add': [
    ("Reducing a symbol to a single 'meaning':",
     ["Is the correct method", "Kills it \u2014 symbols carry inexhaustible, participatory meaning", "Is what the traditions recommend", "Applies only to the cross"],
     1,
     "The Concepts notes: meditation *with* symbols transforms the meditator; single-meaning reduction ends that work."),
    ("The Bodhi tree is cited in this module as an instance of:",
     ["The serpent image", "The tree as axis mundi \u2014 joining underworld, earth, heaven", "The vesica piscis", "A Platonic solid"],
     1,
     "Yggdrasil, the Tree of Life, the Bodhi tree \u2014 the axis image across traditions."),
    ("Phyllotaxis is invoked in this module as:",
     ["A myth about pyramids", "A genuine appearance of \u03c6-type patterning in nature \u2014 unlike most art-architecture claims", "A tarot spread", "A Gnostic text"],
     1,
     "\u03c6 appears in the pentagon and phyllotaxis \u2014 honestly; far fewer artworks than popular books claim."),
    ("Euclid's contribution to the Platonic solids was:",
     ["Discovering them", "Proving these five are all there are", "Carving them", "Naming them after Plato"],
     1,
     "Known to the Greeks, proved complete by Euclid \u2014 the Concepts notes' formula."),
    ("Plato's *Timaeus* used the solids for:",
     ["Musical theory", "Cosmological speculation \u2014 continued by Kepler in 1596", "Tarot design", "Architectural plans"],
     1,
     "From the *Timaeus* to the *Mysterium Cosmographicum*: solids as cosmology \u2014 wrong, but generative."),
    ("The module's 'two-column ledger' separates:",
     ["East from West", "Genuine contemplative practice from hyped or false claims about it", "Ancient from modern", "Signs from symbols"],
     1,
     "The discipline is real, the hype is not \u2014 keep the columns separate."),
],
},

'm22-modern-revival': {
'summary': (
    "Welcome to Module 16 of The Deep Library \u2014 Esoteric & Secret Knowledge. I'm your instructor for this final module, and we're "
    "watching the 20th century detonate: Aleister Crowley receiving *The Book of the Law* in Cairo in 1904 and founding Thelema \u2014 'Do "
    "what thou wilt,' the True Will, through the A\u2234A\u2234 and the O.T.O.; Dion Fortune writing the clearest English Qabalah textbook "
    "ever made; Gerald Gardner founding Wicca in the 1940s\u201350s, claiming a surviving witch-cult that Ronald Hutton's scholarship "
    "relocates to the mid-20th century; and the New Age popularizing \u2014 and diluting \u2014 everything in this course while the academy "
    "simultaneously professionalized the field (Amsterdam chair, 1999; ESSWE). Then the closing discipline, the one the whole course has "
    "been training: source criticism, claim sorting, and charity \u2014 critical reading without contempt. Neither credulity nor "
    "debunking-as-sport. You now have the complete toolkit; this module hands you the license to use it."
),
'glossary': [
    GL % ('Thelema', "Crowley\u2019s system from *The Book of the Law* (Cairo, 1904): \u2018Do what thou wilt shall be the whole of the Law\u2019 \u2014 'will' as the True Will, one\u2019s authentic nature/purpose, not whim."),
    GL % ('True Will', 'the Thelemic technical term for one\u2019s authentic nature and purpose \u2014 the opposite of license or whim.'),
    GL % ('A\u2234A\u2234 / O.T.O.', 'Crowley\u2019s orders: the A\u2234A\u2234 and the Ordo Templi Orientis \u2014 the institutional carriers of Thelema.'),
    GL % ('Dion Fortune', '1890\u20131946 \u2014 *The Mystical Qabalah* (1935), the classic English Qabalah textbook; founder of the Society of the Inner Light.'),
    GL % ('Wicca', 'Gardner\u2019s 1940s\u201350s creation (from Crowley, Freemasonry, folklore \u2014 per Hutton) \u2014 claimed as witch-cult survival, now a genuine lived religion regardless of origins.'),
    GL % ('ESSWE', 'the European Society for the Study of Western Esotericism \u2014 with the 1999 Amsterdam chair, the marker of the field\u2019s academization.'),
],
'proc_intro': (
    "This is the capstone procedure: the full critical-reading workout on any esoteric text you will ever meet. Run it once now, on *The "
    "Book of the Law*'s reception story or on Gardner's witch-cult claim \u2014 it uses every tool from Module 1."
),
'steps': [
    "**Source criticism.** Who wrote this, when, from what sources, for whom? Crowley claimed *The Book of the Law* came via his wife Rose in Cairo, 1904; Gardner claimed initiation into a surviving witch-cult in the 1940s\u201350s. Write the provenance as stated.",
    "**Check the scholarship.** Hutton on Wicca: mid-20th-century creation from Crowley, Freemasonry, folklore. Crowley's biography: the field's most contested. Record what historians accept.",
    "**Sort the claims.** Historical (1904 Cairo dictation; 1940s initiations) vs. symbolic (True Will as doctrine) vs. experiential (practitioners' reported results) \u2014 each judged by its own standards.",
    "**Apply charity.** State the strongest version of each claim before evaluating: Thelema as a serious philosophy of will; Wicca as a genuine lived religion regardless of origins. The course affirms the religion's reality while reporting Hutton's findings.",
    "**Trace both tracks.** The New Age popularization (channeling, crystal healing, 'quantum' mysticism \u2014 dilution) *and* the academization (Amsterdam 1999, ESSWE \u2014 professionalization) happened in the same decades. Chart one example of each.",
    "**Render the closing verdict.** Neither credulity nor debunking-as-sport: the traditions get the same rigor as any human phenomenon, and no more credulity than any extraordinary claim gets. Write your verdict in the module's formula.",
],
'project': (
    "Write the course capstone: a 900-word critical dossier on one 20th-century figure or movement \u2014 Crowley/Thelema, Fortune, "
    "Gardner/Wicca, or the New Age. Four labeled parts: (1) the emic account \u2014 the teaching in its own terms (*The Book of the Law*, "
    "1904, True Will; *The Mystical Qabalah*, 1935; Gardner's witch-cult claim); (2) the etic record \u2014 dates, the contested biography, "
    "Hutton's findings on Wicca, with every claim sourced to this module's Concepts notes; (3) the double track \u2014 one paragraph on "
    "popularization/dilution and one on academization (Amsterdam chair 1999, ESSWE); (4) the verdict \u2014 source criticism, claim sorting, "
    "and charity applied in order, ending with the module's closing formula. This dossier is the comprehensive demonstration of the "
    "Module 1 method on Module 16 material."
),
'honesty': (
    "Crowley's reception claim is reported as his claim \u2014 'he claimed, via his wife Rose' \u2014 never as fact. Gardner's witch-cult "
    "survival is reported as his claim, with Hutton's contrary finding given fully; Wicca's reality as a lived religion is affirmed "
    "alongside, not instead of, the historical verdict. The New Age's dilutions are named plainly ('quantum' mysticism and the rest) while "
    "the academization is recorded as the parallel fact. The closing discipline \u2014 rigor without contempt, skepticism without sport \u2014 "
    "is the course's final and binding contract."
),
'cards_add': [
    ("The Society of the Inner Light?",
     "Dion Fortune's order \u2014 the institutional home of her Qabalistic teaching."),
],
'quiz_add': [
    ("*The Book of the Law* was received, in Crowley's account:",
     ["In London, 1888", "In Cairo, 1904, via his wife Rose", "In Cefal\u00f9, 1920", "In New York, 1875"],
     1,
     "'He claimed, via his wife Rose' \u2014 Cairo, 1904: the reception story, reported as his claim."),
    ("The O.T.O. is:",
     ["A tarot deck", "The Ordo Templi Orientis \u2014 with the A\u2234A\u2234, a carrier of Thelema", "A Theosophical lodge", "A Rosicrucian manifesto"],
     1,
     "The Concepts notes: the A\u2234A\u2234 and the O.T.O. carried Crowley's system."),
    ("Ronald Hutton's scholarship is invoked in this course for:",
     ["The Zohar's dating", "The finding that Gardnerian Wicca is a mid-20th-century creation", "The Enochian language", "The Corpus Hermeticum"],
     1,
     "Hutton: Wicca assembled in the 1940s\u201350s from Crowley, Freemasonry, folklore \u2014 origins as claimed debunked, religion affirmed."),
    ("*The Mystical Qabalah* (1935) is:",
     ["A Crowley ritual", "Dion Fortune's classic English Qabalah textbook", "A Wiccan liturgy", "A Blavatsky work"],
     1,
     "1890\u20131946: Fortune's textbook and the Society of the Inner Light \u2014 see the Concepts notes."),
    ("The 'double track' of recent decades refers to:",
     ["Two rival orders", "New Age popularization/dilution *and* academic professionalization happening together", "Two editions of the Book of the Law", "Tarot and astrology"],
     1,
     "The Concepts notes: popularization and academization as parallel facts about the same decades."),
    ("Debunking-as-sport is rejected because the course's standard is:",
     ["Credulity", "The same rigor as any human phenomenon \u2014 no more credulity than any extraordinary claim gets, and no contempt either", "Ignoring evidence", "Insider belief"],
     1,
     "The closing discipline: source criticism, claim sorting, charity \u2014 critical reading without contempt."),
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
    print('part4 ok: modules 13-16 retrofitted')

if __name__ == '__main__':
    main()
