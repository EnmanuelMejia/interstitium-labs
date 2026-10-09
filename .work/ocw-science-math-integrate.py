"""Integrate MIT OCW Introductory Science & Math collection into course JSONs.
Adds sourceLinks + freshSignals (tagged mit-ocw, foundational) to IL-02, IL-20, IL-04, IL-23.
All briefs are original distillations; URLs verified 2026-10-09. No content copied.
"""
import json, os, copy
from datetime import date

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
TODAY = "2026-10-09"
COLLECTION = "https://ocw.mit.edu/collections/introductory-science-and-math/"

# ---- OCW resources: original distillations, verified URLs ----
RES = {
    "18.01sc": {
        "name": "MIT OCW 18.01SC Single Variable Calculus (Fall 2010)",
        "url": "https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/",
        "note": "OCW Scholar course by Prof. David Jerison: differentiation, applications of differentiation, definite integrals, integration techniques, infinite series (L'Hopital, Taylor). ~150 hours, 75 sessions, 11 problem sets, 5 exams. Designed for independent study.",
        "signal": {
            "id": "2026-10-09-ocw-1801sc-calculus",
            "headline": "MIT 18.01SC Single Variable Calculus folded into the math spine",
            "brief": ("MIT's OCW Scholar edition of Single Variable Calculus (Prof. David Jerison, Fall 2010) is now linked as a "
                      "foundational spine resource. Five units take you from differentiation rules through optimization and related rates, "
                      "into definite integrals and their applications (areas, volumes, work), then integration techniques "
                      "(trig substitution, partial fractions, parts), closing with infinite series and Taylor expansions. "
                      "About 150 hours of sessions, problem sets, and exams with solutions, built for independent study."),
            "tags": ["mit-ocw", "foundational", "calculus", "single-variable"],
            "noahPrompt": ("Ask Noah to build you a study plan through 18.01SC's five units, or to drill you on any one: "
                           "chain rule, optimization, u-substitution, or Taylor series approximations."),
        },
    },
    "18.02sc": {
        "name": "MIT OCW 18.02SC Multivariable Calculus (Fall 2010)",
        "url": "https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/",
        "note": "OCW Scholar course: differential, integral, and vector calculus for functions of more than one variable. Used across physical sciences, engineering, economics, computer graphics. Lecture + recitation videos, Mathlets applets, problem sets, exams.",
        "signal": {
            "id": "2026-10-09-ocw-1802sc-multivariable",
            "headline": "MIT 18.02SC Multivariable Calculus added to the math spine",
            "brief": ("MIT's OCW Scholar Multivariable Calculus extends the 18.01 foundation to functions of several variables: "
                      "partial derivatives, multiple integrals, and vector calculus (line/surface integrals, gradient, divergence, curl, "
                      "Stokes' and divergence theorems). These are the tools behind physics simulations, engineering analysis, "
                      "economics models, and computer graphics. Includes lecture and recitation videos, interactive Mathlets applets, "
                      "worked examples, problem sets, and exams with solutions."),
            "tags": ["mit-ocw", "foundational", "calculus", "multivariable", "vector-calculus"],
            "noahPrompt": ("Ask Noah to explain the geometric meaning of gradient, divergence, and curl, or to walk you through "
                           "setting up a surface integral step by step."),
        },
    },
    "8.01sc": {
        "name": "MIT OCW 8.01SC Classical Mechanics (Fall 2016)",
        "url": "https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/",
        "note": "OCW Scholar course (Prof. Deepto Chakrabarty, Dr. Peter Dourmashkin): kinematics, Newton's laws, circular motion, momentum/impulse, work/energy, collisions, rotation, angular momentum. Two parallel approaches: force laws and conservation laws. No prerequisites; 18.01SC is a corequisite.",
        "signal": {
            "id": "2026-10-09-ocw-801sc-mechanics",
            "headline": "MIT 8.01SC Classical Mechanics linked for systems intuition",
            "brief": ("MIT's OCW Scholar Classical Mechanics (Chakrabarty/Dourmashkin, Fall 2016) builds physical intuition that pays off "
                      "in systems work: kinematics and Newton's laws, circular motion, momentum and impulse, drag forces, work and "
                      "mechanical energy, collision theory, torque, and angular momentum. The course teaches two parallel problem-solving "
                      "approaches, force analysis and conservation laws, over 12 weekly topics from 1D motion to rolling without slipping. "
                      "Lecture videos, worked examples, and problem sets with solutions; no prerequisites."),
            "tags": ["mit-ocw", "foundational", "physics", "mechanics"],
            "noahPrompt": ("Ask Noah how conservation of angular momentum explains a spinning hard drive's gyroscopic stability, "
                           "or to derive the work-energy theorem from Newton's second law."),
        },
    },
    "8.02": {
        "name": "MIT OCW 8.02 Physics II: Electricity and Magnetism (via OCW collection)",
        "url": COLLECTION,
        "note": "OCW Scholar edition with Prof. Walter Lewin's lectures: electric fields, magnetic fields, EM forces, conductors/dielectrics, EM waves, nature of light. Organized in course modules from electric fields through the nature of light, with visualizations of normally invisible EM phenomena. See the OCW introductory science & math collection.",
        "signal": {
            "id": "2026-10-09-ocw-802-em",
            "headline": "MIT 8.02 Electricity & Magnetism linked for signals and networking depth",
            "brief": ("MIT's OCW Scholar Physics II (Prof. Walter Lewin's lecture series) covers the electromagnetism that underpins "
                      "all of computing hardware and networking: electric charge and Coulomb's law, electric fields and potential, "
                      "capacitors and dielectrics, currents and magnetic fields, Ampere's law, Faraday induction, Maxwell's equations, "
                      "and electromagnetic waves. The course visualizes EM phenomena normally invisible to the eye and connects theory "
                      "to real devices: motors, radios, metal detectors, and particle accelerators. Find it via MIT's introductory "
                      "science and math collection."),
            "tags": ["mit-ocw", "foundational", "physics", "electromagnetism", "networking"],
            "noahPrompt": ("Ask Noah to explain how Maxwell's equations predict that light is an electromagnetic wave, or how "
                           "Faraday's law shows up inside a network switch's magnetics."),
        },
    },
    "5.111sc": {
        "name": "MIT OCW 5.111SC Principles of Chemical Science (Fall 2014)",
        "url": "https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/pages/",
        "note": "OCW Scholar course by Prof. Catherine Drennan: atomic structure, chemical bonding, thermodynamics, kinetics, chemical equilibrium across inorganic/organic/physical chemistry. No formal prerequisites; ~12 hrs/week. Lecture videos, notes, problem sets, exams.",
        "signal": {
            "id": "2026-10-09-ocw-5111sc-chemistry",
            "headline": "MIT 5.111SC Principles of Chemical Science added as foundational science",
            "brief": ("MIT's OCW Scholar Principles of Chemical Science (Prof. Catherine Drennan, Fall 2014) gives the chemical "
                      "foundation behind materials, energy, and hardware: atomic and electronic structure, periodic trends, chemical "
                      "bonding and molecular geometry, thermodynamics, chemical kinetics, and equilibrium, spanning inorganic, organic, "
                      "and physical chemistry. No formal prerequisites. Lecture videos, detailed notes, problem sets, and exams with "
                      "solutions; the course frames chemistry as a modern problem-solving tool for energy, environment, and health."),
            "tags": ["mit-ocw", "foundational", "chemistry"],
            "noahPrompt": ("Ask Noah to connect chemical bonding types to material properties, or to walk through how thermodynamics "
                           "governs battery chemistry."),
        },
    },
    "3.091sc": {
        "name": "MIT OCW 3.091SC Introduction to Solid State Chemistry (Fall 2010)",
        "url": "https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/",
        "note": "OCW Scholar course by Prof. Donald Sadoway (DMSE): electronic structure informs bonding informs atomic order. Crystals, metals, glasses, semiconductors, polymers, biomaterials. Real-world: semiconductor manufacturing, lithium batteries, photonic/biomedical devices. Engineering systems are made of solids.",
        "signal": {
            "id": "2026-10-09-ocw-3091sc-solid-state",
            "headline": "MIT 3.091SC Solid State Chemistry linked: the chemistry inside your chips",
            "brief": ("MIT's OCW Scholar Introduction to Solid State Chemistry (Prof. Donald Sadoway) is the chemistry course most "
                      "directly relevant to computing: electronic structure determines bonding, bonding determines atomic arrangement, "
                      "and that determines everything about a solid. Covers crystals, metals, glasses, semiconductors, polymers, and "
                      "biomaterials, with real-world threads through semiconductor manufacturing, lithium batteries, and photonic devices. "
                      "The course's thesis, engineering systems are made of solids, makes it the ideal bridge between chemistry and "
                      "the hardware this program's systems track runs on."),
            "tags": ["mit-ocw", "foundational", "chemistry", "semiconductors", "hardware"],
            "noahPrompt": ("Ask Noah to explain band gaps and doping in semiconductors, or why the atomic arrangement of silicon "
                           "makes modern computing possible."),
        },
    },
    "7.01sc": {
        "name": "MIT OCW 7.01SC Fundamentals of Biology (Fall 2011)",
        "url": "https://ocw.mit.edu/courses/7-01sc-fundamentals-of-biology-fall-2011/",
        "note": "OCW Scholar course drawing on 7.012/7.013/7.014 (Lander, Weinberg, Jacks, Sive, Walker, Chisholm). Four units: Biochemistry, Molecular Biology, Genetics, Recombinant DNA. Lecture excerpts, problems with solutions, TA help sessions, key terms.",
        "signal": {
            "id": "2026-10-09-ocw-701sc-biology",
            "headline": "MIT 7.01SC Fundamentals of Biology added for bioinformatics foundations",
            "brief": ("MIT's OCW Scholar Fundamentals of Biology distills the institute's introductory biology (versions 7.012 through "
                      "7.014, taught by Lander, Weinberg, Jacks, Sive, Walker, and Chisholm) into four units: biochemistry, molecular "
                      "biology, genetics, and recombinant DNA. Each session pairs MIT faculty lecture excerpts with problems, solutions, "
                      "TA help videos, and key terms. The genetics and recombinant-DNA units are the direct on-ramp to bioinformatics "
                      "and computational biology work."),
            "tags": ["mit-ocw", "foundational", "biology", "bioinformatics"],
            "noahPrompt": ("Ask Noah to explain how recombinant DNA techniques identify a gene of interest, or to map the central "
                           "dogma from DNA to protein."),
        },
    },
}

# ---- Course mapping ----
PLAN = {
    "il-02-mathematical-maturity-engine.json": ["18.01sc", "18.02sc"],
    "il-20-mathematics.json": ["18.01sc", "18.02sc"],
    "il-04-systems-linux-windows-networks.json": ["8.01sc", "8.02", "3.091sc"],
    "il-23-frontier-knowledge.json": ["5.111sc", "7.01sc"],
}

def main():
    report = []
    for fname, rkeys in PLAN.items():
        path = os.path.join(BASE, fname)
        with open(path) as f:
            d = json.load(f)
        added_links, added_signals = 0, 0

        sl = d.setdefault("sourceLinks", [])
        have_urls = {e.get("url") for e in sl}
        fs = d.setdefault("freshSignals", [])
        have_ids = {e.get("id") for e in fs}

        for rk in rkeys:
            r = RES[rk]
            if r["url"] not in have_urls:
                sl.append({
                    "name": r["name"],
                    "url": r["url"],
                    "retrieved": TODAY,
                    "note": r["note"],
                })
                have_urls.add(r["url"])
                added_links += 1
            sig = r["signal"]
            if sig["id"] not in have_ids:
                entry = {
                    "id": sig["id"],
                    "date": TODAY,
                    "headline": sig["headline"],
                    "brief": sig["brief"],
                    "sources": [
                        {"label": r["name"], "url": r["url"]},
                        {"label": "MIT OCW Introductory Science & Math collection", "url": COLLECTION},
                    ],
                    "tags": sig["tags"],
                    "noahPrompt": sig["noahPrompt"],
                }
                fs.append(entry)
                have_ids.add(sig["id"])
                added_signals += 1

        d["updatedAt"] = TODAY
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write("\n")
        # validate before replacing
        with open(tmp) as f:
            json.load(f)
        os.replace(tmp, path)
        report.append(f"{d.get('code')}: +{added_links} sourceLinks, +{added_signals} freshSignals "
                      f"(now {len(sl)} links, {len(fs)} signals)")
    print("\n".join(report))

if __name__ == "__main__":
    main()
