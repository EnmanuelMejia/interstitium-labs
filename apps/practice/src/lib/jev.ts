export type Noul = { id: string; kind: "noul"; instructions: string };
export type Choice = { id: string; kind: "choice"; instructions: string; options: string[] };
export type Score = { id: string; kind: "score"; instructions: string };
export type Question = Noul | Choice | Score;

export type Answer =
  | { id: string; kind: "noul"; yes: number }
  | { id: string; kind: "choice"; option: string; yes: number }
  | { id: string; kind: "score"; value: number };

const refuse = /\b(exploit|malware|payload|ransomware|exam dump|stolen credentials?|reverse shell)\b/i;
const readingsQuery = /\bselect\b[\s\S]{0,500}\bfrom\s+readings\b/i;

function words(text: string) {
  return text.toLowerCase().match(/[a-z0-9]+/g) ?? [];
}

function overlap(state: string, cue: string) {
  const hay = new Set(words(state));
  const needles = words(cue).filter((word) => word.length > 2);
  if (!needles.length) return 0;
  const hits = needles.filter((word) => hay.has(word)).length;
  return hits / needles.length;
}

function noul(state: string, question: Noul): number {
  if (question.id === "refuse" || /exploit|malware|dump/i.test(question.instructions)) return refuse.test(state) ? 0.95 : 0.05;
  if (question.id === "sql" || /select against the readings/i.test(question.instructions)) return readingsQuery.test(state) ? 0.95 : 0.05;
  return overlap(state, question.instructions);
}

export function jev(state: string, questions: Question[]): Answer[] {
  return questions.map((question) => {
    if (question.kind === "noul") return { id: question.id, kind: "noul", yes: noul(state, question) };
    if (question.kind === "score") {
      const found = state.match(/\b(0(?:\.\d+)?|1(?:\.0+)?)\b/);
      return { id: question.id, kind: "score", value: found ? Number(found[1]) : overlap(state, question.instructions) };
    }
    const ranked = question.options.map((option) => ({ option, yes: overlap(state, `${question.instructions} ${option}`) }));
    ranked.sort((a, b) => b.yes - a.yes);
    return { id: question.id, kind: "choice", option: ranked[0]?.option ?? question.options[0], yes: ranked[0]?.yes ?? 0 };
  });
}

export function routeTurn(line: string): "refuse" | "remember" | "goal" | "sql" | "teach" | "assist" {
  const answers = jev(line, [
    { id: "refuse", kind: "noul", instructions: "Ask for an exploit, malware, or an exam dump." },
    { id: "sql", kind: "noul", instructions: "A SELECT against the readings table." },
  ]);
  const refused = answers.find((answer) => answer.id === "refuse");
  const query = answers.find((answer) => answer.id === "sql");
  if (refused?.kind === "noul" && refused.yes >= 0.5) return "refuse";
  if (/^(remember|forget)\b/i.test(line)) return "remember";
  if (/^(?:goal:|my goal is\b|add a goal\b)/i.test(line)) return "goal";
  if (query?.kind === "noul" && query.yes >= 0.5) return "sql";
  if (/^(what|why|how|explain|quiz)\b/i.test(line) || line.trim().endsWith("?")) return "teach";
  return "assist";
}

export function memoryFact(line: string) {
  return line.replace(/^(remember|forget)(?:\s+that)?\s+/i, "").trim().slice(0, 160);
}

export function goalFact(line: string) {
  return line.replace(/^(?:goal:\s*|my goal is\s+|add a goal\s+)/i, "").trim().slice(0, 160);
}

export function selectText(line: string) {
  const match = line.match(/\bselect\b[\s\S]*?\bfrom\s+readings\b[^;]*/i);
  return match ? match[0] : "";
}
