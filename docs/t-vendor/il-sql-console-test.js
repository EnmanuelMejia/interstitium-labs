/* il-sql-console.js — real in-browser SQL console (sql.js / SQLite WASM).
   No backend. The database lives in the visitor's browser only. */
(function () {
  "use strict";

  var SQLJS_VERSION = "1.13.0";
  var SQLJS_BASE = "/t-vendor/";

  /* ---------- sample dataset ---------- */
  var SEED_SQL = [
    "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT, signup_date TEXT);",
    "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);",
    "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, qty INTEGER, order_date TEXT, status TEXT);",
    "INSERT INTO customers VALUES",
    "(1,'Ada Lovelace','ada@example.com','Boston','2025-03-14'),",
    "(2,'Grace Hopper','grace@example.com','New York','2025-06-02'),",
    "(3,'Alan Turing','alan@example.com','Boston','2025-09-30'),",
    "(4,'Katherine Johnson','katherine@example.com','Chicago','2026-01-11'),",
    "(5,'Donald Knuth','donald@example.com','Austin','2026-02-19'),",
    "(6,'Barbara Liskov','barbara@example.com','Boston','2026-03-05'),",
    "(7,'Linus Torvalds','linus@example.com','Portland','2026-04-22'),",
    "(8,'Margaret Hamilton','margaret@example.com','New York','2026-05-09');",
    "INSERT INTO products VALUES",
    "(1,'Laptop Pro 16','Computers',1899.00),",
    "(2,'Mechanical Keyboard','Accessories',129.00),",
    "(3,'4K Monitor 27','Monitors',449.00),",
    "(4,'USB-C Dock','Accessories',89.00),",
    "(5,'Laptop Air 13','Computers',1199.00),",
    "(6,'Webcam HD','Accessories',59.00);",
    "INSERT INTO orders VALUES",
    "(1,1,1,1,'2026-01-15','completed'),",
    "(2,1,2,2,'2026-02-03','completed'),",
    "(3,2,5,1,'2026-02-20','completed'),",
    "(4,3,3,1,'2026-03-02','completed'),",
    "(5,4,1,1,'2026-03-18','pending'),",
    "(6,2,4,3,'2026-04-01','completed'),",
    "(7,5,6,2,'2026-04-12','completed'),",
    "(8,6,5,1,'2026-05-06','completed'),",
    "(9,7,2,1,'2026-05-21','pending'),",
    "(10,8,3,2,'2026-06-02','completed'),",
    "(11,1,5,1,'2026-06-15','completed'),",
    "(12,4,2,1,'2026-06-30','completed'),",
    "(13,3,1,1,'2026-07-08','completed'),",
    "(14,6,4,1,'2026-07-19','completed'),",
    "(15,5,3,1,'2026-08-03','completed');"
  ].join("\n");

  /* ---------- guided exercises (original) ---------- */
  var EXERCISES = [
    {
      id: "ex1", title: "1 · SELECT columns",
      task: "List the name and city of every customer.",
      hint: "SELECT name, city FROM customers;",
      solution: "SELECT name, city FROM customers;"
    },
    {
      id: "ex2", title: "2 · WHERE filter",
      task: "List the name and price of every product that costs more than 100.",
      hint: "Filter rows with WHERE price > 100.",
      solution: "SELECT name, price FROM products WHERE price > 100;"
    },
    {
      id: "ex3", title: "3 · ORDER BY + LIMIT",
      task: "Show the name and price of the 3 most expensive products.",
      hint: "ORDER BY price DESC, then LIMIT 3.",
      solution: "SELECT name, price FROM products ORDER BY price DESC LIMIT 3;"
    },
    {
      id: "ex4", title: "4 · JOIN two tables",
      task: "For every order, show the order id and the ordering customer's name.",
      hint: "JOIN orders to customers on customer_id.",
      solution: "SELECT orders.id, customers.name FROM orders JOIN customers ON orders.customer_id = customers.id;"
    },
    {
      id: "ex5", title: "5 · GROUP BY aggregate",
      task: "For each product, show its name and the total quantity ever ordered.",
      hint: "JOIN orders to products, GROUP BY product name, SUM(qty).",
      solution: "SELECT products.name, SUM(orders.qty) AS total_qty FROM orders JOIN products ON orders.product_id = products.id GROUP BY products.name;"
    },
    {
      id: "ex6", title: "6 · HAVING filter",
      task: "Show the name and total revenue (qty × price) of products whose total revenue exceeds 2000.",
      hint: "Aggregate first, then filter groups with HAVING revenue > 2000.",
      solution: "SELECT products.name, SUM(orders.qty * products.price) AS revenue FROM orders JOIN products ON orders.product_id = products.id GROUP BY products.name HAVING revenue > 2000;"
    },
    {
      id: "ex7", title: "7 · Subquery",
      task: "List the names of customers who bought at least one product in the 'Computers' category.",
      hint: "Use WHERE id IN (SELECT ...) to find the customer ids first.",
      solution: "SELECT name FROM customers WHERE id IN (SELECT customer_id FROM orders JOIN products ON orders.product_id = products.id WHERE products.category = 'Computers');"
    },
    {
      id: "ex8", title: "8 · CTE",
      task: "With a CTE, find customers who placed more than 2 orders: show name and order count.",
      hint: "WITH counts AS (...) counts orders per customer, then join back to customers.",
      solution: "WITH counts AS (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id) SELECT customers.name, counts.n FROM counts JOIN customers ON counts.customer_id = customers.id WHERE counts.n > 2;"
    },
    {
      id: "ex9", title: "9 · Window function",
      task: "Rank products by price within each category: show name, category, price, and price_rank.",
      hint: "RANK() OVER (PARTITION BY category ORDER BY price DESC).",
      solution: "SELECT name, category, price, RANK() OVER (PARTITION BY category ORDER BY price DESC) AS price_rank FROM products;"
    },
    {
      id: "ex10", title: "10 · CASE + dates",
      task: "For 2026 orders, show the order id, status, and a period label: 'recent' when order_date is on/after 2026-06-01, else 'earlier'.",
      hint: "CASE WHEN order_date >= '2026-06-01' THEN 'recent' ELSE 'earlier' END AS period.",
      solution: "SELECT id, status, CASE WHEN order_date >= '2026-06-01' THEN 'recent' ELSE 'earlier' END AS period FROM orders WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01';"
    }
  ];

  /* ---------- state ---------- */
  var SQL = null;      // sql.js module
  var db = null;       // current user database
  var engineReady = false;

  function $(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function setStatus(msg, isError) {
    var el = $("sql-status");
    el.textContent = msg;
    el.className = "mt-3 font-mono text-[0.7rem] " + (isError ? "text-red-400" : "text-cyan");
  }

  function renderTable(container, result) {
    var html = '<div class="overflow-x-auto rounded-lg border border-paper/10"><table class="w-full min-w-[24rem] border-collapse text-sm">';
    html += "<thead><tr>" + result.columns.map(function (c) {
      return '<th scope="col" class="border-b border-paper/15 bg-void/60 px-3 py-2 text-left font-mono text-[0.68rem] uppercase tracking-[0.12em] text-gold">' + esc(c) + "</th>";
    }).join("") + "</tr></thead><tbody>";
    result.values.forEach(function (row, ri) {
      html += '<tr class="' + (ri % 2 ? "bg-paper/[0.02]" : "") + '">' + row.map(function (v) {
        return '<td class="border-b border-paper/5 px-3 py-2 font-mono text-[0.78rem] text-paper">' + esc(v) + "</td>";
      }).join("") + "</tr>";
    });
    html += "</tbody></table></div>";
    html += '<p class="mt-2 font-mono text-[0.65rem] text-muted">' + result.values.length + " row" + (result.values.length === 1 ? "" : "s") + "</p>";
    container.innerHTML = html;
  }

  function renderResults(sets) {
    var out = $("sql-results");
    out.innerHTML = "";
    if (!sets || !sets.length) {
      out.innerHTML = '<p class="text-sm text-muted">Query ran — no result rows (statement did not return data).</p>';
      return;
    }
    sets.forEach(function (r, i) {
      var wrap = document.createElement("div");
      if (sets.length > 1) {
        var h = document.createElement("p");
        h.className = "mb-2 font-mono text-[0.65rem] uppercase tracking-[0.14em] text-muted";
        h.textContent = "Result " + (i + 1);
        wrap.appendChild(h);
      }
      var tw = document.createElement("div");
      renderTable(tw, r);
      wrap.appendChild(tw);
      out.appendChild(wrap);
      if (i < sets.length - 1) {
        var hr = document.createElement("div");
        hr.className = "my-4 border-t border-paper/10";
        out.appendChild(hr);
      }
    });
  }

  function pushHistory(sql, ok) {
    try {
      var key = "il_sql_history";
      var h = JSON.parse(localStorage.getItem(key) || "[]");
      h.unshift({ sql: sql, ts: Date.now(), ok: !!ok });
      h = h.slice(0, 30);
      localStorage.setItem(key, JSON.stringify(h));
      renderHistory();
    } catch (e) { /* storage unavailable — fine */ }
  }

  function renderHistory() {
    var list = $("sql-history");
    list.innerHTML = "";
    var h = [];
    try { h = JSON.parse(localStorage.getItem("il_sql_history") || "[]"); } catch (e) {}
    if (!h.length) {
      list.innerHTML = '<li class="text-sm text-muted">No queries yet.</li>';
      return;
    }
    h.forEach(function (item) {
      var li = document.createElement("li");
      var b = document.createElement("button");
      b.type = "button";
      b.className = "w-full rounded-md border border-paper/10 px-3 py-2 text-left font-mono text-[0.7rem] text-muted hover:border-cyan/40 hover:text-paper";
      b.textContent = (item.ok ? "✓ " : "✗ ") + item.sql.replace(/\s+/g, " ").slice(0, 90);
      b.setAttribute("aria-label", "Restore query: " + item.sql.slice(0, 120));
      b.addEventListener("click", function () { $("sql-editor").value = item.sql; $("sql-editor").focus(); });
      li.appendChild(b);
      list.appendChild(li);
    });
  }

  function runQuery() {
    var sql = $("sql-editor").value.trim();
    if (!sql) { setStatus("Type a query first.", true); return; }
    if (!engineReady || !db) { setStatus("Engine not ready yet.", true); return; }
    var t0 = performance.now();
    try {
      var sets = db.exec(sql);
      renderResults(sets);
      var ms = (performance.now() - t0).toFixed(1);
      setStatus("OK · " + sets.length + " statement" + (sets.length === 1 ? "" : "s") + " · " + ms + " ms", false);
      pushHistory(sql, true);
    } catch (err) {
      $("sql-results").innerHTML = '<pre class="rounded-lg border border-red-500/30 bg-red-950/20 p-4 font-mono text-[0.78rem] text-red-300" role="alert">' + esc(err && err.message ? err.message : String(err)) + "</pre>";
      setStatus("Error — see message above.", true);
      pushHistory(sql, false);
    }
  }

  function newSeededDb() {
    var d = new SQL.Database();
    d.exec(SEED_SQL);
    return d;
  }

  function loadSample() {
    if (!engineReady) return;
    db = newSeededDb();
    var t = db.exec("SELECT (SELECT COUNT(*) FROM customers) AS customers, (SELECT COUNT(*) FROM products) AS products, (SELECT COUNT(*) FROM orders) AS orders;");
    renderResults(t);
    setStatus("Sample dataset loaded: customers, products, orders.", false);
  }

  function resetDb() {
    if (!engineReady) return;
    db = new SQL.Database();
    $("sql-results").innerHTML = '<p class="text-sm text-muted">Database reset — empty. Run CREATE TABLE, or load the sample dataset.</p>';
    setStatus("Database reset to empty.", false);
  }

  /* ---------- exercise checker: compare result sets, not query text ---------- */
  function normVal(v) { return v === null || v === undefined ? "NULL" : String(v); }

  function checkExercise(ex) {
    var userSql = $("sql-editor").value.trim();
    var out = $("ex-result");
    if (!userSql) { out.innerHTML = '<p class="text-sm text-muted">Write your query in the editor first, then check.</p>'; return; }
    if (!engineReady) { out.innerHTML = '<p class="text-sm text-red-300">Engine not ready.</p>'; return; }
    try {
      var d1 = newSeededDb(), d2 = newSeededDb();
      var expected = d1.exec(ex.solution);
      var actual = d2.exec(userSql);
      d1.close(); d2.close();
      if (!expected.length || !actual.length) {
        out.innerHTML = '<p class="text-sm text-red-300">✗ Your query returned no result set. The exercise needs a SELECT that returns rows.</p>';
        return;
      }
      var e = expected[expected.length - 1], a = actual[actual.length - 1];
      var eCols = e.columns.map(function (c) { return c.toLowerCase(); });
      var aCols = a.columns.map(function (c) { return c.toLowerCase(); });
      var colsOk = eCols.length === aCols.length && eCols.every(function (c, i) { return c === aCols[i]; });
      if (!colsOk) {
        out.innerHTML = '<p class="text-sm text-red-300">✗ Column mismatch.<br>Expected columns: <code class="text-paper">' + esc(e.columns.join(", ")) + "</code><br>Your columns: <code class=\"text-paper\">" + esc(a.columns.join(", ")) + "</code></p>";
        return;
      }
      function multiset(rows) {
        return rows.map(function (r) { return r.map(normVal).join("\u0001"); }).sort();
      }
      var em = multiset(e.values), am = multiset(a.values);
      var rowsOk = em.length === am.length && em.every(function (r, i) { return r === am[i]; });
      if (rowsOk) {
        out.innerHTML = '<p class="text-sm text-emerald-300">✓ Correct — ' + a.values.length + " row" + (a.values.length === 1 ? "" : "s") + ' match the expected result set.</p>';
      } else {
        out.innerHTML = '<p class="text-sm text-red-300">✗ Row mismatch — expected ' + em.length + " row" + (em.length === 1 ? "" : "s") + ", your query returned " + am.length + ". Check your filters, joins, or aggregates.</p>";
      }
    } catch (err) {
      out.innerHTML = '<pre class="rounded-lg border border-red-500/30 bg-red-950/20 p-3 font-mono text-[0.75rem] text-red-300" role="alert">' + esc(err && err.message ? err.message : String(err)) + "</pre>";
    }
  }

  function renderExercises() {
    var nav = $("ex-nav"), panel = $("ex-panel");
    EXERCISES.forEach(function (ex, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "ex-tab w-full rounded-md border border-paper/10 px-3 py-2 text-left font-mono text-[0.7rem] text-muted hover:border-cyan/40 hover:text-paper" + (i === 0 ? " border-cyan/50 text-paper" : "");
      b.textContent = ex.title;
      b.setAttribute("aria-selected", i === 0 ? "true" : "false");
      b.setAttribute("role", "tab");
      b.addEventListener("click", function () { selectExercise(i); });
      nav.appendChild(b);
    });
    function selectExercise(i) {
      var tabs = nav.querySelectorAll(".ex-tab");
      tabs.forEach(function (t, j) {
        t.setAttribute("aria-selected", j === i ? "true" : "false");
        t.classList.toggle("border-cyan/50", j === i);
        t.classList.toggle("text-paper", j === i);
      });
      var ex = EXERCISES[i];
      panel.innerHTML =
        '<h3 class="font-display text-base text-paper">' + esc(ex.title) + "</h3>" +
        '<p class="mt-2 text-sm text-muted">' + esc(ex.task) + "</p>" +
        '<details class="mt-3"><summary class="cursor-pointer font-mono text-[0.7rem] uppercase tracking-[0.14em] text-cyan">Hint</summary>' +
        '<p class="mt-2 font-mono text-[0.75rem] text-muted">' + esc(ex.hint) + "</p></details>" +
        '<div class="mt-4 flex flex-wrap gap-2">' +
        '<button type="button" id="ex-check" class="inline-flex h-10 items-center rounded-lg bg-paper px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-void">Check my query</button>' +
        '<button type="button" id="ex-fill" class="inline-flex h-10 items-center rounded-lg border border-paper/15 px-4 font-display text-[0.65rem] uppercase tracking-[0.14em] text-paper">Show solution</button>' +
        "</div>" +
        '<div id="ex-result" class="mt-3" aria-live="polite"></div>';
      $("ex-check").addEventListener("click", function () { checkExercise(ex); });
      $("ex-fill").addEventListener("click", function () { $("sql-editor").value = ex.solution; $("sql-editor").focus(); });
    }
    selectExercise(0);
  }

  /* ---------- boot ---------- */
  function failBoot(msg) {
    var banner = $("sql-engine-banner");
    banner.className = "rounded-xl border border-red-500/40 bg-red-950/20 p-4 text-sm text-red-200";
    banner.textContent = msg;
    ["sql-run", "sql-sample", "sql-reset"].forEach(function (id) { $(id).disabled = true; });
    setStatus("Engine failed to load.", true);
  }

  function boot() {
    renderExercises();
    renderHistory();
    if (typeof initSqlJs !== "function") {
      failBoot("Could not load the SQL engine (sql.js). You may be offline — the console needs to fetch the SQLite WebAssembly build from the CDN once. No fake results are shown; the console is disabled until the engine loads.");
      return;
    }
    initSqlJs({ locateFile: function (f) { return SQLJS_BASE + f; } }).then(function (mod) {
      SQL = mod;
      db = new SQL.Database();
      engineReady = true;
      var v = db.exec("SELECT sqlite_version();")[0].values[0][0];
      var banner = $("sql-engine-banner");
      banner.className = "rounded-xl border border-emerald-500/30 bg-emerald-950/20 p-4 text-sm text-emerald-200";
      banner.innerHTML = "SQLite engine running in your browser — nothing leaves your device. <span class=\"font-mono text-[0.7rem] text-muted\">SQLite " + esc(v) + " · sql.js " + esc(SQLJS_VERSION) + "</span>";
      setStatus("Engine ready. Load the sample dataset or start writing SQL.", false);
    }).catch(function (err) {
      failBoot("The SQL engine failed to initialize: " + (err && err.message ? err.message : err) + ". Check your connection and reload.");
    });
  }

  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", function () {
    $("sql-run").addEventListener("click", runQuery);
    $("sql-sample").addEventListener("click", loadSample);
    $("sql-reset").addEventListener("click", resetDb);
    $("sql-clear-history").addEventListener("click", function () {
      try { localStorage.removeItem("il_sql_history"); } catch (e) {}
      renderHistory();
    });
    $("sql-editor").addEventListener("keydown", function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") { ev.preventDefault(); runQuery(); }
    });
    boot();
  });
  }

  /* expose for node-based verification of the checker */
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { SEED_SQL: SEED_SQL, EXERCISES: EXERCISES, SQLJS_VERSION: SQLJS_VERSION };
  }
})();
