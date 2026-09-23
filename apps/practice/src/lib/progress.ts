import { create } from "zustand";
import { persist } from "zustand/middleware";

export type QuizResult = { correct: number; total: number; passed: boolean };
export type LabResult = { score: number; passed: boolean; detail: string };
export type BaselineResult = { theta: number; band: "numerals" | "rates" | "models" | "tails"; asked: number };
export type BuildProof = { artifact: string; who: string; fails: string };

type State = {
  quizzes: Record<string, QuizResult>;
  labs: Record<string, LabResult>;
  notes: Record<string, boolean>;
  obsession: string;
  tutorId: string;
  baseline: BaselineResult | null;
  build: BuildProof;
  memory: string[];
  goals: string[];
  hydrated: boolean;
  setHydrated: (v: boolean) => void;
  saveQuiz: (id: string, result: QuizResult) => void;
  saveLab: (id: string, result: LabResult) => void;
  setNote: (id: string, done: boolean) => void;
  setObsession: (text: string) => void;
  setTutorId: (id: string) => void;
  setBaseline: (result: BaselineResult) => void;
  setBuild: (patch: Partial<BuildProof>) => void;
  addMemory: (text: string) => void;
  dropMemory: (text: string) => void;
  addGoal: (text: string) => void;
};

export const useProgress = create<State>()(
  persist(
    (set) => ({
      quizzes: {},
      labs: {},
      notes: {},
      obsession: "",
      tutorId: "dee",
      baseline: null,
      build: { artifact: "", who: "", fails: "" },
      memory: [],
      goals: [],
      hydrated: false,
      setHydrated: (v) => set({ hydrated: v }),
      saveQuiz: (id, result) => set((s) => ({ quizzes: { ...s.quizzes, [id]: result } })),
      saveLab: (id, result) => set((s) => ({ labs: { ...s.labs, [id]: result } })),
      setNote: (id, done) => set((s) => ({ notes: { ...s.notes, [id]: done } })),
      setObsession: (text) => set({ obsession: text.slice(0, 140) }),
      setTutorId: (id) => set({ tutorId: id }),
      setBaseline: (result) => set({ baseline: result }),
      setBuild: (patch) => set((s) => ({ build: { ...s.build, ...patch } })),
      addMemory: (text) =>
        set((s) => {
          const next = text.replace(/\s+/g, " ").trim().slice(0, 160);
          if (next.length < 2 || s.memory.includes(next)) return s;
          return { memory: [next, ...s.memory].slice(0, 12) };
        }),
      dropMemory: (text) =>
        set((s) => ({ memory: s.memory.filter((item) => !item.toLowerCase().includes(text.toLowerCase())) })),
      addGoal: (text) =>
        set((s) => {
          const next = text.replace(/\s+/g, " ").trim().slice(0, 160);
          if (next.length < 2 || s.goals.includes(next)) return s;
          return { goals: [next, ...s.goals].slice(0, 6) };
        }),
    }),
    {
      name: "interstitium-domain-v1",
      skipHydration: true,
      partialize: (s) => ({
        quizzes: s.quizzes,
        labs: s.labs,
        notes: s.notes,
        obsession: s.obsession,
        tutorId: s.tutorId,
        baseline: s.baseline,
        build: s.build,
        memory: s.memory,
        goals: s.goals,
      }),
    },
  ),
);
