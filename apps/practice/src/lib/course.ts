export type Block =
  | { kind: "h"; text: string }
  | { kind: "p"; text: string }
  | { kind: "ul"; items: string[] }
  | { kind: "note"; title: string; text: string }
  | { kind: "code"; title: string; text: string };

export type QuizQ = { q: string; choices: string[]; answer: number; why: string };

export type Session = {
  id: string;
  index: string;
  week: string;
  weekTitle: string;
  sitting: string;
  title: string;
  minutes: number;
  kicker: string;
  summary: string;
  objectives: string[];
  blocks: Block[];
  labId?: string;
  assignment?: { id: string; title: string; prompt: string };
  quiz: QuizQ[];
};

export type LabMeta = {
  id: string;
  index: string;
  title: string;
  sessionId: string;
  blurb: string;
  pass: string;
};

export const labs: LabMeta[] = [
  {
    id: "iris",
    index: "01",
    title: "Control set — iris",
    sessionId: "s03",
    blurb: "Fit a nearest-neighbor classifier on a clean public dataset before the data turns hostile.",
    pass: "Hold-out accuracy at least 80% with scaling on.",
  },
  {
    id: "malware-prep",
    index: "02",
    title: "Outliers in endpoint telemetry",
    sessionId: "s05",
    blurb: "Load a synthetic malware table, fence outliers, and train a first benign/malicious model.",
    pass: "Run the screen and keep suspicious-API in the feature set. Recall at least 60%.",
  },
  {
    id: "families",
    index: "03",
    title: "Malware family tree",
    sessionId: "s07",
    blurb: "Separate locker, stealer, and loader behavior with a shallow decision tree.",
    pass: "Hold-out accuracy at least 70% and read the learned rules.",
  },
  {
    id: "anomaly",
    index: "04",
    title: "Unsupervised beacon hunt",
    sessionId: "s10",
    blurb: "Isolation Forest and k-means on flow features, scored against a hidden beacon label.",
    pass: "Beacon recall at least 50% — feature choice matters.",
  },
  {
    id: "nlp",
    index: "05",
    title: "Security text intent",
    sessionId: "s12",
    blurb: "Bag-of-words model for benign mail, phishing, and internal alerts. Held-out lines stay unseen.",
    pass: "Held-out accuracy at least 60% with lowercase and punctuation stripping on.",
  },
  {
    id: "adversarial",
    index: "06",
    title: "Evasion and a blunt defense",
    sessionId: "s14",
    blurb: "Nudge a linear malware score along its gradient, then clip and retrain.",
    pass: "Show a flip, then cut remaining flips with a defense.",
  },
  {
    id: "capstone",
    index: "07",
    title: "Endpoint malware detector",
    sessionId: "s16",
    blurb: "Clean a dirty export, choose features, train, and defend a SOC threshold.",
    pass: "Drop broken rows, clip glitches, dedupe, then F1 at least 72% with false-positive rate under 20%.",
  },
];

export function labById(id: string) {
  return labs.find((l) => l.id === id);
}

export const sessions: Session[] = [
  {
    id: "s00",
    index: "00",
    week: "00",
    weekTitle: "Arrival",
    sitting: "Source cohort · Tue 6 Oct · welcome",
    title: "How this domain is built",
    minutes: 25,
    kicker: "Orientation",
    summary: "What you will practice, what is original, and how briefings, benches, and the capstone connect.",
    objectives: [
      "Map the nine-week arc onto a self-paced domain",
      "See which work is a briefing, a bench, or a field note",
      "Know what this reconstruction deliberately does not copy",
    ],
    blocks: [
      {
        kind: "p",
        text: "Interstitium Labs treats AI-aided cybersecurity as connective tissue: the space between a statistical model and a security operations decision. The public live course that this domain tracks is a nine-week sequence — two sittings a week — covering machine learning for detection, six guided labs in Python, and a capstone that trains a malware detector. Those lectures, slides, and notebooks are not public. This domain does not reproduce them, and it is not affiliated with that school, with Microsoft, or with the architect who teaches the cohort.",
      },
      {
        kind: "p",
        text: "What is public is the outline: the topics, the lab targets, the assignment rhythm, and the capstone shape. That outline is reconstructed here as original briefings, case files, and benches you can run in the browser. Each bench has a scikit-learn port so the same exercise still fits a Jupyter notebook.",
      },
      {
        kind: "h",
        text: "The unit of practice",
      },
      {
        kind: "ul",
        items: [
          "Briefing — the idea, with a worked security example.",
          "Bench — a model you fit yourself. Synthetic telemetry only. No live malware, no binaries.",
          "Field note — the assignment. Some complete when the bench clears a bar; the notebook setup is yours to mark.",
          "Case file — a short operational story. The live cohort uses guest speakers twice; those talks are not published, so the matching sittings carry an original operator note instead.",
          "Capstone — clean a dirty endpoint export, train a detector, and pick a threshold you can defend.",
        ],
      },
      {
        kind: "note",
        title: "Tools the outline names",
        text: "Python, Jupyter, scikit-learn, and seaborn. The benches mirror that workflow: load a table, preprocess, fit, score, and look at the picture. You do not need a notebook server to finish the domain. If you want the port, each bench includes a short script.",
      },
      {
        kind: "p",
        text: "Progress stays in this browser. There is no class server and no account. Passing a checkpoint quiz marks the briefing. Clearing a bench marks its field note.",
      },
    ],
    quiz: [
      {
        q: "What is the unit of practice in this domain?",
        choices: [
          "A vendor dashboard you cannot rerun",
          "A briefing plus a bench you can rerun",
          "A proctored certification exam",
        ],
        answer: 1,
        why: "Every sitting is something you can reopen: an argument, then a model with a pass bar.",
      },
      {
        q: "Where does your progress live?",
        choices: ["On a cohort server", "Only in this browser", "In a Microsoft tenant"],
        answer: 1,
        why: "There is no account. Clearing the cache clears the transcript.",
      },
    ],
  },
  {
    id: "s01",
    index: "01",
    week: "01",
    weekTitle: "Foundations",
    sitting: "Source cohort · Thu 8 Oct · introduction",
    title: "Models meet the threat model",
    minutes: 35,
    kicker: "Briefing",
    summary: "AI, machine learning, and the four words defenders already use: threat, vulnerability, attack, defense.",
    objectives: [
      "Separate AI, machine learning, and deep learning without the marketing fog",
      "Place a model inside a threat model instead of beside it",
      "Name where scoring helps a SOC, and where it cannot",
    ],
    blocks: [
      {
        kind: "h",
        text: "Three words people collapse",
      },
      {
        kind: "p",
        text: "Artificial intelligence is the ambition: software that does work we used to reserve for a trained person. Machine learning is the method most of this domain uses: fit a function to examples, then score new examples. Deep learning is a family of those functions — many stacked layers — useful when the raw input is a document, a packet sequence, or a binary, and you do not want to hand-build every feature. Most of the labs in the published outline stay with classical methods in scikit-learn. That is deliberate. A logistic regression you can explain will beat a transformer you cannot defend in a change-advisory meeting.",
      },
      {
        kind: "h",
        text: "The four security words",
      },
      {
        kind: "ul",
        items: [
          "Threat — an actor or event that can do harm. A crew that steals session tokens.",
          "Vulnerability — a weakness they can use. A long-lived refresh token sitting in a readable store.",
          "Attack — the use of that weakness. A phish, then a token replay, then a mailbox rule.",
          "Defense — a control that reduces likelihood or impact. Phishing-resistant sign-in, token binding, a detection on odd OAuth grants.",
        ],
      },
      {
        kind: "p",
        text: "A model is not a fifth word. It is a way to implement detection, ranking, or grouping inside a defense. If you cannot name the threat and the decision the score changes, you do not have a security use case. You have a demo.",
      },
      {
        kind: "note",
        title: "Where this shows up in real pipelines",
        text: "Mail gateways have scored spam with statistical token models for decades. Endpoint products classify families so an analyst does not reverse every sample. Identity systems baseline sign-in and page on deviation. None of these replace the control that would have stopped the attack. They change who looks at what, and how fast.",
      },
      {
        kind: "p",
        text: "The failure mode to remember this week: a novel technique with no features in your table is invisible to the model trained last quarter. Detection engineering still starts with a hypothesis, not with an algorithm menu.",
      },
    ],
    quiz: [
      {
        q: "Which of these is a vulnerability, not a threat or an attack?",
        choices: [
          "A crew that wants mailbox access",
          "A phish already sitting in an inbox",
          "A refresh token stored where any local process can read it",
        ],
        answer: 2,
        why: "The weakness is the exposed token. The crew is the threat. The phish is an attack in progress.",
      },
      {
        q: "Where does machine learning usually help first in a SOC?",
        choices: [
          "Replacing the incident commander",
          "Ranking and grouping telemetry so a human sees the strange slice",
          "Proving that no zero-day exists",
        ],
        answer: 1,
        why: "Models are triage. They do not close incidents and they cannot prove a negative.",
      },
    ],
  },
  {
    id: "s02",
    index: "02",
    week: "01",
    weekTitle: "Foundations",
    sitting: "Source cohort · Tue 13 Oct · machine learning fundamentals",
    title: "Learning that generalizes",
    minutes: 40,
    kicker: "Briefing",
    summary: "Supervised and unsupervised learning, three algorithms the outline names, and the split that keeps you honest.",
    objectives: [
      "Match supervised and unsupervised learning to security jobs",
      "Explain linear regression, logistic regression, and a decision tree in analyst language",
      "Split data so the test set cannot leak into the fit",
    ],
    blocks: [
      {
        kind: "h",
        text: "Two regimes",
      },
      {
        kind: "p",
        text: "Supervised learning has a label. Malicious or not. Family name. Phish or internal alert. You show the model examples of each and ask it to predict the label on a new row. Unsupervised learning has no label, or you refuse to trust the one you have. You ask which points sit apart from the mass. That is the usual shape of anomaly detection on a new log source.",
      },
      {
        kind: "h",
        text: "Three algorithms, said plainly",
      },
      {
        kind: "ul",
        items: [
          "Linear regression draws a straight line through a number you want to predict — failed sign-ins per hour, bytes per flow. It is a poor malware detector. It is a decent baseline for volume.",
          "Logistic regression is the yes/no cousin. It still uses a weighted sum of features, then squashes that sum into a probability. The weights are the explanation: which feature pushes the score up.",
          "A decision tree asks a sequence of thresholds. Entropy above 7.1 and unsigned? Call it suspicious. Analysts can read the rule. Trees overfit if you let them grow until every leaf is pure.",
        ],
      },
      {
        kind: "h",
        text: "Train, validate, test",
      },
      {
        kind: "p",
        text: "Training data is what the fit sees. Validation data is how you choose k, a threshold, or a tree depth — you may look at it many times, so it becomes slightly worn. Test data is touched once, at the end, or your accuracy is a story you told yourself. The outline’s first assignment is environmental: stand up a notebook and prove you can execute a cell. The scientific habit starts in the same sitting. Fit every preprocessor on the training rows only. If you compute a mean on the full file and then split, the test set has already whispered into the model.",
      },
      {
        kind: "code",
        title: "Field note 1 — notebook, local",
        text: "python -m venv .venv && source .venv/bin/activate\npip install jupyter scikit-learn seaborn pandas\njupyter lab\n# new notebook: import sklearn, pandas, seaborn; print versions",
      },
      {
        kind: "note",
        title: "In this domain",
        text: "There is no remote Jupyter server to join. Mark the field note once you either have a local notebook that imports those three libraries, or you have opened Bench 01 and run it once. The bench is the supported runtime.",
      },
    ],
    assignment: {
      id: "a1",
      title: "Field note 1 — runtime",
      prompt:
        "Stand up a notebook that imports pandas, scikit-learn, and seaborn — or open Bench 01 and run a fit. Then mark this note.",
    },
    quiz: [
      {
        q: "You standardize using the mean of the entire file, then split into train and test. What happened?",
        choices: [
          "Correct preprocessing",
          "The test set leaked into the fit",
          "The problem became unsupervised",
        ],
        answer: 1,
        why: "Statistics used for scaling must be learned on training rows and applied unchanged to the rest.",
      },
      {
        q: "Logistic regression is the natural fit when the label is",
        choices: [
          "A continuous byte count",
          "A yes or no you want as a probability",
          "A cluster id you do not have yet",
        ],
        answer: 1,
        why: "Logistic regression outputs a probability for a binary label. Counts want regression. Unknown groups want clustering.",
      },
    ],
  },
  {
    id: "s03",
    index: "03",
    week: "02",
    weekTitle: "First fit",
    sitting: "Source cohort · Thu 15 Oct · scikit-learn and preprocessing",
    title: "From a table to a model",
    minutes: 45,
    kicker: "Bench",
    summary: "The scikit-learn workflow on the iris control set, then the same gestures on dirtier security tables.",
    objectives: [
      "Walk the basic fit loop: load, split, preprocess, fit, predict, score",
      "See why a clean dataset is the control experiment",
      "Preprocess with intent — scaling, not superstition",
    ],
    blocks: [
      {
        kind: "p",
        text: "The published lab uses the iris dataset: three flower species, four measurements, no missing values, no adversary. That is the point. If your pipeline cannot separate setosa from the other two on petal length, it will not survive a malware table. Iris is the control. Endpoint telemetry comes next.",
      },
      {
        kind: "h",
        text: "The workflow",
      },
      {
        kind: "ul",
        items: [
          "Load rows and name the label column so it cannot sneak in as a feature.",
          "Split first.",
          "Fit preprocessing on train. Scaling puts features on a comparable range so a distance model does not ignore petal width just because sepal length has bigger numbers.",
          "Fit the estimator. Here, k nearest neighbors: a new flower gets the majority label of the k closest training flowers.",
          "Score on the hold-out. Look at which pair you confused. Versicolor and virginica overlap. Setosa should not.",
        ],
      },
      {
        kind: "code",
        title: "sklearn port — iris",
        text: "from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\n\nX, y = load_iris(return_X_y=True)\nXtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7, stratify=y)\nclf = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))\nclf.fit(Xtr, ytr)\nprint(clf.score(Xte, yte))",
      },
      {
        kind: "note",
        title: "Field note 2",
        text: "The cohort’s second assignment pulls the capstone file and cleans it. You will do that cleaning for real on the capstone bench. This week, prove the loop on iris: scale on, petal features available, hold-out accuracy at least 80%.",
      },
    ],
    labId: "iris",
    assignment: {
      id: "a2",
      title: "Field note 2 — preprocess the control set",
      prompt: "On Bench 01, scale the measurements and clear 80% hold-out accuracy. The capstone cleaning comes later, on dirtier rows.",
    },
    quiz: [
      {
        q: "Why does the outline start with iris?",
        choices: [
          "Flowers are a malware family",
          "It is a clean control before the data turns hostile",
          "seaborn refuses to import otherwise",
        ],
        answer: 1,
        why: "You want a pipeline that works when nothing is missing and the classes are real, so later failures are about the security data.",
      },
      {
        q: "Scaling matters most for",
        choices: [
          "Models that use distance or a weighted sum",
          "The alphabetical order of column names",
          "Whether the notebook kernel is Python 3",
        ],
        answer: 0,
        why: "k-NN and linear models are sensitive to units. A tree that only thresholds one feature at a time is less so.",
      },
    ],
  },
  {
    id: "s04",
    index: "04",
    week: "02",
    weekTitle: "First fit",
    sitting: "Source cohort · Tue 20 Oct · AI for threat detection",
    title: "Three ways to say suspicious",
    minutes: 35,
    kicker: "Case",
    summary: "Anomaly detection, intrusion detection, and malware classification are different decisions wearing similar slides.",
    objectives: [
      "Separate anomaly, intrusion, and malware detection by the label they assume",
      "Place a detector on the host or on the wire without pretending they are the same",
      "Read a false-positive failure as a product bug, not a math bug",
    ],
    blocks: [
      {
        kind: "p",
        text: "Threat detection is not one model. Anomaly detection asks what does not look like the recent baseline. It shines on a new log source and fails when the baseline itself is messy — patch Tuesday, a marketing launch, a VPN migration. Intrusion detection looks for attack patterns in traffic or host events, signature or behavior. Malware detection asks whether this file or this process is hostile, often with a family name attached. Mixing the three in one slide deck is how programs buy a platform that pages on weather.",
      },
      {
        kind: "h",
        text: "Case file — Harborline DNS",
      },
      {
        kind: "p",
        text: "A fictional mid-size SOC turned on an unsupervised detector across all DNS queries and called it their AI program. The first week it learned that the finance team’s SaaS, the CDN, and a noisy monitoring agent were all anomalies, because each was rare in the global table. They did not have a detection. They had a popularity contest. The repair was feature discipline: score rarity of the registered domain plus a beaconing regularity on the same host, suppress newly onboarded agents for seven days, and never page on a score without a second weak signal. The algorithm did not change. The decision did.",
      },
      {
        kind: "ul",
        items: [
          "Anomaly: no attack label required at fit time. Evaluation still needs some labels or you cannot tell attacks from odd-but-benign.",
          "Intrusion detection: a hypothesis about a technique. The model is optional.",
          "Malware classification: a label, a feature pipeline that does not detonate the world, and a family taxonomy someone owns.",
        ],
      },
    ],
    quiz: [
      {
        q: "Anomaly detection differs from malware classification because",
        choices: [
          "Anomalies are always malware",
          "It looks for deviation and may have no attack label when it is fit",
          "It only works on images",
        ],
        answer: 1,
        why: "Classification needs examples of the classes. Anomaly methods need a picture of normal, and they still need a way to be graded later.",
      },
      {
        q: "A signature intrusion system fails open on",
        choices: [
          "Traffic that matches a known rule",
          "A novel pattern that has no signature yet",
          "Every packet under 64 bytes",
        ],
        answer: 1,
        why: "Signatures are precise and blind to what they have not been told. That gap is why behavior and anomaly layers exist.",
      },
    ],
  },
  {
    id: "s05",
    index: "05",
    week: "03",
    weekTitle: "Hostile tables",
    sitting: "Source cohort · Thu 22 Oct · outliers and anomaly detection",
    title: "Outliers are a hypothesis",
    minutes: 45,
    kicker: "Bench",
    summary: "IQR fences, why entropy lies, and a first binary model on synthetic endpoint rows.",
    objectives: [
      "Fence outliers without calling every extreme point an incident",
      "Engineer malware-like features and know which ones benign software shares",
      "Train and score a first classification model the way the outline’s second lab sets up",
    ],
    blocks: [
      {
        kind: "p",
        text: "An outlier is a row that is far from the bulk of a feature. A z-score past three, or a point outside the Tukey fences (1.5 times the interquartile range beyond the quartiles), is a candidate. It is not a verdict. Sensors glitch. A backup job really does move that many bytes. The analyst move is to ask what mechanism would produce the extreme, then decide whether the mechanism is hostile.",
      },
      {
        kind: "h",
        text: "Features the malware labs lean on",
      },
      {
        kind: "ul",
        items: [
          "Entropy — packed and encrypted payloads look random. So do compressed installers and archives.",
          "Imports and suspicious API counts — file, process, and network calls that packers and stealers favor. Legitimate updaters share some of them.",
          "Section count, packer flag, signature missing — cheap static bits. Easy to evade, still useful in combination.",
          "Beacon rate and obfuscated strings — dynamic-ish summaries. In this domain they are columns in a synthetic table, not traces from a detonated sample.",
        ],
      },
      {
        kind: "p",
        text: "The outline’s assignment here is to import the malware table into a dataframe. Bench 02 is that import. The rows are generated, labeled, and safe. Real malware corpora exist for researchers under controlled conditions; this domain never asks you to download a sample.",
      },
      {
        kind: "code",
        title: "sklearn port — fences and a first model",
        text: "import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\n\ndf = pd.read_csv('telemetry.csv')  # your export, not a live sample set\nq1, q3 = df.entropy.quantile([0.25, 0.75])\niqr = q3 - q1\ndf['entropy_outlier'] = (df.entropy < q1 - 1.5 * iqr) | (df.entropy > q3 + 1.5 * iqr)\ny = df.label\nX = df.drop(columns=['label', 'id'])\nXtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=11)\npipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))\npipe.fit(Xtr, ytr)\nprint(pipe.score(Xte, yte))",
      },
    ],
    labId: "malware-prep",
    assignment: {
      id: "a3",
      title: "Field note 3 — import the telemetry",
      prompt: "Open Bench 02, keep suspicious-API in the model, and clear 60% recall on the hold-out malware rows.",
    },
    quiz: [
      {
        q: "A point outside the IQR fence is",
        choices: ["Automatically an intrusion", "A candidate outlier that still needs a mechanism", "Proof the sensor is dead"],
        answer: 1,
        why: "Fences are a screen. The incident starts when you can say why the point is extreme.",
      },
      {
        q: "High entropy is a weak feature alone because",
        choices: [
          "Entropy cannot be computed on files",
          "Packed installers and archives are legitimate and also high-entropy",
          "Entropy is an unsupervised algorithm",
        ],
        answer: 1,
        why: "Benign software compresses and packs too. Entropy is a hint inside a set of features, not a block rule.",
      },
    ],
  },
  {
    id: "s06",
    index: "06",
    week: "03",
    weekTitle: "Hostile tables",
    sitting: "Source cohort · Tue 27 Oct · AI for vulnerability assessment",
    title: "The backlog is the problem",
    minutes: 30,
    kicker: "Case",
    summary: "Scanning, prediction, and why a probability of exploitation is a sorting tool, not a pentest.",
    objectives: [
      "Separate discovery, prioritization, and exploit development",
      "Use a learned probability to reorder work, not to skip exposure",
      "Know what automated discovery systematically misses",
    ],
    blocks: [
      {
        kind: "p",
        text: "Vulnerability assessment in the outline covers scanning, predicting which flaws matter, and automated discovery. A scanner tells you the flaw is present. It does not tell you whether anyone is using it, whether the asset is reachable, or whether a compensating control already contains it. Pentesting spends humans on that argument for a slice of the estate. Machine learning shows up in the middle: given thousands of findings, which ones are likely to be exploited in the wild soon.",
      },
      {
        kind: "p",
        text: "EPSS, the Exploit Prediction Scoring System, is the public example of that idea. It is a probability, updated as exploitation evidence changes, meant to be read next to severity and next to your exposure. A critical bug on an isolated test host is not the same object as a medium bug on an internet-facing gateway with a known exploit. Models that emit only a severity remix are how teams relearn CVSS with extra steps.",
      },
      {
        kind: "note",
        title: "Case file — the Tuesday backlog",
        text: "An infrastructure group had 14,000 open findings and a patch window that could absorb about 200 changes. They sorted by CVSS and burned the window on library noise inside build containers. A second sort — known exploitation, external exposure, and whether the package was actually loaded — moved the window onto edge devices and a stale VPN. No model wrote the change ticket. The model only refused to let severity be the only column.",
      },
      {
        kind: "ul",
        items: [
          "Automated discovery finds known sinks, dependency versions, and some insecure patterns.",
          "It misses broken authorization, trust between services, and business logic.",
          "AI-assisted pentest tools can draft a test plan. They do not own the rules of engagement.",
        ],
      },
    ],
    quiz: [
      {
        q: "A model that predicts likelihood of exploitation is most useful when",
        choices: [
          "It replaces the asset inventory",
          "It reorders a backlog too large to patch at once",
          "CVSS is deleted, including exposure",
        ],
        answer: 1,
        why: "The value is sorting scarce change windows. Exposure and severity still belong in the decision.",
      },
      {
        q: "Automated vulnerability discovery still misses",
        choices: [
          "Logic and trust bugs that do not look like a known sink",
          "Every bug in a dependency, by definition",
          "Version numbers",
        ],
        answer: 0,
        why: "Scanners are strong on known patterns and weak on how your system is allowed to trust itself.",
      },
    ],
  },
  {
    id: "s07",
    index: "07",
    week: "04",
    weekTitle: "Families and response",
    sitting: "Source cohort · Thu 29 Oct · malware classification",
    title: "Families, not just malice",
    minutes: 45,
    kicker: "Bench",
    summary: "Static versus dynamic features, and a shallow tree that names locker, stealer, or loader.",
    objectives: [
      "Contrast static features with dynamic ones",
      "See why family labels overlap when packers are shared",
      "Read a decision tree as an analyst-facing explanation",
    ],
    blocks: [
      {
        kind: "p",
        text: "Benign versus malicious is a gate. Family is how response changes. A locker that encrypts shares is not handled like a stealer that has already shipped cookies, or a loader whose only job is to fetch the next stage. Static analysis reads the file without running it: headers, imports, strings, entropy, packer stubs. Dynamic analysis runs it in a controlled detonation and watches behavior. The outline’s lab builds classifiers in scikit-learn on extracted features. This bench does the same on synthetic family rows. Nothing here is a specimen.",
      },
      {
        kind: "h",
        text: "What the tree is allowed to say",
      },
      {
        kind: "p",
        text: "A shallow tree — a few thresholds — is the teaching model because you can read it back. If file-writes are high and network calls are low, the leaf tends to say locker. If clipboard and network are both high, stealer. If network is high and the section count is low, loader. Deep trees memorize the training noise, including the packer bit, and then call every packed benign installer a family member. The assignment paired with this sitting is visualization: plot the features, see which split carries information, and relate labels to outliers. The bench ranks features by how cleanly a single threshold separates classes.",
      },
      {
        kind: "code",
        title: "seaborn port — one feature, three families",
        text: "import seaborn as sns\nimport matplotlib.pyplot as plt\nfrom sklearn.tree import DecisionTreeClassifier, export_text\n\nsns.boxplot(data=df, x='family', y='file_writes')\nplt.show()\nclf = DecisionTreeClassifier(max_depth=3, random_state=7)\nclf.fit(Xtr, ytr)\nprint(export_text(clf, feature_names=list(Xtr.columns)))",
      },
    ],
    labId: "families",
    assignment: {
      id: "a4",
      title: "Field note 4 — features and rules",
      prompt: "On Bench 03, fit the tree, read the rules, and clear 70% hold-out accuracy. The importance bars are the seaborn picture, in place.",
    },
    quiz: [
      {
        q: "Family labels are harder than benign versus malicious because",
        choices: [
          "Static features are illegal to compute",
          "Classes are finer and share packers and libraries",
          "There is only one possible family",
        ],
        answer: 1,
        why: "Overlap is the whole difficulty. A packer used by three families will dominate a careless model.",
      },
      {
        q: "Static features are attractive because",
        choices: [
          "They require detonating every file",
          "They can be extracted without executing the file",
          "They cannot be evaded",
        ],
        answer: 1,
        why: "You can score at ingress without running hostile code. Evasion is still easy, which is why behavior layers exist.",
      },
    ],
  },
  {
    id: "s08",
    index: "08",
    week: "04",
    weekTitle: "Families and response",
    sitting: "Source cohort · Tue 3 Nov · incident response, guest",
    title: "The model in the response loop",
    minutes: 30,
    kicker: "Case",
    summary: "Enrichment, correlation, and containment — with a human still accountable for the action.",
    objectives: [
      "Place AI inside triage, not in the incident commander’s chair",
      "Collapse many alerts into one case",
      "Treat containment recommendations as proposals",
    ],
    blocks: [
      {
        kind: "p",
        text: "The live cohort inserts a guest in this sitting. That talk is not public, so this briefing is an operator note instead: what a response lead actually wants from a model. They do not want a paragraph of confidence. They want the related alerts already grouped, the asset owner named, the last three similar cases linked, and a containment step that says what it will break.",
      },
      {
        kind: "h",
        text: "A loop that survives contact",
      },
      {
        kind: "ul",
        items: [
          "Enrich — identity, asset criticality, whether the binary is signed by you, whether the destination is new.",
          "Correlate — one intrusion is often twenty alerts. A model that clusters them saves a queue. A model that duplicates them creates one.",
          "Recommend — isolate host, kill process, revoke token. Each recommendation needs a rollback and a human accept.",
          "Record — the features and the threshold, so the next shift can disagree with evidence.",
        ],
      },
      {
        kind: "note",
        title: "Case file — auto-isolate",
        text: "A plant network let an endpoint score isolate hosts without review. A buggy definition update flagged the historian service. Isolation stopped the process that operators use to see the line. The model was not malicious. The authority was. After that, high scores opened a case with a proposed action. Isolation of anything on the control network required a named human. Detection latency went up by a few minutes. Production incidents of that class went to zero.",
      },
    ],
    quiz: [
      {
        q: "The safe role of a model during response is",
        choices: [
          "Isolate every high score with no review",
          "Enrich, cluster, and propose an action a human can reject",
          "Write the customer notice on its own",
        ],
        answer: 1,
        why: "Authority stays with the responder. The model prepares the case.",
      },
      {
        q: "Correlation earns its keep when",
        choices: [
          "One intrusion emits many alerts that should be one case",
          "You want more pages per analyst",
          "The SIEM has no timestamps",
        ],
        answer: 0,
        why: "The win is fewer cases with more context, not a louder queue.",
      },
    ],
  },
  {
    id: "s09",
    index: "09",
    week: "05",
    weekTitle: "Behavior",
    sitting: "Source cohort · Thu 5 Nov · user behavior analytics",
    title: "People as a signal",
    minutes: 30,
    kicker: "Case",
    summary: "Baselines, insider risk, and account takeover — and the bias hiding in normal.",
    objectives: [
      "Define a behavioral baseline without surveilling for its own sake",
      "Separate a slow insider pattern from a sudden account takeover",
      "Notice when normal encodes a prejudice about who looks suspicious",
    ],
    blocks: [
      {
        kind: "p",
        text: "User and entity behavior analytics compares today’s actions to a baseline for that account and its peers. The useful version is narrow: sign-in location and agent, new OAuth grants, mailbox rules, mass downloads, impossible travel. The useless version is a score on a person’s whole life at work. Security does not need keystroke mood. It needs a small set of actions tied to account takeover and data theft.",
      },
      {
        kind: "h",
        text: "Two different shapes",
      },
      {
        kind: "ul",
        items: [
          "Account takeover is sudden. New country, new device, a consent to Mail.Read, a forwarding rule, then quiet. The baseline break is sharp.",
          "Insider risk is often slower and easier to abuse as a program. A person with legitimate access copies a trove. The features overlap with a job change, a travel week, or a shared mailbox. False accusations are the harm.",
        ],
      },
      {
        kind: "note",
        title: "Case file — the night desk",
        text: "A financial-services UEBA flagged the overnight payments desk every week. Their peers worked days, so night logons, bulk file access, and a shared account looked like theft. The model had learned the majority schedule and called the minority job an anomaly. The fix was a peer group that actually matched the role, a suppression for the shared account’s documented pattern, and a rule that a behavior score alone could not open an HR case. Technical control first. Employment action never on a score alone.",
      },
    ],
    quiz: [
      {
        q: "Account takeover often looks like",
        choices: [
          "A role changing slowly across a year",
          "A familiar account with a new location, a new OAuth grant, or a new mailbox rule",
          "A planned firewall change",
        ],
        answer: 1,
        why: "Takeover is a break in the account’s own recent pattern, usually fast and specific.",
      },
      {
        q: "A UEBA program becomes unfair when",
        choices: [
          "Features are only packet sizes on a router",
          "A minority work pattern is defined as suspicion",
          "You write down the feature list",
        ],
        answer: 1,
        why: "If normal means the majority schedule, nights, travel, and shared roles become investigations.",
      },
    ],
  },
  {
    id: "s10",
    index: "10",
    week: "05",
    weekTitle: "Behavior",
    sitting: "Source cohort · Tue 10 Nov · unsupervised anomaly detection",
    title: "Hunting without a label",
    minutes: 45,
    kicker: "Bench",
    summary: "K-means, Isolation Forest, and why One-Class SVM is the third name on the outline.",
    objectives: [
      "Explain isolation, distance-to-centroid, and a one-class boundary",
      "See a beaconing cluster that volume features hide",
      "Score an unsupervised method against a small labeled check set",
    ],
    blocks: [
      {
        kind: "p",
        text: "The outline names three unsupervised tools. K-means slices the table into k groups and you inspect small or distant groups. Isolation Forest throws random thresholds until a point is alone; points that isolate quickly are candidates. One-Class SVM learns a boundary around the bulk and marks the outside. It is sensitive to scaling and to the kernel, which is why this bench lets you feel the first two directly and treats the third as required reading rather than a second implementation.",
      },
      {
        kind: "p",
        text: "You still need a way to know if the candidates are attacks. The bench hides a beacon label and scores your recall. That is the teaching cheat the real SOC does not get on day one — and then builds, slowly, with confirmed incidents. If you feed the model only duration, the beacons hide inside normal. If you include interval regularity and rare-port, they separate. Feature choice is the detection.",
      },
      {
        kind: "code",
        title: "sklearn port — isolation forest",
        text: "from sklearn.ensemble import IsolationForest\nfrom sklearn.preprocessing import StandardScaler\n\nZ = StandardScaler().fit_transform(Xtr)\niso = IsolationForest(contamination=0.12, random_state=7)\niso.fit(Z)\npred = iso.predict(StandardScaler().fit(Xtr).transform(Xte))  # fit scaler on train only\n# pred == -1 means outlier",
      },
      {
        kind: "note",
        title: "About that snippet",
        text: "The comment is the lesson. Fitting the scaler on all rows, or refitting it on the test set, leaks. In production the scaler is part of the training artifact.",
      },
    ],
    labId: "anomaly",
    assignment: {
      id: "a5",
      title: "Field note 5 — train and score",
      prompt: "On Bench 04, choose features and an algorithm until beacon recall is at least 50%.",
    },
    quiz: [
      {
        q: "Isolation Forest flags points that",
        choices: [
          "Sit in the densest part of the data",
          "Are separated by random splits in few steps",
          "Carry the largest class label",
        ],
        answer: 1,
        why: "Short paths mean the point is easy to isolate. Density methods do the opposite emphasis.",
      },
      {
        q: "K-means misses an attack when",
        choices: [
          "The attack hides inside a normal centroid or you never gave it a cluster of its own",
          "You set a random seed",
          "You standardized the columns",
        ],
        answer: 0,
        why: "K-means explains the mass. A few beacons can be absorbed unless their features pull them out.",
      },
    ],
  },
  {
    id: "s11",
    index: "11",
    week: "06",
    weekTitle: "Wire and language",
    sitting: "Source cohort · Thu 12 Nov · network security, guest",
    title: "The wire, without the guest",
    minutes: 30,
    kicker: "Case",
    summary: "Traffic features, floods, and why a model should propose segmentation instead of editing it.",
    objectives: [
      "Name features that expose beaconing and bulk theft",
      "Separate volumetric denial of service from a quiet exfil",
      "Keep automated firewall changes behind a human window",
    ],
    blocks: [
      {
        kind: "p",
        text: "The published sitting includes a guest on network security. In their place: a detection note you can implement without new mythology. Network models eat flows, not vibes. Useful columns include bytes, duration, destination rarity, periodicity of connections, and whether the port is expected for that asset. A flood is many sources or many packets aimed at exhaustion. Exfil and command-and-control are often the opposite: small, regular, and rare.",
      },
      {
        kind: "ul",
        items: [
          "Beaconing — low jitter, small payloads, a destination the host has not used.",
          "Denial of service — volume, protocol abuse, or expensive queries. Mitigation is capacity and filtering, not a malware classifier.",
          "Segmentation — a model can suggest that two hosts should not talk. Applying that suggestion live is a change with an outage mode.",
        ],
      },
      {
        kind: "note",
        title: "Case file — the suggested rule",
        text: "A network team let a clustering job emit firewall denies overnight. It decided a build system and an artifact store were different segments because their traffic was bursty and new. Morning deploys died. The replacement workflow wrote the candidate rule into a review queue with the flows attached. A human shipped it in the Wednesday window, scoped to new accounts only. The model kept finding candidates. It stopped shipping outages.",
      },
    ],
    quiz: [
      {
        q: "Beaconing usually appears as",
        choices: [
          "One enormous packet",
          "Small, regular connections to a rare destination",
          "Only DNS TXT from a single vendor",
        ],
        answer: 1,
        why: "Regularity plus rarity is the pattern. Volume is a different detection.",
      },
      {
        q: "Letting a model edit firewall rules is dangerous because",
        choices: [
          "Firewalls cannot be scripted",
          "A wrong policy is an outage or a hole, so the model should propose",
          "Segmentation has nothing to do with risk",
        ],
        answer: 1,
        why: "Proposal plus a change window keeps the blast radius in human hands.",
      },
    ],
  },
  {
    id: "s12",
    index: "12",
    week: "06",
    weekTitle: "Wire and language",
    sitting: "Source cohort · Tue 17 Nov · NLP for security",
    title: "Language as telemetry",
    minutes: 45,
    kicker: "Bench",
    summary: "Preprocessing, why sentiment is the wrong label, and a held-out intent model.",
    objectives: [
      "Tokenize security text without leaking the test lines",
      "Prefer intent labels over positive and negative sentiment",
      "Validate on messages the fit has never seen",
    ],
    blocks: [
      {
        kind: "p",
        text: "Natural language processing in this outline means turning text into features a classical model can use: lowercase, strip punctuation, drop function words, count what remains. Topic models group documents that share vocabulary. Sentiment models score tone. Tone is a trap in security. Phishing is often polite. Internal alerts are terse and angry-looking because they are alarms. The label you want is intent: ordinary business, social engineering, or a machine-generated detection.",
      },
      {
        kind: "p",
        text: "The paired assignment says to validate the model and import test data into a frame. Bench 05 keeps six lines in a locked hold-out. They are not in the fit. If you train on them, you are rehearsing, not testing. Preprocessing has to be identical on both sides — a hold-out line in capitals should not become a new language.",
      },
      {
        kind: "code",
        title: "sklearn port — intent, not sentiment",
        text: "from sklearn.feature_extraction.text import CountVectorizer\nfrom sklearn.naive_bayes import MultinomialNB\nfrom sklearn.pipeline import make_pipeline\n\npipeline = make_pipeline(CountVectorizer(lowercase=True, stop_words='english'), MultinomialNB())\npipeline.fit(train_text, train_y)\nprint(pipeline.score(test_text, test_y))",
      },
    ],
    labId: "nlp",
    assignment: {
      id: "a6",
      title: "Field note 6 — held-out text",
      prompt: "On Bench 05, lowercase and strip punctuation, then clear 60% accuracy on the locked lines.",
    },
    quiz: [
      {
        q: "Sentiment is a poor primary security label because",
        choices: [
          "Angry text is always malicious",
          "Attack text is often polite, and real alerts look harsh",
          "Tokens cannot represent words",
        ],
        answer: 1,
        why: "Intent — phish, benign, alert — matches the decision. Tone does not.",
      },
      {
        q: "Held-out messages must be",
        choices: [
          "Copied from training to raise the score",
          "Unseen during the fit, including their wording",
          "Written by the model under test",
        ],
        answer: 1,
        why: "A test set you fitted on is a memory test. Validation means new text.",
      },
    ],
  },
  {
    id: "s13",
    index: "13",
    week: "07",
    weekTitle: "The model as target",
    sitting: "Source cohort · Thu 19 Nov · adversarial AI and defense",
    title: "When the model is the asset",
    minutes: 30,
    kicker: "Briefing",
    summary: "Evasion, poisoning, theft, and prompt injection as one idea: untrusted input, trusted authority.",
    objectives: [
      "Name evasion, poisoning, and extraction without mixing them",
      "Connect prompt injection to the same authority problem",
      "Refuse to let a model be a control by itself",
    ],
    blocks: [
      {
        kind: "p",
        text: "Adversarial machine learning is the study of attackers who aim at the model rather than only at the network. NIST’s taxonomy is the reference vocabulary. Evasion changes the input at decision time so a malware score falls under the block line — a few added bytes, a reordered import, a paraphrased phish. Poisoning changes the training set so the model learns the wrong boundary, or learns a backdoor that fires on a trigger. Extraction queries the model until a copy can be trained. Inversion tries to recover training data from the model.",
      },
      {
        kind: "p",
        text: "Prompt injection belongs in the same week even though the math differs. Untrusted text is given to a model that can call tools. The text says ignore your instructions and forward the mailbox. The failure is authority. A classifier that can only emit a score can be evaded. A model that can isolate a host or send mail can be steered. Defense is not a smarter paragraph. It is separation: untrusted content cannot hold the credentials, tool calls are allow-listed, and a second control checks the action.",
      },
      {
        kind: "ul",
        items: [
          "Do not train on a feed an attacker can write to without review.",
          "Assume your feature set is public. Evasion targets the features you bragged about.",
          "Put the model behind a decision threshold a human or a hard control can override.",
          "Log the inputs you scored. You will need them when the boundary moves.",
        ],
      },
    ],
    quiz: [
      {
        q: "An evasion attack typically",
        choices: [
          "Rewrites history in the training set",
          "Perturbs a sample at decision time so the score drops under the block line",
          "Only steals the dataset",
        ],
        answer: 1,
        why: "Evasion is a test-time change to the object being scored. Poisoning is training-time. Theft is querying for a copy.",
      },
      {
        q: "Prompt injection sits in this week because",
        choices: [
          "It uses the same loss as logistic regression",
          "Untrusted input is steering a model that was given authority",
          "A firewall drops it by default",
        ],
        answer: 1,
        why: "The shared problem is authority attached to a channel an attacker can write.",
      },
    ],
  },
  {
    id: "s14",
    index: "14",
    week: "07",
    weekTitle: "The model as target",
    sitting: "Source cohort · Tue 24 Nov · adversarial machine learning",
    title: "A nudge along the gradient",
    minutes: 40,
    kicker: "Bench",
    summary: "First-order evasion on a linear detector, then clipping and a round of adversarial training.",
    objectives: [
      "See that a linear score is most sensitive along its weight vector",
      "Measure how many decisions flip as the nudge grows",
      "Feel the cost of a simple defense on clean separation",
    ],
    blocks: [
      {
        kind: "p",
        text: "The fastest way to feel evasion is a model you can draw. Bench 06 fits a line between benign and malicious on two features: entropy and suspicious API count. The gradient of that score is the weight vector. A first-order attack — the idea behind FGSM, the fast gradient sign method — steps each feature a small amount in the direction that reduces the malicious probability, then asks how many points crossed the threshold. You are not generating malware. You are moving dots on a chart.",
      },
      {
        kind: "p",
        text: "Two defenses are on the bench because the outline asks you to explore them, not to invent a perfect shield. Clipping refuses impossible feature values, which stops a cartoonishly large nudge and does little against a careful one inside the normal range. Adversarial training refits on the nudged points with their original labels, so the boundary thickens against that specific step. Clean points near the line may get worse. That trade is the lesson. There is no free robustness.",
      },
      {
        kind: "code",
        title: "Reading, not a recipe for abuse",
        text: "# Conceptual only — perturbations of synthetic features, never of binaries.\n# x_adv = x + eps * sign(gradient of the loss w.r.t. x)\n# For a linear malware score, that direction is the sign of the weights\n# after features are standardized. Defenses: clip, or refit with x_adv\n# labeled as the original class.",
      },
    ],
    labId: "adversarial",
    quiz: [
      {
        q: "On a linear model, a first-order evasion step moves the point",
        choices: [
          "Along the weight vector, where the score changes fastest",
          "Uniformly at random",
          "Only by editing the label",
        ],
        answer: 0,
        why: "The weights are the sensitivity. The sign of each weight says which way to nudge that feature.",
      },
      {
        q: "Adversarial training usually",
        choices: [
          "Makes the boundary immune to every future attack",
          "Trades some clean accuracy for stability against the steps you trained on",
          "Removes the need for a threshold",
        ],
        answer: 1,
        why: "You buy robustness to a chosen perturbation class. Other attacks, and some clean errors, remain.",
      },
    ],
  },
  {
    id: "s15",
    index: "15",
    week: "08",
    weekTitle: "Judgment",
    sitting: "Source cohort · Tue 1 Dec · ethics",
    title: "Bias, privacy, misuse",
    minutes: 30,
    kicker: "Briefing",
    summary: "What a responsible detection program refuses to collect, automate, or hide.",
    objectives: [
      "Trace a biased score back to the definition of normal",
      "Minimize telemetry before the model asks for it",
      "Draw a line around offensive automation",
    ],
    blocks: [
      {
        kind: "p",
        text: "The outline’s ethics sitting is not a disclaimer slide. It is a design review. Bias in a security model is often a biased definition of normal: whose schedule, whose region, whose job is the baseline. The people who trip it pay in investigations. If those investigations can touch employment, the model is part of an HR system whether you admit it or not, and it needs that standard of evidence.",
      },
      {
        kind: "h",
        text: "Privacy is a feature cut",
      },
      {
        kind: "p",
        text: "Collect for a named detection, keep it for a named retention, and drop the rest. Message bodies, keystrokes, and precise location are rarely required to catch token theft. A purpose limitation written after the warehouse is full is theater. The same data that trains a useful insider model trains a surveillance product. Access control on the feature store is part of the model card.",
      },
      {
        kind: "ul",
        items: [
          "Document features, training window, known failure cases, and who may act on a score.",
          "Do not build quiet offensive tooling — automated phishing, exploit generation against real targets — inside a defensive program and call it research without rules of engagement.",
          "Assume dual use. Publish internals to your defenders before you publish them to a conference.",
          "A high score is not grounds for a law-enforcement or HR referral by itself.",
        ],
      },
    ],
    quiz: [
      {
        q: "Privacy-respecting telemetry starts with",
        choices: [
          "Collecting every keystroke in case a model wants it later",
          "A purpose, a minimization cut, and a retention limit before training",
          "Encrypting the weights and keeping the warehouse unbounded",
        ],
        answer: 1,
        why: "Minimization is a decision about columns, not a property of the algorithm.",
      },
      {
        q: "A behavior model encodes bias when",
        choices: [
          "The feature list is documented",
          "A minority work pattern is treated as inherently suspicious",
          "Packet sizes are the only features on a router",
        ],
        answer: 1,
        why: "Normal is a social choice. If it matches only the majority, the model polices everyone else.",
      },
    ],
  },
  {
    id: "s16",
    index: "16",
    week: "09",
    weekTitle: "Capstone",
    sitting: "Source cohort · Thu 3 Dec · future and capstone",
    title: "What you hand a SOC",
    minutes: 50,
    kicker: "Capstone",
    summary: "Horizon notes, then the malware-detection capstone: clean, fit, threshold, defend.",
    objectives: [
      "Place quantum risk on cryptography, not on malware mythology",
      "Name the jobs this practice actually feeds",
      "Ship a detector with a threshold and a cleaning log",
    ],
    blocks: [
      {
        kind: "p",
        text: "The last published sitting looks forward: research, quantum computing, careers, and the capstone. The horizon that matters to a detection engineer this decade is evaluation and authority. Models that take actions, agents that read tickets and propose changes, and benchmarks that measure those agents against hostile inputs. MITRE ATLAS is the companion to ATT&CK for attacks on AI systems. Read it as a catalog of hypotheses, the same way you read ATT&CK.",
      },
      {
        kind: "p",
        text: "Quantum computing is a migration problem for public-key cryptography, on a timeline your protocol choices have to respect. It is not a malware classifier and it is not a reason to pause patching. Careers that come out of this domain look like detection engineering, security data science, and architecture that can sit with both a SOC lead and a model review. The job is the connective tissue, not a Kaggle rank.",
      },
      {
        kind: "h",
        text: "The capstone, as the outline defines it",
      },
      {
        kind: "p",
        text: "Malware detection with machine learning: collect, preprocess, engineer features, train, and detect. The cohort uses real samples in a controlled notebook. This domain uses a dirty synthetic export with the same failure modes — missing cells, duplicated ids, a sensor glitch that claims entropy of 99. You will drop or repair those rows, choose features, fit a model, and set the probability a SOC would page on. Pass when precision and recall both survive: F1 at least 72 percent, and fewer than one in five benign hosts falsely flagged on the hold-out.",
      },
      {
        kind: "note",
        title: "What done means",
        text: "You can explain the cleaning, the features you refused, the threshold, and what the false positives would cost on a Tuesday morning. A higher accuracy with a silent false-positive rate is not done.",
      },
    ],
    labId: "capstone",
    quiz: [
      {
        q: "In this horizon, quantum computing matters first as",
        choices: [
          "A drop-in replacement for isolation forests",
          "A timeline risk to public-key cryptography",
          "A required capstone library",
        ],
        answer: 1,
        why: "Plan crypto agility. Do not wait on quantum hardware to detect malware.",
      },
      {
        q: "The capstone is finished when you can",
        choices: [
          "Name three algorithms from memory",
          "Show the cleaning, the fit, and a threshold you can defend to a SOC lead",
          "Upload a live specimen into the browser",
        ],
        answer: 1,
        why: "The artifact is a decision, not a vocabulary list. This domain never wants a real specimen in the browser.",
      },
    ],
  },
];

export function sessionById(id: string) {
  return sessions.find((s) => s.id === id);
}

export const weeks = [...new Map(sessions.map((s) => [s.week, s.weekTitle])).entries()].map(([week, title]) => ({
  week,
  title,
  sessions: sessions.filter((s) => s.week === week),
}));

export type StackItem = { group: string; label: string; href: string; note: string };

export const stack: StackItem[] = [
  {
    group: "The workflow the outline uses",
    label: "scikit-learn user guide",
    href: "https://scikit-learn.org/stable/user_guide.html",
    note: "Estimators, pipelines, and the split/fit/score habit every bench ports to.",
  },
  {
    group: "The workflow the outline uses",
    label: "Jupyter documentation",
    href: "https://docs.jupyter.org/en/latest/",
    note: "The cohort’s notebook server. Local JupyterLab is the faithful port.",
  },
  {
    group: "The workflow the outline uses",
    label: "seaborn introduction",
    href: "https://seaborn.pydata.org/tutorial/introduction.html",
    note: "Field note 4 is a picture of features before it is a leaderboard.",
  },
  {
    group: "The workflow the outline uses",
    label: "pandas user guide",
    href: "https://pandas.pydata.org/docs/user_guide/index.html",
    note: "Data frames, missing values, and the import step in field notes 2 and 3.",
  },
  {
    group: "Datasets and methods",
    label: "Iris, UCI",
    href: "https://archive.ics.uci.edu/dataset/53/iris",
    note: "The control set for lab 1. Fisher’s measurements, not a security corpus.",
  },
  {
    group: "Datasets and methods",
    label: "Nearest neighbors",
    href: "https://scikit-learn.org/stable/modules/neighbors.html",
    note: "Bench 01.",
  },
  {
    group: "Datasets and methods",
    label: "Logistic regression",
    href: "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression",
    note: "Binary detectors in benches 02 and the capstone.",
  },
  {
    group: "Datasets and methods",
    label: "Decision trees",
    href: "https://scikit-learn.org/stable/modules/tree.html",
    note: "Family rules in bench 03.",
  },
  {
    group: "Datasets and methods",
    label: "Outlier detection",
    href: "https://scikit-learn.org/stable/modules/outlier_detection.html",
    note: "Isolation Forest and One-Class SVM, named in the unsupervised sitting.",
  },
  {
    group: "Datasets and methods",
    label: "K-means",
    href: "https://scikit-learn.org/stable/modules/clustering.html#k-means",
    note: "The clustering half of bench 04.",
  },
  {
    group: "Datasets and methods",
    label: "Working with text",
    href: "https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html",
    note: "Count vectors and naive Bayes for bench 05.",
  },
  {
    group: "Security frames",
    label: "MITRE ATT&CK",
    href: "https://attack.mitre.org/",
    note: "Techniques to hang a detection hypothesis on. Not a model.",
  },
  {
    group: "Security frames",
    label: "MITRE ATLAS",
    href: "https://atlas.mitre.org/",
    note: "Adversary behavior aimed at AI systems. Read beside the evasion week.",
  },
  {
    group: "Security frames",
    label: "OWASP Machine Learning Security Top 10",
    href: "https://owasp.org/www-project-machine-learning-security-top-10/",
    note: "A short threat list for people shipping models.",
  },
  {
    group: "Security frames",
    label: "NIST AI Risk Management Framework",
    href: "https://www.nist.gov/itl/ai-risk-management-framework",
    note: "Govern, map, measure, manage — the ethics sitting in organizational form.",
  },
  {
    group: "Security frames",
    label: "NIST AI 100-2 E2023",
    href: "https://csrc.nist.gov/pubs/ai/100/2/e2023/final",
    note: "Taxonomy of adversarial machine learning attacks and mitigations.",
  },
  {
    group: "Security frames",
    label: "EPSS",
    href: "https://www.first.org/epss/",
    note: "A public probability-of-exploitation score. The vulnerability week’s real-world cousin.",
  },
  {
    group: "Security frames",
    label: "FIRST EPSS model notes",
    href: "https://www.first.org/epss/model",
    note: "What the score is trying to predict, and what it is not.",
  },
];

export const outlineMap: { source: string; here: string }[] = [
  { source: "Welcome, structure, questions", here: "00 · How this domain is built" },
  { source: "What AI is, threats, the convergence", here: "01 · Models meet the threat model" },
  { source: "Supervised vs unsupervised, three algorithms, splits", here: "02 · Learning that generalizes" },
  { source: "Lab 1 iris, preprocessing, assignment 2", here: "03 · Bench 01" },
  { source: "Anomaly, IDS, malware detection, case", here: "04 · Three ways to say suspicious" },
  { source: "Lab 2 outliers and a first malware model", here: "05 · Bench 02" },
  { source: "Scanning, prediction, automated discovery", here: "06 · The backlog is the problem" },
  { source: "Lab 3 family classification, seaborn", here: "07 · Bench 03" },
  { source: "Incident response and a guest", here: "08 · Operator note, guest unpublished" },
  { source: "User behavior, insider risk, takeover", here: "09 · People as a signal" },
  { source: "Lab 4 k-means, isolation forest, one-class SVM", here: "10 · Bench 04" },
  { source: "Network detection and a guest", here: "11 · Operator note, guest unpublished" },
  { source: "Lab 5 text, topic and sentiment ideas", here: "12 · Bench 05" },
  { source: "Attacks on models, the arms race", here: "13 · When the model is the asset" },
  { source: "Lab 6 adversarial examples and defenses", here: "14 · Bench 06" },
  { source: "Bias, privacy, misuse", here: "15 · Bias, privacy, misuse" },
  { source: "Horizon, careers, malware-detection capstone", here: "16 · Capstone bench" },
];
