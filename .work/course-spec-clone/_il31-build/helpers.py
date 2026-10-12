# IL-31 build helpers — imported by part files and the assembler.
import json, hashlib

def card(front, back):
    return {"front": front, "back": back}

def quiz(q, choices, answer, explain):
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

def drillitem(prompt, answer, explain):
    return {"prompt": prompt, "answer": answer, "explain": explain}

def drill(id_, items):
    return {"id": id_, "items": items}

def lab(id_, title, brief, steps, checkpoint, deliverable):
    return {"id": id_, "title": title, "brief": brief, "steps": steps,
            "checkpoint": checkpoint, "deliverable": deliverable}

def mocktask(id_, q, choices, answer, explain, type_="mcq"):
    return {"id": id_, "q": q, "choices": choices, "answer": answer,
            "explain": explain, "type": type_}

def video(title, url, source, blurb, durationMin, order):
    return {"title": title, "url": url, "source": source, "blurb": blurb,
            "durationMin": durationMin, "order": order,
            "watchBefore": "notes", "verifiedUtc": "2026-10-09T12:00:00Z",
            "httpStatus": 200}

def pdf(title, url, source, blurb, pages=None, animated=False):
    return {"title": title, "url": url, "source": source, "blurb": blurb,
            "pages": pages, "animated": animated,
            "verifiedUtc": "2026-10-09T12:00:00Z", "httpStatus": 200}

PDF_LIB = "https://interstitiumlabs.dev/pdf-library/"

def mkpdf(title, blurb, pages=8, animated=True):
    return pdf(title, PDF_LIB, "Interstitium Labs", blurb, pages=pages, animated=animated)

def module(id_, title, summary, objectives, estimatedMinutes, weight,
           prerequisiteFor, crossLinks, cards, quiz_q, drills, handsOnLab,
           mockTask, videos, pdfs, notes):
    return {"id": id_, "code": "IL-31", "title": title, "summary": summary,
            "objectives": objectives, "estimatedMinutes": estimatedMinutes,
            "weight": weight, "prerequisiteFor": prerequisiteFor,
            "crossLinks": crossLinks, "cards": cards, "quiz": quiz_q,
            "drills": drills, "handsOnLab": handsOnLab, "mockTask": mockTask,
            "videos": videos, "pdfs": pdfs, "notes": notes}
