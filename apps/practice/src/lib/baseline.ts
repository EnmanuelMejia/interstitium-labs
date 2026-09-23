export type MathItem = {
  id: string;
  b: number;
  topic: string;
  prompt: string;
  choices: string[];
  answer: number;
};

export const mathItems: MathItem[] = [
  { id: "m1", b: -1.6, topic: "arithmetic", prompt: "A service handles 240 requests in 60 seconds. What is the rate, in requests per second?", choices: ["4", "30", "180", "14400"], answer: 0 },
  { id: "m2", b: -1.4, topic: "arithmetic", prompt: "Three of twenty hosts are unhealthy. What fraction is unhealthy?", choices: ["3/20", "20/3", "3%", "17/20"], answer: 0 },
  { id: "m3", b: -1.2, topic: "arithmetic", prompt: "An error budget allows 10 failures. You have used 4. How many remain?", choices: ["6", "14", "40", "2.5"], answer: 0 },
  { id: "m4", b: -0.8, topic: "algebra", prompt: "If 2x + 6 = 18, what is x?", choices: ["6", "12", "9", "3"], answer: 0 },
  { id: "m5", b: -0.6, topic: "algebra", prompt: "A bill is p plus 10%. Which expression is the total?", choices: ["1.1p", "p + 10", "p/10", "10p"], answer: 0 },
  { id: "m6", b: -0.4, topic: "rates", prompt: "Start at 10 ms. Double it three times. What do you have?", choices: ["80 ms", "30 ms", "40 ms", "13 ms"], answer: 0 },
  { id: "m7", b: 0, topic: "rates", prompt: "p99 is 400 ms and the mean is 40 ms. What is the responsible reading?", choices: ["The tail is an order of magnitude slower than the mean", "The mean is the user experience", "p99 must be a bug because it is larger", "They measure the same requests"], answer: 0 },
  { id: "m8", b: 0.2, topic: "logs", prompt: "log10(1000) equals", choices: ["3", "10", "100", "1"], answer: 0 },
  { id: "m9", b: 0.4, topic: "logs", prompt: "A metric moves from 100 to 1000. In log10 units, the change is", choices: ["1", "10", "900", "3"], answer: 0 },
  { id: "m10", b: 0.6, topic: "probability", prompt: "A fair check fails independently with probability 0.1 twice in a row. The probability both fail is", choices: ["0.01", "0.2", "0.1", "0.5"], answer: 0 },
  { id: "m11", b: 0.8, topic: "probability", prompt: "You page on a positive. Precision is true positives over", choices: ["all positives you paged", "all real incidents", "all hosts", "the false negatives"], answer: 0 },
  { id: "m12", b: 1.0, topic: "probability", prompt: "A 0.1% error rate on 2,000,000 requests is how many errors?", choices: ["2000", "200", "20", "2"], answer: 0 },
  { id: "m13", b: 1.3, topic: "models", prompt: "A hold-out set that you tune on is no longer", choices: ["a test", "a sample", "numeric", "a feature"], answer: 0 },
  { id: "m14", b: 1.5, topic: "models", prompt: "Standard deviation of a constant column is", choices: ["0", "1", "the mean", "undefined only for integers"], answer: 0 },
  { id: "m15", b: 1.7, topic: "tails", prompt: "An error budget of 0.1% over 30 days of 1,000,000 requests a day allows how many errors in the month?", choices: ["30000", "3000", "1000", "300"], answer: 0 },
  { id: "m16", b: 1.9, topic: "tails", prompt: "If recall is 0.5 and precision is 1, you are", choices: ["missing half the real cases and paging no false ones", "paging twice as often as you should", "perfect", "unable to compute F1"], answer: 0 },
];

export type Band = "numerals" | "rates" | "models" | "tails";

export function bandOf(theta: number): Band {
  if (theta < -0.6) return "numerals";
  if (theta < 0.3) return "rates";
  if (theta < 1.1) return "models";
  return "tails";
}

export const bandCopy: Record<Band, string> = {
  numerals: "Start on counts, fractions, and rates. The ops-math path is the next reading, not a harder exam.",
  rates: "Rates and percentages are reliable. Log scales and tails are the fringe.",
  models: "You can read a metric and a probability. The next gap is the tail and the hold-out.",
  tails: "The baseline sits in the tail. Use it on a real budget, not as a trophy.",
};

export function nextItem(theta: number, used: string[]): MathItem | null {
  const open = mathItems.filter((item) => !used.includes(item.id));
  if (!open.length) return null;
  return open.reduce((best, item) => (Math.abs(item.b - theta) < Math.abs(best.b - theta) ? item : best));
}

export function stepTheta(theta: number, correct: boolean): number {
  const next = theta + (correct ? 0.45 : -0.45);
  return Math.max(-2, Math.min(2, next));
}

export const BASELINE_LENGTH = 8;
