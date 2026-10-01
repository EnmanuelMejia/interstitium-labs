(function () {
  "use strict";
  var host = document.querySelector("[data-il-roles]");
  if (!host) return;

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function lis(a) {
    return (a || [])
      .map(function (x) {
        return "<li>" + esc(x) + "</li>";
      })
      .join("");
  }

  function modHTML(m, i) {
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

  function stageHTML(st, n, seqById) {
    var seq = st.distilledId ? seqById[st.distilledId] : null;
    var mods = seq
      ? (seq.modules || [])
          .map(function (m, i) {
            return modHTML(m, i);
          })
          .join("")
      : "";
    return (
      '<li class="flex gap-4">' +
      '<span class="flex size-8 shrink-0 items-center justify-center rounded-full border border-cyan/40 font-mono text-xs text-cyan">' +
      n +
      "</span>" +
      '<div class="min-w-0 flex-1 rounded-xl border border-paper/10 bg-panel p-4">' +
      '<div class="flex flex-wrap items-baseline justify-between gap-2">' +
      '<h4 class="font-display text-base text-paper">' +
      esc(st.title) +
      "</h4>" +
      (st.cert
        ? '<span class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-gold">Exam: ' +
          esc(st.cert) +
          "</span>"
        : "") +
      "</div>" +
      (st.note ? '<p class="mt-1 text-sm text-muted">' + esc(st.note) + "</p>" : "") +
      (seq
        ? '<details class="mt-3 rounded-lg border border-gold/30 bg-void/50 px-4 py-3">' +
          "<summary class='cursor-pointer font-display text-[0.68rem] uppercase tracking-[0.14em] text-gold'>Study sequence: " +
          esc(seq.title) +
          " (" +
          (seq.modules || []).length +
          " modules)</summary>" +
          '<div class="mt-3 space-y-2">' +
          mods +
          "</div></details>"
        : "") +
      "</div></li>"
    );
  }

  function toolingHTML(t) {
    if (!t) return "";
    function links(a) {
      return (a || [])
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
    }
    var fw = links(t.frameworks),
      ides = links(t.ides),
      man = t.manual
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

  function roleHTML(r, seqById) {
    return (
      '<article class="rounded-xl border border-paper/10 bg-ink/40 p-5 sm:p-6">' +
      '<p class="font-mono text-[0.6rem] uppercase tracking-[0.28em] text-cyan">Role track</p>' +
      '<h3 class="mt-2 font-display text-2xl text-paper">' +
      esc(r.title) +
      "</h3>" +
      '<p class="mt-1 text-sm text-muted">' +
      esc(r.tagline || "") +
      "</p>" +
      '<p class="mt-3 text-sm text-paper/90"><span class="text-gold">Outcome:</span> ' +
      esc(r.outcome || "") +
      "</p>" +
      toolingHTML(r.tooling) +
      '<ol class="mt-5 space-y-4">' +
      (r.stages || [])
        .map(function (st, i) {
          return stageHTML(st, i + 1, seqById);
        })
        .join("") +
      "</ol>" +
      (r.milestone
        ? '<p class="mt-5 rounded-lg border border-paper/10 bg-void/40 p-4 text-sm text-muted"><span class="font-mono text-[0.6rem] uppercase tracking-[0.16em] text-gold">Milestone · </span>' +
          esc(r.milestone) +
          "</p>"
        : "") +
      "</article>"
    );
  }

  Promise.all([
    fetch("/assets/il-role-tracks.json", { credentials: "same-origin", cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("roles " + r.status);
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
        (data.roles || [])
          .map(function (r) {
            return roleHTML(r, seqById);
          })
          .join("") +
        (data.note
          ? '<p class="mt-6 text-xs text-muted">' + esc(data.note) + "</p>"
          : "");
    })
    .catch(function () {
      host.innerHTML =
        '<p class="text-sm text-muted">Role tracks are unavailable right now.</p>';
    });
})();
