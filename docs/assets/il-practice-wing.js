/* Practice wing. Text only. No model calls. */
(function () {
  var items = [{"id":"m1","b":-1.6,"topic":"arithmetic","prompt":"A service handles 240 requests in 60 seconds. What is the rate, in requests per second?","choices":["4","30","180","14400"],"answer":0},{"id":"m2","b":-1.4,"topic":"arithmetic","prompt":"Three of twenty hosts are unhealthy. What fraction is unhealthy?","choices":["3/20","20/3","3%","17/20"],"answer":0},{"id":"m3","b":-1.2,"topic":"arithmetic","prompt":"An error budget allows 10 failures. You have used 4. How many remain?","choices":["6","14","40","2.5"],"answer":0},{"id":"m4","b":-0.8,"topic":"algebra","prompt":"If 2x + 6 = 18, what is x?","choices":["6","12","9","3"],"answer":0},{"id":"m5","b":-0.6,"topic":"algebra","prompt":"A bill is p plus 10%. Which expression is the total?","choices":["1.1p","p + 10","p/10","10p"],"answer":0},{"id":"m6","b":-0.4,"topic":"rates","prompt":"Start at 10 ms. Double it three times. What do you have?","choices":["80 ms","30 ms","40 ms","13 ms"],"answer":0},{"id":"m7","b":0,"topic":"rates","prompt":"p99 is 400 ms and the mean is 40 ms. What is the responsible reading?","choices":["The tail is an order of magnitude slower than the mean","The mean is the user experience","p99 must be a bug because it is larger","They measure the same requests"],"answer":0},{"id":"m8","b":0.2,"topic":"logs","prompt":"log10(1000) equals","choices":["3","10","100","1"],"answer":0},{"id":"m9","b":0.4,"topic":"logs","prompt":"A metric moves from 100 to 1000. In log10 units, the change is","choices":["1","10","900","3"],"answer":0},{"id":"m10","b":0.6,"topic":"probability","prompt":"A fair check fails independently with probability 0.1 twice in a row. The probability both fail is","choices":["0.01","0.2","0.1","0.5"],"answer":0},{"id":"m11","b":0.8,"topic":"probability","prompt":"You page on a positive. Precision is true positives over","choices":["all positives you paged","all real incidents","all hosts","the false negatives"],"answer":0},{"id":"m12","b":1,"topic":"probability","prompt":"A 0.1% error rate on 2,000,000 requests is how many errors?","choices":["2000","200","20","2"],"answer":0},{"id":"m13","b":1.3,"topic":"models","prompt":"A hold-out set that you tune on is no longer","choices":["a test","a sample","numeric","a feature"],"answer":0},{"id":"m14","b":1.5,"topic":"models","prompt":"Standard deviation of a constant column is","choices":["0","1","the mean","undefined only for integers"],"answer":0},{"id":"m15","b":1.7,"topic":"tails","prompt":"An error budget of 0.1% over 30 days of 1,000,000 requests a day allows how many errors in the month?","choices":["30000","3000","1000","300"],"answer":0},{"id":"m16","b":1.9,"topic":"tails","prompt":"If recall is 0.5 and precision is 1, you are","choices":["missing half the real cases and paging no false ones","paging twice as often as you should","perfect","unable to compute F1"],"answer":0}];
  var bandCopy = {"numerals":"Start on counts, fractions, and rates. The ops-math path is the next reading, not a harder exam.","rates":"Rates and percentages are reliable. Log scales and tails are the fringe.","models":"You can read a metric and a probability. The next gap is the tail and the hold-out.","tails":"The baseline sits in the tail. Use it on a real budget, not as a trophy."};
  var LENGTH = 8;
  var rooms = [
    ["Learn", "/learn/"],
    ["Paths", "/paths/"],
    ["Prep", "/prep/"],
    ["Academy", "/academy/"],
    ["Coach", "/coach/"],
    ["Library", "/library/"]
  ];
  var audit = [
    ["Pace", "Self-paced. No deadlines.", "Held"],
    ["Assistant", "Noah drafts and remembers on the server. This page does not send mail or spend money.", "Partial"],
    ["This wing", "Placement and the bench run here. The frontier turn does not.", "Partial"],
    ["Host", "Tomorrow, at the machine. The disk is not erased from the site.", "Gap"]
  ];
  var readings = [
    { id: 1, host: "edge", rate: 12, errors: 1 },
    { id: 2, host: "core", rate: 40, errors: 0 },
    { id: 3, host: "edge", rate: 9, errors: 4 },
    { id: 4, host: "db", rate: 3, errors: 0 }
  ];

  function el(tag, text) {
    var node = document.createElement(tag);
    if (text != null) node.textContent = text;
    return node;
  }
  function nextItem(theta, used) {
    var open = items.filter(function (item) { return used.indexOf(item.id) < 0; });
    if (!open.length) return null;
    return open.reduce(function (best, item) {
      return Math.abs(item.b - theta) < Math.abs(best.b - theta) ? item : best;
    });
  }
  function bandOf(theta) {
    if (theta < -0.6) return "numerals";
    if (theta < 0.3) return "rates";
    if (theta < 1.1) return "models";
    return "tails";
  }
  function runSql(source) {
    var sql = source.trim().replace(/;+\s*$/, "");
    var match = sql.match(/^select\s+(.+?)\s+from\s+readings(?:\s+where\s+(.+?))?(?:\s+order\s+by\s+(\w+)(?:\s+(asc|desc))?)?$/i);
    if (!match) return { error: "SELECT on readings, with optional WHERE and ORDER BY." };
    var cols = ["id", "host", "rate", "errors"];
    var picked = match[1].trim() === "*" ? cols : match[1].split(",").map(function (c) { return c.trim(); });
    if (picked.some(function (c) { return cols.indexOf(c) < 0; })) return { error: "Unknown column." };
    var rows = readings.slice();
    if (match[2]) {
      var clause = match[2].trim().match(/^(\w+)\s*(>|>=|<|<=|=|!=)\s*(\d+)$/);
      if (!clause || cols.indexOf(clause[1]) < 0) return { error: "WHERE must be one comparison." };
      var n = Number(clause[3]);
      rows = rows.filter(function (row) {
        var left = row[clause[1]];
        if (clause[2] === ">") return left > n;
        if (clause[2] === ">=") return left >= n;
        if (clause[2] === "<") return left < n;
        if (clause[2] === "<=") return left <= n;
        if (clause[2] === "!=") return left !== n;
        return left === n;
      });
    }
    if (match[3]) {
      var key = match[3];
      var dir = (match[4] || "asc").toLowerCase() === "desc" ? -1 : 1;
      rows.sort(function (a, b) { return a[key] > b[key] ? dir : a[key] < b[key] ? -dir : 0; });
    }
    return { columns: picked, rows: rows };
  }

  var nav = document.getElementById("rooms");
  rooms.forEach(function (room) {
    var a = el("a", room[0]);
    a.href = room[1];
    nav.appendChild(a);
    nav.appendChild(document.createTextNode(" "));
  });

  var place = document.getElementById("place");
  var theta = 0, used = [], pick = -1, current = nextItem(0, []);
  function paintPlace() {
    place.textContent = "";
    if (!current) {
      var band = bandOf(theta);
      place.appendChild(el("p", band + ". " + bandCopy[band]));
      return;
    }
    place.appendChild(el("p", (used.length + 1) + " / " + LENGTH + " · " + current.topic));
    place.appendChild(el("h3", current.prompt));
    current.choices.forEach(function (choice, i) {
      var button = el("button", choice);
      button.type = "button";
      button.className = "row";
      button.addEventListener("click", function () {
        pick = i;
        var correct = pick === current.answer;
        theta = Math.max(-2, Math.min(2, theta + (correct ? 0.45 : -0.45)));
        used.push(current.id);
        current = used.length >= LENGTH ? null : nextItem(theta, used);
        paintPlace();
      });
      place.appendChild(button);
    });
  }
  paintPlace();

  var box = document.getElementById("sql");
  box.value = "select host, rate from readings where errors > 0 order by rate desc";
  document.getElementById("run").addEventListener("click", function () {
    var out = document.getElementById("out");
    out.textContent = "";
    var result = runSql(box.value);
    if (result.error) {
      out.appendChild(el("p", result.error));
      return;
    }
    result.rows.forEach(function (row) {
      out.appendChild(el("p", result.columns.map(function (col) { return col + " " + row[col]; }).join(", ")));
    });
    if (!result.rows.length) out.appendChild(el("p", "No rows."));
  });

  var table = document.createElement("table");
  audit.forEach(function (row) {
    var tr = document.createElement("tr");
    row.forEach(function (cell) { tr.appendChild(el("td", cell)); });
    table.appendChild(tr);
  });
  document.getElementById("audit").appendChild(table);
})();
