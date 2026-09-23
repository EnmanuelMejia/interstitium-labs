/** Small, deterministic teaching implementations. Not a substitute for scikit-learn. */

export type Rng = () => number;

export function mulberry32(seed: number): Rng {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function clamp(n: number, lo: number, hi: number) {
  return Math.max(lo, Math.min(hi, n));
}

export function mean(xs: number[]) {
  if (!xs.length) return 0;
  return xs.reduce((s, v) => s + v, 0) / xs.length;
}

export function stdev(xs: number[]) {
  if (xs.length < 2) return 0;
  const m = mean(xs);
  const v = xs.reduce((s, x) => s + (x - m) ** 2, 0) / xs.length;
  return Math.sqrt(v);
}

export function standardize(rows: number[][]) {
  if (!rows.length) return { xs: [] as number[][], mean: [] as number[], std: [] as number[] };
  const d = rows[0].length;
  const mu = Array.from({ length: d }, (_, j) => mean(rows.map((r) => r[j])));
  const sd = Array.from({ length: d }, (_, j) => stdev(rows.map((r) => r[j])) || 1);
  const xs = rows.map((r) => r.map((v, j) => (v - mu[j]) / sd[j]));
  return { xs, mean: mu, std: sd };
}

export function applyScale(row: number[], mu: number[], sd: number[]) {
  return row.map((v, j) => (v - mu[j]) / (sd[j] || 1));
}

export function invertScale(row: number[], mu: number[], sd: number[]) {
  return row.map((v, j) => v * (sd[j] || 1) + mu[j]);
}

export function shuffle<T>(rows: T[], rng: Rng): T[] {
  const a = rows.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export function splitRows<T>(rows: T[], testRatio: number, seed: number) {
  const shuffled = shuffle(rows, mulberry32(seed));
  const nTest = clamp(Math.round(shuffled.length * testRatio), 1, Math.max(1, shuffled.length - 1));
  return { test: shuffled.slice(0, nTest), train: shuffled.slice(nTest) };
}

function sigmoid(z: number) {
  const c = clamp(z, -20, 20);
  return 1 / (1 + Math.exp(-c));
}

export type LinearModel = { w: number[]; b: number; mean: number[]; std: number[] };

export function fitLogistic(raw: number[][], y: number[], lr = 0.6, epochs = 420): LinearModel {
  const { xs, mean: mu, std: sd } = standardize(raw);
  const d = xs[0]?.length ?? 0;
  const w = Array(d).fill(0);
  let b = 0;
  const n = xs.length || 1;
  for (let e = 0; e < epochs; e++) {
    const gw = Array(d).fill(0);
    let gb = 0;
    for (let i = 0; i < xs.length; i++) {
      let z = b;
      for (let j = 0; j < d; j++) z += w[j] * xs[i][j];
      const err = sigmoid(z) - y[i];
      for (let j = 0; j < d; j++) gw[j] += err * xs[i][j];
      gb += err;
    }
    for (let j = 0; j < d; j++) w[j] -= (lr * gw[j]) / n;
    b -= (lr * gb) / n;
  }
  return { w, b, mean: mu, std: sd };
}

export function linearScore(model: LinearModel, raw: number[]) {
  const z = applyScale(raw, model.mean, model.std);
  let s = model.b;
  for (let j = 0; j < model.w.length; j++) s += model.w[j] * z[j];
  return s;
}

export function linearProba(model: LinearModel, raw: number[]) {
  return sigmoid(linearScore(model, raw));
}

export function knnPredict(
  trainX: number[][],
  trainY: string[],
  query: number[],
  k: number,
  scale = true,
) {
  const mu = scale ? standardize(trainX).mean : trainX[0].map(() => 0);
  const sd = scale ? standardize(trainX).std : trainX[0].map(() => 1);
  const xs = trainX.map((row) => applyScale(row, mu, sd));
  const q = applyScale(query, mu, sd);
  const ranked = xs
    .map((row, i) => {
      let dist = 0;
      for (let j = 0; j < row.length; j++) dist += (row[j] - q[j]) ** 2;
      return { dist, y: trainY[i] };
    })
    .sort((a, b) => a.dist - b.dist)
    .slice(0, Math.max(1, k));
  const votes = new Map<string, number>();
  for (const r of ranked) votes.set(r.y, (votes.get(r.y) ?? 0) + 1);
  let best = ranked[0]?.y ?? "";
  let bestN = -1;
  for (const [label, n] of votes) {
    if (n > bestN) {
      best = label;
      bestN = n;
    }
  }
  return best;
}

export type Confusion = { labels: string[]; matrix: number[][]; accuracy: number };

export function confusion(yTrue: string[], yPred: string[]): Confusion {
  const labels = [...new Set([...yTrue, ...yPred])];
  const index = new Map(labels.map((l, i) => [l, i]));
  const matrix = labels.map(() => labels.map(() => 0));
  yTrue.forEach((t, i) => {
    matrix[index.get(t)!][index.get(yPred[i])!] += 1;
  });
  const correct = yTrue.reduce((s, t, i) => s + (t === yPred[i] ? 1 : 0), 0);
  return { labels, matrix, accuracy: yTrue.length ? correct / yTrue.length : 0 };
}

export function binaryScores(yTrue: number[], yProb: number[], threshold: number) {
  let tp = 0,
    fp = 0,
    tn = 0,
    fn = 0;
  yTrue.forEach((y, i) => {
    const pred = yProb[i] >= threshold ? 1 : 0;
    if (pred === 1 && y === 1) tp++;
    else if (pred === 1 && y === 0) fp++;
    else if (pred === 0 && y === 0) tn++;
    else fn++;
  });
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  const fpr = fp + tn ? fp / (fp + tn) : 0;
  const acc = (tp + tn) / Math.max(1, yTrue.length);
  return { tp, fp, tn, fn, precision, recall, f1, fpr, acc };
}

export function iqrFences(xs: number[]) {
  const s = xs.slice().sort((a, b) => a - b);
  const q = (p: number) => {
    if (!s.length) return 0;
    const i = (s.length - 1) * p;
    const lo = Math.floor(i);
    const hi = Math.ceil(i);
    return s[lo] * (1 - (i - lo)) + s[hi] * (i - lo);
  };
  const q1 = q(0.25);
  const q3 = q(0.75);
  const iqr = q3 - q1;
  return { q1, q3, lo: q1 - 1.5 * iqr, hi: q3 + 1.5 * iqr };
}

type TreeNode =
  | { leaf: true; label: string; n: number }
  | { leaf: false; feature: number; thr: number; left: TreeNode; right: TreeNode };

function gini(labels: string[]) {
  const counts = new Map<string, number>();
  for (const y of labels) counts.set(y, (counts.get(y) ?? 0) + 1);
  let s = 0;
  for (const c of counts.values()) {
    const p = c / labels.length;
    s += p * p;
  }
  return 1 - s;
}

function majority(labels: string[]) {
  const counts = new Map<string, number>();
  for (const y of labels) counts.set(y, (counts.get(y) ?? 0) + 1);
  let best = labels[0] ?? "";
  let n = -1;
  for (const [k, v] of counts) {
    if (v > n) {
      best = k;
      n = v;
    }
  }
  return best;
}

function buildTree(X: number[][], y: string[], depth: number, maxDepth: number): TreeNode {
  const pure = y.every((v) => v === y[0]);
  if (pure || depth >= maxDepth || y.length < 6) return { leaf: true, label: majority(y), n: y.length };
  const parent = gini(y);
  let bestGain = 0;
  let bestF = 0;
  let bestThr = 0;
  const d = X[0].length;
  for (let f = 0; f < d; f++) {
    const vals = [...new Set(X.map((r) => r[f]))].sort((a, b) => a - b);
    for (let i = 0; i < vals.length - 1; i++) {
      const thr = (vals[i] + vals[i + 1]) / 2;
      const leftY: string[] = [];
      const rightY: string[] = [];
      y.forEach((label, row) => (X[row][f] <= thr ? leftY : rightY).push(label));
      if (!leftY.length || !rightY.length) continue;
      const gain = parent - (leftY.length / y.length) * gini(leftY) - (rightY.length / y.length) * gini(rightY);
      if (gain > bestGain) {
        bestGain = gain;
        bestF = f;
        bestThr = thr;
      }
    }
  }
  if (bestGain <= 1e-6) return { leaf: true, label: majority(y), n: y.length };
  const lX: number[][] = [];
  const lY: string[] = [];
  const rX: number[][] = [];
  const rY: string[] = [];
  X.forEach((row, i) => {
    if (row[bestF] <= bestThr) {
      lX.push(row);
      lY.push(y[i]);
    } else {
      rX.push(row);
      rY.push(y[i]);
    }
  });
  return {
    leaf: false,
    feature: bestF,
    thr: bestThr,
    left: buildTree(lX, lY, depth + 1, maxDepth),
    right: buildTree(rX, rY, depth + 1, maxDepth),
  };
}

function predictTree(node: TreeNode, row: number[]): string {
  if (node.leaf) return node.label;
  return predictTree(row[node.feature] <= node.thr ? node.left : node.right, row);
}

export type Rule = { text: string };

function rulesOf(node: TreeNode, names: string[], prefix: string[], out: Rule[]) {
  if (node.leaf) {
    out.push({ text: `${prefix.join(" and ") || "all rows"} → ${node.label} (n=${node.n})` });
    return;
  }
  const name = names[node.feature] ?? `f${node.feature}`;
  rulesOf(node.left, names, [...prefix, `${name} ≤ ${node.thr.toFixed(2)}`], out);
  rulesOf(node.right, names, [...prefix, `${name} > ${node.thr.toFixed(2)}`], out);
}

export function fitTree(X: number[][], y: string[], names: string[], maxDepth = 3) {
  const tree = buildTree(X, y, 0, maxDepth);
  const rules: Rule[] = [];
  rulesOf(tree, names, [], rules);
  return { predict: (row: number[]) => predictTree(tree, row), rules };
}

export function univariateGain(X: number[][], y: string[]) {
  const parent = gini(y);
  return X[0].map((_, f) => {
    const vals = X.map((r) => r[f]).sort((a, b) => a - b);
    const mid = vals[Math.floor(vals.length / 2)] ?? 0;
    const left: string[] = [];
    const right: string[] = [];
    y.forEach((label, i) => (X[i][f] <= mid ? left : right).push(label));
    if (!left.length || !right.length) return 0;
    return parent - (left.length / y.length) * gini(left) - (right.length / y.length) * gini(right);
  });
}

type IsoNode = { leaf: true; size: number } | { leaf: false; feature: number; split: number; left: IsoNode; right: IsoNode };

function cFactor(n: number) {
  if (n <= 1) return 0;
  if (n === 2) return 1;
  const H = Math.log(n - 1) + 0.5772156649;
  return 2 * H - (2 * (n - 1)) / n;
}

function buildIso(rows: number[][], depth: number, maxDepth: number, rng: Rng): IsoNode {
  if (rows.length <= 1 || depth >= maxDepth) return { leaf: true, size: rows.length };
  const f = Math.floor(rng() * rows[0].length);
  let min = Infinity;
  let max = -Infinity;
  for (const r of rows) {
    min = Math.min(min, r[f]);
    max = Math.max(max, r[f]);
  }
  if (!(max > min)) return { leaf: true, size: rows.length };
  const split = min + rng() * (max - min);
  const left = rows.filter((r) => r[f] < split);
  const right = rows.filter((r) => r[f] >= split);
  if (!left.length || !right.length) return { leaf: true, size: rows.length };
  return {
    leaf: false,
    feature: f,
    split,
    left: buildIso(left, depth + 1, maxDepth, rng),
    right: buildIso(right, depth + 1, maxDepth, rng),
  };
}

function isoPath(node: IsoNode, x: number[], depth: number): number {
  if (node.leaf) return depth + cFactor(node.size);
  return isoPath(x[node.feature] < node.split ? node.left : node.right, x, depth + 1);
}

export function isolationScores(raw: number[][], seed = 7, trees = 40) {
  if (raw.length < 8) return raw.map(() => 0);
  const { xs } = standardize(raw);
  const rng = mulberry32(seed);
  const maxDepth = Math.ceil(Math.log2(Math.max(2, Math.min(64, xs.length))));
  const sampleN = Math.min(64, xs.length);
  const forest: IsoNode[] = [];
  for (let t = 0; t < trees; t++) {
    const sample: number[][] = [];
    for (let i = 0; i < sampleN; i++) sample.push(xs[Math.floor(rng() * xs.length)]);
    forest.push(buildIso(sample, 0, maxDepth, rng));
  }
  const c = cFactor(sampleN) || 1;
  return xs.map((row) => {
    const h = mean(forest.map((node) => isoPath(node, row, 0)));
    return 2 ** (-h / c);
  });
}

export function kmeans(raw: number[][], k: number, seed = 3, iters = 24) {
  const { xs } = standardize(raw);
  const rng = mulberry32(seed);
  const centroids = shuffle(xs, rng).slice(0, k).map((r) => r.slice());
  let assign = xs.map(() => 0);
  for (let iter = 0; iter < iters; iter++) {
    assign = xs.map((row) => {
      let best = 0;
      let bestD = Infinity;
      centroids.forEach((c, i) => {
        let d = 0;
        for (let j = 0; j < row.length; j++) d += (row[j] - c[j]) ** 2;
        if (d < bestD) {
          bestD = d;
          best = i;
        }
      });
      return best;
    });
    for (let i = 0; i < k; i++) {
      const members = xs.filter((_, row) => assign[row] === i);
      if (!members.length) continue;
      for (let j = 0; j < centroids[i].length; j++) centroids[i][j] = mean(members.map((m) => m[j]));
    }
  }
  const dist = xs.map((row, i) => {
    const c = centroids[assign[i]];
    let d = 0;
    for (let j = 0; j < row.length; j++) d += (row[j] - c[j]) ** 2;
    return Math.sqrt(d);
  });
  return { assign, dist };
}

export type NBModel = {
  classes: string[];
  logPrior: number[];
  tokenLog: Map<string, number[]>;
  denom: number[];
};

export function tokenize(text: string, opts: { lower: boolean; punct: boolean; stop: boolean }) {
  let t = opts.lower ? text.toLowerCase() : text;
  if (opts.punct) t = t.replace(/[^a-zA-Z0-9\s]/g, " ");
  const stops = new Set(
    "a an the to of in on for is at by we you your our it be this that from with and or as if will not".split(" "),
  );
  return t
    .split(/\s+/)
    .map((w) => w.trim())
    .filter((w) => w.length > 1 && (!opts.stop || !stops.has(w.toLowerCase())));
}

export function fitNB(docs: string[][], labels: string[]): NBModel {
  const classes = [...new Set(labels)];
  const idx = new Map(classes.map((c, i) => [c, i]));
  const counts = classes.map(() => 0);
  labels.forEach((l) => counts[idx.get(l)!]++);
  const tokenCounts = new Map<string, number[]>();
  const totals = classes.map(() => 0);
  docs.forEach((tokens, i) => {
    const ci = idx.get(labels[i])!;
    const seen = new Set(tokens);
    for (const tok of seen) {
      if (!tokenCounts.has(tok)) tokenCounts.set(tok, classes.map(() => 0));
      tokenCounts.get(tok)![ci] += 1;
      totals[ci] += 1;
    }
  });
  const v = tokenCounts.size || 1;
  const tokenLog = new Map<string, number[]>();
  for (const [tok, arr] of tokenCounts) {
    tokenLog.set(
      tok,
      arr.map((c, i) => Math.log((c + 1) / (totals[i] + v))),
    );
  }
  const n = labels.length || 1;
  return {
    classes,
    logPrior: counts.map((c) => Math.log((c + 1) / (n + classes.length))),
    tokenLog,
    denom: totals.map((t) => Math.log(1 / (t + v))),
  };
}

export function predictNB(model: NBModel, tokens: string[]) {
  const scores = model.logPrior.slice();
  const unique = [...new Set(tokens)];
  for (const tok of unique) {
    const row = model.tokenLog.get(tok);
    if (!row) {
      model.denom.forEach((d, i) => (scores[i] += d));
    } else {
      row.forEach((v, i) => (scores[i] += v));
    }
  }
  let best = 0;
  scores.forEach((s, i) => {
    if (s > scores[best]) best = i;
  });
  return model.classes[best];
}

export function fmtPct(n: number) {
  return `${Math.round(n * 100)}%`;
}

export function fmtNum(n: number, digits = 2) {
  if (!Number.isFinite(n)) return "—";
  return n.toFixed(digits);
}
