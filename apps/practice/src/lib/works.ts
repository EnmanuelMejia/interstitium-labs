export const runSteps = [
  { title: "Token", text: "The model scores the next piece of text. It does not open your database unless you wrote that call." },
  { title: "Budget", text: "The context window is a length limit. A long prompt that crowds out the passage will answer from habit." },
  { title: "Source", text: "If the sentence is fluent and the passage does not support it, the sentence is still wrong." },
  { title: "Measure", text: "Hold out a set you do not tune on. Precision and recall are the exam, not a feeling that it sounds right." },
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
    why: "The Lewis et al. pattern only helps if the reader can see a relevant passage.",
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
