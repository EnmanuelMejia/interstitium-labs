export type Rung = { name: string; practice: string; href?: string };

export type Ladder = {
  id: string;
  role: string;
  pace: string;
  note: string;
  catalog: { label: string; href: string };
  rungs: Rung[];
};

export const ladders: Ladder[] = [
  {
    id: "java",
    role: "Java, associate to architect",
    pace: "No deadline",
    note: "Oracle owns the exams. This page does not store their questions or ship a JDK. The rungs are the order of work. The button opens their catalog.",
    catalog: { label: "Oracle Java training", href: "https://education.oracle.com/java" },
    rungs: [
      { name: "Associate", practice: "Read the language against the official tutorial, then explain one type in a sentence.", href: "https://docs.oracle.com/javase/tutorial/" },
      { name: "Professional", practice: "Trace one request through the full-stack path. Name the failure.", href: "/paths/bny-fullstack" },
      { name: "Architect", practice: "Defend a paved path: probes, policy, and who is on call.", href: "/paths/platform-sre" },
    ],
  },
  {
    id: "sql",
    role: "SQL, associate to architect",
    pace: "No deadline",
    note: "SQL practice is the bench: SELECT on one table. Oracle still owns the exams and the rest of the dialect.",
    catalog: { label: "Oracle Database training", href: "https://education.oracle.com/oracle-database" },
    rungs: [
      { name: "Associate", practice: "One SELECT you can read aloud, then run it on the bench.", href: "/editor" },
      { name: "Professional", practice: "A model with a label that is not the future leaking in.", href: "/paths/data-analyst-to-ml" },
      { name: "Architect", practice: "Retention, identity, and the log you would show the next shift.", href: "/paths/aws-cloud-ops" },
    ],
  },
  {
    id: "systems",
    role: "C, C++, and the shell",
    pace: "No deadline",
    note: "GCC and the bash desk are the open tools. Perl, PowerShell, and the rest are traces on Muse until a parser exists. No proprietary IDE is bundled.",
    catalog: { label: "GCC manuals", href: "https://gcc.gnu.org/onlinedocs/" },
    rungs: [
      { name: "Shell", practice: "Make the log 640 and leave the bytes alone.", href: "/desk" },
      { name: "C and C++", practice: "Read the manual for the warning you would not silence.", href: "https://gcc.gnu.org/onlinedocs/" },
      { name: "Operator", practice: "A script that fails non-zero and names the object it touched.", href: "/paths/python-systems" },
    ],
  },
  {
    id: "linux",
    role: "Linux administrator",
    pace: "No deadline",
    note: "The RHCSA is taken on Red Hat's systems. The spine here is the recovery order, not their exam.",
    catalog: { label: "RHCSA", href: "https://www.redhat.com/en/services/certification/rhcsa" },
    rungs: [
      { name: "Essentials", practice: "Permissions, processes, journald.", href: "/paths/linux-lf-essentials" },
      { name: "Spine", practice: "Boot, users, units, under a clock you set yourself.", href: "/paths/linux-rhcsa-spine" },
      { name: "Host", practice: "RHEL 10.2 on the metal, KVM for the guest.", href: "/host" },
    ],
  },
  {
    id: "platform",
    role: "Platform by role",
    pace: "No deadline",
    note: "KodeKloud-style means a role, then a cert catalog, then a studio. The studios are ours. The exams stay on the vendor.",
    catalog: { label: "CNCF certifications", href: "https://www.cncf.io/training/certification/" },
    rungs: [
      { name: "Kubernetes", practice: "Objects, then the scheduling decision.", href: "/paths/k8s-cka-exceed" },
      { name: "Delivery", practice: "Git, a gate that can fail, drift versus plan.", href: "/paths/iac-terraform-gitops" },
      { name: "Security", practice: "A hypothesis, a log source, and a false-positive story.", href: "/paths/secops-blue-team" },
    ],
  },
];
