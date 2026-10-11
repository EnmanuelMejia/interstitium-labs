# Batch 7 — occult-esoteric: Esoteric Traditions
# Intellectual/cultural history framing; historical claims kept distinct from belief.
DOMAIN = "occult-esoteric"

SIMS = [
    {
        "id": "occult-esoteric-sim-1",
        "title": "Attribute the Symbol",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A museum registrar hands you an uncatalogued engraving: a serpent eating its own tail inside a triangle. Attribute it correctly.",
        "steps": [
            {
                "symptom": "Engraving: ouroboros (serpent eating its tail) enclosed in a triangle. No caption, no date.",
                "evidence": [
                    ["Motif", "Ouroboros — documented in Egyptian, Greek alchemical, and Norse sources"],
                    ["Frame", "Triangle — in Western esotericism, often the alchemical tria prima or trinitarian geometry"],
                    ["Style", "Line engraving consistent with 17th-century European print"]
                ],
                "options": [
                    "Norse mythology — Jörmungandr, the world-serpent",
                    "European alchemical tradition: the ouroboros as cyclical transformation, framed by the triangle of the tria prima — attribute as 17th-century alchemical emblem",
                    "Christian Trinity diagram — the triangle proves it"
                ],
                "correct": 1,
                "explain": "Attribution weighs all evidence: the ouroboros is pan-cultural, but the triangle frame plus 17th-century engraving style points to the European alchemical emblem tradition (cf. the Chrysopoeia of Cleopatra's imagery as transmitted through early modern prints). Single-motif attribution is the classic error."
            },
            {
                "symptom": "A donor claims the engraving 'proves alchemists discovered the conservation of matter.'",
                "evidence": [
                    ["Claim", "Symbolic image = scientific discovery"],
                    ["What the sources say", "Alchemical texts speak of cyclical transformation and unity, not quantitative conservation"],
                    ["Your role", "Registrar, not believer or debunker"]
                ],
                "options": [
                    "Agree — the donor funds the wing",
                    "Record the donor's interpretation as provenance commentary, but catalog the piece by what the scholarship supports: an emblem of cyclical transformation in the alchemical tradition",
                    "Remove the piece — the claim taints it"
                ],
                "correct": 1,
                "explain": "The registrar's discipline: document the claim as part of the object's modern reception history, but attribute the object itself on scholarly evidence. Historical claims and belief claims get separate fields."
            },
            {
                "symptom": "The catalog entry is due. What does a responsible entry contain?",
                "evidence": [
                    ["Constraint", "Must serve scholars, respect the tradition's own terms, and not endorse supernatural claims"],
                    ["Audience", "Public museum catalog, all backgrounds"]
                ],
                "options": [
                    "A debunking essay explaining why alchemy was wrong",
                    "Description of the image, attribution with evidence, the tradition's own reading of the symbol, and a clear marker where description ends and interpretation begins",
                    "Only the physical description — interpretation is too risky"
                ],
                "correct": 1,
                "explain": "Good cataloging does three things: describes, attributes with evidence, and presents the tradition's self-understanding — with the seams visible. Neither endorsement nor ridicule; scholarship."
            }
        ],
        "debrief": "Esoteric scholarship is attribution work: weigh every piece of evidence, separate the object's history from its modern reception, and mark where description ends and interpretation begins.",
        "points": 15
    },
    {
        "id": "occult-esoteric-sim-2",
        "title": "The Archive Choice",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "You're researching the transmission of Hermetic texts. Two archives, one travel grant. Choose like a historian.",
        "steps": [
            {
                "id": "grant",
                "text": "One travel grant. Archive A: a private collection with a rumored 15th-century Corpus Hermeticum manuscript — unverified, owner eccentric, access uncertain. Archive B: a university library with complete Ficino correspondence and catalogued marginalia — solid, unglamorous. Where do you go?",
                "choices": [
                    {"label": "Archive A — the rumored manuscript could rewrite the field", "feedback": "You spend three weeks negotiating access and see the manuscript for one afternoon. It's a 19th-century copy. The rumor was the find.", "points": 3, "next": "rumor"},
                    {"label": "Archive B — the correspondence will show HOW Hermetic ideas actually traveled", "feedback": "Ficino's letters show the real transmission network: who read what, who argued with whom. Transmission history is built from correspondence, not rumors.", "points": 10, "next": "letters"},
                    {"label": "Split the grant: one week each", "feedback": "Two shallow visits instead of one deep one. You leave both archives just as the real work begins.", "points": 4, "next": "shallow"}
                ]
            },
            {
                "id": "rumor",
                "text": "The 'manuscript' is a 19th-century copy with an invented provenance. The owner wants you to authenticate it anyway. What now?",
                "choices": [
                    {"label": "Authenticate it — the owner might fund future research", "feedback": "A false authentication corrupts the scholarly record permanently. No grant is worth that.", "points": 0, "next": "END"},
                    {"label": "Document it accurately as a 19th-century copy and study its invented provenance as reception history", "feedback": "The salvage: the forgery itself becomes evidence — of 19th-century occult revival appetites. Reception history rescues the trip.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "shallow",
                "text": "Both visits were too short for real findings. Your advisor asks what the trip produced. Honest answer?",
                "choices": [
                    {"label": "Write it up ambitiously — a thin finding dressed as a breakthrough", "feedback": "Overclaiming from thin archival work is how the field's credibility problems start.", "points": 1, "next": "END"},
                    {"label": "Report the negative result honestly and request a focused return trip to Archive B", "feedback": "Negative results are data. The honest report plus a targeted proposal is how real archival careers are built.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "letters",
                "text": "In Ficino's letters you find him arguing with a colleague about whether the Corpus Hermeticum predates Moses — the dating controversy that shaped Renaissance magic. How do you handle the fact that Ficino was wrong (it's 2nd–3rd century CE, shown by Casaubon in 1614)?",
                "choices": [
                    {"label": "Present Ficino's error as foolishness — we know better now", "feedback": "Presentism. Ficino worked without Casaubon's philology; the interesting question is what the belief ENABLED, not that it was wrong.", "points": 3, "next": "END"},
                    {"label": "Show how the (false) ancient dating authorized the whole Renaissance magical program — the error is historically productive", "feedback": "This is the historian's move: the belief's truth value and its historical force are separate questions. Wrong dating, enormous consequences — that's the story.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Transmission history runs on correspondence and documented reading, not rumors. And a belief's falsity doesn't cancel its historical force — often the force is the story.",
        "points": 20
    },
    {
        "id": "occult-esoteric-sim-3",
        "title": "Order the Transmission",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Put the transmission of Hermetic literature to the Latin West in chronological order.",
        "steps": {
            "context": "How did the Corpus Hermeticum reach Renaissance readers? Order these transmission events earliest to latest.",
            "items": [
                "Hermetic texts composed in Roman Egypt (2nd–3rd century CE)",
                "Arabic scholars preserve and comment on Hermetic material (8th–10th century)",
                "Greek manuscript reaches Florence; Ficino commissioned to translate (1460s)",
                "Ficino's Latin Pimander printed — the Renaissance magical program ignites (1471)",
                "Casaubon's philological dating shows the texts are late antique, not Mosaic (1614)"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Egyptian composition, Arabic preservation, Florentine translation, print explosion, then philological correction. Transmission is a relay across civilizations — every handoff reshapes what arrives.",
        "points": 10
    },
    {
        "id": "occult-esoteric-sim-4",
        "title": "Audit the Transcription",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "A digitized grimoire transcription has 3 cataloging errors that misattribute its contents. Find them.",
        "steps": {
            "config": "# ms-447.conf — 'digitized grimoire'\ntitle = 'The Lesser Key'          # line 2\ndate = 1641                     # line 3\nlanguage = latin                # line 4\ncontents = demons, angels       # line 5\nprovenance = 'Solomon, 10th c.' # line 6\nscript = secretary_hand         # line 7\ncondition = fragile             # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Title misattributed: the contents (lines 4–5) don't match the Lesser Key of Solomon's known structure — this is a composite commonplace book, not the Key.", "fix": "title = 'Composite commonplace book (so-called)' pending full collation."},
                {"line": 3, "description": "Date 1641 is the watermark date of the paper, not the manuscript — the secretary hand suggests late 17th century.", "fix": "date = 'late 17th century (paper watermarked 1641)'."},
                {"line": 6, "description": "Provenance 'Solomon, 10th c.' repeats the manuscript's own legendary claim as fact — a classic cataloging error.", "fix": "provenance = 'Unknown English compiler; Solomon attribution is internal legend, not evidence.'"}
            ]
        },
        "debrief": "Lines 4, 5, 7, 8 are sound observations. The errors: misattributed title, watermark mistaken for manuscript date, and legend recorded as provenance. Manuscripts lie about themselves; the catalog must not repeat the lie as fact.",
        "points": 15
    },
    {
        "id": "occult-esoteric-sim-5",
        "title": "Curate the Exhibition",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "You're curating 'Symbols of Transformation' for a public museum. Practitioners, scholars, and skeptics will all walk through. Curate honestly.",
        "steps": [
            {
                "id": "curate",
                "text": "Opening gallery: alchemical imagery. A practitioner group asks that the exhibition 'honor the living tradition'; a skeptic group demands 'no endorsement of pseudoscience'. Your framing?",
                "choices": [
                    {"label": "Frame it as debunking: 'what alchemists got wrong'", "feedback": "Half your audience came to learn about a tradition's inner logic; they get a lecture. The practitioners leave insulted, the curious leave uninformed.", "points": 2, "next": "cold"},
                    {"label": "Frame it as intellectual history: what practitioners believed, why it made sense then, how it shaped science and art — with belief claims clearly marked", "feedback": "The frame holds everyone: practitioners see their tradition taken seriously, skeptics see claims marked as claims, scholars see the evidence. History, not apologetics.", "points": 10, "next": "holds"},
                    {"label": "Avoid all interpretation — just hang the images with dates", "feedback": "Images without context are decoration. Visitors project their own assumptions, which is exactly what curation should prevent.", "points": 3, "next": "cold"}
                ]
            },
            {
                "id": "cold",
                "text": "Attendance is fine but the reviews say 'shallow' and 'preachy'. A school group of 16-year-olds arrives tomorrow. Any repair?",
                "choices": [
                    {"label": "Add one strong object label: a single image traced from Egyptian source through Arabic commentary to the European print — transmission made visible", "feedback": "One excellent label teaches the method: follow the image across civilizations. The students get the one thing the exhibition was missing — how we know.", "points": 7, "next": "END"},
                    {"label": "Leave it — the run ends in three weeks", "feedback": "The exhibition closes as it opened: competent, forgettable, and a missed chance.", "points": 2, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "holds",
                "text": "The frame is working. Now the tarot gallery: the museum owns a 15th-century Visconti-Sforza deck. A donor wants the label to say tarot 'was designed for divination'. The scholarship says it was a card game first; divination use is 18th century. The donor funds the catalog. What does the label say?",
                "choices": [
                    {"label": "What the donor wants — the catalog needs funding", "feedback": "You've sold the label. Every scholar who reads it will know, and the museum's credibility is the actual endowment.", "points": 1, "next": "END"},
                    {"label": "The scholarship: a 15th-century game deck, with divination uses documented from the 18th century — and a sidebar on how the myth of ancient origins formed", "feedback": "The label teaches two histories: the deck's, and the myth's. The donor may grumble; the catalog stays honest. That's the job.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Curation is applied historiography: take every tradition seriously on its own terms, mark belief claims as such, and never sell a label. The transmission story — how things traveled — is usually the most honest exhibit of all.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "occult-esoteric-console-1",
        "title": "Organize the Symbol Archive",
        "console": "linux-desktop",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "The digitization project's files need archival order: a manuscripts directory, a protected transcription file, and proper permissions.",
        "tasks": [
            {"id": "occult-esoteric-console-1-t1", "instruction": "Create the directory /home/user/manuscripts.", "validate": {"action": "create-dir", "params": {"path": "/home/user/manuscripts"}}, "hint": "Create directory form: PATH /home/user/manuscripts."},
            {"id": "occult-esoteric-console-1-t2", "instruction": "Create the file /home/user/manuscripts/ms-447.txt for the transcription.", "validate": {"action": "create-file", "params": {"path": "/home/user/manuscripts/ms-447.txt"}}, "hint": "Create file form: PATH /home/user/manuscripts/ms-447.txt."},
            {"id": "occult-esoteric-console-1-t3", "instruction": "Set mode 600 on /home/user/manuscripts/ms-447.txt — unpublished transcriptions are restricted.", "validate": {"action": "chmod", "params": {"path": "/home/user/manuscripts/ms-447.txt", "mode": "600"}}, "hint": "Select the file row, then chmod form with mode 600."}
        ],
        "debrief": "Archives run on order and restriction: dedicated directories, named transcriptions, tight permissions on unpublished work. Scholarship needs the same custody discipline as evidence."
    },
    {
        "id": "occult-esoteric-console-2",
        "title": "Build the Correspondences Database",
        "console": "db-admin",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The symbol-correspondence index lives in a database. Create it, add the archivist user, grant access, and back it up.",
        "tasks": [
            {"id": "occult-esoteric-console-2-t1", "instruction": "Create a database named 'correspondences'.", "validate": {"action": "create-database", "params": {"name": "correspondences"}}, "hint": "Databases section: create database 'correspondences'."},
            {"id": "occult-esoteric-console-2-t2", "instruction": "Create a database user named 'archivist'.", "validate": {"action": "create-user", "params": {"name": "archivist"}}, "hint": "Users & grants section: create user 'archivist'."},
            {"id": "occult-esoteric-console-2-t3", "instruction": "Grant SELECT on 'correspondences' to 'archivist'.", "validate": {"action": "grant-priv", "params": {"db": "correspondences", "user": "archivist", "priv": "SELECT"}}, "hint": "Grants form: DB correspondences, USER archivist, PRIVILEGE SELECT."},
            {"id": "occult-esoteric-console-2-t4", "instruction": "Back up the 'correspondences' database.", "validate": {"action": "backup", "params": {"db": "correspondences"}}, "hint": "Databases section: click 'Back up' on correspondences."}
        ],
        "debrief": "A research database is infrastructure: least-privilege access for the archivist, and backups before the exhibition opens. Lost correspondences are lost scholarship."
    },
    {
        "id": "occult-esoteric-console-3",
        "title": "Query the Traditions Index",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Query the traditions index: which symbols appear in which traditions, and where did the attributions come from?",
        "tasks": [
            {"id": "occult-esoteric-console-3-t1", "instruction": "Create the table 'symbols' with columns: id INT, name TEXT, tradition TEXT, century TEXT.", "validate": {"action": "create-table", "params": {"name": "symbols", "columns": "id INT, name TEXT, tradition TEXT, century TEXT"}}, "hint": "Tables section: create 'symbols' with columns exactly: id INT, name TEXT, tradition TEXT, century TEXT."},
            {"id": "occult-esoteric-console-3-t2", "instruction": "Create an index on symbols(tradition).", "validate": {"action": "create-index", "params": {"table": "symbols", "column": "tradition"}}, "hint": "Create index: TABLE symbols, COLUMN tradition."},
            {"id": "occult-esoteric-console-3-t3", "instruction": "Run a query selecting all symbols where tradition is 'alchemy'.", "validate": {"action": "run-query", "params": {"match": "alchemy"}}, "hint": "Type: SELECT * FROM symbols WHERE tradition = 'alchemy'; — must contain 'alchemy'."},
            {"id": "occult-esoteric-console-3-t4", "instruction": "Run a query counting symbols grouped by tradition.", "validate": {"action": "run-query", "params": {"match": "GROUP BY tradition"}}, "hint": "Type: SELECT tradition, COUNT(*) FROM symbols GROUP BY tradition; — must contain 'GROUP BY tradition'."}
        ],
        "debrief": "Comparative work is query work: structure the attestations, then ask which symbols travel across traditions and which stay home. Transmission patterns emerge from GROUP BY."
    },
    {
        "id": "occult-esoteric-console-4",
        "title": "Configure the Exhibition Site",
        "console": "generic-web",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Set up the exhibition's web presence: name it, set the contact, and submit.",
        "tasks": [
            {"id": "occult-esoteric-console-4-t1", "instruction": "Set site_name to 'Symbols of Transformation'.", "validate": {"action": "set-field", "params": {"id": "site_name", "value": "Symbols of Transformation"}}, "hint": "Set site name form: VALUE 'Symbols of Transformation'."},
            {"id": "occult-esoteric-console-4-t2", "instruction": "Set admin_email to 'curator@example.org'.", "validate": {"action": "set-field", "params": {"id": "admin_email", "value": "curator@example.org"}}, "hint": "Set admin email form: VALUE 'curator@example.org'."},
            {"id": "occult-esoteric-console-4-t3", "instruction": "Submit the settings form.", "validate": {"action": "submit-form", "params": {}}, "hint": "Click 'Submit settings'."}
        ],
        "debrief": "Public scholarship needs a public front door: named, contactable, and deliberately configured — like the exhibition itself."
    }
]

MISSIONS = [
    {
        "id": "occult-esoteric-term-1",
        "title": "Survey the Scriptorium",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient among the sources: list the workspace and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "README.md", "hint": "Type: ls — the listing includes README.md."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "study notes", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Surveyed. Know the corpus before interpreting a single symbol."
    },
    {
        "id": "occult-esoteric-term-2",
        "title": "Copy the Maxim",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Transcribe the Emerald Tablet's most famous line into maxim.txt — scribal work, done carefully.",
        "objectives": ["Write the maxim to maxim.txt", "Read it back"],
        "checks": [
            {"command_pattern": "echo.*>\\s*maxim\\.txt", "expect_contains": "", "hint": "Type: echo \"as above, so below\" > maxim.txt (no output on success)."},
            {"command_pattern": "cat\\s+maxim\\.txt", "expect_contains": "as above, so below", "hint": "Type: cat maxim.txt — the transcribed maxim appears."}
        ],
        "success_message": "Transcribed. The scribe's first virtue is fidelity to the source."
    },
    {
        "id": "occult-esoteric-term-3",
        "title": "Collate the Copies",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Append two variant readings, then collate: count lines and search for the key phrase.",
        "objectives": ["Append variant readings", "Count the lines", "Search for the phrase"],
        "checks": [
            {"command_pattern": "echo.*>>\\s*maxim\\.txt", "expect_contains": "", "hint": "Type: echo \"variant: as within, so without\" >> maxim.txt — append twice with different variants."},
            {"command_pattern": "wc\\s+-l\\s+maxim\\.txt", "expect_contains": "maxim.txt", "hint": "Type: wc -l maxim.txt."},
            {"command_pattern": "grep\\s+above\\s+maxim\\.txt", "expect_contains": "as above", "hint": "Type: grep above maxim.txt — the original line is shown."}
        ],
        "success_message": "Collated. Variants are data — the stemma grows from exactly this work."
    },
    {
        "id": "occult-esoteric-term-4",
        "title": "Seal the Transcription",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Seal your transcription with a hash — any later alteration breaks the seal.",
        "objectives": ["Hash the maxim"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "as above", "hint": "Type: sha256sum as above so below — the real hash plus your text are echoed."}
        ],
        "success_message": "Sealed. The archive trusts what it can verify."
    },
    {
        "id": "occult-esoteric-term-5",
        "title": "Read the Marginalia",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Marginalia lives at the edges of the page — read the edges of the log.",
        "objectives": ["Read the first lines of the log", "Read the last lines of the log"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "server starting", "hint": "Type: head -n 2 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log."}
        ],
        "success_message": "Marginalia read. Scholars have always learned most from what's written in the margins."
    },
    {
        "id": "occult-esoteric-term-6",
        "title": "Verify the Provenance",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Check the environment your work runs in — provenance applies to tools too.",
        "objectives": ["Print the environment", "Confirm the user identity"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps — prints the environment including USER=candidate."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Provenance verified. Know your instruments as well as your sources."
    },
    {
        "id": "occult-esoteric-term-7",
        "title": "Consult the Distant Library",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Before citing a digital archive, verify it resolves and responds.",
        "objectives": ["Resolve the archive domain", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig archive.example.org."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping archive.example.org."}
        ],
        "success_message": "Archive reachable. A source you cannot reach is a rumor."
    }
]
