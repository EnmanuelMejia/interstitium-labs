export type FsNode = { kind: "dir" | "file"; mode: number; content?: string; children?: Record<string, FsNode> };

export type BashState = {
  cwd: string;
  fs: FsNode;
  log: string[];
};

function dir(mode: number, children: Record<string, FsNode>): FsNode {
  return { kind: "dir", mode, children };
}
function file(mode: number, content: string): FsNode {
  return { kind: "file", mode, content };
}

export function initialBash(): BashState {
  return {
    cwd: "/home/svc",
    log: [],
    fs: dir(0o755, {
      home: dir(0o755, {
        svc: dir(0o700, {}),
      }),
      var: dir(0o755, {
        log: dir(0o755, {
          "app.log": file(0o666, "started\n"),
        }),
      }),
    }),
  };
}

function parts(path: string, cwd: string) {
  const abs = path.startsWith("/") ? path : `${cwd}/${path}`;
  const bits = abs.split("/").filter((p) => p && p !== ".");
  const out: string[] = [];
  for (const bit of bits) {
    if (bit === "..") out.pop();
    else out.push(bit);
  }
  return out;
}

function lookup(root: FsNode, bits: string[]): FsNode | null {
  let cur = root;
  for (const bit of bits) {
    if (cur.kind !== "dir" || !cur.children?.[bit]) return null;
    cur = cur.children[bit];
  }
  return cur;
}

export function bashPicture(state: BashState) {
  const node = lookup(state.fs, ["var", "log", "app.log"]);
  const mode = node && node.kind === "file" ? (node.mode & 0o777).toString(8) : "missing";
  const body = node && node.kind === "file" ? (node.content ?? "").replace(/\n$/, "") : "";
  const history = state.log.length ? state.log.map((line) => `$ ${line}`).join("\n") : "$";
  return [`${state.cwd}`, `app.log  ${mode}  ${body || "(empty)"}`, history].join("\n");
}
export function bashGoalMet(state: BashState) {
  const node = lookup(state.fs, ["var", "log", "app.log"]);
  return Boolean(node && node.kind === "file" && node.mode === 0o640 && node.content === "started\n");
}

export function runBash(state: BashState, line: string): { state: BashState; out: string; error?: string } {
  const raw = line.trim();
  if (!raw) return { state, out: "" };
  if (raw.length > 120) return { state, out: "", error: "Line too long." };
  if (/[;&|`$<>\\]/.test(raw) || raw.includes("\n")) {
    return { state, out: "", error: "Metacharacters are refused. This is a parser, not a shell." };
  }
  const argv = raw.split(/\s+/);
  const cmd = argv[0];
  const next: BashState = {
    cwd: state.cwd,
    log: [...state.log, raw].slice(-40),
    fs: structuredClone(state.fs),
  };

  if (cmd === "pwd") return { state: next, out: next.cwd };
  if (cmd === "ls") {
    const target = argv[1] ? parts(argv[1], next.cwd) : parts(next.cwd, next.cwd);
    const node = lookup(next.fs, target);
    if (!node) return { state, out: "", error: "No such path." };
    if (node.kind === "file") return { state: next, out: argv[1] ?? next.cwd };
    return { state: next, out: Object.keys(node.children ?? {}).sort().join("  ") };
  }
  if (cmd === "cd") {
    const dest = argv[1] ?? "/home/svc";
    const bits = parts(dest, next.cwd);
    const node = lookup(next.fs, bits);
    if (!node || node.kind !== "dir") return { state, out: "", error: "Not a directory." };
    next.cwd = "/" + bits.join("/");
    if (next.cwd === "/") next.cwd = "/";
    return { state: next, out: "" };
  }
  if (cmd === "cat") {
    if (!argv[1]) return { state, out: "", error: "cat needs a path." };
    const node = lookup(next.fs, parts(argv[1], next.cwd));
    if (!node || node.kind !== "file") return { state, out: "", error: "Not a file." };
    return { state: next, out: node.content ?? "" };
  }
  if (cmd === "chmod") {
    if (!/^0?[0-7]{3}$/.test(argv[1] ?? "") || !argv[2]) {
      return { state, out: "", error: "chmod wants an octal mode and a path. Example: chmod 640 /var/log/app.log" };
    }
    const node = lookup(next.fs, parts(argv[2], next.cwd));
    if (!node) return { state, out: "", error: "No such path." };
    node.mode = Number.parseInt(argv[1], 8);
    return { state: next, out: "" };
  }
  return { state, out: "", error: `Unknown command: ${cmd}. Try pwd, ls, cd, cat, chmod.` };
}
