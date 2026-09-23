import { create } from "zustand";
import { persist } from "zustand/middleware";

export type QuizResult = { correct: number; total: number; passed: boolean };
export type LabResult = { score: number; passed: boolean; detail: string };

type State = {
  quizzes: Record<string, QuizResult>;
  labs: Record<string, LabResult>;
  notes: Record<string, boolean>;
  obsession: string;
  tutorId: string;
  hydrated: boolean;
  setHydrated: (v: boolean) => void;
  saveQuiz: (id: string, result: QuizResult) => void;
  saveLab: (id: string, result: LabResult) => void;
  setNote: (id: string, done: boolean) => void;
  setObsession: (text: string) => void;
  setTutorId: (id: string) => void;
};

export const useProgress = create<State>()(
  persist(
    (set) => ({
      quizzes: {},
      labs: {},
      notes: {},
      obsession: "",
      tutorId: "dee",
      hydrated: false,
      setHydrated: (v) => set({ hydrated: v }),
      saveQuiz: (id, result) => set((s) => ({ quizzes: { ...s.quizzes, [id]: result } })),
      saveLab: (id, result) => set((s) => ({ labs: { ...s.labs, [id]: result } })),
      setNote: (id, done) => set((s) => ({ notes: { ...s.notes, [id]: done } })),
      setObsession: (text) => set({ obsession: text.slice(0, 140) }),
      setTutorId: (id) => set({ tutorId: id }),
    }),
    {
      name: "interstitium-domain-v1",
      skipHydration: true,
      partialize: (s) => ({ quizzes: s.quizzes, labs: s.labs, notes: s.notes, obsession: s.obsession, tutorId: s.tutorId }),
    },
  ),
);
