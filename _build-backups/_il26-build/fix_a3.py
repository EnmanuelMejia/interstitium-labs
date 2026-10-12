# Fix M33 q4 (botched system) + enforce 2/2/2/2 on M33 quiz
import re
p = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/build_a.py"
s = open(p).read()
start = s.index('M33 = {"id": "IL26-M33"')
end = s.index('MODULES += [M28', start)
region = s[start:end]
pat = re.compile(r'"quiz": \[.*?\](?=,\s*\n "drills")', re.S)
new_items = '''
  {"q": "Dot product of [2,3] and [4,-1]?", "choices": ["5", "11", "8", "6"], "answer": 0, "explain": "2*4 + 3*(-1) = 8 - 3 = 5."},
  {"q": "What does a dot product of 0 mean geometrically?", "choices": ["Parallel.", "Orthogonal (perpendicular).", "Identical vectors.", "Zero vector."], "answer": 1, "explain": "a.b = |a||b|cos(theta) = 0 means theta = 90 degrees."},
  {"q": "(2x3) times (3x2) matrix product has shape?", "choices": ["(3x3)", "(6x6)", "(2x2)", "Undefined"], "answer": 2, "explain": "(m x n)(n x p) = (m x p): (2x2)."},
  {"q": "Solve: x + y = 7, 2x - y = 5.", "choices": ["x=3, y=4", "x=5, y=2", "x=2, y=5", "x=4, y=3"], "answer": 3, "explain": "Add the equations: 3x = 12 -> x = 4, then y = 3. Check: 8-3=5."},
  {"q": "Largest eigenvalue of [[4,2],[2,3]]?", "choices": ["5.562", "4.0", "3.0", "1.438"], "answer": 0, "explain": "l^2 - 7l + 8 = 0 -> l = (7+sqrt(17))/2 = 5.562."},
  {"q": "The normal equations solve for?", "choices": ["Eigenvalues.", "The least-squares beta: X^T X beta = X^T y.", "The determinant.", "The matrix inverse directly."], "answer": 1, "explain": "They minimize ||y - X beta||^2: the projection of y onto the column space of X."},
  {"q": "Two near-duplicate feature columns cause?", "choices": ["Faster training.", "Higher R-squared always.", "Multicollinearity: unstable coefficients.", "Sparser models."], "answer": 2, "explain": "Near-singular X^T X amplifies noise; coefficients swing wildly."},
  {"q": "Cosine similarity range; what does 1 mean?", "choices": ["[0,1]; 1 = identical.", "Any real; 1 = orthogonal.", "[0,inf); 1 = unrelated.", "[-1,1]; 1 = identical direction."], "answer": 3, "explain": "Cosine in [-1,1]; 1 means the vectors point the same way."},'''
assert pat.search(region)
region2 = pat.sub(lambda mm: '"quiz": [' + new_items + ']', region, count=1)
s = s[:start] + region2 + s[end:]
open(p, "w").write(s)
print("M33 quiz fixed")
