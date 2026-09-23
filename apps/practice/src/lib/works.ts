export const runSteps = [
  { title: "Token", text: "The model scores the next piece of text. It does not open your database unless you wrote that call." },
  { title: "Budget", text: "The context window is a length limit. A long prompt that crowds out the passage will answer from habit." },
  { title: "Source", text: "If the sentence is fluent and the passage does not support it, the sentence is still wrong." },
  { title: "Measure", text: "Hold out a set you do not tune on. Precision and recall are the exam, not a feeling that it sounds right." },
];

export const shelves = [
  {
    id: "ocw",
    title: "MIT 6.7960",
    href: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/video_galleries/lecture-videos/",
    note: "Their lecture videos stay on OpenCourseWare. This run is the order, in our words.",
    steps: [
      { title: "Train", text: "Lecture 2 is how a net is trained: a loss, a step, and a repeat. Watch theirs. Then say the loss in one sentence." },
      { title: "Transformers", text: "Lecture 8 is the architecture. Attention mixes tokens. It does not open a database." },
      { title: "Language", text: "Lecture 21 is language models. A fluent sentence can still be unsupported." },
    ],
  },
  {
    id: "hf",
    title: "Hugging Face",
    href: "https://huggingface.co/learn/llm-course/chapter1/1",
    note: "Their LLM course, from the introduction. We do not paste the chapters here.",
    steps: [
      { title: "Introduction", text: "Chapter 1 starts at what a transformer computes. Read it on their site, then sit the practice exam on this page." },
      { title: "Language", text: "The following page is natural language processing and large language models. The exam below is still ours." },
    ],
  },
];

export const practiceExam = [
  {
    q: "Without a retrieval step, a language model",
    choices: ["predicts a next token from its training", "queries your tables by default", "signs a ledger transaction", "issues a certificate"],
    answer: 0,
    why: "Retrieval is something you add. Fluency is not a lookup.",
  },
  {
    q: "Retrieval-augmented generation fails when",
    choices: ["the passage is irrelevant and the answer is still fluent", "you show the passage beside the answer", "the index is empty and you refuse", "you cite the paper"],
    answer: 0,
    why: "The pattern only helps if the reader can see a relevant passage.",
  },
  {
    q: "A set you tune prompts on is",
    choices: ["no longer a test", "a stronger test", "the context window", "a certificate"],
    answer: 0,
    why: "Touch it once. After that it is training.",
  },
  {
    q: "This practice exam is",
    choices: ["original to Interstitium, not a vendor certificate", "issued by a business bootcamp", "a campus admission test", "an Oracle exam"],
    answer: 0,
    why: "Passing it records a score on this device. It does not grant anyone else's credential.",
  },
];

export const passages = [
  { id: "a", text: "A diffusion model is trained to reverse a noise process, one step at a time." },
  { id: "b", text: "A projection in a column store is a physical design for how rows sit on disk." },
  { id: "c", text: "A pipeline is green only when a failed test can turn it red." },
  { id: "d", text: "A certificate of attendance means you were present, not that you passed a proficiency exam." },
];

export const retrievalQuery = "What is a model trained to reverse, one step at a time?";
export const retrievalAnswer = "a";

export type EvalRow = { p: number; y: 0 | 1 };
export const evalRows: EvalRow[] = [
  { p: 0.92, y: 1 },
  { p: 0.81, y: 1 },
  { p: 0.7, y: 0 },
  { p: 0.55, y: 1 },
  { p: 0.2, y: 0 },
  { p: 0.1, y: 0 },
];

export function evalAt(threshold: number) {
  let tp = 0;
  let fp = 0;
  let fn = 0;
  for (const row of evalRows) {
    const pred = row.p >= threshold;
    if (pred && row.y === 1) tp += 1;
    else if (pred && row.y === 0) fp += 1;
    else if (!pred && row.y === 1) fn += 1;
  }
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  return { tp, fp, fn, precision, recall, passed: precision >= 0.6 && recall >= 0.66 };
}

export const academyPhases = [
  {
    name: "Build",
    text: "Name one thing and the artifact someone can run. A campus term is not required.",
    steps: [
      { title: "Name", text: "One obsession. If you cannot say it in a sentence, it is still a pile of interests." },
      { title: "Artifact", text: "Something another person can run: a page, a query, a detector, a proof. Not a mood." },
    ],
    check: {
      q: "The build phase is done when",
      choices: ["someone else can run the artifact", "a city has been booked", "a certificate arrived", "the calendar says April"],
      answer: 0,
      why: "The academy method is the thing in the world, not the term.",
    },
  },
  {
    name: "Field",
    text: "Leave the desk. The other school sends people abroad in May. Here the field is whoever has to use the thing.",
    steps: [
      { title: "Who", text: "Name the person who uses it. If that person is only you, say so." },
      { title: "Friction", text: "Write the sentence they used when it failed. Their words, not a slogan." },
    ],
    check: {
      q: "Field work means",
      choices: ["a real user, not a booked trip", "a required month abroad", "a sponsor panel", "an admission essay"],
      answer: 0,
      why: "We keep the contact with the work. We do not sell the travel.",
    },
  },
  {
    name: "Return",
    text: "Bring it back. Say how it fails in the open, and what you would hand the next person.",
    steps: [
      { title: "Fail", text: "A failure you can demonstrate beats a failure you describe." },
      { title: "Hand-off", text: "The next person should start without you in the room. That note is the course." },
    ],
    check: {
      q: "You return when",
      choices: ["the failure is visible and the next person has a note", "the season ends", "a mentor from their campus replies", "the video library is finished"],
      answer: 0,
      why: "Return is a hand-off, not a date.",
    },
  },
];
