# Fix quiz distributions for M28/M29/M30 + numeric corrections, then validate
import re
p = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/build_a.py"
s = open(p).read()

def set_quiz(s, mod_id, new_items):
    # replace quiz array inside module mod_id region
    start = s.index(mod_id)
    next_m = s.index('MODULES', start) if False else len(s)
    # find next 'M3x = ' marker after start
    m = re.search(r'\nM\d\d = \{"id": "IL26-M', s[start+10:])
    end = start + 10 + m.start() if m else len(s)
    region = s[start:end]
    pat = re.compile(r'"quiz": \[.*?\](?=,\s*\n "drills")', re.S)
    assert pat.search(region), mod_id
    region2 = pat.sub(lambda mm: '"quiz": [' + new_items + ']', region, count=1)
    return s[:start] + region2 + s[end:]

q28 = '''
  {"q": "Simplify: (5^2)^3 / 5^4.", "choices": ["5^6", "5^2 = 25", "5^10", "5"], "answer": 1, "explain": "(5^2)^3 = 5^6; 5^6/5^4 = 5^2 = 25."},
  {"q": "10,000 rows grow 5% per week. Rows after 10 weeks?", "choices": ["15,000", "16,000", "16,289", "16,500"], "answer": 2, "explain": "10,000 * 1.05^10 = 10,000 * 1.6289 = 16,289."},
  {"q": "Solve: 2^(3x) = 64.", "choices": ["x = 2", "x = 3", "x = 4", "x = 6"], "answer": 0, "explain": "64 = 2^6, so 3x = 6, x = 2."},
  {"q": "log3(27) + log3(1/3) = ?", "choices": ["3", "0", "4", "2"], "answer": 3, "explain": "log3(27)=3, log3(1/3)=-1; 3 + (-1) = 2."},
  {"q": "A value halves every 4 years. Fraction remaining after 12 years?", "choices": ["1/2", "1/4", "1/8", "1/16"], "answer": 2, "explain": "12/4 = 3 half-lives: (1/2)^3 = 1/8."},
  {"q": "Why is a log-scale y-axis used for a viral-growth chart?", "choices": ["It makes exponential growth a straight line so growth rates are comparable.", "It hides the growth.", "It is required for all time series.", "It converts percents to counts."], "answer": 0, "explain": "On a log axis, exponentials linearize; equal slopes = equal growth rates."},
  {"q": "Solve ln(x) = 2.", "choices": ["x = 2e", "x = ln 2", "x = 100", "x = e^2 ~ 7.39"], "answer": 3, "explain": "ln(x)=2 means x = e^2 = 7.389..."},
  {"q": "200,000 emails decay 3%/month. Remaining after 12 months (nearest)?", "choices": ["128,000", "138,760", "164,000", "200,000"], "answer": 1, "explain": "200,000 * 0.97^12 = 200,000 * 0.6938 = 138,760."},'''

q29 = '''
  {"q": "Evaluate sum_{i=1}^{5} 3i.", "choices": ["45", "30", "15", "60"], "answer": 0, "explain": "3 * (1+2+3+4+5) = 3*15 = 45."},
  {"q": "sum_{i=1}^{n} i = n(n+1)/2. What is sum_{i=1}^{50} i?", "choices": ["2,500", "1,275", "1,250", "1,326"], "answer": 1, "explain": "50*51/2 = 1,275."},
  {"q": "Which identity is FALSE?", "choices": ["sum (a_i + b_i) = sum a_i + sum b_i", "sum (c*a_i) = c * sum a_i", "sum (a_i * b_i) = sum a_i * sum b_i", "sum_{i=1}^{n} 1 = n"], "answer": 2, "explain": "Products do not distribute over sums that way; the other three are the linearity of summation."},
  {"q": "SQL: revenue has some NULLs. How do SUM(revenue) and SUM(COALESCE(revenue,0)) compare?", "choices": ["Equal - NULLs are skipped either way.", "First treats NULLs as zero.", "Both count NULLs as rows.", "First skips NULLs; equal only if no NULLs present."], "answer": 3, "explain": "SUM ignores NULLs; COALESCE zeroes them. Results differ exactly when NULLs exist."},
  {"q": "Population variance of [2, 4, 4, 4, 5, 5, 7, 9]?", "choices": ["4", "4.57", "5", "3.5"], "answer": 0, "explain": "Mean = 5. Squared deviations: 9+1+1+1+0+0+4+16 = 32. 32/8 = 4."},
  {"q": "Geometric series: 1 + 2 + 4 + 8 + 16 = ?", "choices": ["30", "31", "32", "15"], "answer": 1, "explain": "(1-2^5)/(1-2) = 31."},
  {"q": "sum x_i^2 - n*(x-bar)^2 computes what?", "choices": ["The mean.", "The range.", "Sum of squared deviations from the mean.", "The sum of absolute deviations."], "answer": 2, "explain": "It is the one-pass identity for sum (x_i - x-bar)^2."},
  {"q": "In pandas, when does df['x'].sum() diverge from a naive row loop in sigma notation?", "choices": ["They never diverge.", "Only for string columns.", "Only for empty frames.", "When NaNs are present: pandas skips NaN by default like SQL skips NULL."], "answer": 3, "explain": "pandas .sum() skips NaN by default (skipna=True), mirroring SQL's NULL behavior."},'''

q30 = '''
  {"q": "Set A has 60 members, B has 45, intersection 30. Union size?", "choices": ["105", "135", "75", "45"], "answer": 2, "explain": "60 + 45 - 30 = 75 (inclusion-exclusion)."},
  {"q": "Which is equivalent to NOT (premium AND active)?", "choices": ["(NOT premium) OR (NOT active)", "(NOT premium) AND (NOT active)", "premium OR active", "NOT premium AND active"], "answer": 0, "explain": "De Morgan: NOT(A AND B) = (NOT A) OR (NOT B)."},
  {"q": "customers LEFT JOIN orders where one customer has 3 orders: that customer contributes how many rows?", "choices": ["1", "0", "2", "3"], "answer": 3, "explain": "LEFT JOIN fans out on right-side duplicates: 3 matching order rows."},
  {"q": "(A AND B) OR C with A=F, B=F, C=T evaluates to?", "choices": ["FALSE", "TRUE", "NULL", "UNKNOWN"], "answer": 1, "explain": "(F AND F) = F; F OR T = T."},
  {"q": "Cohort 'purchased in Q3 but never refunded' is which set operation?", "choices": ["Union", "Intersection", "Set difference", "Cartesian product"], "answer": 2, "explain": "Q3 purchasers minus refunded users = EXCEPT / set difference."},
  {"q": "SQL precedence: NOT a OR b AND c parses as?", "choices": ["(NOT a) OR (b AND c)", "NOT (a OR b) AND c", "(NOT a OR b) AND c", "NOT a OR b OR c"], "answer": 0, "explain": "NOT binds tightest, then AND, then OR: (NOT a) OR (b AND c)."},
  {"q": "INNER JOIN on a key present in both tables returns which set?", "choices": ["Left table fully", "Key intersection", "Key union", "Cartesian product"], "answer": 1, "explain": "INNER JOIN keeps only rows whose keys appear in both tables - the intersection."},
  {"q": "200 leads: 120 qualified, 90 contacted, 50 both. Qualified but not contacted?", "choices": ["50", "40", "120", "70"], "answer": 3, "explain": "Set difference: 120 - 50 = 70."},'''

s = set_quiz(s, 'M28 = {"id": "IL26-M28"', q28)
s = set_quiz(s, 'M29 = {"id": "IL26-M29"', q29)
s = set_quiz(s, 'M30 = {"id": "IL26-M30"', q30)

# Numeric corrections
s = s.replace("round(np.log1p(rev).mean(), 3)) # 3.029", "round(np.log1p(rev).mean(), 3)) # 3.298")
s = s.replace("round(np.expm1(np.log1p(rev).mean()), 1))  # 19.7", "round(np.expm1(np.log1p(rev).mean()), 1))  # 26.0")
s = s.replace("(19.7) is the honest 'typical' value here.", "(26.0) is the honest 'typical' value here.")
s = s.replace("print(mean, round(var_def,4), round(var_short,4))  # 18.0 151.3333 151.3333",
              "print(mean, round(var_def,4), round(var_short,4))  # 18.0 151.6667 151.6667")
s = s.replace("# Both formulas agree: 151.33 (population variance; divide by n-1 for sample).",
              "# Both formulas agree: 151.67 (population variance; divide by n-1 for sample).")
s = s.replace('"back": "Mean 18.0, variance 151.33."', '"back": "Mean 18.0, population variance 151.67."')
s = s.replace("(1.0393)^12 - 1 = 58.9%", "(1.0393)^12 - 1 = 58.8%")
open(p, "w").write(s)
print("patched")
