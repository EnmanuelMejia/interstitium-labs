/* Practice wing. Text only. No model calls. */
(function () {
  var items = [{"id":"m1","b":-1.6,"topic":"arithmetic","prompt":"A service handles 240 requests in 60 seconds. What is the rate, in requests per second?","choices":["4","30","180","14400"],"answer":0},{"id":"m2","b":-1.4,"topic":"arithmetic","prompt":"Three of twenty hosts are unhealthy. What fraction is unhealthy?","choices":["3/20","20/3","3%","17/20"],"answer":0},{"id":"m3","b":-1.2,"topic":"arithmetic","prompt":"An error budget allows 10 failures. You have used 4. How many remain?","choices":["6","14","40","2.5"],"answer":0},{"id":"m4","b":-0.8,"topic":"algebra","prompt":"If 2x + 6 = 18, what is x?","choices":["6","12","9","3"],"answer":0},{"id":"m5","b":-0.6,"topic":"algebra","prompt":"A bill is p plus 10%. Which expression is the total?","choices":["1.1p","p + 10","p/10","10p"],"answer":0},{"id":"m6","b":-0.4,"topic":"rates","prompt":"Start at 10 ms. Double it three times. What do you have?","choices":["80 ms","30 ms","40 ms","13 ms"],"answer":0},{"id":"m7","b":0,"topic":"rates","prompt":"p99 is 400 ms and the mean is 40 ms. What is the responsible reading?","choices":["The tail is an order of magnitude slower than the mean","The mean is the user experience","p99 must be a bug because it is larger","They measure the same requests"],"answer":0},{"id":"m8","b":0.2,"topic":"logs","prompt":"log10(1000) equals","choices":["3","10","100","1"],"answer":0},{"id":"m9","b":0.4,"topic":"logs","prompt":"A metric moves from 100 to 1000. In log10 units, the change is","choices":["1","10","900","3"],"answer":0},{"id":"m10","b":0.6,"topic":"probability","prompt":"A fair check fails independently with probability 0.1 twice in a row. The probability both fail is","choices":["0.01","0.2","0.1","0.5"],"answer":0},{"id":"m11","b":0.8,"topic":"probability","prompt":"You page on a positive. Precision is true positives over","choices":["all positives you paged","all real incidents","all hosts","the false negatives"],"answer":0},{"id":"m12","b":1,"topic":"probability","prompt":"A 0.1% error rate on 2,000,000 requests is how many errors?","choices":["2000","200","20","2"],"answer":0},{"id":"m13","b":1.3,"topic":"models","prompt":"A hold-out set that you tune on is no longer","choices":["a test","a sample","numeric","a feature"],"answer":0},{"id":"m14","b":1.5,"topic":"models","prompt":"Standard deviation of a constant column is","choices":["0","1","the mean","undefined only for integers"],"answer":0},{"id":"m15","b":1.7,"topic":"tails","prompt":"An error budget of 0.1% over 30 days of 1,000,000 requests a day allows how many errors in the month?","choices":["30000","3000","1000","300"],"answer":0},{"id":"m16","b":1.9,"topic":"tails","prompt":"If recall is 0.5 and precision is 1, you are","choices":["missing half the real cases and paging no false ones","paging twice as often as you should","perfect","unable to compute F1"],"answer":0},{"id":"m17","b":2.0,"topic":"matrices","prompt":"A (2x3) matrix times a (3x2) matrix gives a matrix of shape","choices":["2x2","3x3","2x3","6x6"],"answer":0},{"id":"m18","b":1.6,"topic":"matrices","prompt":"For any compatible vector v, the identity matrix I satisfies","choices":["Iv = v","Iv = 0","Iv = v^T","Iv = 1"],"answer":0},{"id":"m19","b":1.8,"topic":"matrices","prompt":"The transpose of a (2x3) matrix has shape","choices":["3x2","2x3","3x3","2x2"],"answer":0},{"id":"m20","b":1.4,"topic":"matrices","prompt":"The dot product (1,2) . (3,4) equals","choices":["11","7","10","5"],"answer":0},{"id":"m21","b":1.2,"topic":"matrices","prompt":"The Euclidean length of the vector (3,4) is","choices":["5","7","12","25"],"answer":0},{"id":"m22","b":2.2,"topic":"matrices","prompt":"A square matrix with determinant 0","choices":["has no inverse","is the identity","is always symmetric","has all positive eigenvalues"],"answer":0},{"id":"m23","b":1.4,"topic":"stats","prompt":"The mean of [2, 4, 6] is","choices":["4","6","3","12"],"answer":0},{"id":"m24","b":1.8,"topic":"stats","prompt":"In a right-skewed distribution, the mean is typically ___ the median","choices":["greater than","less than","equal to","unrelated to"],"answer":0},{"id":"m25","b":1.6,"topic":"stats","prompt":"Standard error of the mean shrinks like","choices":["1/sqrt(n)","1/n^2","n","it does not shrink"],"answer":0},{"id":"m26","b":2.0,"topic":"stats","prompt":"About 95% of a normal distribution lies within","choices":["2 standard deviations of the mean","1 standard deviation","the interquartile range","3 medians"],"answer":0},{"id":"m27","b":2.2,"topic":"stats","prompt":"Correlation between two variables","choices":["does not imply causation","proves causation","is always between 0 and 1","requires normality"],"answer":0},{"id":"m28","b":1.6,"topic":"stats","prompt":"The variance of X is defined as","choices":["E[(X - mean)^2]","E[X]^2","the square root of the mean","max(X) - min(X)"],"answer":0},{"id":"m29","b":1.2,"topic":"calculus","prompt":"d/dx of x^2 is","choices":["2x","x^2","2","x"],"answer":0},{"id":"m30","b":1.4,"topic":"calculus","prompt":"Gradient descent steps","choices":["opposite the gradient","along the gradient","perpendicular to the gradient","toward the origin"],"answer":0},{"id":"m31","b":1.8,"topic":"calculus","prompt":"The chain rule says d/dx f(g(x)) equals","choices":["f'(g(x)) * g'(x)","f'(x) * g'(x)","f(g'(x))","f'(g(x)) + g'(x)"],"answer":0},{"id":"m32","b":1.6,"topic":"calculus","prompt":"If gradient descent diverges, the first fix to try is","choices":["a smaller learning rate","a larger learning rate","more layers","less data"],"answer":0},{"id":"m33","b":2.0,"topic":"optimization","prompt":"For a convex function, any local minimum","choices":["is a global minimum","is a saddle point","is a maximum","may be neither"],"answer":0},{"id":"m34","b":2.2,"topic":"optimization","prompt":"An L2 (ridge) penalty on weights","choices":["shrinks weights toward zero","grows weights","makes the loss non-convex","only affects the bias"],"answer":0},{"id":"m35","b":2.4,"topic":"optimization","prompt":"A positive-semidefinite Hessian everywhere means the function is","choices":["convex","concave","linear","discontinuous"],"answer":0},{"id":"m36","b":2.6,"topic":"optimization","prompt":"At a saddle point the Hessian has","choices":["both positive and negative eigenvalues","all positive eigenvalues","all zero eigenvalues","no eigenvalues"],"answer":0},{"id":"m37","b":0.8,"topic":"probability","prompt":"For any event A, P(not A) equals","choices":["1 - P(A)","P(A)^2","P(A)/2","1 + P(A)"],"answer":0},{"id":"m38","b":1.0,"topic":"probability","prompt":"X is Binomial(n=100, p=0.1). Its expected value is","choices":["10","50","5","1"],"answer":0},{"id":"m39","b":1.4,"topic":"probability","prompt":"A 99%-accurate test for a 1-in-1000 condition: a positive result means roughly","choices":["2% chance of the condition","99% chance","95% chance","50% chance"],"answer":0},{"id":"m40","b":1.2,"topic":"probability","prompt":"If each of two independent checks fails with probability 0.1, P(at least one fails) is","choices":["0.19","0.2","0.01","0.1"],"answer":0},{"id":"m41","b":-1.2,"topic":"arithmetic","prompt":"15% of 200 is","choices":["30","15","35","300"],"answer":0},{"id":"m42","b":-0.8,"topic":"algebra","prompt":"If 3x - 7 = 11, then x is","choices":["6","4","18","2"],"answer":0},{"id":"m43","b":-0.6,"topic":"rates","prompt":"Start at 80 ms. Halve it three times. What do you have?","choices":["10 ms","40 ms","20 ms","77 ms"],"answer":0},{"id":"m44","b":0.4,"topic":"logs","prompt":"log2(32) equals","choices":["5","16","6","2"],"answer":0},{"id":"m45","b":1.5,"topic":"tails","prompt":"Traffic doubles every 3 days. After 30 days it has grown by a factor of","choices":["1024","10","60","90"],"answer":0},{"id":"m46","b":1.3,"topic":"models","prompt":"A model great on training data but poor on hold-out data is","choices":["overfitting","underfitting","converged","calibrated"],"answer":0},{"id":"m47","b":-1.0,"topic":"arithmetic","prompt":"Split 50 in the ratio 3:2. The parts are","choices":["30 and 20","25 and 25","35 and 15","40 and 10"],"answer":0},{"id":"m48","b":-0.4,"topic":"algebra","prompt":"If y = 2x + 1 and x = 3, then y is","choices":["7","6","9","5"],"answer":0},{"id":"m49","b":-0.2,"topic":"rates","prompt":"At 5 requests per second for 2 minutes, total requests are","choices":["600","10","300","150"],"answer":0},{"id":"m50","b":0.6,"topic":"logs","prompt":"log10(0.001) equals","choices":["-3","3","-10","0.01"],"answer":0},{"id":"m51","b":1.1,"topic":"probability","prompt":"P(at least one success) for two independent trials equals","choices":["1 - P(no successes)","P(both succeed)","the sum of the two probabilities","always 0.5"],"answer":0},{"id":"m52","b":1.7,"topic":"models","prompt":"Raising a classifier's threshold typically","choices":["raises precision and lowers recall","raises recall and lowers precision","raises both","changes neither"],"answer":0}];
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
