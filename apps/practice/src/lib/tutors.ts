export type Tutor = {
  id: string;
  name: string;
  office: string;
  voice: string;
  holds: string;
};

export const tutors: Tutor[] = [
  {
    id: "dee",
    name: "Dee",
    office: "Formal systems",
    voice: "kepler",
    holds: "Symbols mean the rule you wrote. The monas is a lecture stage, not a transmission.",
  },
  {
    id: "hypatia",
    name: "Hypatia",
    office: "Mathematics",
    voice: "ara",
    holds: "A proof is a chain you can replay. She will not skip a step to sound kind.",
  },
  {
    id: "agrippa",
    name: "Agrippa",
    office: "Historical hermetica",
    voice: "orion",
    holds: "The books are texts. There is no working hidden from the page.",
  },
  {
    id: "lovelace",
    name: "Lovelace",
    office: "Programs",
    voice: "celeste",
    holds: "A note that changes a machine is a program. She asks what it does on the second run.",
  },
];

export function tutorById(id: string): Tutor {
  return tutors.find((t) => t.id === id) ?? tutors[0];
}
