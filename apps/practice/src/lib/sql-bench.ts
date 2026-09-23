export type SqlValue = string | number;
export type SqlRow = Record<string, SqlValue>;

export const readings: SqlRow[] = [
  { id: 1, host: "edge", rate: 12, errors: 1 },
  { id: 2, host: "core", rate: 40, errors: 0 },
  { id: 3, host: "edge", rate: 9, errors: 4 },
  { id: 4, host: "db", rate: 3, errors: 0 },
];

const columns = ["id", "host", "rate", "errors"] as const;

export type SqlResult = { columns: string[]; rows: SqlRow[]; error?: string };

function compare(left: SqlValue, op: string, right: SqlValue): boolean {
  if (op === "=") return left === right;
  if (op === "!=") return left !== right;
  if (typeof left !== "number" || typeof right !== "number") return false;
  if (op === ">") return left > right;
  if (op === "<") return left < right;
  if (op === ">=") return left >= right;
  if (op === "<=") return left <= right;
  return false;
}

function parseLiteral(raw: string): SqlValue | null {
  const text = raw.trim();
  if (/^'[^']*'$/.test(text)) return text.slice(1, -1);
  if (/^-?\d+(\.\d+)?$/.test(text)) return Number(text);
  return null;
}

function where(row: SqlRow, clause: string): boolean | null {
  const parts = clause.split(/\s+and\s+/i);
  for (const part of parts) {
    const match = part.trim().match(/^(\w+)\s*(!=|>=|<=|=|>|<)\s*(.+)$/);
    if (!match) return null;
    const [, col, op, raw] = match;
    if (!columns.includes(col as (typeof columns)[number])) return null;
    const right = parseLiteral(raw);
    if (right === null) return null;
    if (!compare(row[col], op, right)) return false;
  }
  return true;
}

export function runSql(source: string): SqlResult {
  const sql = source.trim().replace(/;+\s*$/, "");
  if (!sql) return { columns: [], rows: [], error: "Empty statement." };
  const count = sql.match(/^select\s+count\(\*\)\s+from\s+readings(?:\s+where\s+(.+))?$/i);
  if (count) {
    const filtered = filter(readings, count[1]);
    if (!filtered) return { columns: [], rows: [], error: "WHERE must be column, operator, value, joined by AND." };
    return { columns: ["count"], rows: [{ count: filtered.length }] };
  }
  const match = sql.match(/^select\s+(.+?)\s+from\s+readings(?:\s+where\s+(.+?))?(?:\s+order\s+by\s+(\w+)(?:\s+(asc|desc))?)?$/i);
  if (!match) {
    return {
      columns: [],
      rows: [],
      error: "This bench runs SELECT on readings, with optional WHERE and ORDER BY. Joins, inserts, and other catalogs are not here.",
    };
  }
  const list = match[1].trim();
  const picked = list === "*" ? [...columns] : list.split(",").map((col) => col.trim());
  if (picked.some((col) => !columns.includes(col as (typeof columns)[number]))) {
    return { columns: [], rows: [], error: "Unknown column. readings has id, host, rate, errors." };
  }
  const filtered = filter(readings, match[2]);
  if (!filtered) return { columns: [], rows: [], error: "WHERE must be column, operator, value, joined by AND." };
  const order = match[3];
  if (order && !columns.includes(order as (typeof columns)[number])) {
    return { columns: [], rows: [], error: "ORDER BY must name a column of readings." };
  }
  const dir = (match[4] || "asc").toLowerCase() === "desc" ? -1 : 1;
  const rows = order
    ? filtered.slice().sort((a, b) => (a[order] > b[order] ? dir : a[order] < b[order] ? -dir : 0))
    : filtered;
  return {
    columns: picked,
    rows: rows.map((row) => Object.fromEntries(picked.map((col) => [col, row[col]]))),
  };
}

function filter(rows: SqlRow[], clause: string | undefined): SqlRow[] | null {
  if (!clause) return rows;
  const out: SqlRow[] = [];
  for (const row of rows) {
    const ok = where(row, clause);
    if (ok === null) return null;
    if (ok) out.push(row);
  }
  return out;
}

export function javaNotes(source: string): string[] {
  const notes: string[] = [];
  if (!/class\s+[A-Za-z_]\w*/.test(source)) notes.push("A Java file this small still needs a class declaration.");
  const open = (source.match(/\{/g) || []).length;
  const close = (source.match(/\}/g) || []).length;
  if (open !== close) notes.push(`Braces do not match: ${open} open, ${close} close.`);
  if (!notes.length) notes.push("The shape is balanced. This page still has no JVM. The manual is the compiler.");
  return notes;
}
