/**
 * NoahDoc — inline document rendering for Noah AI tutoring.
 * (Interstitium original. No dependencies, CSP-safe, no CDN.)
 *
 * NoahDoc.render(container, doc) where doc = { type, ... }:
 *   pdf       { url, title }                    — native inline viewer + nav
 *   code      { language, code, title }         — highlighted + line numbers + copy
 *   markdown  { text, title }                   — full md render
 *   table     { columns:[], rows:[[]], title }  — sortable + filterable
 *   csv       { text, title }                   — parsed then table
 *   image     { url, alt }                      — zoom/pan viewer
 *   video     { url, poster }                   — inline player
 *   terminal  { text, title }                   — styled terminal block
 *   diagram   { kind:'flow', nodes, edges }     — canvas flowchart (no Mermaid CDN)
 *   math      { tex }                           — styled math (common constructs)
 *
 * All output is sandboxed text — never innerHTML from untrusted sources
 * without escaping. Code/markdown go through the escaper first.
 */
(function (g) {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function css() {
    if (document.getElementById('noahdoc-css')) return;
    var s = document.createElement('style'); s.id = 'noahdoc-css';
    s.textContent = [
      '.noahdoc{border:1px solid rgba(255,255,255,.12);border-radius:12px;overflow:hidden;',
      'background:rgba(4,7,12,.92);margin:10px 0;max-width:100%;}',
      '.noahdoc-head{display:flex;align-items:center;gap:8px;padding:8px 12px;',
      'background:rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.08);',
      'font-size:12px;color:#8b93a5;letter-spacing:.04em;}',
      '.noahdoc-head .t{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#dbe4ee;}',
      '.noahdoc-body{padding:0;}',
      '.noahdoc-copy{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);',
      'color:#dbe4ee;border-radius:6px;font-size:11px;padding:4px 10px;cursor:pointer;}',
      '.noahdoc-copy:hover{border-color:#c9a227;color:#fff;}',
      '.noahdoc pre{margin:0;padding:12px 0;overflow-x:auto;font-family:ui-monospace,Menlo,Consolas,monospace;',
      'font-size:12.5px;line-height:1.55;color:#dbe4ee;}',
      '.noahdoc .cl{display:flex;} .noahdoc .ln{flex:0 0 44px;text-align:right;padding-right:12px;',
      'color:#5b6b82;user-select:none;} .noahdoc .lc{flex:1;padding-right:12px;white-space:pre;}',
      '.noahdoc .tok-k{color:#c792ea;} .noahdoc .tok-s{color:#a5e075;} .noahdoc .tok-c{color:#5b6b82;font-style:italic;}',
      '.noahdoc .tok-n{color:#f78c6c;} .noahdoc .tok-f{color:#82aaff;}',
      '.noahdoc .md{padding:14px 16px;color:#dbe4ee;font-size:13.5px;line-height:1.65;}',
      '.noahdoc .md h1,.noahdoc .md h2,.noahdoc .md h3{color:#fff;margin:.8em 0 .4em;}',
      '.noahdoc .md table{border-collapse:collapse;width:100%;margin:10px 0;font-size:12.5px;}',
      '.noahdoc .md th,.noahdoc .md td{border:1px solid rgba(255,255,255,.14);padding:6px 10px;text-align:left;}',
      '.noahdoc .md th{background:rgba(255,255,255,.06);}',
      '.noahdoc .md code{background:rgba(255,255,255,.08);padding:1px 6px;border-radius:4px;font-size:12px;}',
      '.noahdoc table.dt{width:100%;border-collapse:collapse;font-size:12.5px;color:#dbe4ee;}',
      '.noahdoc table.dt th{position:sticky;top:0;background:#0d141d;cursor:pointer;padding:8px 10px;',
      'text-align:left;border-bottom:1px solid rgba(255,255,255,.14);white-space:nowrap;}',
      '.noahdoc table.dt th:hover{color:#c9a227;}',
      '.noahdoc table.dt td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,.06);}',
      '.noahdoc .dt-filter{width:100%;box-sizing:border-box;background:rgba(255,255,255,.05);',
      'border:1px solid rgba(255,255,255,.14);border-radius:6px;color:#dbe4ee;padding:6px 10px;margin:8px 0;font-size:12px;}',
      '.noahdoc .dt-wrap{max-height:320px;overflow:auto;padding:0 12px 12px;}',
      '.noahdoc .imgview{position:relative;overflow:hidden;touch-action:none;cursor:grab;}',
      '.noahdoc .imgview img{display:block;max-width:100%;transform-origin:0 0;}',
      '.noahdoc .term{background:#05070c;color:#a5e075;font-family:ui-monospace,Menlo,monospace;',
      'font-size:12.5px;padding:12px 14px;overflow-x:auto;white-space:pre-wrap;line-height:1.6;}',
      '.noahdoc .term .p{color:#5EEAD4;}',
      '.noahdoc video{width:100%;display:block;background:#000;}',
      '.noahdoc .math{padding:16px;text-align:center;color:#fff;font-size:16px;font-family:Georgia,serif;}',
      '.noahdoc .pdfnav{display:flex;gap:8px;align-items:center;}',
      '.noahdoc .pdfnav button{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);',
      'color:#dbe4ee;border-radius:6px;padding:4px 12px;cursor:pointer;font-size:12px;}',
      '.noahdoc embed.pdf{width:100%;height:480px;border:0;background:#111;}'
    ].join('');
    document.head.appendChild(s);
  }

  /* ---------- code highlighting (regex, per language) ---------- */

  var KEYWORDS = {
    python: 'def|class|return|import|from|if|elif|else|for|while|try|except|with|as|lambda|yield|await|async|pass|raise|in|is|not|and|or|None|True|False',
    javascript: 'function|const|let|var|return|if|else|for|while|class|new|await|async|import|export|from|try|catch|throw|typeof|in|of|this|null|undefined|true|false',
    typescript: 'function|const|let|var|return|if|else|for|while|class|new|await|async|import|export|from|try|catch|throw|typeof|in|of|this|interface|type|enum|null|undefined|true|false',
    rust: 'fn|let|mut|return|if|else|for|while|loop|match|struct|enum|impl|trait|pub|use|mod|crate|as|in|ref|move|const|static|true|false|Some|None|Ok|Err',
    go: 'func|var|const|return|if|else|for|range|struct|interface|type|package|import|go|defer|chan|map|true|false|nil',
    sql: 'SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|ON|GROUP|BY|ORDER|HAVING|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|TABLE|ALTER|DROP|AND|OR|NOT|NULL|AS|DISTINCT|LIMIT',
    bash: 'if|then|else|elif|fi|for|while|do|done|function|return|echo|exit|export|local|in|case|esac',
    java: 'public|private|protected|class|interface|extends|implements|static|final|void|int|long|double|boolean|return|if|else|for|while|new|try|catch|import|package|this|null|true|false'
  };

  function highlight(code, lang) {
    var h = esc(code);
    /* comments */
    h = h.replace(/(\/\/[^\n]*|#[^\n]*|--[^\n]*)/g, '\u0001$1\u0002');
    /* strings */
    h = h.replace(/(&quot;.*?&quot;|&#x27;.*?&#x27;|`[^`]*`)/g, '\u0003$1\u0004');
    /* numbers */
    h = h.replace(/\b(\d[\d_]*(?:\.\d+)?)\b/g, '\u0005$1\u0006');
    var kw = KEYWORDS[lang];
    if (kw) {
      var re = new RegExp('\\b(' + kw + ')\\b', 'g');
      h = h.replace(re, '\u0007$1\u0008');
    }
    /* function calls */
    h = h.replace(/([a-zA-Z_][\w]*)(?=\()/g, '\u0009$1\u000A');
    return h
      .replace(/\u0001/g, '<span class="tok-c">').replace(/\u0002/g, '</span>')
      .replace(/\u0003/g, '<span class="tok-s">').replace(/\u0004/g, '</span>')
      .replace(/\u0005/g, '<span class="tok-n">').replace(/\u0006/g, '</span>')
      .replace(/\u0007/g, '<span class="tok-k">').replace(/\u0008/g, '</span>')
      .replace(/\u0009/g, '<span class="tok-f">').replace(/\u000A/g, '</span>');
  }

  /* ---------- markdown (safe subset) ---------- */

  function markdown(src) {
    var lines = esc(src).split('\n'), out = [], i = 0, inCode = false, codeLang = '', codeBuf = [];
    function flushCode() {
      if (codeBuf.length) {
        out.push('<pre><code>' + highlight(codeBuf.join('\n'), codeLang) + '</code></pre>');
        codeBuf = []; codeLang = '';
      }
    }
    while (i < lines.length) {
      var L = lines[i];
      var fence = L.match(/^```(\w*)/);
      if (fence) {
        if (inCode) { flushCode(); inCode = false; }
        else { inCode = true; codeLang = fence[1] || ''; }
        i++; continue;
      }
      if (inCode) { codeBuf.push(L); i++; continue; }
      var hm = L.match(/^(#{1,4})\s+(.*)/);
      if (hm) { out.push('<h' + hm[1].length + '>' + inline(hm[2]) + '</h' + hm[1].length + '>'); i++; continue; }
      if (/^\s*-\s+/.test(L)) {
        out.push('<ul>'); 
        while (i < lines.length && /^\s*-\s+/.test(lines[i])) { out.push('<li>' + inline(lines[i].replace(/^\s*-\s+/, '')) + '</li>'); i++; }
        out.push('</ul>'); continue;
      }
      if (/^\s*\d+\.\s+/.test(L)) {
        out.push('<ol>');
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) { out.push('<li>' + inline(lines[i].replace(/^\s*\d+\.\s+/, '')) + '</li>'); i++; }
        out.push('</ol>'); continue;
      }
      if (/^\|.*\|$/.test(L)) {
        var rows = [];
        while (i < lines.length && /^\|.*\|$/.test(lines[i])) { rows.push(lines[i]); i++; }
        out.push(mdTable(rows)); continue;
      }
      if (/^\s*$/.test(L)) { i++; continue; }
      out.push('<p>' + inline(L) + '</p>'); i++;
    }
    flushCode();
    return out.join('\n');
    function inline(s) {
      return s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
              .replace(/\*([^*]+)\*/g, '<em>$1</em>')
              .replace(/`([^`]+)`/g, '<code>$1</code>')
              .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:#5EEAD4">$1</a>');
    }
    function mdTable(rows) {
      var cells = rows.map(function (r) { return r.replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); }); });
      var body = cells.filter(function (_, ix) { return ix !== 1; });
      var h = '<table><thead><tr>' + cells[0].map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead><tbody>';
      body.slice(1).forEach(function (r) { h += '<tr>' + r.map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>'; });
      return h + '</tbody></table>';
    }
  }

  /* ---------- renderers ---------- */

  function header(title, extra) {
    var h = el('div', 'noahdoc-head', '<span class="t">' + esc(title || 'Document') + '</span>');
    if (extra) h.appendChild(extra);
    return h;
  }

  function copyBtn(text) {
    var b = el('button', 'noahdoc-copy', 'Copy');
    b.type = 'button';
    b.addEventListener('click', function () {
      function done() { b.textContent = 'Copied ✓'; setTimeout(function () { b.textContent = 'Copy'; }, 1500); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta); done();
      }
    });
    return b;
  }

  var R = {
    pdf: function (box, d) {
      var nav = el('span', 'pdfnav');
      var prev = el('button', '', '‹ Prev'), next = el('button', '', 'Next ›');
      var pg = el('span', '', 'Page ');
      var num = el('b', '', '1'); pg.appendChild(num);
      var frame = document.createElement('embed');
      frame.className = 'pdf'; frame.type = 'application/pdf'; frame.src = d.url;
      var cur = 1;
      prev.addEventListener('click', function () { if (cur > 1) { cur--; num.textContent = cur; frame.src = d.url + '#page=' + cur; } });
      next.addEventListener('click', function () { cur++; num.textContent = cur; frame.src = d.url + '#page=' + cur; });
      nav.appendChild(prev); nav.appendChild(pg); nav.appendChild(next);
      box.appendChild(header(d.title || 'PDF', nav));
      var body = el('div', 'noahdoc-body'); body.appendChild(frame); box.appendChild(body);
    },

    code: function (box, d) {
      box.appendChild(header((d.title || 'Code') + ' · ' + (d.language || 'text'), copyBtn(d.code || '')));
      var body = el('div', 'noahdoc-body');
      var pre = el('pre', '');
      var lines = highlight(d.code || '', d.language || '').split('\n');
      pre.innerHTML = lines.map(function (l, i) {
        return '<span class="cl"><span class="ln">' + (i + 1) + '</span><span class="lc">' + (l || ' ') + '</span></span>';
      }).join('');
      body.appendChild(pre); box.appendChild(body);
    },

    markdown: function (box, d) {
      box.appendChild(header(d.title || 'Notes'));
      var body = el('div', 'noahdoc-body');
      var md = el('div', 'md'); md.innerHTML = markdown(d.text || '');
      body.appendChild(md); box.appendChild(body);
    },

    table: function (box, d) {
      box.appendChild(header(d.title || 'Data'));
      var body = el('div', 'noahdoc-body');
      var filter = el('input', 'dt-filter'); filter.placeholder = 'Filter rows…'; filter.type = 'search';
      var wrap = el('div', 'dt-wrap');
      var table = el('table', 'dt');
      var cols = d.columns || [], rows = (d.rows || []).slice();
      var sortCol = -1, sortDir = 1;
      function paint(data) {
        table.innerHTML = '<thead><tr>' + cols.map(function (c, i) {
          return '<th data-c="' + i + '">' + esc(c) + (sortCol === i ? (sortDir > 0 ? ' ▲' : ' ▼') : '') + '</th>';
        }).join('') + '</tr></thead><tbody>' +
        data.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>'; }).join('') +
        '</tbody>';
      }
      function current() {
        var q = filter.value.trim().toLowerCase();
        var data = rows.filter(function (r) {
          return !q || r.some(function (c) { return String(c).toLowerCase().indexOf(q) >= 0; });
        });
        if (sortCol >= 0) {
          data = data.slice().sort(function (a, b) {
            var x = a[sortCol], y = b[sortCol];
            var nx = parseFloat(x), ny = parseFloat(y);
            var cmp = (!isNaN(nx) && !isNaN(ny)) ? nx - ny : String(x).localeCompare(String(y));
            return cmp * sortDir;
          });
        }
        return data;
      }
      table.addEventListener('click', function (e) {
        var th = e.target.closest('th'); if (!th) return;
        var c = parseInt(th.getAttribute('data-c'), 10);
        if (sortCol === c) sortDir *= -1; else { sortCol = c; sortDir = 1; }
        paint(current());
      });
      filter.addEventListener('input', function () { paint(current()); });
      paint(rows);
      body.appendChild(filter); wrap.appendChild(table); body.appendChild(wrap); box.appendChild(body);
    },

    csv: function (box, d) {
      var lines = String(d.text || '').trim().split('\n');
      function parse(line) {
        var out = [], cur = '', q = false;
        for (var i = 0; i < line.length; i++) {
          var ch = line[i];
          if (q) {
            if (ch === '"') { if (line[i+1] === '"') { cur += '"'; i++; } else q = false; }
            else cur += ch;
          } else if (ch === '"') q = true;
          else if (ch === ',') { out.push(cur); cur = ''; }
          else cur += ch;
        }
        out.push(cur); return out;
      }
      R.table(box, { title: d.title || 'Spreadsheet', columns: parse(lines[0] || ''), rows: lines.slice(1).map(parse) });
    },

    image: function (box, d) {
      box.appendChild(header(d.alt || 'Image'));
      var body = el('div', 'noahdoc-body');
      var view = el('div', 'imgview');
      var img = document.createElement('img'); img.src = d.url; img.alt = d.alt || '';
      view.appendChild(img); body.appendChild(view); box.appendChild(body);
      var scale = 1, ox = 0, oy = 0, sx = 0, sy = 0, drag = false;
      function apply() { img.style.transform = 'translate(' + ox + 'px,' + oy + 'px) scale(' + scale + ')'; }
      view.addEventListener('wheel', function (e) {
        e.preventDefault();
        scale = Math.min(5, Math.max(1, scale * (e.deltaY < 0 ? 1.15 : 0.87)));
        apply();
      }, { passive: false });
      view.addEventListener('pointerdown', function (e) { drag = true; sx = e.clientX - ox; sy = e.clientY - oy; view.setPointerCapture(e.pointerId); });
      view.addEventListener('pointermove', function (e) { if (drag) { ox = e.clientX - sx; oy = e.clientY - sy; apply(); } });
      view.addEventListener('pointerup', function () { drag = false; });
      view.addEventListener('dblclick', function () { scale = 1; ox = 0; oy = 0; apply(); });
    },

    video: function (box, d) {
      box.appendChild(header(d.title || 'Video'));
      var body = el('div', 'noahdoc-body');
      var v = document.createElement('video');
      v.src = d.url; v.controls = true; v.preload = 'metadata';
      if (d.poster) v.poster = d.poster;
      body.appendChild(v); box.appendChild(body);
    },

    terminal: function (box, d) {
      box.appendChild(header(d.title || 'Terminal', copyBtn(d.text || '')));
      var body = el('div', 'noahdoc-body');
      var t = el('div', 'term');
      t.innerHTML = esc(d.text || '').replace(/^(\$|&gt;|#)(.*)$/gm, '<span class="p">$1</span>$2');
      body.appendChild(t); box.appendChild(body);
    },

    diagram: function (box, d) {
      box.appendChild(header(d.title || 'Diagram'));
      var body = el('div', 'noahdoc-body');
      var cv = document.createElement('canvas');
      cv.style.width = '100%'; cv.style.height = '300px'; cv.style.display = 'block';
      body.appendChild(cv); box.appendChild(body);
      if (g.NoahViz && g.NoahViz.flow) {
        g.NoahViz.flow(cv, { title: d.title, nodes: d.nodes || [], edges: d.edges || [] });
      } else {
        var f = (function () {
          var r = cv.getBoundingClientRect(), dpr = Math.min(2, g.devicePixelRatio || 1);
          cv.width = r.width * dpr; cv.height = 300 * dpr;
          var c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0);
          c.fillStyle = '#0a0f1c'; c.fillRect(0, 0, r.width, 300);
          c.fillStyle = '#8b93a5'; c.font = '13px system-ui'; c.textAlign = 'center';
          c.fillText('Diagram engine loading…', r.width / 2, 150);
        })();
      }
    },

    math: function (box, d) {
      box.appendChild(header(d.title || 'Math'));
      var body = el('div', 'noahdoc-body');
      var m = el('div', 'math');
      /* render common TeX constructs as styled HTML; full KaTeX needs CDN (CSP-blocked) */
      var h = esc(d.tex || '')
        .replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, '<span style="display:inline-block;vertical-align:middle;text-align:center"><span style="border-bottom:1px solid #fff;padding:0 6px">$1</span><br><span style="padding:0 6px">$2</span></span>')
        .replace(/\\sqrt\{([^}]*)\}/g, '√<span style="border-top:1px solid #fff">$1</span>')
        .replace(/\\sum_/g, '∑').replace(/\\int_/g, '∫').replace(/\\infty/g, '∞')
        .replace(/\\alpha/g, 'α').replace(/\\beta/g, 'β').replace(/\\gamma/g, 'γ')
        .replace(/\\delta/g, 'δ').replace(/\\theta/g, 'θ').replace(/\\lambda/g, 'λ')
        .replace(/\\mu/g, 'μ').replace(/\\sigma/g, 'σ').replace(/\\pi/g, 'π')
        .replace(/\^(\{[^}]*\}|\w)/g, '<sup>$1</sup>').replace(/_(\{[^}]*\}|\w)/g, '<sub>$1</sub>')
        .replace(/\\times/g, '×').replace(/\\cdot/g, '·').replace(/\\leq/g, '≤').replace(/\\geq/g, '≥')
        .replace(/\\neq/g, '≠').replace(/\\rightarrow/g, '→');
      m.innerHTML = h;
      body.appendChild(m); box.appendChild(body);
    }
  };

  g.NoahDoc = {
    version: 1,
    types: Object.keys(R),
    render: function (container, doc) {
      css();
      var box = el('div', 'noahdoc');
      try {
        var fn = R[doc.type];
        if (!fn) {
          box.appendChild(header('Unsupported'));
          var b = el('div', 'noahdoc-body');
          var p = el('div', 'md'); p.innerHTML = '<div class="md" style="padding:14px">Cannot render type: ' + esc(doc.type) + '</div>';
          b.appendChild(p); box.appendChild(b);
        } else fn(box, doc);
      } catch (e) {
        box.appendChild(header('Render error'));
      }
      container.appendChild(box);
      return box;
    }
  };
})(typeof window !== 'undefined' ? window : this);
