# Fix quiz answer distributions in build_a.py (must be exactly 2/2/2/2 per module)
import re
p = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/build_a.py"
s = open(p).read()

new_m26_quiz = ''' "quiz": [
  {"q": "What is 120 - 4 * (3 + 5)^2 / 8?", "choices": ["88", "64", "104", "72"], "answer": 0, "explain": "Parentheses: (3+5)=8. Exponent: 8^2=64. Multiply/divide: 4*64=256, 256/8=32. Subtract: 120-32=88."},
  {"q": "A conversion rate goes from 2.0% to 2.5%. Which statement is correct?", "choices": ["A 0.5% increase.", "A 25% relative increase and a 0.5 percentage-point increase.", "A 25 percentage-point increase.", "A 125% relative increase."], "answer": 1, "explain": "Relative change = 0.5/2.0 = 25%; percentage-point change = 2.5 - 2.0 = 0.5 points."},
  {"q": "Which channel has the best click-through rate: A = 7/200, B = 4.1%, C = 0.035?", "choices": ["A at 3.5%", "C at 3.5%", "B at 4.1%", "A and C tie for best"], "answer": 2, "explain": "A = 3.5%, B = 4.1%, C = 3.5%. B wins outright; A and C merely tie for worst."},
  {"q": "60 tickets in 8.5 hours is how many tickets per hour (2 decimals)?", "choices": ["7.50", "6.82", "7.29", "7.06"], "answer": 3, "explain": "60 / 8.5 = 7.0588... = 7.06 tickets/hour."},
  {"q": "Solve for x: 4x - 7 = 25.", "choices": ["x = 4.5", "x = 32", "x = 6", "x = 8"], "answer": 3, "explain": "4x = 32, x = 8. Check: 4*8 - 7 = 25."},
  {"q": "Revenue grows 10% in year 1 and 10% in year 2. Total two-year growth?", "choices": ["20%", "19%", "21%", "22%"], "answer": 2, "explain": "1.10 x 1.10 = 1.21 -> 21%. Percent changes compound; they don't add."},
  {"q": "What is (-3) * (-4) + 10 / (-2)?", "choices": ["-17", "7", "12", "17"], "answer": 1, "explain": "(-3)(-4) = 12; 10/(-2) = -5; 12 + (-5) = 7."},
  {"q": "Solve the proportion 3/4 = x/20.", "choices": ["x = 15", "x = 12", "x = 60", "x = 5"], "answer": 0, "explain": "Cross-multiply: 4x = 60, x = 15."}],'''

new_m27_quiz = ''' "quiz": [
  {"q": "f(x) = 2x - 1, g(x) = x^2. What is g(f(3))?", "choices": ["11", "25", "49", "5"], "answer": 1, "explain": "f(3) = 5, g(5) = 25."},
  {"q": "Slope between (1200, 300) and (2000, 460)?", "choices": ["0.2 leads/dollar", "5 leads/dollar", "160 leads/dollar", "0.8 leads/dollar"], "answer": 0, "explain": "(460-300)/(2000-1200) = 160/800 = 0.2."},
  {"q": "Vertex of y = -2x^2 + 80x - 100?", "choices": ["(40, 500)", "(-20, -700)", "(10, 300)", "(20, 700)"], "answer": 3, "explain": "x = -80/(2*-2) = 20; y = -2(400)+1600-100 = 700."},
  {"q": "Users double every 6 months from 1,000. Users after 18 months?", "choices": ["4,000", "3,000", "8,000", "16,000"], "answer": 2, "explain": "18/6 = 3 doublings: 1,000 -> 2,000 -> 4,000 -> 8,000."},
  {"q": "Residuals alternate -1, 0, -1, 0, +1. What does the pattern suggest?", "choices": ["The model may be the wrong shape; investigate curvature.", "The model fits perfectly.", "More data is needed; nothing can be said.", "The residuals must be re-centered."], "answer": 0, "explain": "Patterned residuals indicate systematic misfit — the true relationship is likely curved."},
  {"q": "Solve log2(x) = 5.", "choices": ["x = 10", "x = 25", "x = 2.5", "x = 32"], "answer": 3, "explain": "log2(x)=5 means 2^5 = x = 32."},
  {"q": "What is the y-intercept of L = 0.2S + 60?", "choices": ["0.2", "60", "300", "1200"], "answer": 1, "explain": "In y = mx + b, the intercept b = 60 (leads at zero spend — a model artifact, not a real measurement)."},
  {"q": "Inverse of f(x) = 3x + 2?", "choices": ["f^-1(x) = x/3 - 2", "f^-1(x) = 3x - 2", "f^-1(x) = (x-2)/3", "f^-1(x) = (x+2)/3"], "answer": 2, "explain": "y = 3x+2 -> swap: x = 3y+2 -> y = (x-2)/3."}],'''

# Replace M26 quiz block: from '"quiz": [' after M26's cards up to the first '],\n "drills"'
# Safer: split on the M27 marker
head, rest = s.split('M27 = {"id": "IL26-M27"', 1)
m26_part, m27_part = rest.split('MODULES += [M26, M27]', 1) if False else (None, None)
# Simpler: locate the two quiz arrays by unique first question
import re
def swap_quiz(s, first_q_marker, new_block):
    i = s.index(first_q_marker)
    qstart = s.rindex('"quiz": [', 0, i)
    # find matching close: the array ends with '}],' before '"drills"'
    j = s.index('"drills"', qstart)
    k = s.rindex(']', 0, j)
    return s[:qstart] + new_block + s[k+1:]

s = swap_quiz(s, '"What is 120 - 4 * (3 + 5)^2 / 8?"', new_m26_quiz)
s = swap_quiz(s, '"f(x) = 2x - 1, g(x) = x^2. What is g(f(3))?"', new_m27_quiz)
open(p, "w").write(s)
print("patched OK")
