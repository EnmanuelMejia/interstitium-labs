import { useEffect, useRef, useState } from "react";
import { askTutor, speakTutor } from "@/lib/muse-ask";
import { useProgress } from "@/lib/progress";
import { tutorById, tutors } from "@/lib/tutors";

type Line = { who: "you" | "tutor"; text: string; via?: string };

function speakOpen(text: string) {
  if (typeof window === "undefined" || !window.speechSynthesis) return false;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text.slice(0, 420));
  utterance.rate = 0.96;
  window.speechSynthesis.speak(utterance);
  return true;
}

function playMp3(b64: string) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const url = URL.createObjectURL(new Blob([bytes], { type: "audio/mpeg" }));
  const audio = new Audio(url);
  return new Promise<void>((resolve, reject) => {
    audio.onended = () => {
      URL.revokeObjectURL(url);
      resolve();
    };
    audio.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("playback"));
    };
    void audio.play().catch((err) => {
      URL.revokeObjectURL(url);
      reject(err instanceof Error ? err : new Error("playback"));
    });
  });
}

export function TutorDesk() {
  const tutorId = useProgress((s) => s.tutorId);
  const setTutorId = useProgress((s) => s.setTutorId);
  const obsession = useProgress((s) => s.obsession);
  const setObsession = useProgress((s) => s.setObsession);
  const tutor = tutorById(tutorId);
  const [draft, setDraft] = useState("");
  const [lines, setLines] = useState<Line[]>([]);
  const [pending, setPending] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [error, setError] = useState("");
  const [voiceOn, setVoiceOn] = useState(true);
  const scroller = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scroller.current?.scrollTo({ top: scroller.current.scrollHeight });
  }, [lines, pending]);

  function send() {
    const line = draft.trim();
    if (line.length < 2 || pending) return;
    const prior = lines
      .slice(-4)
      .map((item) => `${item.who === "you" ? "Learner" : "Noah"}: ${item.text}`)
      .join("\n");
    setLines((curr) => [...curr, { who: "you", text: line }]);
    setDraft("");
    setPending(true);
    setError("");
    void askTutor({ data: { tutorId: tutor.id, line, obsession, prior } })
      .then(async (res) => {
        if (!res.ok) {
          setError(res.error);
          return;
        }
        setLines((curr) => [
          ...curr,
          {
            who: "tutor",
            text: res.text,
            via: res.provider === "jev" ? `jev · ${res.route}` : `jev · ${res.route} · ${res.provider} · ${res.model}`,
          },
        ]);
        if (!voiceOn) return;
        if (speakOpen(res.text)) return;
        setSpeaking(true);
        const said = await speakTutor({ data: { text: res.text, voice: res.voice } });
        if (!said.ok) setError(said.error);
        else await playMp3(said.audio);
      })
      .catch(() => setError("The tutor could not be reached."))
      .finally(() => {
        setPending(false);
        setSpeaking(false);
      });
  }

  return (
    <section className="mt-8">
      <div className="flex gap-2 overflow-x-auto pb-1">
        {tutors.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setTutorId(item.id)}
            className={
              "min-h-11 shrink-0 rounded-full border px-3 text-sm " +
              (item.id === tutor.id ? "border-fg bg-surface-2 text-fg" : "border-line text-muted")
            }
          >
            {item.name}
          </button>
        ))}
      </div>
      <div className={"stage-well mt-4 overflow-hidden rounded-xl border border-line " + (speaking ? "tutor-live" : "")}>
        <div className="grid gap-6 p-4 sm:grid-cols-[180px_1fr] sm:p-6">
          <div className="flex flex-col items-center justify-end">
            <svg viewBox="0 0 64 64" className="size-24 sm:size-28" aria-hidden>
              <circle cx="32" cy="32" r="23" fill="none" stroke="currentColor" className="text-fg" strokeWidth="1.4" />
              <path d="M32 16 46 44H18Z" fill="none" className="text-gold" stroke="currentColor" strokeWidth="1.4" />
              <rect x="22" y="22" width="5" height="20" className="text-gold" fill="currentColor" />
              <path d="M35 22h5v14h8v4H35Z" className="text-gold" fill="currentColor" />
              <ellipse cx="32" cy="33" rx="16" ry="6" fill="none" className="text-cyan" stroke="currentColor" strokeWidth="1.3" transform="rotate(-18 32 33)" />
              <circle cx="32" cy="33" r="3.2" className="text-gold" fill="currentColor" />
              <path d="M12 30c2-6 6-8 8-8M52 30c-2-6-6-8-8-8" fill="none" className="text-cyan" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
              <circle cx="12" cy="32" r="3.2" fill="none" className="text-cyan" stroke="currentColor" strokeWidth="1.4" />
              <circle cx="52" cy="32" r="3.2" fill="none" className="text-cyan" stroke="currentColor" strokeWidth="1.4" />
            </svg>
            <div className="mt-3 flex flex-nowrap gap-1" aria-hidden>
              {Array.from({ length: 10 }, (_, i) => (
                <span key={i} className="tutor-key h-2 w-2 shrink-0 rounded-sm bg-gold" />
              ))}
            </div>
            <p className="mt-3 text-center text-xs tracking-[0.14em] text-muted uppercase">{tutor.name} · {tutor.office}</p>
          </div>
          <div>
            <div ref={scroller} className="flex max-h-72 min-h-40 flex-col gap-3 overflow-y-auto pr-1">
              {lines.length === 0 ? (
                <p className="max-w-[46ch] rounded-lg border border-line bg-bg px-3 py-3 text-sm text-fg/90">
                  {tutor.holds} Name what you are building. There is no due date.
                </p>
              ) : null}
              {lines.map((item, i) => (
                <p
                  key={`${item.who}-${i}`}
                  className={
                    "max-w-[46ch] rounded-lg border px-3 py-3 text-sm " +
                    (item.who === "tutor"
                      ? "border-line bg-bg text-fg/90"
                      : "ml-auto border-gold/40 bg-surface-2 text-fg")
                  }
                >
                  <span className="mb-1 block text-xs tracking-[0.14em] text-muted uppercase">
                    {item.who === "tutor" ? "Noah" : "You"}
                  </span>
                  {item.text}
                  {item.via ? <span className="mt-2 block text-xs text-muted">{item.via}</span> : null}
                </p>
              ))}
              {pending ? <p className="text-sm text-muted">At the keys.</p> : null}
            </div>
            <label className="mt-4 block text-sm text-muted" htmlFor="obsession">
              The one build. Kept on this device. Not a semester.
            </label>
            <input
              id="obsession"
              value={obsession}
              onChange={(e) => setObsession(e.target.value)}
              maxLength={140}
              className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm text-fg"
              placeholder="A detector, a proof, a service"
            />
            <label className="mt-4 block text-sm text-muted" htmlFor="tutor-line">
              Speak to Noah
            </label>
            <textarea
              id="tutor-line"
              value={draft}
              onChange={(e) => setDraft(e.target.value.slice(0, 500))}
              rows={3}
              className="mt-2 w-full rounded-lg border border-line bg-bg px-3 py-2 text-sm text-fg"
            />
            <div className="mt-3 flex flex-wrap items-center gap-3">
              <button
                type="button"
                disabled={pending || draft.trim().length < 2}
                onClick={send}
                className="min-h-11 rounded-md bg-accent px-4 text-sm font-medium text-accent-fg disabled:opacity-40"
              >
                {pending ? "Listening" : "Send"}
              </button>
              <button
                type="button"
                onClick={() => setVoiceOn((v) => !v)}
                className="min-h-11 rounded-md border border-line px-4 text-sm"
                aria-pressed={voiceOn}
              >
                {voiceOn ? "Voice on" : "Voice off"}
              </button>
            </div>
            {error ? <p className="mt-3 text-sm text-warn">{error}</p> : null}
          </div>
        </div>
      </div>
      <p className="mt-3 max-w-[68ch] text-sm text-muted">
        The figure is the mark with headphones and a keyboard, not a portrait and not another company’s avatar. The voice
        is synthesized speech for this reply. It is not a film performance.
      </p>
    </section>
  );
}
