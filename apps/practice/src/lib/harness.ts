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

export async function tutorChat(system: string, user: string, maxTokens: number): Promise<ChatResult> {
  const ollama = process.env.OLLAMA_BASE_URL?.replace(/\/$/, "");
  const ollamaModel = process.env.OLLAMA_MODEL || OPEN_MODEL;
  if (ollama) {
    try {
      const text = await complete(
        `${ollama}/v1/chat/completions`,
        { "Content-Type": "application/json" },
        ollamaModel,
        system,
        user,
        maxTokens,
      );
      if (text) return { ok: true, text, provider: "ollama", model: ollamaModel };
    } catch {
      /* the next open provider, then the frontier */
    }
  }

  const hf = process.env.HF_TOKEN;
  const hfModel = process.env.HF_MODEL || HF_DEFAULT;
  if (hf) {
    try {
      const text = await complete(
        "https://router.huggingface.co/v1/chat/completions",
        { "Content-Type": "application/json", Authorization: `Bearer ${hf}` },
        hfModel,
        system,
        user,
        maxTokens,
      );
      if (text) return { ok: true, text, provider: "huggingface", model: hfModel };
    } catch {
      /* frontier is the scale step, not the default */
    }
  }

  const frontier = process.env.XAI_API_KEY;
  if (frontier) {
    try {
      const text = await complete(
        "https://api.x.ai/v1/chat/completions",
        { "Content-Type": "application/json", Authorization: `Bearer ${frontier}` },
        FRONTIER_MODEL,
        system,
        user,
        maxTokens,
      );
      if (text) return { ok: true, text, provider: "frontier", model: FRONTIER_MODEL };
    } catch {
      return { ok: false, error: "The frontier model could not be reached. The question still stands." };
    }
  }

  return {
    ok: false,
    error: "No open weight is configured, and the frontier model is not configured. On the host, set OLLAMA_BASE_URL. Hugging Face is the second open path. The question still stands.",
  };
}

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
