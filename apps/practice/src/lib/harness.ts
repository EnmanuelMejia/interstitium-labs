export type ProviderId = "ollama" | "huggingface" | "frontier";

export type ChatOk = { ok: true; text: string; provider: ProviderId; model: string };
export type ChatResult = ChatOk | { ok: false; error: string };

const OPEN_MODEL = "qwen2.5:7b";
const HF_DEFAULT = "Qwen/Qwen2.5-7B-Instruct";
const FRONTIER_MODEL = "grok-4.5";

function clip(text: string, max: number) {
  const clean = text.replace(/\s+/g, " ").trim();
  return clean ? clean.slice(0, max) : "";
}

async function complete(
  url: string,
  headers: Record<string, string>,
  model: string,
  system: string,
  user: string,
  maxTokens: number,
): Promise<string | null> {
  const res = await fetch(url, {
    method: "POST",
    headers,
    signal: AbortSignal.timeout(20000),
    body: JSON.stringify({
      model,
      max_tokens: maxTokens,
      temperature: 0.4,
      messages: [
        { role: "system", content: system },
        { role: "user", content: user },
      ],
    }),
  });
  if (!res.ok) return null;
  const body = (await res.json()) as { choices?: { message?: { content?: string } }[] };
  return clip(body.choices?.[0]?.message?.content ?? "", 900) || null;
}

type Slot = "ollama" | "huggingface" | "frontier";

async function slot(which: Slot, system: string, user: string, maxTokens: number): Promise<ChatOk | null> {
  if (which === "ollama") {
    const ollama = process.env.OLLAMA_BASE_URL?.replace(/\/$/, "");
    if (!ollama) return null;
    const model = process.env.OLLAMA_MODEL || OPEN_MODEL;
    const text = await complete(`${ollama}/v1/chat/completions`, { "Content-Type": "application/json" }, model, system, user, maxTokens);
    return text ? { ok: true, text, provider: "ollama", model } : null;
  }
  if (which === "huggingface") {
    const hf = process.env.HF_TOKEN;
    if (!hf) return null;
    const model = process.env.HF_MODEL || HF_DEFAULT;
    const text = await complete(
      "https://router.huggingface.co/v1/chat/completions",
      { "Content-Type": "application/json", Authorization: `Bearer ${hf}` },
      model,
      system,
      user,
      maxTokens,
    );
    return text ? { ok: true, text, provider: "huggingface", model } : null;
  }
  const frontier = process.env.XAI_API_KEY;
  if (!frontier) return null;
  const text = await complete(
    "https://api.x.ai/v1/chat/completions",
    { "Content-Type": "application/json", Authorization: `Bearer ${frontier}` },
    FRONTIER_MODEL,
    system,
    user,
    maxTokens,
  );
  return text ? { ok: true, text, provider: "frontier", model: FRONTIER_MODEL } : null;
}

export async function tutorChat(
  system: string,
  user: string,
  maxTokens: number,
  prefer: "open" | "frontier" = "open",
): Promise<ChatResult> {
  const order: Slot[] = prefer === "frontier" ? ["frontier", "ollama", "huggingface"] : ["ollama", "huggingface", "frontier"];
  for (const which of order) {
    try {
      const hit = await slot(which, system, user, maxTokens);
      if (hit) return hit;
    } catch {
      /* the next slot */
    }
  }
  return {
    ok: false,
    error: "No open weight is configured, and the frontier model is not configured. On the host, set OLLAMA_BASE_URL. Hugging Face is the second open path. The question still stands.",
  };
}

export const noahGraph = [
  { id: "office", does: "Bind the office and the obsession. No model call yet." },
  { id: "model", does: "Teach stays on an open weight. An assistant task tries the frontier model first, then falls back." },
  { id: "tool", does: "Jev, a local scorer, picks refuse, the SQL bench, or teach. TypeSafe’s hosted model is not called." },
  { id: "stop", does: "Return the line. The learner speaks next. That pause is the human interrupt." },
] as const;

export function harnessConfig() {
  return {
    ollama: Boolean(process.env.OLLAMA_BASE_URL),
    huggingface: Boolean(process.env.HF_TOKEN),
    frontier: Boolean(process.env.XAI_API_KEY),
    ollamaModel: process.env.OLLAMA_MODEL || OPEN_MODEL,
    hfModel: process.env.HF_MODEL || HF_DEFAULT,
    frontierModel: FRONTIER_MODEL,
  };
}
