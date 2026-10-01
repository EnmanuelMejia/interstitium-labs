(function () {
  "use strict";
  var host = document.querySelector("[data-il-roadmaps]");
  if (!host) return;

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function modHTML(m, i) {
    function lis(a) {
      return (a || [])
        .map(function (x) {
          return "<li>" + esc(x) + "</li>";
        })
        .join("");
    }
    var refs = (m.sourceRefs || [])
      .map(function (u) {
        return (
          '<a class="text-cyan hover:text-paper" href="' +
          esc(u) +
          '" target="_blank" rel="noopener noreferrer">' +
          esc(u) +
          "</a>"
        );
      })
      .join("<br>");
    return (
      '<details class="rounded-lg border border-paper/10 bg-void/40 px-4 py-3">' +
      "<summary class='cursor-pointer font-display text-sm text-paper'>" +
      esc(i + 1) +
      ". " +
      esc(m.title) +
      "</summary>" +
      '<div class="mt-3 space-y-3 text-sm text-muted">' +
      '<div><p class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Objectives</p><ul class="mt-1 list-disc space-y-1 pl-5">' +
      lis(m.objectives) +
      "</ul></div>" +
      '<div><p class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Key concepts</p><ul class="mt-1 list-disc space-y-1 pl-5">' +
      lis(m.keyConcepts) +
      "</ul></div>" +
      '<div><p class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Hands-on labs</p><ul class="mt-1 list-disc space-y-1 pl-5">' +
      lis(m.labs) +
      "</ul></div>" +
      '<div><p class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Checkpoints</p><ul class="mt-1 list-disc space-y-1 pl-5">' +
      lis(m.checkpoints) +
      "</ul></div>" +
      (refs
        ? '<div><p class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Source references</p><p class="mt-1 break-all text-[0.7rem]">' +
          refs +
          "</p></div>"
        : "") +
      "</div></details>"
    );
  }

  function nodeHTML(n, seqById) {
    var seq = n.distilledId ? seqById[n.distilledId] : null;
    var mods = seq
      ? (seq.modules || [])
          .map(function (m, i) {
            return modHTML(m, i);
          })
          .join("")
      : "";
    return (
      '<li class="rounded-xl border border-paper/10 bg-panel p-5">' +
      '<div class="flex flex-wrap items-baseline justify-between gap-2">' +
      '<h4 class="font-display text-base text-paper">' +
      esc(n.cert) +
      "</h4>" +
      '<span class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-cyan">' +
      esc(n.level || "") +
      (n.heldByFounder
        ? ' <span class="ml-1 rounded border border-gold/50 px-1 text-gold">Held by founder</span>'
        : "") +
      "</span></div>" +
      (n.prereq
        ? '<p class="mt-2 text-sm text-muted"><span class="text-gold">Prerequisite:</span> ' +
          esc(n.prereq) +
          "</p>"
        : "") +
      (n.officialUrl
        ? '<p class="mt-2 text-sm"><a class="text-cyan hover:text-paper" href="' +
          esc(n.officialUrl) +
          '" target="_blank" rel="noopener noreferrer">Official exam page →</a></p>'
        : "") +
      (seq
        ? '<details class="mt-3 rounded-lg border border-gold/30 bg-void/50 px-4 py-3">' +
          "<summary class='cursor-pointer font-display text-[0.68rem] uppercase tracking-[0.14em] text-gold'>Study sequence: " +
          esc(seq.title) +
          "</summary>" +
          '<p class="mt-2 text-xs text-muted">' +
          esc(seq.disclaimer || "") +
          "</p>" +
          '<div class="mt-3 space-y-2">' +
          mods +
          "</div></details>"
        : n.sequence
          ? '<p class="mt-2 text-sm text-muted">' + esc(n.sequence) + "</p>"
          : "") +
      "</li>"
    );
  }

  function toolingHTML(t) {
    if (!t) return "";
    var fw = (t.frameworks || [])
      .map(function (f) {
        return (
          '<a class="text-cyan hover:text-paper" href="' +
          esc(f.url) +
          '" target="_blank" rel="noopener noreferrer">' +
          esc(f.name) +
          "</a>"
        );
      })
      .join(" · ");
    var ides = (t.ides || [])
      .map(function (f) {
        return (
          '<a class="text-cyan hover:text-paper" href="' +
          esc(f.url) +
          '" target="_blank" rel="noopener noreferrer">' +
          esc(f.name) +
          "</a>"
        );
      })
      .join(" · ");
    var man = t.manual
      ? '<a class="text-cyan hover:text-paper" href="' +
        esc(t.manual.url) +
        '" target="_blank" rel="noopener noreferrer">RTFM: ' +
        esc(t.manual.name) +
        " →</a>"
      : "";
    if (!fw && !ides && !man) return "";
    return (
      '<div class="mt-4 rounded-lg border border-paper/10 bg-void/40 p-4 text-sm text-muted">' +
      '<p class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Frameworks · IDEs · Manuals</p>' +
      (fw ? '<p class="mt-2"><span class="text-paper/80">Frameworks:</span> ' + fw + "</p>" : "") +
      (ides ? '<p class="mt-1"><span class="text-paper/80">IDEs:</span> ' + ides + "</p>" : "") +
      (man ? '<p class="mt-1">' + man + "</p>" : "") +
      "</div>"
    );
  }

  function ladderHTML(l, seqById) {
    return (
      '<article class="rounded-xl border border-paper/10 bg-ink/40 p-5 sm:p-6">' +
      '<h3 class="font-display text-xl text-paper">' +
      esc(l.title) +
      "</h3>" +
      '<p class="mt-1 text-sm text-muted">' +
      esc(l.lede || "") +
      "</p>" +
      toolingHTML(l.tooling) +
      '<ol class="mt-4 space-y-3">' +
      l.nodes.map(function (n) { return nodeHTML(n, seqById); }).join("") +
      "</ol></article>"
    );
  }

  Promise.all([
    fetch("/assets/il-cert-roadmaps.json", { credentials: "same-origin", cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("roadmaps " + r.status);
      return r.json();
    }),
    fetch("/assets/il-distilled.json", { credentials: "same-origin", cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("distilled " + r.status);
      return r.json();
    }),
  ])
    .then(function (pair) {
      var data = pair[0],
        dist = pair[1],
        seqById = {};
      (dist.distillations || []).forEach(function (x) {
        seqById[x.id] = x;
      });
      host.innerHTML =
        (data.ladders || [])
          .map(function (l) {
            return ladderHTML(l, seqById);
          })
          .join("") +
        (data.note
          ? '<p class="mt-6 text-xs text-muted">' + esc(data.note) + "</p>"
          : "");
    })
    .catch(function () {
      host.innerHTML =
        '<p class="text-sm text-muted">Certification roadmaps are unavailable right now.</p>';
    });
})();
