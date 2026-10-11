"""Batch 13: Programming & CS Fundamentals — 28 BBG-style visual guides."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bbg_style import *

CAT = "Programming & CS Fundamentals"


def codeblock(c, x, y, lines, w=468, lh=15, fsize=9.5, fill=BOX_BLUE):
    """Mono code panel; y = top. Returns bottom y."""
    h = len(lines) * lh + 16
    y0 = y - h
    c.setFillColor(fill); c.roundRect(x, y0, w, h, 6, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(MONO_FONT, fsize)
    ty = y - 15
    for ln in lines:
        c.drawString(x + 10, ty, ln); ty -= lh
    return y0


def h2(c, x, y, text, size=12):
    c.setFillColor(INK); c.setFont(TITLE_FONT, size)
    c.drawString(x, y, text)
    return y


def pdf_big_o(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Big O Notation\nVisual Guide",
               "How runtime grows with input size —\nthe one idea behind every performance claim.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Growth Curves: The Complexity Zoo",
                       "Shape matters more than constants: compare how each class explodes as n grows.")
    import math
    ox, oy = 110, 190
    c.setStrokeColor(INK); c.setLineWidth(1.5)
    c.line(ox, oy, ox + 380, oy); c.line(ox, oy, ox, oy + 370)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(ox + 360, oy - 18, "n"); c.drawString(ox - 32, oy + 372, "time")
    curves = [("O(1)", GREEN, lambda n: 30),
              ("O(log n)", TEAL, lambda n: 30 * math.log2(n + 1)),
              ("O(2^n)", ACCENT2, lambda n: 1.6 * (2 ** n)),
              ("O(n)", ACCENT, lambda n: 30 * n),
              ("O(n^2)", RED, lambda n: 3.2 * n * n),
              ("O(n log n)", ORANGE, lambda n: 15 * n * math.log2(n + 1))]
    for name, color, f in curves:
        c.setStrokeColor(color); c.setLineWidth(2)
        p = c.beginPath()
        for i in range(0, 101):
            n = i / 10.0
            x = ox + n * 36
            yy = oy + min(f(n), 365)
            if i == 0: p.moveTo(x, yy)
            else: p.lineTo(x, yy)
        c.drawPath(p)
    lx = 72; ly = 150
    c.setFont(BODY_FONT, 9.5)
    for name, color, f in curves:
        c.setStrokeColor(color); c.setLineWidth(3); c.line(lx, ly, lx + 26, ly)
        c.setFillColor(INK); c.drawString(lx + 32, ly - 3, name)
        lx += 78
        if lx > 460: lx = 72; ly -= 16
    note(c, 72, 96, 468, "Same n, wildly different bills: at n=1M, O(n) is a million ops, O(n^2) is a trillion. Pick the shape first, optimize constants later.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Reading Big O: The Three Rules",
                       "Simplify any expression down to its dominant shape.")
    y0 = codeblock(c, 72, y, [
        "  3n^2 + 5n + 100      ->  O(n^2)     # drop lower-order terms",
        "  2n                  ->  O(n)       # drop constants",
        "  O(n) + O(log n)     ->  O(n)       # keep the dominant term",
        "  nested loops n x n  ->  O(n^2)",
        "  loop halves n       ->  O(log n)   # binary search",
        "  recursion 2T(n/2)+n ->  O(n log n) # merge sort",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Rule 1 — drop constants: O(2n) is O(n). Hardware speed is not the algorithm's business.",
        "Rule 2 — drop lower-order terms: for large n, n^2 dwarfs 1000n.",
        "Rule 3 — worst case by default: unless stated, Big O describes the worst-case input.",
        "Log bases don't matter: log2 n and log10 n differ by a constant factor.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Best / Average / Worst Case",
                       "One algorithm, three stories — linear search for target T.")
    # array of cells
    vals = ["a", "b", "T", "d", "e", "f"]
    for i, v in enumerate(vals):
        fill = BOX_GREEN if v == "T" else BOX_BLUE
        box(c, 72 + i * 72, 470, 64, 56, fill, v, "", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 440, "Best case: T is first  ->  O(1).  One comparison and done.")
    c.drawString(72, 422, "Average case: T is anywhere  ->  O(n/2) = O(n).")
    c.drawString(72, 404, "Worst case: T is last or absent  ->  O(n).  Every element checked.")
    y0 = codeblock(c, 72, 360, [
        "  for x in arr:            # linear search",
        "      if x == T: return i   # best: 1 step, worst: n steps",
    ])
    note(c, 72, y0 - 60, 468, "Interviews test worst case; production cares about average case. Know which one you're quoting — and say it out loud.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Amortized Analysis",
                       "Occasional expensive ops, averaged over a long sequence.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y, "Appending to a dynamic array (capacity doubles on fill):")
    costs = [1, 1, 1, 1, 5, 1, 1, 1, 1, 9]
    bx = 72
    for i, k in enumerate(costs):
        h = 20 + k * 14
        fill = BOX_RED if k > 1 else BOX_GREEN
        c.setFillColor(fill); c.roundRect(bx, 300, 40, h, 5, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(BODY_FONT, 8)
        c.drawCentredString(bx + 20, 292, f"push{i+1}")
        bx += 46
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 262, "Most pushes cost 1 (red bars = resize + copy).  Total for n pushes < 3n  ->  O(1) amortized.")
    bullet_list(c, 72, 225, [
        "Aggregate method: bound the total cost of n operations, divide by n.",
        "Amortized O(1) is not worst-case O(1): a single push can still cost O(n).",
        "Real-time systems hate amortization spikes — they need true worst-case bounds.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Space Complexity",
                       "Time gets the glory; memory decides whether it runs at all.")
    rows = [("O(1) extra", "in-place swap, two pointers", BOX_GREEN),
            ("O(log n)", "balanced recursion depth", BOX_TEAL),
            ("O(n)", "copy of input, hash map of n keys", BOX_ORANGE),
            ("O(n^2)", "adjacency matrix for n nodes", BOX_RED)]
    yy = y
    for name, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    y0 = codeblock(c, 72, yy - 10, [
        "  def reverse(arr):          # O(1) extra space",
        "      i, j = 0, len(arr)-1  # two pointers, no copy",
        "      while i < j: arr[i], arr[j] = arr[j], arr[i]; i+=1; j-=1",
    ])
    note(c, 72, y0 - 60, 468, "Count auxiliary space (beyond the input). Recursion depth counts — a 'clever' recursive O(n) can hide O(n) stack space.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Big-O Gotchas",
                       "Where smart people misread the notation.")
    bullet_list(c, 72, y, [
        "Small n: constants dominate. O(n^2) with tiny constants beats O(n log n) for n under 100.",
        "Hidden constants: O(n) with a 10-second constant loses to O(n^2) with a 1ms one — at small n.",
        "Big O is an upper bound. Tight bound = Big Theta; lower bound = Big Omega.",
        "'O(n) time, O(1) space' is the gold standard for array problems — aim for it.",
        "Amortized != average != worst case. Name the analysis you're using.",
        "n must be defined: O(n*m) for an n x m grid, O(V+E) for graphs.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Big O Notation — Remember",
                 ["Growth shape beats constants: compare O(n) vs O(n^2) before micro-optimizing.",
                  "Simplify with three rules: drop constants, drop lower-order terms, keep the dominant term.",
                  "Quote best/average/worst explicitly — linear search is O(1), O(n), O(n) across the three.",
                  "Amortized O(1) (dynamic array append) averages rare expensive resizes over many cheap ops.",
                  "Space counts too: recursion depth and copies are real memory costs."],
                 pg)
    c.save(); print("wrote", path)


def pdf_arrays(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Arrays\nVisual Guide",
               "Contiguous memory, O(1) indexing —\nthe foundation every other structure is built on.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Contiguous Memory Layout",
                       "Elements sit side by side; the index IS the address math.")
    vals = ["12", "7", "42", "9"]
    for i, v in enumerate(vals):
        box(c, 72 + i * 110, 440, 100, 64, BOX_BLUE, v, f"idx {i}", font_size=13)
        c.setFillColor(MUTED); c.setFont(MONO_FONT, 8.5)
        c.drawCentredString(72 + i * 110 + 50, 428, f"0x100{i*4:X}")
    y0 = codeblock(c, 72, 400, [
        "  address(i) = base + i * elem_size",
        "  arr[2] -> 0x1000 + 2*4 = 0x1008   # one multiply-add: O(1)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "No pointers between elements — the CPU computes locations arithmetically.",
        "Fixed size at allocation: the block must be contiguous, so growing means moving.",
        "elem_size is known at compile time (int=4B, double=8B) — hence the simple math.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Operation Costs",
                       "What each operation really pays.")
    ops = [("Read arr[i]", "O(1)", "address math", BOX_GREEN),
           ("Append (space)", "O(1)*", "write at end", BOX_GREEN),
           ("Insert at k", "O(n)", "shift k..n right", BOX_ORANGE),
           ("Delete at k", "O(n)", "shift k+1..n left", BOX_ORANGE),
           ("Search (unsorted)", "O(n)", "scan", BOX_RED)]
    yy = y
    for name, cost, desc, fill in ops:
        box(c, 72, yy - 52, 468, 56, fill, f"{name}  —  {cost}", desc, font_size=11.5)
        yy -= 70
    note(c, 72, 130, 468, "*Append is O(1) amortized for dynamic arrays (see step 4) — but O(n) worst case when a resize fires.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Cache Locality: The Hidden Superpower",
                       "Sequential access rides the CPU cache; random access stalls it.")
    for i in range(8):
        box(c, 72 + i * 58, 470, 52, 54, BOX_GREEN, f"a[{i}]", "", font_size=10)
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.rect(66, 462, 240, 70, fill=0, stroke=1)
    c.rect(306, 462, 240, 70, fill=0, stroke=1)
    c.setFillColor(ACCENT); c.setFont(BODY_FONT, 10)
    c.drawCentredString(186, 446, "cache line 1 (64 B)")
    c.drawCentredString(426, 446, "cache line 2 (64 B)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 410, "Reading a[0] pulls the whole 64-byte line into L1 — a[1..15] are then nearly free.")
    bullet_list(c, 72, 375, [
        "Spatial locality: neighbors arrive together — linear scans are 10-100x faster than pointer hops.",
        "Why arrays beat linked lists in practice despite identical Big O for scans.",
        "Strided access (every 16th element) defeats the cache — same O(n), far slower wall-clock.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Dynamic Arrays: Growth Strategy",
                       "Capacity doubles when full — copies are rare by design.")
    # before
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Before push (cap=4, size=4):")
    for i in range(4):
        box(c, 72 + i * 62, y - 60, 56, 50, BOX_BLUE, f"{i+1}", "", font_size=11)
    arrow(c, 330, y - 35, 380, y - 35, color=RED, width=2, label="push -> full!")
    # after
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y - 110, "After: allocate 8, copy 4, then push:")
    for i in range(5):
        box(c, 72 + i * 62, y - 170, 56, 50, BOX_GREEN, f"{i+1}", "", font_size=11)
    for i in range(5, 8):
        box(c, 72 + i * 62, y - 170, 56, 50, BOX_TEAL, "·", "free", font_size=11)
    y0 = codeblock(c, 72, y - 200, [
        "  total copy cost for n pushes: 1+2+4+...+n/2 < n",
        "  => O(1) amortized per push      # doubling is the trick",
    ])
    note(c, 72, y0 - 60, 468, "Grow by 1.5x (not 2x) if memory is tight — fewer wasted slots, slightly more copies. Python lists over-allocate ~1.125x.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Insert & Delete: The Shift Tax",
                       "Everything after the hole moves — that's the O(n).")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Insert X at index 1:")
    vals = ["a", "X", "b", "c", "d"]
    for i, v in enumerate(vals):
        fill = BOX_ORANGE if v == "X" else BOX_BLUE
        box(c, 72 + i * 80, y - 70, 70, 56, fill, v, "", font_size=12)
    arrow(c, 140, y - 42, 210, y - 42, color=RED, width=2, label="shift right")
    arrow(c, 300, y - 42, 380, y - 42, color=RED, width=2, label="shift right")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y - 130, "Delete at index 2:")
    vals2 = ["a", "b", "d"]
    for i, v in enumerate(vals2):
        box(c, 72 + i * 80, y - 200, 70, 56, BOX_BLUE, v, "", font_size=12)
    arrow(c, 300, y - 172, 220, y - 172, color=RED, width=2, label="shift left")
    bullet_list(c, 72, y - 250, [
        "Insert/delete at the END is O(1); at the FRONT is O(n) — design around this.",
        "Swap-with-last trick: unordered delete in O(1) by overwriting with the tail.",
        "Frequent middle inserts? That's the linked list's home turf.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Array Pitfalls",
                       "Small mistakes, big crashes.")
    bullet_list(c, 72, y, [
        "Off-by-one: valid indices are 0..n-1. The #1 bug in array code — draw the fenceposts.",
        "Bounds are unchecked in C: arr[100] on a 10-array reads garbage or segfaults.",
        "Stack overflow: a 10MB array as a local variable blows the typical 8MB stack — malloc it.",
        "0-based vs 1-based: know your language; mixing them corrupts index math.",
        "ArrayList vs LinkedList: default to ArrayList — cache locality wins until proven otherwise.",
        "Multidimensional arrays are still flat: a[i][j] = base + (i*cols + j) * size.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Arrays — Remember",
                 ["Contiguous memory + index math (base + i*size) gives O(1) random access.",
                  "Sequential scans exploit cache lines — arrays beat pointer structures in wall-clock time.",
                  "Dynamic arrays double capacity on fill: O(1) amortized append, O(n) worst-case resize.",
                  "Insert/delete in the middle costs O(n) shifts; swap-with-last gives O(1) unordered delete.",
                  "Watch off-by-ones, unchecked bounds, and stack allocation of big arrays."],
                 pg)
    c.save(); print("wrote", path)


def pdf_linked_lists(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Linked Lists\nVisual Guide",
               "Nodes and pointers —\nO(1) surgery at the cost of O(n) reach.",
               CAT, None); pg += 1

    def draw_chain(cy, vals, x0=72, w=84, gap=44, highlight=None):
        x = x0
        for i, v in enumerate(vals):
            fill = BOX_ORANGE if i == highlight else BOX_BLUE
            c.setFillColor(fill); c.roundRect(x, cy, w, 52, 8, fill=1, stroke=0)
            c.setStrokeColor(INK); c.setLineWidth(1.2); c.roundRect(x, cy, w, 52, 8, fill=0, stroke=1)
            c.line(x + w / 2, cy, x + w / 2, cy + 52)
            c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
            c.drawCentredString(x + w / 4, cy + 21, str(v))
            c.setFont(BODY_FONT, 9); c.setFillColor(MUTED)
            c.drawCentredString(x + 3 * w / 4, cy + 21, "next")
            if i < len(vals) - 1:
                arrow(c, x + w, cy + 26, x + w + gap, cy + 26, color=ACCENT, width=1.8)
            x += w + gap
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
        c.drawString(x + 4, cy + 22, "NULL")

    y = section_header(c, 1, 6, "Anatomy of a Node",
                       "Data plus a pointer to the next node — the list is a chain of handshakes.")
    draw_chain(470, ["A", "B", "C", "D"])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Each node: [ data | next* ].  The list only stores a head pointer — reach node k by hopping k times: O(n).")
    y0 = codeblock(c, 72, 385, [
        "  struct Node { int data; Node* next; };",
        "  Node* head -> [A|*] -> [B|*] -> [C|*] -> [D|*] -> NULL",
    ])
    note(c, 72, y0 - 60, 468, "No contiguous block needed: nodes scatter across the heap. Growing the list never copies — but you lose cache locality.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Singly vs Doubly Linked",
                       "One direction is cheap; two directions cost a pointer per node.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Singly: forward only")
    draw_chain(y - 70, ["A", "B", "C"], x0=72, w=80, gap=40)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y - 140, "Doubly: forward + back (prev pointer)")
    x = 72
    for i, v in enumerate(["A", "B", "C"]):
        c.setFillColor(BOX_TEAL); c.roundRect(x, y - 210, 80, 52, 8, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.roundRect(x, y - 210, 80, 52, 8, fill=0, stroke=1)
        c.line(x + 27, y - 210, x + 27, y - 158); c.line(x + 53, y - 210, x + 53, y - 158)
        c.setFillColor(INK); c.setFont(TITLE_FONT, 10)
        c.drawCentredString(x + 40, y - 184, v)
        if i < 2:
            arrow(c, x + 80, y - 172, x + 120, y - 172, color=ACCENT, width=1.8)
            arrow(c, x + 120, y - 196, x + 80, y - 196, color=TEAL, width=1.8)
        x += 120
    bullet_list(c, 72, y - 270, [
        "Doubly: O(1) delete given the node (no predecessor hunt); singly needs the previous node.",
        "Cost: one extra pointer per node + more careful surgery (two links to rewire).",
        "Circular variants: tail.next = head — handy for round-robin schedulers.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Pointer Surgery: Insert & Delete",
                       "Rewire in the right order — or lose the rest of the list.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Insert X after B:")
    draw_chain(y - 70, ["A", "B", "D"], x0=72, w=76, gap=36)
    box(c, 300, y - 150, 76, 52, BOX_ORANGE, "X", "new", font_size=11)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawString(72, y - 120, "1. X.next = B.next   (point new node at D FIRST)")
    c.drawString(72, y - 138, "2. B.next = X       (then swing B forward)")
    arrow(c, 338, y - 124, 420, y - 60, color=RED, width=1.8)
    arrow(c, 250, y - 132, 300, y - 124, color=RED, width=1.8)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y - 190, "Delete C (have its predecessor B):")
    draw_chain(y - 260, ["A", "B", "D"], x0=72, w=76, gap=36, highlight=1)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 300, "B.next = C.next  —  C is unlinked in one assignment: O(1). Then free(C).")
    note(c, 72, y - 360, 468, "Order matters: doing step 2 first orphans D forever (memory leak). New link before breaking the old one — always.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Reversal: The Classic",
                       "Three pointers walk the list, flipping links as they go.")
    draw_chain(y - 60, ["A", "B", "C", "D"], x0=72, w=70, gap=30)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 110, "Pointers: prev=NULL, curr=head.  Each step:")
    y0 = codeblock(c, 72, y - 130, [
        "  while curr:",
        "      nxt = curr.next   # 1. save next (else we lose it)",
        "      curr.next = prev  # 2. flip the link backwards",
        "      prev, curr = curr, nxt   # 3. advance both",
        "  head = prev           # new head = old tail",
    ])
    # flipped mini diagram
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y0 - 40, "Result:")
    x = 72
    for i, v in enumerate(["D", "C", "B", "A"]):
        box(c, x, y0 - 110, 70, 52, BOX_GREEN, v, "", font_size=11)
        if i < 3:
            arrow(c, x, y0 - 84, x - 30, y0 - 84, color=ACCENT, width=1.8)
        x += 100
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, y0 - 130, "O(n) time, O(1) space — the iterative version beats recursion here (no stack depth).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Floyd's Cycle Detection",
                       "Tortoise and hare: if there's a loop, the fast runner laps the slow one.")
    draw_chain(y - 60, ["A", "B", "C", "D", "E"], x0=72, w=64, gap=28)
    arrow(c, 72 + 5 * 92 - 28, y - 20, 72 + 2 * 92 + 32, y - 20, color=RED, width=2, label="loop back to C")
    y0 = codeblock(c, 72, y - 120, [
        "  slow = fast = head",
        "  while fast and fast.next:",
        "      slow = slow.next        # 1 step",
        "      fast = fast.next.next  # 2 steps",
        "      if slow is fast: return True   # met inside the loop",
        "  return False",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Why it works: in a cycle, fast gains one node per round — a meeting is inevitable.",
        "O(n) time, O(1) space — no hash set needed.",
        "Bonus: from the meeting point, classic math finds the cycle's start (mu).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Linked List vs Array",
                       "Pick by access pattern, not by habit.")
    rows = [("Random access arr[i]", "Array O(1)", "List O(n)", BOX_BLUE),
            ("Insert/delete at ends", "Array: back O(1)", "List: both O(1)*", BOX_GREEN),
            ("Insert/delete middle", "Array O(n) shifts", "List O(1) rewire*", BOX_ORANGE),
            ("Memory overhead", "none per element", "1-2 pointers/elem", BOX_RED),
            ("Cache locality", "excellent", "poor (scattered)", BOX_TEAL)]
    yy = y
    for name, a, b, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"{a}   vs   {b}", font_size=11)
        yy -= 70
    note(c, 72, 120, 468, "*List O(1) assumes you already hold the node/position — reaching it still costs O(n). Arrays win by default; lists win for constant middle surgery.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Linked Lists — Remember",
                 ["Nodes hold data + next (doubly: + prev); the list is a chain of handshakes, O(n) to reach node k.",
                  "Insert/delete is O(1) pointer surgery — but rewire new-links-before-old or you leak the tail.",
                  "Iterative reversal: save next, flip link, advance — O(n) time, O(1) space.",
                  "Floyd's tortoise-and-hare finds cycles in O(n) time, O(1) space.",
                  "Default to arrays; reach for lists when middle insert/delete dominates and locality doesn't matter."],
                 pg)
    c.save(); print("wrote", path)


def pdf_stacks_queues(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Stacks & Queues\nVisual Guide",
               "LIFO and FIFO —\ntwo disciplines that run parsers, schedulers, and search.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Stack: Last In, First Out",
                       "Push on top, pop from top — like a stack of plates.")
    for i, v in enumerate(["A", "B", "C"]):
        box(c, 200, 300 + i * 62, 200, 56, BOX_BLUE, v, "", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(420, 420, "<- top")
    arrow(c, 440, 480, 400, 480, color=GREEN, width=2.5, label="push D")
    arrow(c, 400, 360, 440, 360, color=RED, width=2.5, label="pop -> C")
    y0 = codeblock(c, 72, 260, [
        "  push(x): stack.append(x)   # O(1)",
        "  pop():   return stack.pop()  # O(1), LIFO order",
        "  peek():  stack[-1]           # look, don't touch",
    ])
    bullet_list(c, 72, y0 - 30, [
        "The call stack IS a stack: each call pushes a frame, return pops it.",
        "Undo (Ctrl+Z), back-button history, expression parsing — all stacks.",
        "Overflow: pushing past capacity (or infinite recursion) crashes the party.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Queue: First In, First Out",
                       "Enqueue at the rear, dequeue from the front — a checkout line.")
    for i, v in enumerate(["A", "B", "C", "D"]):
        box(c, 72 + i * 105, 440, 95, 60, BOX_GREEN, v, "", font_size=12)
    arrow(c, 500, 470, 540, 470, color=GREEN, width=2.5, label="enqueue E")
    arrow(c, 40, 470, 68, 470, color=RED, width=2.5, label="dequeue")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 420, "front ->"); c.drawRightString(540, 420, "<- rear")
    y0 = codeblock(c, 72, 390, [
        "  from collections import deque",
        "  q = deque(); q.append(x)   # enqueue O(1)",
        "  q.popleft()               # dequeue O(1), FIFO order",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Never popleft() a Python list — it's O(n) shifts. deque is the real queue.",
        "BFS, print spoolers, task schedulers, message brokers: all FIFO at heart.",
        "Circular buffer: fixed-size queue in an array with head/tail wrapping via modulo.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Deque: Double-Ended Queue",
                       "Push and pop from BOTH ends — stack and queue in one.")
    for i, v in enumerate(["B", "C", "D"]):
        box(c, 150 + i * 100, 440, 90, 60, BOX_TEAL, v, "", font_size=12)
    arrow(c, 130, 470, 146, 470, color=ACCENT, width=2.5, label="left")
    arrow(c, 444, 470, 460, 470, color=ACCENT, width=2.5, label="right")
    arrow(c, 146, 430, 130, 430, color=MUTED, width=2)
    arrow(c, 460, 430, 444, 430, color=MUTED, width=2)
    y0 = codeblock(c, 72, 390, [
        "  dq.appendleft(x); dq.append(x)      # push either end O(1)",
        "  dq.popleft();     dq.pop()         # pop either end O(1)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Sliding-window maximum, palindrome checks, work-stealing schedulers.",
        "A deque used from one end only IS a stack; from opposite ends, a queue.",
        "Implemented as a doubly-linked list of blocks — O(1) both ends, cache-friendly chunks.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Pattern: Monotonic Stack",
                       "'Next greater element' in O(n) — each element pushed and popped once.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y, "nums = [2, 1, 2, 4, 3]  ->  next greater = [4, 2, 4, -1, -1]")
    y0 = codeblock(c, 72, y - 20, [
        "  st = []                       # decreasing stack of indices",
        "  for i, x in enumerate(nums):",
        "      while st and nums[st[-1]] < x:",
        "          ans[st.pop()] = x     # x is their 'next greater'",
        "      st.append(i)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Invariant: the stack stays monotonic (decreasing) — violators get resolved immediately.",
        "Each index enters and leaves once: O(n) total, despite the nested loop.",
        "Siblings: daily temperatures, largest rectangle in histogram, trapping rain water.",
    ], font_size=10.5, gap=24)
    note(c, 72, 150, 468, "The 'while inside for looks O(n^2)' trap: count total pushes/pops, not loop nesting. Amortized thinking again.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Queue via Two Stacks",
                       "Amortized O(1) FIFO from LIFO parts — a favorite interview build.")
    box(c, 72, 440, 180, 70, BOX_BLUE, "inbox", "push here", font_size=12)
    box(c, 320, 440, 180, 70, BOX_GREEN, "outbox", "pop here", font_size=12)
    arrow(c, 252, 475, 318, 475, color=ACCENT, width=2.5, label="transfer when empty")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "enqueue: push to inbox.   dequeue: if outbox empty, pour inbox into outbox (reverses order), then pop.")
    y0 = codeblock(c, 72, 370, [
        "  def dequeue(self):",
        "      if not self.out:                     # refill rarely",
        "          while self.inbox: self.out.append(self.inbox.pop())",
        "      return self.out.pop()                 # O(1) amortized",
    ])
    note(c, 72, y0 - 60, 468, "Each element moves inbox->outbox exactly once: n dequeues cost O(n) total. The reverse trick (stack via queues) is the mirror image.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Where They Show Up",
                       "Recognize the shape, reach for the structure.")
    rows = [("Undo / redo", "stack of actions", BOX_BLUE),
            ("Browser back button", "stack of pages", BOX_BLUE),
            ("BFS graph search", "queue of frontier nodes", BOX_GREEN),
            ("Task scheduler", "queue of ready jobs", BOX_GREEN),
            ("Expression evaluation", "two stacks: operands + operators", BOX_ORANGE),
            ("Sliding window max", "monotonic deque", BOX_TEAL)]
    yy = y
    for name, desc, fill in rows:
        box(c, 72, yy - 48, 468, 52, fill, name, desc, font_size=11)
        yy -= 64
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Stacks & Queues — Remember",
                 ["Stack = LIFO (push/pop O(1)); queue = FIFO (enqueue/dequeue O(1)) — use deque, not list, for queues.",
                  "The call stack, undo history, and expression parsing are all stacks in disguise.",
                  "Monotonic stack solves 'next greater' patterns in O(n) — each element pushed/popped once.",
                  "Two stacks build an amortized-O(1) queue; the transfer reverses order exactly once per element.",
                  "Deque gives O(1) at both ends — stack and queue unified."],
                 pg)
    c.save(); print("wrote", path)


def pdf_hash_tables(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Hash Tables\nVisual Guide",
               "Average O(1) lookup —\nthe engine inside dicts, sets, caches, and indexes.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "The Pipeline: Key -> Hash -> Index",
                       "A hash function turns any key into an array slot.")
    box(c, 72, 440, 120, 70, BOX_BLUE, '"apple"', "key", font_size=12)
    box(c, 232, 440, 150, 70, BOX_ORANGE, "hash()", "deterministic\nmixer", font_size=12)
    box(c, 422, 440, 118, 70, BOX_GREEN, "idx 4", "h % capacity", font_size=12)
    arrow(c, 192, 475, 230, 475, color=ACCENT, width=2.5)
    arrow(c, 382, 475, 420, 475, color=ACCENT, width=2.5)
    for i in range(6):
        fill = BOX_GREEN if i == 4 else BOX_TEAL
        box(c, 72 + i * 78, 300, 70, 54, fill, f"[{i}]", "apple" if i == 4 else "", font_size=10)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 260, "index = hash(key) mod capacity.  Same key -> same hash -> same slot, every time.")
    bullet_list(c, 72, 225, [
        "Good hash: deterministic, fast, uniform — spreads keys evenly across slots.",
        "Modulo maps the huge hash space down to table capacity.",
        "Keys must be hashable AND immutable (strings, tuples) — mutating a key corrupts lookup.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Collisions Are Inevitable",
                       "Pigeonhole principle: more possible keys than slots.")
    box(c, 72, 460, 120, 64, BOX_BLUE, '"apple"', "h % 8 = 4", font_size=11)
    box(c, 72, 380, 120, 64, BOX_ORANGE, '"mango"', "h % 8 = 4", font_size=11)
    arrow(c, 192, 492, 260, 440, color=RED, width=2.5)
    arrow(c, 192, 412, 260, 400, color=RED, width=2.5)
    box(c, 270, 400, 90, 90, BOX_RED, "[4]", "ONE slot\ntwo keys!", font_size=11)
    bullet_list(c, 72, 330, [
        "Birthday paradox: collisions appear far earlier than intuition says (~sqrt(capacity) keys).",
        "A hash table is a collision-resolution strategy with a hash function attached.",
        "Two families: chaining (external) vs open addressing (in-place probing).",
    ], font_size=10.5, gap=24)
    note(c, 72, 180, 468, "Worst case with bad collisions: O(n) per op — a degenerate table is a linked list wearing a costume.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Chaining: Buckets of Lists",
                       "Each slot holds a chain — collisions just lengthen it.")
    for i in range(4):
        box(c, 72, 520 - i * 62, 70, 52, BOX_TEAL, f"[{i}]", "", font_size=11)
    box(c, 180, 520, 90, 52, BOX_BLUE, "apple", "", font_size=10)
    box(c, 180, 458, 90, 52, BOX_BLUE, "kiwi", "", font_size=10)
    box(c, 310, 458, 90, 52, BOX_ORANGE, "mango", "collision!", font_size=10)
    box(c, 180, 396, 90, 52, BOX_BLUE, "pear", "", font_size=10)
    arrow(c, 142, 546, 178, 546, color=ACCENT, width=1.8)
    arrow(c, 142, 484, 178, 484, color=ACCENT, width=1.8)
    arrow(c, 270, 484, 308, 484, color=RED, width=1.8)
    arrow(c, 142, 422, 178, 422, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 330, "Lookup: hash to the slot, then linear-scan its (short) chain comparing full keys.")
    bullet_list(c, 72, 295, [
        "Simple, deletion-friendly (just unlink), never 'full' — but pays pointer overhead.",
        "Java HashMap, Python's old dict design family: chains (plus tree-ification past 8).",
        "Long chains signal a bad hash function or an overloaded table — resize, don't suffer.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Open Addressing: Probe for Home",
                       "Everything lives IN the array — collisions probe neighboring slots.")
    for i in range(7):
        v = {2: "apple", 3: "mango", 4: "kiwi"}.get(i, "")
        fill = BOX_BLUE if v else BOX_TEAL
        box(c, 72 + i * 66, 470, 60, 54, fill, v, f"[{i}]", font_size=10)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawString(72, 440, "mango wanted [2] (taken) -> probed [3]")
    y0 = codeblock(c, 72, 405, [
        "  linear:    i, i+1, i+2, ...      # simple, clusters badly",
        "  quadratic: i, i+1, i+4, i+9 ...  # spreads, needs care",
        "  double:    i + k*h2(key) ...     # second hash as step",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Deletion needs tombstones: a bare empty slot would break probe chains.",
        "Cache-friendly (one flat array) — why Python dicts and Swiss tables use it.",
        "Primary clustering: linear probing clumps fill into long runs — keep load low.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Load Factor & Resizing",
                       "Fullness is the enemy — resize BEFORE performance collapses.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y, "load factor  a = n / capacity")
    for i in range(8):
        fill = BOX_GREEN if i < 6 else BOX_TEAL
        box(c, 72 + i * 58, y - 70, 52, 50, fill, "x" if i < 6 else "", "", font_size=10)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawString(72, y - 100, "a = 6/8 = 0.75  ->  RESIZE: allocate 16, rehash every key")
    arrow(c, 250, y - 130, 250, y - 160, color=RED, width=2.5)
    for i in range(16):
        fill = BOX_GREEN if i in (1, 4, 7, 9, 12, 14) else BOX_TEAL
        box(c, 72 + i * 29, y - 220, 26, 44, fill, "", "", font_size=8)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, y - 245, "new capacity 16, a back to 0.375 — keys land on fresh slots via rehash")
    bullet_list(c, 72, y - 285, [
        "Resize at a ~ 0.7 (chaining) or ~ 0.5 (open addressing) — probing degrades fast past half full.",
        "Resize = allocate bigger + rehash ALL keys (indices change with capacity): O(n), amortized.",
        "Python dict: grows at 2/3 full; over-allocates to keep resizes rare.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Hash Table Pitfalls",
                       "Fast on average — fragile at the edges.")
    bullet_list(c, 72, y, [
        "Mutable keys: hash computed at insert, key mutated later -> entry is lost forever.",
        "Bad hash (e.g. constant): every op degrades to O(n) — hash-flooding DoS attacks exploit this.",
        "Iteration order is NOT insertion order (unless the table guarantees it, like Python 3.7+ dicts).",
        "Floating-point keys: 0.1+0.2 != 0.3 — equality and hashing must agree, or lookups miss.",
        "Resizing pauses: latency-sensitive systems pre-size tables or resize incrementally.",
        "Custom objects: define BOTH __hash__ and __eq__ consistently — equal objects must hash equal.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Hash Tables — Remember",
                 ["Pipeline: hash(key) mod capacity -> slot; same key always lands together.",
                  "Collisions are certain: chain them (buckets of lists) or probe (linear/quadratic/double).",
                  "Watch the load factor: resize (allocate + rehash all) around 0.7 chaining / 0.5 probing.",
                  "Average O(1), worst O(n) — a bad hash function turns your table into a linked list.",
                  "Keys must be immutable and hash-consistent with equality."],
                 pg)
    c.save(); print("wrote", path)


def pdf_trees(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Trees\nVisual Guide",
               "Hierarchies with O(log n) superpowers —\nwhen balance is kept.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Anatomy of a Tree",
                       "Root at top, leaves at bottom, one path between any two nodes.")
    box(c, 256, 520, 100, 52, BOX_BLUE, "8 (root)", "", font_size=11)
    box(c, 120, 420, 100, 52, BOX_GREEN, "3", "", font_size=11)
    box(c, 392, 420, 100, 52, BOX_GREEN, "10", "", font_size=11)
    box(c, 72, 320, 90, 52, BOX_TEAL, "1", "leaf", font_size=11)
    box(c, 190, 320, 90, 52, BOX_TEAL, "6", "", font_size=11)
    box(c, 440, 320, 90, 52, BOX_TEAL, "14", "leaf", font_size=11)
    for x1, y1, x2, y2 in [(306, 520, 170, 472), (306, 520, 442, 472),
                           (170, 420, 117, 372), (170, 420, 235, 372),
                           (442, 420, 485, 372)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 280, "depth(root)=0; height = longest root->leaf path (here: 2).  Binary tree: at most 2 children per node.")
    bullet_list(c, 72, 245, [
        "Parent/child/sibling, subtree, ancestor — the family vocabulary of hierarchies.",
        "A tree with n nodes has exactly n-1 edges — one path between any pair.",
        "File systems, DOM, org charts, decision trees: trees model nesting everywhere.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "BST: Ordered by Construction",
                       "Smaller keys left, larger keys right — search prunes half the tree per step.")
    box(c, 256, 500, 100, 52, BOX_BLUE, "8", "", font_size=11)
    box(c, 120, 400, 100, 52, BOX_GREEN, "3", "", font_size=11)
    box(c, 392, 400, 100, 52, BOX_GREEN, "10", "", font_size=11)
    box(c, 72, 300, 90, 52, BOX_TEAL, "1", "", font_size=11)
    box(c, 190, 300, 90, 52, BOX_TEAL, "6", "", font_size=11)
    for x1, y1, x2, y2 in [(306, 500, 170, 452), (306, 500, 442, 452),
                           (170, 400, 117, 352), (170, 400, 235, 352)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT, width=1.8)
    y0 = codeblock(c, 72, 265, [
        "  search(6): 8 -> go left (6<8) -> 3 -> go right (6>3) -> 6 FOUND",
        "  insert(4): 8 -> 3 -> 6 -> left of 6 (4<6): attach.  O(h)",
        "  delete: 0/1 child -> splice; 2 children -> swap with successor",
    ])
    note(c, 72, y0 - 60, 468, "h = height. Balanced: h ~ log n -> O(log n). Degenerate: h = n -> O(n). Balance is EVERYTHING (step 4).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Traversals: Three Orders",
                       "Same tree, three visit sequences — recursion does the walking.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y, "Tree:     8")
    c.drawString(72, y - 20, "        /   \\")
    c.drawString(72, y - 40, "       3     10")
    c.drawString(72, y - 60, "      / \\")
    c.drawString(72, y - 80, "     1   6")
    y0 = codeblock(c, 220, y, [
        "  inorder   (L, root, R): 1, 3, 6, 8, 10  # sorted!",
        "  preorder  (root, L, R): 8, 3, 1, 6, 10  # copy structure",
        "  postorder (L, R, root): 1, 6, 3, 10, 8  # delete safely",
    ], w=320)
    bullet_list(c, 72, y0 - 30, [
        "Inorder on a BST yields sorted order — the cheapest sort you'll ever write.",
        "Preorder records structure (serialize); postorder children-before-parent (free memory).",
        "Level order (BFS) visits by depth — needs a queue, not recursion.",
        "Morris traversal: O(1) space inorder via temporary threading — interview gold.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "The Degenerate Trap",
                       "Insert sorted data into a naive BST and it becomes a linked list.")
    x = 72
    for i, v in enumerate([1, 2, 3, 4, 5]):
        box(c, x, 560 - i * 62, 80, 52, BOX_RED, str(v), "", font_size=11)
        if i < 4:
            arrow(c, x + 80, 560 - i * 62 + 26, x + 80, 560 - (i + 1) * 62 + 52, color=RED, width=1.8)
        x += 20
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawString(330, 480, "height = n-1")
    c.drawString(330, 462, "search = O(n)  -- BST advantage: GONE")
    bullet_list(c, 72, 380, [
        "Adversarial (or merely sorted) input is common: timestamps, IDs, logs.",
        "Fix options: randomize insertion, or use a self-balancing tree (next step).",
        "Treaps/skip lists: randomization achieves balance with high probability.",
    ], font_size=10.5, gap=24)
    note(c, 72, 240, 468, "This is why 'just use a BST' is never the full answer — always ask how balance is maintained.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Self-Balancing: The Rotation Idea",
                       "Restore balance locally with rotations — O(log n) guaranteed.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Right rotation (left-left case):")
    box(c, 72, 470, 70, 50, BOX_ORANGE, "y", "", font_size=11)
    box(c, 150, 470, 70, 50, BOX_GREEN, "x", "", font_size=11)
    box(c, 230, 470, 70, 50, BOX_TEAL, "T3", "", font_size=10)
    arrow(c, 142, 495, 150, 495, color=ACCENT, width=1.8)
    arrow(c, 310, 495, 380, 495, color=ACCENT, width=2.5, label="rotate")
    box(c, 400, 470, 70, 50, BOX_GREEN, "x", "", font_size=11)
    box(c, 480, 470, 70, 50, BOX_ORANGE, "y", "", font_size=11)
    bullet_list(c, 72, 420, [
        "Rotation rewires 3 pointers, preserves inorder (sorted) order — O(1) local fix.",
        "AVL: height diff at most 1, rotate on violation — strictest balance, fastest lookup.",
        "Red-black: looser color rules, fewer rotations — the pragmatic default (Linux, Java TreeMap, C++ map).",
        "B-trees: the disk edition — wide nodes, minimal I/O. Databases live here.",
    ], font_size=10.5, gap=26)
    note(c, 72, 200, 468, "You won't hand-roll these in production — but knowing WHY the stdlib map is O(log n) separates users from engineers.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Tree Height vs Performance",
                       "Every tree algorithm's cost is a function of height.")
    rows = [("Balanced binary (n=1M)", "height ~ 20", "search O(log n)", BOX_GREEN),
            ("Degenerate chain (n=1M)", "height = 1M", "search O(n)", BOX_RED),
            ("B-tree (n=1M, fanout 100)", "height ~ 3", "3 disk reads", BOX_BLUE),
            ("Trie (keys length L)", "height = L", "lookup O(L)", BOX_TEAL)]
    yy = y
    for name, h, cost, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"{h}  ->  {cost}", font_size=11)
        yy -= 70
    note(c, 72, 150, 468, "Rule of thumb: if your tree can degenerate, it will — in production, on a Friday, with sorted input.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Trees — Remember",
                 ["Vocabulary: root, leaf, depth, height; n nodes -> n-1 edges, one path between nodes.",
                  "BST invariant (smaller keys left, larger right) makes search/insert/delete O(h) — height decides.",
                  "Inorder = sorted, preorder = structure, postorder = children-first; BFS = level order.",
                  "Sorted input degenerates naive BSTs to O(n) chains — self-balance (AVL/red-black) or randomize.",
                  "Rotations fix balance locally in O(1) while preserving order; B-trees extend the idea to disk."],
                 pg)
    c.save(); print("wrote", path)


def pdf_graphs(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Graphs\nVisual Guide",
               "Nodes and edges —\nthe model behind maps, networks, and dependencies.",
               CAT, None); pg += 1

    y = section_header(c, 1, 7, "Anatomy of a Graph",
                       "Vertices connected by edges — directed or not, weighted or not.")
    pts = {"A": (150, 520), "B": (330, 560), "C": (470, 500), "D": (200, 400), "E": (420, 380)}
    for name, (px, py) in pts.items():
        c.setFillColor(BOX_BLUE); c.circle(px, py, 26, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.circle(px, py, 26, fill=0, stroke=1)
        c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawCentredString(px, py - 4, name)
    for (a, b), w in [(("A", "B"), 4), (("B", "C"), 2), (("A", "D"), 7), (("D", "E"), 1), (("C", "E"), 5), (("B", "D"), 3)]:
        (x1, y1), (x2, y2) = pts[a], pts[b]
        arrow(c, x1, y1, x2, y2, color=ACCENT, width=1.5, label=str(w))
    bullet_list(c, 72, 330, [
        "Directed: edges have arrows (web links, dependencies). Undirected: mutual (friendships, roads).",
        "Weighted: edges carry costs (distance, latency, price) — unweighted = every edge costs 1.",
        "Degree, path, cycle, connected component — the basic vocabulary.",
        "Dense vs sparse decides the representation (next step).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 7, "Adjacency List vs Matrix",
                       "The representation IS the performance.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Adjacency LIST — sparse graphs (E << V^2)")
    y0 = codeblock(c, 72, y - 20, [
        "  A -> [B, D]      # only real edges stored",
        "  B -> [A, C, D]",
        "  C -> [B, E]",
        "  space O(V+E); neighbors of u in O(degree(u))",
    ])
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y0 - 36, "Adjacency MATRIX — dense graphs")
    y1 = codeblock(c, 72, y0 - 56, [
        "      A  B  C  D  E",
        "  A [ 0  1  0  1  0 ]",
        "  B [ 1  0  1  1  0 ]   # edge? O(1) lookup",
        "  space O(V^2) — wasteful when sparse",
    ])
    bullet_list(c, 72, y1 - 30, [
        "Default to adjacency lists — real graphs (social, web, road) are sparse.",
        "Matrix wins for dense graphs and O(1) edge-existence checks.",
        "Edge list (u,v,w triples): simplest for Kruskal's and streaming.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 7, "BFS: Breadth-First Search",
                       "Wave outward level by level — shortest path in unweighted graphs.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y, "From A:  visit order  A -> B -> D -> C -> E   (level by level)")
    y0 = codeblock(c, 72, y - 20, [
        "  queue = deque([start]); visited = {start}",
        "  while queue:",
        "      u = queue.popleft()          # FIFO = level order",
        "      for v in adj[u]:",
        "          if v not in visited: visited.add(v); queue.append(v)",
    ])
    box(c, 72, y0 - 90, 140, 60, BOX_BLUE, "queue", "FIFO", font_size=11)
    box(c, 250, y0 - 90, 140, 60, BOX_GREEN, "visited set", "no repeats", font_size=11)
    box(c, 72, y0 - 165, 468, 60, BOX_ORANGE, "O(V + E)", "each vertex + edge touched once", font_size=11)
    note(c, 72, y0 - 230, 468, "First time BFS reaches a node = fewest edges from start. That single property powers shortest-path, 6-degrees, and bipartite checks.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 7, "DFS: Depth-First Search",
                       "Plunge down one path before backtracking — recursion's natural walk.")
    y0 = codeblock(c, 72, y, [
        "  def dfs(u):",
        "      visited.add(u)",
        "      for v in adj[u]:",
        "          if v not in visited: dfs(v)   # go deep first",
        "  # iterative version: swap the queue for a STACK",
    ])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y0 - 36, "From A (adj order B,D):  A -> B -> C -> E -> D   (dives before spreading)")
    bullet_list(c, 72, y0 - 70, [
        "BFS vs DFS: same O(V+E), different order — queue spreads, stack dives.",
        "DFS powers: cycle detection, topological sort, connected components, maze solving.",
        "Recursion depth = longest path — deep graphs overflow the call stack; go iterative.",
        "Colors (white/gray/black) track discovery state for cycle detection in directed graphs.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 7, "Dijkstra: Shortest Weighted Path",
                       "Greedy + priority queue: always settle the closest unsettled node.")
    y0 = codeblock(c, 72, y, [
        "  dist = {all: INF}; dist[start] = 0",
        "  pq = [(0, start)]                       # min-heap by distance",
        "  while pq:",
        "      d, u = heappop(pq)                  # closest unsettled",
        "      if d > dist[u]: continue",
        "      for v, w in adj[u]:                 # relax edges",
        "          if dist[u] + w < dist[v]:",
        "              dist[v] = dist[u] + w; heappush(pq, (dist[v], v))",
    ])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y0 - 36, "A->E: A-B(4)-C(2)-E(5) = 11  vs  A-D(7)-E(1) = 8  ->  Dijkstra settles D first, finds 8.")
    bullet_list(c, 72, y0 - 70, [
        "O((V+E) log V) with a binary heap — the log is the priority queue.",
        "REQUIRES non-negative weights: negative edges need Bellman-Ford (O(VE)).",
        "GPS routing, network latency, flight pricing — all Dijkstra underneath.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 7, "Topological Sort: Order the Dependencies",
                       "Linearize a DAG so every edge points forward — builds, courses, task plans.")
    box(c, 72, 480, 90, 54, BOX_BLUE, "code", "", font_size=11)
    box(c, 200, 480, 90, 54, BOX_BLUE, "test", "", font_size=11)
    box(c, 328, 480, 90, 54, BOX_GREEN, "build", "", font_size=11)
    box(c, 456, 480, 84, 54, BOX_ORANGE, "deploy", "", font_size=11)
    for x1, x2 in [(162, 200), (290, 328), (418, 456)]:
        arrow(c, x1, 507, x2, 507, color=ACCENT, width=2)
    y0 = codeblock(c, 72, 440, [
        "  Kahn's: repeatedly emit nodes with in-degree 0, delete their edges",
        "  DFS-based: postorder of a DFS, reversed",
        "  leftover nodes with in-degree > 0  =>  CYCLE (no valid order!)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Only DAGs (directed acyclic) have a topological order — cycles make it impossible.",
        "Make, course prerequisites, spreadsheet calc chains, migration ordering.",
        "Cycle detection via topo sort doubles as a 'is my dependency graph sane?' check.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 7, 7, "Graph Algorithm Chooser",
                       "Match the problem to the walk.")
    rows = [("Shortest path, unweighted", "BFS", "O(V+E)", BOX_GREEN),
            ("Shortest path, weighted +", "Dijkstra", "O((V+E) log V)", BOX_BLUE),
            ("Shortest path, negative w", "Bellman-Ford", "O(VE)", BOX_ORANGE),
            ("All pairs", "Floyd-Warshall", "O(V^3)", BOX_TEAL),
            ("Dependency order", "Topo sort (Kahn/DFS)", "O(V+E)", BOX_PURP),
            ("Min cost to connect all", "Kruskal / Prim (MST)", "O(E log E)", BOX_BLUE)]
    yy = y
    for name, algo, cost, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, f"{algo}", f"{name} — {cost}", font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Graphs — Remember",
                 ["Model: vertices + edges; directed/undirected, weighted/unweighted, dense/sparse.",
                  "Adjacency list is the default (O(V+E) space); matrix for dense graphs and O(1) edge checks.",
                  "BFS (queue) = level order = shortest path unweighted; DFS (stack/recursion) = dive deep.",
                  "Dijkstra settles closest-first via min-heap — needs non-negative weights.",
                  "Topological sort linearizes DAGs; leftover nodes mean a cycle."],
                 pg)
    c.save(); print("wrote", path)


def pdf_heaps(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Heaps & Priority Queues\nVisual Guide",
               "'Most urgent first' —\nthe structure behind schedulers and top-k.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "The Heap Property + Array Embedding",
                       "Parent beats children; the tree lives inside a flat array.")
    box(c, 256, 500, 90, 52, BOX_BLUE, "100", "i=0", font_size=12)
    box(c, 140, 400, 90, 52, BOX_GREEN, "70", "i=1", font_size=11)
    box(c, 372, 400, 90, 52, BOX_GREEN, "80", "i=2", font_size=11)
    box(c, 90, 300, 80, 50, BOX_TEAL, "40", "i=3", font_size=10)
    box(c, 200, 300, 80, 50, BOX_TEAL, "60", "i=4", font_size=10)
    box(c, 420, 300, 80, 50, BOX_TEAL, "75", "i=5", font_size=10)
    for x1, y1, x2, y2 in [(301, 500, 185, 452), (301, 500, 417, 452),
                           (185, 400, 130, 350), (185, 400, 240, 350),
                           (417, 400, 460, 350)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT, width=1.6)
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, 262, "array: [100, 70, 80, 40, 60, 75]")
    y0 = codeblock(c, 72, 240, [
        "  parent(i) = (i-1)//2;  left(i) = 2i+1;  right(i) = 2i+2",
        "  max-heap: parent >= children   # root = max, always",
        "  NOT sorted: [100,70,80,...] — only the heap order holds",
    ])
    note(c, 72, y0 - 60, 468, "Complete binary tree: filled left-to-right, so the array has no holes. A heap is a priority queue — NOT a sorted list.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Sift Up, Sift Down, Heapify",
                       "All heap ops are 'restore the property by swapping along one path'.")
    y0 = codeblock(c, 72, y, [
        "  push(x): append at end, SIFT UP while x > parent     # O(log n)",
        "  pop():   take root, move last -> root, SIFT DOWN     # O(log n)",
        "  peek():  root                                        # O(1)",
        "  heapify(arr): sift down from last parent -> root     # O(n)!",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Sift up/down each walk one root-to-leaf path: height = log n.",
        "heapify is O(n), not O(n log n): most nodes sit near the leaves (short sifts).",
        "Building by n pushes costs O(n log n) — heapify the array instead.",
        "Python: heapq is a MIN-heap; negate values for max-heap behavior.",
    ], font_size=10.5, gap=26)
    note(c, 72, 190, 468, "Interview trap: 'sort with a heap' = heapsort O(n log n). 'K smallest' = heap of size k (next step).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Priority Queue in Action",
                       "ER triage: severity outranks arrival order.")
    rows = [("chest pain", "P1", BOX_RED), ("fever", "P3", BOX_ORANGE),
            ("cardiac arrest", "P0", BOX_RED), ("sprain", "P4", BOX_GREEN)]
    yy = y
    for name, pri, fill in rows:
        box(c, 72, yy - 48, 300, 52, fill, name, f"priority {pri}", font_size=11)
        yy -= 62
    arrow(c, 400, y - 100, 400, y - 260, color=ACCENT, width=2.5, label="heappop order")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(420, y - 130, "P0 cardiac")
    c.drawString(420, y - 160, "P1 chest pain")
    c.drawString(420, y - 190, "P3 fever")
    c.drawString(420, y - 220, "P4 sprain")
    bullet_list(c, 72, yy - 20, [
        "OS schedulers, Dijkstra's frontier, A* search, event simulation — all priority queues.",
        "Stable tie-break: push (priority, counter, item) so FIFO breaks ties deterministically.",
        "Decrease-key: Dijkstra needs it; lazy deletion (skip stale entries) avoids the complexity.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Pattern: Top-K",
                       "K largest in a stream — keep a min-heap of exactly k.")
    y0 = codeblock(c, 72, y, [
        "  import heapq",
        "  h = []",
        "  for x in stream:                       # n items, unknown length",
        "      heapq.heappush(h, x)",
        "      if len(h) > k: heapq.heappop(h)    # evict the smallest",
        "  # h holds the k largest; root = kth largest.  O(n log k)",
    ])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y0 - 36, "stream: 5, 1, 9, 3, 7,  ...   k=3   ->   heap keeps [5, 7, 9]")
    bullet_list(c, 72, y0 - 70, [
        "O(n log k) time, O(k) space — beats full sort O(n log n) when k is much smaller than n.",
        "Mirror: k smallest -> max-heap of size k (negate in Python).",
        "Median of a stream: max-heap (low half) + min-heap (high half) — the two-heap tango.",
    ], font_size=10.5, gap=24)
    note(c, 72, 170, 468, "'Top k frequent': count with a hash map, then top-k the counts — hash table + heap, the classic combo.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Scheduling with Heaps",
                       "Merge k sorted lists; schedule tasks with cooldowns.")
    y0 = codeblock(c, 72, y, [
        "  # merge k sorted lists: heap of (head_value, list_id)",
        "  push each list's head; repeatedly pop min, push its successor",
        "  # => O(N log k) for N total elements",
        "",
        "  # task scheduler (cooldown n): max-heap of remaining counts",
        "  # + queue of cooling tasks; always run the most-remaining task",
    ])
    bullet_list(c, 72, y0 - 30, [
        "K-way merge beats pairwise merging: O(N log k) vs O(N k).",
        "Huffman coding: repeatedly merge two lightest nodes via min-heap — optimal prefix codes.",
        "CPU scheduling (priority), bandwidth allocation, discrete-event sims: heaps schedule the future.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Heap Facts & Traps",
                       "What the heap is not.")
    bullet_list(c, 72, y, [
        "A heap is NOT sorted — only root-vs-children order holds. Don't binary-search it.",
        "Find-min in a max-heap is O(n): the min hides among the leaves.",
        "Heap vs sorted array: heap wins for repeated extract-min; array wins for scans.",
        "d-ary heaps (more children): shallower, better cache behavior — used in real Dijkstra.",
        "Binomial/Fibonacci heaps: theoretically faster decrease-key; rarely worth the complexity.",
        "Memory heaps (malloc arenas) share only the NAME — different concept entirely.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Heaps & Priority Queues — Remember",
                 ["Heap property (parent beats children) in a complete tree embedded in an array: parent(i)=(i-1)//2.",
                  "Push/pop = sift along one path: O(log n); peek O(1); heapify an array in O(n).",
                  "Priority queues power triage, schedulers, Dijkstra, A*, and event simulation.",
                  "Top-k pattern: bounded heap of size k -> O(n log k) time, O(k) space.",
                  "A heap is not sorted — never binary-search it; min of a max-heap is O(n)."],
                 pg)
    c.save(); print("wrote", path)


def pdf_sorting(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Sorting Algorithms\nVisual Guide",
               "From bubble to quicksort —\nwhat O(n log n) really costs and buys.",
               CAT, None); pg += 1

    y = section_header(c, 1, 7, "The Comparison Model",
                       "Sorting by comparing pairs — the arena every classic sort fights in.")
    vals = [5, 2, 9, 1, 7]
    for i, v in enumerate(vals):
        box(c, 72 + i * 88, 470, 78, 56, BOX_BLUE, str(v), "", font_size=13)
    arrow(c, 160, 440, 200, 440, color=RED, width=2.5, label="compare")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Decision tree: n! possible orders -> any comparison sort needs >= log2(n!) ~ n log n comparisons.")
    y0 = codeblock(c, 72, 370, [
        "  n=8:   8! = 40320 orders -> need >= 16 comparisons",
        "  n=1M:  n log n ~ 20M comparisons minimum",
        "  escape hatch: non-comparison sorts (counting/radix) beat it with extra assumptions",
    ])
    note(c, 72, y0 - 60, 468, "The n log n lower bound applies ONLY to comparison sorts. Counting sort hits O(n+k) by never comparing — keys must be small integers.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 7, "The O(n^2) Trio",
                       "Simple, slow, and still useful for tiny n.")
    y0 = codeblock(c, 72, y, [
        "  bubble:    swap adjacent inversions, repeat     # early-exit if no swaps",
        "  selection: pick min of rest, swap into place   # fewest writes: O(n)",
        "  insertion: grow sorted prefix, insert next     # O(n) on nearly-sorted!",
    ])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y0 - 36, "insertion sort on [1,2,3,5,4]: one shift — nearly O(n). On reversed: O(n^2).")
    bullet_list(c, 72, y0 - 70, [
        "Adaptive: insertion sort exploits existing order — why Timsort uses it for small runs.",
        "Selection sort: exactly n swaps — pick it when writes are expensive (flash memory).",
        "All three are in-place O(1) space and stable-ish; all die past n ~ 10^4.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 7, "Merge Sort: Divide & Conquer",
                       "Split, sort, merge — guaranteed O(n log n), stable.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, y, "[5 2 9 1 7 3]")
    c.drawString(72, y - 28, "/            \\")
    c.drawString(72, y - 52, "[5 2 9]      [1 7 3]")
    c.drawString(72, y - 80, "/     \\      /     \\")
    c.drawString(72, y - 104, "[5 2] [9]  [1 7] [3]")
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 10)
    c.drawString(330, y - 130, "merge up: [2 5] [9] -> [2 5 9]")
    c.drawString(330, y - 150, "merge up: [1 7] [3] -> [1 3 7]")
    c.drawString(330, y - 170, "merge: [1 2 3 5 7 9]  DONE")
    y0 = codeblock(c, 72, y - 210, [
        "  T(n) = 2T(n/2) + O(n)   # two halves + linear merge",
        "  => O(n log n) always, O(n) extra space for merging",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Stable: equal elements keep their order — merge takes from the left first.",
        "External sorting: merge sort streams from disk — the database sort.",
        "Predictable: no bad inputs, unlike quicksort — pick it when worst case matters.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 7, "Quicksort: Partition & Conquer",
                       "Pick a pivot, partition around it, recurse — the practical champion.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y, "[5 2 9 1 7 3]   pivot = 5")
    c.drawString(72, y - 26, "partition ->  [2 1 3]  5  [9 7]     # < pivot | pivot | > pivot")
    c.drawString(72, y - 52, "recurse  ->  [1 2 3]  5  [7 9]")
    y0 = codeblock(c, 72, y - 90, [
        "  Lomuto: pivot = last; i tracks boundary of '< pivot'",
        "  Hoare:  two fingers walk inward, swap inversions  # fewer swaps",
        "  avg O(n log n); worst O(n^2) on sorted input + bad pivot",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Pivot choice is everything: random or median-of-3 defeats adversarial input.",
        "In-place, cache-friendly — why it's the default in most standard libraries.",
        "Introsort (std::sort): quicksort + heapsort fallback when recursion goes too deep.",
        "3-way partition (Dutch flag): O(n) on arrays with many duplicates.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 7, "Heap Sort: The Heap Does the Work",
                       "Heapify, then repeatedly extract-max to the end.")
    y0 = codeblock(c, 72, y, [
        "  heapify(arr)                 # O(n): max-heap in place",
        "  for end in reversed(range(n)):",
        "      swap(arr[0], arr[end])   # max -> its final slot",
        "      sift_down(0, end)        # restore heap on prefix",
        "  # O(n log n) worst case, O(1) space — but NOT stable",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Guaranteed O(n log n) with O(1) space — the safe in-place choice.",
        "Not stable: equal elements can leapfrog during swaps.",
        "Poor cache behavior vs quicksort: sifting jumps across the array — slower in practice.",
        "Interview use: 'sort with O(1) space and guaranteed n log n' -> heapsort.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 7, "Stability & Choosing",
                       "Equal keys: does their original order survive?")
    rows = [("Quicksort", "avg n log n", "unstable*", "fastest in practice", BOX_BLUE),
            ("Merge sort", "n log n", "stable", "needs O(n) space", BOX_GREEN),
            ("Heap sort", "n log n", "unstable", "O(1) space guarantee", BOX_ORANGE),
            ("Timsort", "n log n", "stable", "Python/Java default", BOX_TEAL),
            ("Counting/radix", "n + k", "stable", "non-comparison, bounded keys", BOX_PURP)]
    yy = y
    for name, t, stab, note_, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, f"{name} — {t}", f"{stab} · {note_}", font_size=11)
        yy -= 70
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, 120, "*quicksort can be stabilized with index tie-breaks, at a cost.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 7, 7, "Sorting Wisdom",
                       "Rules that survive contact with production.")
    bullet_list(c, 72, y, [
        "n under ~50: insertion sort wins — constants beat asymptotics (Timsort knows this).",
        "Need stability (sort by name, then by age)? Stable sort or composite keys.",
        "Nearly sorted input: insertion O(n); quicksort with naive pivot degrades to O(n^2).",
        "Huge data, tiny RAM: external merge sort — stream runs from disk.",
        "Just call the stdlib sort: decades of tuning (introsort/Timsort) beat hand-rolled code.",
        "Sorting is the gateway: binary search, two pointers, and dedup all assume sorted input.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Sorting Algorithms — Remember",
                 ["Comparison sorts can't beat n log n (decision-tree bound); counting/radix escape via assumptions.",
                  "Merge sort: guaranteed O(n log n), stable, O(n) space — the safe divide-and-conquer.",
                  "Quicksort: average O(n log n), in-place, cache-hot — but pivot choice decides worst case.",
                  "Heap sort: O(n log n) worst case in O(1) space, unstable, cache-cold.",
                  "Stability matters when equal keys carry order; defaults: Timsort (Python/Java), introsort (C++)."],
                 pg)
    c.save(); print("wrote", path)


def pdf_searching(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Searching Algorithms\nVisual Guide",
               "Finding needles —\nfrom linear scans to binary search mastery.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Linear vs Binary: The Setup",
                       "Sorted input unlocks logarithmic search.")
    for i, v in enumerate([1, 3, 5, 7, 9, 11, 13]):
        box(c, 72 + i * 66, 470, 60, 54, BOX_BLUE, str(v), "", font_size=11)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawString(72, 440, "linear: check 1,3,5,7... until hit  ->  O(n)")
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 10)
    c.drawString(72, 422, "binary: check 7, then half the range  ->  O(log n)")
    bullet_list(c, 72, 385, [
        "Binary search needs RANDOM ACCESS + SORTED order — arrays, not linked lists.",
        "n=1B: linear touches a billion; binary touches ~30. Sorting once pays forever.",
        "Unsorted + one search? Linear wins. Unsorted + many searches? Sort first, then binary.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Binary Search Mechanics",
                       "Halve the range every step — the loop invariant is everything.")
    for i, v in enumerate([1, 3, 5, 7, 9, 11, 13]):
        fill = BOX_GREEN if v == 7 else BOX_BLUE
        box(c, 72 + i * 66, 500, 60, 54, fill, str(v), "mid" if v == 7 else "", font_size=11)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 478, "lo")
    c.drawRightString(540, 478, "hi")
    y0 = codeblock(c, 72, 440, [
        "  lo, hi = 0, n - 1",
        "  while lo <= hi:                      # invariant: answer in [lo, hi]",
        "      mid = lo + (hi - lo) // 2        # no overflow, unlike (lo+hi)//2",
        "      if a[mid] == T: return mid",
        "      elif a[mid] < T: lo = mid + 1    # discard left half",
        "      else: hi = mid - 1              # discard right half",
        "  return -1",
    ])
    note(c, 72, y0 - 60, 468, "The two classic bugs: mid overflow in fixed-width ints, and infinite loops from lo=mid / hi=mid without +/-1. Exclude mid every step.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Bounds Variants: lower_bound / upper_bound",
                       "Duplicates? Find the FIRST or LAST occurrence, not just any.")
    for i, v in enumerate([1, 3, 5, 5, 5, 9, 11]):
        fill = BOX_ORANGE if v == 5 and i == 2 else BOX_BLUE
        box(c, 72 + i * 66, 480, 60, 54, fill, str(v), "first" if (v == 5 and i == 2) else "", font_size=11)
    y0 = codeblock(c, 72, 440, [
        "  # lower_bound: first i with a[i] >= T   (bisect_left)",
        "  lo, hi = 0, n",
        "  while lo < hi:",
        "      mid = (lo + hi) // 2",
        "      if a[mid] < T: lo = mid + 1",
        "      else: hi = mid          # mid could BE the answer: keep it",
        "  return lo",
    ])
    bullet_list(c, 72, y0 - 30, [
        "lower_bound(5) -> index 2 (first 5); upper_bound(5) -> index 5 (first > 5).",
        "Count of T = upper - lower. Insertion point = lower_bound — keeps array sorted.",
        "Half-open [lo, hi) + 'hi = mid keeps candidate' is the bug-free template.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Search in Rotated Sorted Array",
                       "One half is always sorted — find it, then decide.")
    vals = [7, 9, 11, 1, 3, 5]
    for i, v in enumerate(vals):
        fill = BOX_ORANGE if i < 3 else BOX_GREEN
        box(c, 72 + i * 72, 480, 64, 54, fill, str(v), "", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "pivot somewhere inside; target T=3")
    y0 = codeblock(c, 72, 420, [
        "  # each step: identify the SORTED half via a[lo] <= a[mid]",
        "  if a[lo] <= a[mid]:            # left half sorted",
        "      if a[lo] <= T < a[mid]: hi = mid - 1",
        "      else: lo = mid + 1",
        "  else:                          # right half sorted",
        "      if a[mid] < T <= a[hi]: lo = mid + 1",
        "      else: hi = mid - 1",
    ])
    note(c, 72, y0 - 60, 468, "With duplicates, a[lo]==a[mid] hides which half is sorted — shrink lo+=1 and continue (degrades toward O(n) worst case).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Interpolation & Exponential Search",
                       "When binary's blind halving isn't the best probe.")
    y0 = codeblock(c, 72, y, [
        "  # interpolation: probe by VALUE, not position",
        "  pos = lo + (T - a[lo]) * (hi - lo) // (a[hi] - a[lo])",
        "  # uniform data: O(log log n) avg; skewed data: O(n) worst",
        "",
        "  # exponential: find range by doubling, then binary search it",
        "  bound = 1; while bound < n and a[bound] < T: bound *= 2",
        "  binary_search(a, bound//2, min(bound, n))   # O(log i): i = answer idx",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Interpolation = 'phone-book search': uniform keys (IDs, timestamps) converge insanely fast.",
        "Exponential search: unbounded/infinite arrays — no n needed, optimal when answer is near the start.",
        "Ternary search: two mids, for unimodal (bitonic) functions — not for sorted arrays.",
        "Jump search: sqrt(n) blocks — a historical curiosity; binary dominates.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Search Cheatsheet",
                       "Pick the probe for the terrain.")
    rows = [("Unsorted, one query", "linear scan", "O(n)", BOX_RED),
            ("Sorted array", "binary search", "O(log n)", BOX_GREEN),
            ("Sorted + duplicates", "lower/upper bound", "O(log n)", BOX_BLUE),
            ("Rotated sorted", "modified binary", "O(log n)", BOX_ORANGE),
            ("Uniform keys", "interpolation", "O(log log n) avg", BOX_TEAL),
            ("Unbounded / infinite", "exponential", "O(log i)", BOX_PURP)]
    yy = y
    for name, algo, cost, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, f"{algo} — {cost}", name, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Searching Algorithms — Remember",
                 ["Binary search needs sorted + random access; it halves the range each step: O(log n).",
                  "Loop invariant 'answer in [lo,hi]' + excluding mid every step = bug-free template.",
                  "lower_bound/upper_bound find first/last occurrences and insertion points in duplicates.",
                  "Rotated arrays: one half is always sorted — identify it, then decide.",
                  "Interpolation (uniform data) and exponential (unbounded) search beat blind halving."],
                 pg)
    c.save(); print("wrote", path)


def pdf_dp(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Dynamic Programming\nVisual Guide",
               "Solve once, reuse forever —\nturning exponential recursion into polynomial tables.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Overlapping Subproblems",
                       "Naive recursion recomputes the same states exponentially many times.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y, "fib(5)")
    c.drawString(140, y - 30, "fib(4)            fib(3)")
    c.drawString(180, y - 60, "fib(3)   fib(2)   fib(2)  fib(1)")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10.5)
    c.drawString(180, y - 84, "fib(3) computed TWICE -> fib(2) THREE times...")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 115, "Call tree has ~2^n nodes for fib(n). The subproblems overlap massively.")
    bullet_list(c, 72, y - 150, [
        "DP applies when: optimal substructure (optimal solution built from optimal subsolutions)...",
        "...AND overlapping subproblems (same states recur) — else it's just divide & conquer.",
        "Two implementations: memoization (top-down) and tabulation (bottom-up). Same complexity.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Memoization: Recursion + Memory",
                       "Top-down: compute on demand, cache every result.")
    y0 = codeblock(c, 72, y, [
        "  from functools import lru_cache",
        "  @lru_cache(maxsize=None)",
        "  def fib(n):",
        "      if n < 2: return n",
        "      return fib(n-1) + fib(n-2)   # each n computed ONCE",
        "  # O(n) time, O(n) space (cache + recursion stack)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Natural to write: take the naive recursion, add a cache — done.",
        "Only computes states actually visited — wins on sparse state spaces.",
        "Costs: recursion depth (stack overflow on deep n) + cache overhead.",
        "lru_cache turns any pure recursive function into a memoized one in one line.",
    ], font_size=10.5, gap=26)
    note(c, 72, 180, 468, "Memoization answers 'have I seen this state?' Tabulation answers 'in what order do I fill states?' Both kill the recomputation.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Tabulation: Bottom-Up Tables",
                       "Fill a table in dependency order — no recursion at all.")
    y0 = codeblock(c, 72, y, [
        "  def fib(n):",
        "      dp = [0, 1] + [0]*(n-1)",
        "      for i in range(2, n+1):",
        "          dp[i] = dp[i-1] + dp[i-2]   # subsolutions ready",
        "      return dp[n]",
        "",
        "  # space-optimized: only dp[i-1], dp[i-2] needed -> O(1) space",
        "  a, b = 0, 1",
        "  for _ in range(n): a, b = b, a + b",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Iterative: no stack overflow, often faster (no call overhead).",
        "Computes ALL states up to n — wasteful if only a few are needed.",
        "Space optimization: keep only the previous row(s) — knapsack goes O(n*W) -> O(W).",
        "Rule: if the transition uses only k previous rows, keep k rows.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "The DP Recipe",
                       "Five steps that solve any DP problem.")
    steps = [("1. State", "dp[i] = answer for prefix/subproblem i — define it precisely", BOX_BLUE),
             ("2. Transition", "dp[i] = f(dp[j]) for j < i — how states combine", BOX_GREEN),
             ("3. Base cases", "dp[0], dp[1]... — the seeds the recurrence grows from", BOX_ORANGE),
             ("4. Order", "fill so dependencies are ready — usually increasing i", BOX_TEAL),
             ("5. Answer", "which cell holds the final answer? dp[n], max(dp)...", BOX_PURP)]
    yy = y
    for name, desc, fill in steps:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, 130, 468, "90% of DP debugging is a wrong state definition. If you can't say dp[i] in one sentence, the definition is wrong.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Classic Patterns",
                       "Three archetypes that cover most DP interviews.")
    y0 = codeblock(c, 72, y, [
        "  # 0/1 KNAPSACK: take-or-skip each item",
        "  dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])",
        "",
        "  # LIS (longest increasing subsequence): O(n^2), or O(n log n) patience",
        "  dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])",
        "",
        "  # EDIT DISTANCE: insert/delete/replace",
        "  dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Knapsack family: subset sum, partition, coin change (unbounded = reuse items).",
        "Sequence family: LCS, LIS, edit distance — 2D tables over two strings.",
        "Interval/grid family: matrix paths, burst balloons — expand the interval.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "DP Traps",
                       "Where DP solutions go wrong.")
    bullet_list(c, 72, y, [
        "Greedy confusion: DP explores all choices; greedy commits — coin change needs DP for arbitrary coins.",
        "State too small: 1D when the transition needs 2D (knapsack needs item index AND weight).",
        "Wrong order: filling dp[i] before dp[i-1] is ready — tabulation order must respect dependencies.",
        "Off-by-one bases: dp[0] means 'empty prefix' — get it wrong and everything shifts.",
        "Exponential state: n=100 with 2^n states isn't DP, it's wishful thinking — find a smaller state.",
        "Forgetting the space optimization — and forgetting when it breaks reconstruction of the actual solution.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Dynamic Programming — Remember",
                 ["DP needs optimal substructure + overlapping subproblems — else it's divide & conquer.",
                  "Memoization (top-down + cache) and tabulation (bottom-up table) give the same complexity.",
                  "Recipe: state -> transition -> base cases -> fill order -> answer cell.",
                  "Knapsack (take-or-skip), LIS/LCS (sequences), edit distance (insert/delete/replace) are the archetypes.",
                  "Optimize space to the last k rows — but keep full tables when you must reconstruct the solution."],
                 pg)
    c.save(); print("wrote", path)


def pdf_recursion(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Recursion\nVisual Guide",
               "Functions calling functions —\nthe call stack, base cases, and when to iterate instead.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "The Call Stack: Frames in Action",
                       "Each call pushes a frame; return pops it. factorial(3) traced:")
    frames = [("fact(3)", "n=3, waiting on fact(2)", BOX_BLUE),
              ("fact(2)", "n=2, waiting on fact(1)", BOX_BLUE),
              ("fact(1)", "n=1, BASE -> returns 1", BOX_GREEN)]
    yy = y
    for name, desc, fill in frames:
        box(c, 150, yy - 52, 312, 56, fill, name, desc, font_size=11)
        yy -= 66
    arrow(c, 480, y - 40, 480, y - 230, color=ACCENT, width=2.5, label="unwind: 1*1=1, 2*1=2, 3*2=6")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, yy - 20, "Frame holds: parameters, locals, return address. Depth 3 here — depth n costs O(n) stack space.")
    note(c, 72, yy - 80, 468, "Python default recursion limit: 1000 frames. Deep recursion (long chains, big grids) needs iteration or sys.setrecursionlimit + care.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Anatomy: Base Case + Recursive Step",
                       "Two parts, both mandatory — miss one and it never ends.")
    y0 = codeblock(c, 72, y, [
        "  def factorial(n):",
        "      if n <= 1: return 1          # BASE CASE: smallest input, no recursion",
        "      return n * factorial(n - 1)  # RECURSIVE STEP: smaller problem",
        "",
        "  # every call must move TOWARD the base case: n -> n-1 -> ... -> 1",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Base case: the answer you know directly — without it: infinite recursion -> RecursionError.",
        "Progress: each call shrinks the problem — n-1, half the array, one subtree.",
        "Trust the recursion: assume factorial(n-1) works; your only job is the n-case.",
        "Multiple base cases are fine (fib needs n under 2); zero base cases is a bug.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Trace It: Fibonacci's Explosion",
                       "Beautiful definition, catastrophic runtime — without memoization.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y, "fib(5)")
    c.drawString(120, y - 32, "fib(4)                fib(3)")
    c.drawString(150, y - 64, "fib(3)    fib(2)      fib(2) fib(1)")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10.5)
    c.drawString(72, y - 100, "~2^n calls.  fib(50) = 12.5 TRILLION calls — heat death first.")
    y0 = codeblock(c, 72, y - 130, [
        "  # recurrence: T(n) = T(n-1) + T(n-2) + O(1)  =>  T(n) = O(2^n)",
        "  # fix: memoize (DP!) or iterate — both O(n)",
    ])
    note(c, 72, y0 - 60, 468, "Recursion + overlapping subproblems = exponential. The fix is memoization — which is exactly dynamic programming (see the DP guide).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Tail Recursion",
                       "Recursive call is the LAST action — in theory, optimizable to a loop.")
    y0 = codeblock(c, 72, y, [
        "  # TAIL recursive: nothing left to do after the call",
        "  def fact_tr(n, acc=1):",
        "      if n <= 1: return acc",
        "      return fact_tr(n - 1, acc * n)   # last action = the call",
        "",
        "  # NOT tail: work remains after the call returns",
        "  def fact(n):",
        "      if n <= 1: return 1",
        "      return n * fact(n - 1)           # multiply AFTER return",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Tail-call optimization (TCO): reuse the frame instead of pushing — O(1) stack.",
        "Scheme/Haskell do TCO; Python and Java do NOT — write the loop yourself there.",
        "Accumulator parameter carries the 'work so far' — the standard tail-recursion transform.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Recursion vs Iteration",
                       "Same power, different trade-offs.")
    rows = [("Readability", "mirrors problem structure", "loop bookkeeping visible", BOX_GREEN),
            ("Tree/graph walks", "natural (DFS)", "explicit stack needed", BOX_BLUE),
            ("Overhead", "call frames + returns", "minimal", BOX_ORANGE),
            ("Depth limits", "stack overflow risk", "no limit", BOX_RED),
            ("State", "implicit in frames", "explicit variables", BOX_TEAL)]
    yy = y
    for name, rec, it, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"recursion: {rec}  |  iteration: {it}", font_size=10.5)
        yy -= 70
    note(c, 72, 120, 468, "Rule: recurse for branching structures (trees, backtracking); iterate for long linear chains. Convert with an explicit stack when both matter.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Recursion Patterns",
                       "Five shapes you'll meet again and again.")
    rows = [("Linear", "fact(n), linked-list walk — one recursive call", BOX_BLUE),
            ("Binary", "fib, merge sort — two calls, combine results", BOX_GREEN),
            ("Multi-way", "tree DFS, permutations — loop over children", BOX_TEAL),
            ("Backtracking", "try, recurse, UNDO — N-queens, Sudoku", BOX_ORANGE),
            ("Divide & conquer", "split, solve, merge — quicksort, mergesort", BOX_PURP)]
    yy = y
    for name, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Recursion — Remember",
                 ["Each call pushes a frame (params, locals, return addr); depth n costs O(n) stack.",
                  "Base case + progress toward it: miss either and you get infinite recursion.",
                  "Naive fib is O(2^n) from overlapping subproblems — memoize or iterate to O(n).",
                  "Tail recursion (call is the last action) enables TCO — but Python/Java don't do it.",
                  "Recurse for branching structures, iterate for long chains; convert with an explicit stack."],
                 pg)
    c.save(); print("wrote", path)


def pdf_oop(path):
    c = new_canvas(path); pg = 1
    title_page(c, "OOP Principles\nVisual Guide",
               "Encapsulation, inheritance, polymorphism —\nand knowing when NOT to use them.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "The Four Pillars",
                       "One idea each — the rest of OOP is commentary.")
    pillars = [("Encapsulation", "hide state, expose behavior", BOX_BLUE),
               ("Abstraction", "model essentials, ignore the rest", BOX_TEAL),
               ("Inheritance", "reuse via is-a hierarchies", BOX_GREEN),
               ("Polymorphism", "one interface, many behaviors", BOX_ORANGE)]
    bx = 72
    for name, desc, fill in pillars:
        box(c, bx, y - 80, 108, 76, fill, name, "", font_size=10)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8.5)
        words = desc.split(); lines, cur = [], ""
        for wd in words:
            if c.stringWidth(cur + " " + wd, BODY_FONT, 8.5) > 96: lines.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        lines.append(cur)
        ty = y - 108
        for ln in lines[:2]: c.drawCentredString(bx + 54, ty, ln); ty -= 11
        bx += 120
    bullet_list(c, 72, y - 130, [
        "OOP bundles DATA with the CODE that operates on it — an object owns its state.",
        "Class = blueprint; object = instance; method = function bound to an object.",
        "The pillars reinforce each other: encapsulation enables safe polymorphism.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Encapsulation: Hide the Gears",
                       "Private state, public behavior — invariants enforced at the boundary.")
    y0 = codeblock(c, 72, y, [
        "  class BankAccount:",
        "      def __init__(self): self.__balance = 0   # private by convention",
        "      def deposit(self, amt):",
        "          if amt <= 0: raise ValueError        # invariant HERE",
        "          self.__balance += amt",
        "      def balance(self): return self.__balance  # read-only view",
    ])
    box(c, 72, y0 - 90, 220, 60, BOX_RED, "balance = -500?", "impossible: no setter", font_size=10.5)
    box(c, 320, y0 - 90, 220, 60, BOX_GREEN, "deposit(100)", "validated at the gate", font_size=10.5)
    bullet_list(c, 72, y0 - 130, [
        "If every method preserves the invariant, the object can never be invalid.",
        "Exposing raw fields invites every caller to break your assumptions — don't.",
        "Tell, don't ask: call account.withdraw(x), don't read balance and do math outside.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Inheritance: The Is-A Chain",
                       "Subclasses reuse and specialize — power with a coupling cost.")
    box(c, 216, 500, 180, 60, BOX_BLUE, "Animal", "speak(), move()", font_size=12)
    box(c, 72, 400, 150, 60, BOX_GREEN, "Dog", "speak() -> 'woof'", font_size=11)
    box(c, 246, 400, 150, 60, BOX_GREEN, "Cat", "speak() -> 'meow'", font_size=11)
    box(c, 420, 400, 120, 60, BOX_TEAL, "Robot?", "NOT an animal!", font_size=11)
    arrow(c, 147, 400, 280, 500, color=ACCENT, width=1.8)
    arrow(c, 321, 400, 316, 500, color=ACCENT, width=1.8)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 545, "inherits")
    y0 = codeblock(c, 72, 360, [
        "  class Dog(Animal):",
        "      def speak(self): return 'woof'   # override",
        "  # Dog reuses Animal.move() for free — but is now COUPLED to Animal",
    ])
    note(c, 72, y0 - 60, 468, "Fragile base class: changing Animal can silently break every subclass. Inheritance is the strongest coupling in OOP — spend it wisely.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Polymorphism: One Call, Many Behaviors",
                       "Code to the interface — the object decides what 'speak' means.")
    y0 = codeblock(c, 72, y, [
        "  def chorus(animals):",
        "      for a in animals: print(a.speak())  # no ifs, no type checks",
        "",
        "  chorus([Dog(), Cat(), Bird()])",
        "  # woof / meow / chirp — dynamic dispatch picks the method",
    ])
    box(c, 72, y0 - 90, 468, 64, BOX_ORANGE, "a.speak()", "compile-time: unknown  |  run-time: resolved by actual type", font_size=11)
    bullet_list(c, 72, y0 - 130, [
        "Subtype polymorphism: subclasses stand in for the base type (Liskov's rule).",
        "Duck typing: 'if it speaks like a duck' — Python/JavaScript skip the hierarchy entirely.",
        "Kills switch-on-type chains: new animal = new class, zero edits to chorus().",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Composition Over Inheritance",
                       "Has-a beats is-a: assemble behavior instead of inheriting it.")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y, "Brittle: deep hierarchy")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, y - 22, "Vehicle -> Car -> SportsCar -> ConvertibleSportsCar ...")
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y - 60, "Flexible: compose parts")
    y0 = codeblock(c, 72, y - 80, [
        "  class Car:",
        "      def __init__(self, engine, brakes):  # has-a engine, has-a brakes",
        "          self.engine, self.brakes = engine, brakes",
        "  # swap ElectricEngine for V8 — no hierarchy surgery",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Inheritance locks behavior at COMPILE time; composition swaps it at RUN time.",
        "Strategy pattern IS composition: the algorithm becomes a swappable part.",
        "Rule of thumb: inherit for true is-a (rare); compose for everything else.",
    ], font_size=10.5, gap=24)
    note(c, 72, 150, 468, "The Gang of Four said it first: 'favor object composition over class inheritance.' Thirty years later, still the best OOP advice.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "OOP Traps",
                       "Where object thinking goes wrong.")
    bullet_list(c, 72, y, [
        "God objects: one class doing everything — encapsulation without boundaries.",
        "Inheritance for code reuse alone: reuse is composition's job; inheritance is for polymorphism.",
        "Getters/setters for every field: that's a struct with extra steps, not encapsulation.",
        "Premature hierarchies: three levels deep before the second use case exists.",
        "Anemic domain models: data classes + procedural services — OOP syntax, procedural soul.",
        "Not everything is an object: pure transforms and pipelines often read better as functions.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "OOP Principles — Remember",
                 ["Encapsulation: private state + validating methods keep objects always-valid.",
                  "Inheritance reuses via is-a but couples tightly — fragile base classes bite.",
                  "Polymorphism: code to the interface; dynamic dispatch picks the behavior.",
                  "Prefer composition (has-a, swappable at run time) over inheritance (locked at compile time).",
                  "Getters-for-everything and god objects are OOP-shaped procedural code."],
                 pg)
    c.save(); print("wrote", path)


def pdf_solid(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SOLID Principles\nVisual Guide",
               "Five design rules —\neach with a before/after that shows the payoff.",
               CAT, None); pg += 1

    def before_after(yy, before_lines, after_lines, h):
        y0 = codeblock(c, 72, yy, ["  # BEFORE"] + before_lines, w=228, fsize=9, fill=BOX_RED)
        y1 = codeblock(c, 312, yy, ["  # AFTER"] + after_lines, w=228, fsize=9, fill=BOX_GREEN)
        return min(y0, y1)

    y = section_header(c, 1, 6, "S — Single Responsibility",
                       "One class, one reason to change.")
    yy = before_after(y, [
        "  class Report:",
        "      def generate(self): ...",
        "      def save_to_db(self): ...",
        "      def email(self): ...",
        "      def print_pdf(self): ...",
    ], [
        "  class Report:        # data only",
        "      def generate(self): ...",
        "  class ReportSaver: ...   # persistence",
        "  class ReportMailer: ...  # delivery",
    ], 0)
    bullet_list(c, 72, yy - 30, [
        "'Reason to change' = an axis of requirements: formatting vs storage vs delivery.",
        "Smaller classes are easier to test, name, and delete.",
        "Smell: a class whose methods never touch the same fields — it's two classes already.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "O — Open / Closed",
                       "Open for extension, closed for modification.")
    yy = before_after(y, [
        "  def price(o):",
        "      if o.type == 'book': ...",
        "      elif o.type == 'food': ...",
        "      elif o.type == 'NEW': ...  # edit me!",
    ], [
        "  class Pricer:          # interface",
        "      def price(self, o): ...",
        "  class BookPricer(Pricer): ...",
        "  # new type = new class, zero edits",
    ], 0)
    bullet_list(c, 72, yy - 30, [
        "New behavior arrives as NEW code, not edits to old code — old paths stay proven.",
        "Polymorphism is the mechanism: the if-chain becomes a class hierarchy.",
        "Plugin architectures are OCP at scale: core closed, extensions open.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "L — Liskov Substitution",
                       "Subclasses must honor the base contract — no surprises.")
    yy = before_after(y, [
        "  class Rect:",
        "      def set_w(self, w): ...",
        "      def set_h(self, h): ...",
        "  class Square(Rect):",
        "      def set_w(self, w):  # sets BOTH!",
        "          ...             # breaks callers",
    ], [
        "  class Shape:            # shared interface",
        "      def area(self): ...",
        "  class Rect(Shape): ...",
        "  class Square(Shape): ...  # siblings, not parent/child",
    ], 0)
    bullet_list(c, 72, yy - 30, [
        "The classic violation: Square is-a Rectangle mathematically, but NOT behaviorally.",
        "Test: any code using the base must work unchanged with the subclass.",
        "Violations hide in overridden methods that weaken preconditions or strengthen postconditions.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "I — Interface Segregation",
                       "No client should depend on methods it doesn't use.")
    yy = before_after(y, [
        "  class Worker:  # fat interface",
        "      def work(self): ...",
        "      def eat(self): ...",
        "  class Robot(Worker):",
        "      def eat(self): raise ...  # forced lie!",
    ], [
        "  class Workable:          # small interfaces",
        "      def work(self): ...",
        "  class Eatable:",
        "      def eat(self): ...",
        "  class Robot(Workable): ...  # only what it needs",
    ], 0)
    bullet_list(c, 72, yy - 30, [
        "Fat interfaces force empty/throwing methods — lies in the type system.",
        "Small role interfaces compose freely: Workable + Eatable as needed.",
        "Same idea as Unix tools: do one thing, combine via composition.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "D — Dependency Inversion",
                       "Depend on abstractions, not concretions.")
    box(c, 72, 480, 200, 60, BOX_RED, "OrderService", "-> MySQL directly", font_size=11)
    arrow(c, 272, 510, 300, 510, color=RED, width=2)
    box(c, 310, 480, 200, 60, BOX_RED, "MySQL", "concrete", font_size=11)
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 12); c.drawCentredString(306, 440, "invert it")
    arrow(c, 306, 430, 306, 400, color=GREEN, width=2.5)
    box(c, 72, 320, 200, 60, BOX_GREEN, "OrderService", "-> Repository", font_size=11)
    box(c, 310, 320, 200, 60, BOX_BLUE, "MySQLRepo", "implements Repository", font_size=11)
    arrow(c, 272, 350, 300, 350, color=GREEN, width=2)
    y0 = codeblock(c, 72, 290, [
        "  # constructor injection: pass the abstraction in",
        "  svc = OrderService(repo=MySQLRepo())   # or FakeRepo() in tests!",
    ])
    bullet_list(c, 72, y0 - 30, [
        "High-level policy (orders) must not depend on low-level detail (MySQL).",
        "Testing payoff: swap the real repo for a fake — no database in unit tests.",
        "The interface is owned by the HIGH-level module — it declares what it needs.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "SOLID Together",
                       "Five rules, one direction: change gets cheaper.")
    bullet_list(c, 72, y, [
        "SRP splits by reason to change; OCP makes change additive; LSP keeps substitution safe.",
        "ISP keeps contracts small; DIP points dependencies at abstractions.",
        "SOLID serves MAINTAINABILITY — for a 100-line script, it's over-engineering. Apply by scale.",
        "Smells that call for SOLID: shotgun surgery, rigid if-chains, untestable constructors.",
        "Principles guide, not laws: a pragmatic violation with a comment beats dogmatic purity.",
        "Pair with: composition over inheritance, dependency injection, and small functions.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SOLID Principles — Remember",
                 ["S: one class, one reason to change — split by axes of requirements.",
                  "O: extend with new code, don't edit proven code — polymorphism over if-chains.",
                  "L: subclasses must honor the base contract (Square is not a behavioral Rectangle).",
                  "I: small role interfaces beat fat ones — no forced empty methods.",
                  "D: depend on abstractions; inject concretions — testability is the payoff."],
                 pg)
    c.save(); print("wrote", path)


def pdf_patterns_1(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Design Patterns I: Creational\nVisual Guide",
               "Who makes the objects —\nfive ways to control creation.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Singleton: One Instance, Global Access",
                       "A class that refuses to be built twice.")
    y0 = codeblock(c, 72, y, [
        "  class Config:",
        "      _inst = None",
        "      def __new__(cls):",
        "          if cls._inst is None: cls._inst = super().__new__(cls)",
        "          return cls._inst     # every call returns THE instance",
    ])
    box(c, 72, y0 - 80, 140, 56, BOX_BLUE, "Config()", "", font_size=10.5)
    box(c, 252, y0 - 80, 140, 56, BOX_BLUE, "Config()", "", font_size=10.5)
    arrow(c, 212, y0 - 52, 250, y0 - 52, color=ACCENT, width=1.8)
    arrow(c, 392, y0 - 52, 430, y0 - 52, color=ACCENT, width=1.8)
    box(c, 432, y0 - 80, 108, 56, BOX_GREEN, "THE", "instance", font_size=11)
    bullet_list(c, 72, y0 - 120, [
        "Use for: config, connection pools, loggers — truly singular resources.",
        "Costs: global state in disguise — hidden coupling, painful tests (can't isolate).",
        "Threads: double-checked locking or module-level init — naive singletons race.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Factory Method: Let Subclasses Decide",
                       "Define the interface for creation; subclasses pick the class.")
    box(c, 72, 480, 150, 60, BOX_BLUE, "Dialog", "createButton()", font_size=11)
    box(c, 260, 480, 120, 60, BOX_GREEN, "WinDialog", "WinButton", font_size=10.5)
    box(c, 420, 480, 120, 60, BOX_GREEN, "MacDialog", "MacButton", font_size=10.5)
    arrow(c, 222, 510, 258, 510, color=ACCENT, width=1.8)
    arrow(c, 380, 510, 418, 510, color=ACCENT, width=1.8)
    y0 = codeblock(c, 72, 440, [
        "  class Dialog:",
        "      def render(self): btn = self.create_button()  # subclass decides",
        "  class WinDialog(Dialog):",
        "      def create_button(self): return WinButton()",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Client code never names a concrete class — the factory method hides it.",
        "OCP in action: new platform = new Dialog subclass, zero client edits.",
        "Simple factory (a plain function) covers 80% of cases — reach for the pattern when subclasses vary.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Abstract Factory: Families of Products",
                       "Create CONSISTENT sets — WinButton with WinCheckbox, never mixed.")
    box(c, 72, 490, 200, 60, BOX_PURP, "GUIFactory", "create_button()\ncreate_checkbox()", font_size=10.5)
    box(c, 310, 490, 110, 60, BOX_BLUE, "WinFactory", "", font_size=10.5)
    box(c, 430, 490, 110, 60, BOX_GREEN, "MacFactory", "", font_size=10.5)
    arrow(c, 272, 520, 308, 520, color=ACCENT, width=1.8)
    box(c, 72, 400, 110, 54, BOX_BLUE, "WinButton", "", font_size=10)
    box(c, 200, 400, 130, 54, BOX_BLUE, "WinCheckbox", "", font_size=10)
    box(c, 350, 400, 110, 54, BOX_GREEN, "MacButton", "", font_size=10)
    box(c, 478, 400, 62, 54, BOX_GREEN, "MacBox", "", font_size=9)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawString(72, 370, "WinButton + MacCheckbox together = broken UI. The factory guarantees matching sets.")
    bullet_list(c, 72, 335, [
        "Factory method makes ONE product; abstract factory makes a FAMILY.",
        "Swap entire product lines by swapping one factory object.",
        "Cost: adding a new product means touching every factory — plan the family upfront.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Builder: Step-by-Step Construction",
                       "Telescoping constructors are unreadable — build fluently instead.")
    y0 = codeblock(c, 72, y, [
        "  # BEFORE: what does False mean here?",
        "  Pizza(size=12, cheese=True, pepperoni=False, gluten_free=True, ...)",
        "",
        "  # AFTER: readable, optional steps, validated at build()",
        "  pizza = (PizzaBuilder().size(12).cheese().gluten_free().build())",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Each method returns self (fluent) — steps read like a sentence.",
        "build() validates the whole: required fields present, combos legal.",
        "Director: a preset recipe (margherita()) over the same builder steps.",
        "Immutable result: builder is mutable, the built object is frozen.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Prototype: Clone, Don't Rebuild",
                       "Copy a configured exemplar instead of constructing from scratch.")
    y0 = codeblock(c, 72, y, [
        "  import copy",
        "  base_enemy = Enemy(hp=100, ai='aggressive', sprite=load('orc.png'))",
        "  orc2 = copy.deepcopy(base_enemy)   # configured copy, cheap",
        "  orc2.hp = 150                      # tweak the clone",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Wins when construction is expensive (parsed assets, DB rows, complex graphs).",
        "Shallow vs deep copy: shared references bite — deepcopy nests, shallow shares.",
        "Registry of prototypes: ask for 'orc' by name, get a fresh clone — a factory of clones.",
        "Spawn systems in games: one archetype per enemy type, cloned per spawn.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Creational Chooser",
                       "Which creation pattern for which pain?")
    rows = [("Exactly one instance", "Singleton", "config, pools — beware global state", BOX_BLUE),
            ("Subclass picks the class", "Factory Method", "platform-specific objects", BOX_GREEN),
            ("Consistent product families", "Abstract Factory", "themed UI kits", BOX_PURP),
            ("Many optional parameters", "Builder", "fluent, validated construction", BOX_ORANGE),
            ("Expensive to construct", "Prototype", "clone a configured exemplar", BOX_TEAL)]
    yy = y
    for name, pat, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, pat, f"{name} — {desc}", font_size=11)
        yy -= 70
    note(c, 72, 130, 468, "Start simple: a function returning objects IS a factory. Promote to a pattern only when creation logic itself needs organizing.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Creational Patterns — Remember",
                 ["Singleton: one instance, global access — truly singular resources only; it's global state.",
                  "Factory Method: subclasses decide which class to instantiate; clients stay decoupled.",
                  "Abstract Factory: builds consistent FAMILIES of products (never mix WinButton with MacCheckbox).",
                  "Builder: fluent step-by-step construction with validation at build(); kills telescoping constructors.",
                  "Prototype: clone configured exemplars when construction is expensive — mind shallow vs deep copy."],
                 pg)
    c.save(); print("wrote", path)


def pdf_patterns_2(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Design Patterns II: Structural\nVisual Guide",
               "How objects fit together —\nfive ways to compose interfaces.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Adapter: Make Incompatible Interfaces Fit",
                       "The plug converter — wrap it, don't rewrite it.")
    box(c, 72, 460, 140, 64, BOX_BLUE, "Client", "wants USB-C", font_size=11)
    box(c, 350, 460, 140, 64, BOX_ORANGE, "OldPrinter", "only USB-A", font_size=11)
    box(c, 211, 460, 140, 64, BOX_GREEN, "Adapter", "USB-C -> USB-A", font_size=10.5)
    arrow(c, 212, 492, 209, 492, color=ACCENT, width=2)
    arrow(c, 351, 492, 348, 492, color=ACCENT, width=2)
    y0 = codeblock(c, 72, 420, [
        "  class PrinterAdapter(Printer):      # looks like a Printer",
        "      def __init__(self, old): self.old = old",
        "      def print(self, doc): self.old.print_usb_a(doc)  # translates",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Client talks to the TARGET interface; the adapter translates to the ADAPTEE.",
        "Use when: third-party library, legacy code, or API version mismatch.",
        "Object adapter (composition) beats class adapter (inheritance) — more flexible.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Decorator: Add Behavior in Layers",
                       "Wrap the object — each layer adds one responsibility.")
    box(c, 72, 480, 110, 56, BOX_BLUE, "Coffee", "$2", font_size=11)
    arrow(c, 182, 508, 210, 508, color=ACCENT, width=2)
    box(c, 212, 480, 110, 56, BOX_GREEN, "+ Milk", "$0.5", font_size=11)
    arrow(c, 322, 508, 350, 508, color=ACCENT, width=2)
    box(c, 352, 480, 110, 56, BOX_ORANGE, "+ Sugar", "$0.2", font_size=11)
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 11)
    c.drawString(72, 448, "total: $2.70 — any combination, no class explosion")
    y0 = codeblock(c, 72, 415, [
        "  class Milk(CoffeeDecorator):",
        "      def cost(self): return self.coffee.cost() + 0.5  # wrap + extend",
        "  # vs subclassing: MilkCoffee, SugarCoffee, MilkSugarCoffee... 2^n classes!",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Same interface in and out — decorators stack transparently.",
        "Python's @decorators and Java I/O streams are decorators in the wild.",
        "Order can matter: encryption-then-compress differs from compress-then-encrypt.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Facade: One Simple Door",
                       "Hide a messy subsystem behind a clean function.")
    box(c, 216, 470, 180, 60, BOX_GREEN, "encode_video(file)", "the facade", font_size=12)
    for i, name in enumerate(["Demuxer", "Decoder", "Filters", "Encoder", "Muxer"]):
        box(c, 72 + i * 96, 370, 88, 54, BOX_BLUE, name, "", font_size=9.5)
        arrow(c, 306, 470, 72 + i * 96 + 44, 424, color=MUTED, width=1.2)
    y0 = codeblock(c, 72, 330, [
        "  def encode_video(f):           # client calls ONE function",
        "      raw = Demuxer(f).split()   # facade orchestrates five subsystems",
        "      ...",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Facade doesn't hide the subsystem — power users can still go direct.",
        "Libraries live here: requests hides sockets, SSL, and redirects behind get().",
        "One facade per workflow; don't build a god-facade over everything.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Proxy: A Stand-In with Control",
                       "Same interface, extra gatekeeping — lazy, protective, or remote.")
    box(c, 72, 470, 130, 60, BOX_BLUE, "Client", "", font_size=11)
    box(c, 250, 470, 140, 60, BOX_GREEN, "Proxy", "checks first", font_size=11)
    box(c, 430, 470, 110, 60, BOX_ORANGE, "Real", "heavy", font_size=11)
    arrow(c, 202, 500, 248, 500, color=ACCENT, width=2)
    arrow(c, 390, 500, 428, 500, color=ACCENT, width=2)
    rows = [("Virtual proxy", "lazy-load the heavy object (big images, ORM)", BOX_BLUE),
            ("Protection proxy", "auth check before the call proceeds", BOX_RED),
            ("Remote proxy", "local stub for a remote object (RPC)", BOX_TEAL),
            ("Caching proxy", "memoize expensive results", BOX_GREEN)]
    yy = 400
    for name, desc, fill in rows:
        box(c, 72, yy - 48, 468, 52, fill, name, desc, font_size=11)
        yy -= 64
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Composite: Trees of Uniform Parts",
                       "Treat a leaf and a whole subtree the same way.")
    box(c, 216, 500, 180, 56, BOX_PURP, "Folder", "children[]", font_size=12)
    box(c, 72, 400, 120, 56, BOX_BLUE, "File A", "leaf", font_size=11)
    box(c, 216, 400, 180, 56, BOX_PURP, "Folder", "children[]", font_size=11)
    box(c, 420, 400, 120, 56, BOX_BLUE, "File B", "leaf", font_size=11)
    arrow(c, 280, 500, 132, 456, color=ACCENT, width=1.8)
    arrow(c, 330, 500, 306, 456, color=ACCENT, width=1.8)
    y0 = codeblock(c, 72, 360, [
        "  class Node:",
        "      def size(self): ...            # File: its bytes",
        "  class Folder(Node):                # Composite: sum of children",
        "      def size(self): return sum(k.size() for k in self.children)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Client code never asks 'file or folder?' — one interface, recursive structure.",
        "DOM trees, org charts, UI widget hierarchies, arithmetic expressions.",
        "Price: the interface must fit BOTH leaves and composites — keep it minimal.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Structural Chooser",
                       "Which assembly pattern for which pain?")
    rows = [("Incompatible interfaces", "Adapter", "wrap and translate", BOX_BLUE),
            ("Add behavior dynamically", "Decorator", "layered wrapping", BOX_GREEN),
            ("Simplify a subsystem", "Facade", "one clean entry point", BOX_ORANGE),
            ("Control access to an object", "Proxy", "lazy / guard / remote / cache", BOX_TEAL),
            ("Part-whole hierarchies", "Composite", "leaf and group, one interface", BOX_PURP)]
    yy = y
    for name, pat, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, pat, f"{name} — {desc}", font_size=11)
        yy -= 70
    note(c, 72, 130, 468, "Adapter vs Facade vs Proxy: adapter CHANGES an interface, facade SIMPLIFIES many, proxy KEEPS the interface and adds control.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Structural Patterns — Remember",
                 ["Adapter wraps incompatible interfaces (USB-C to USB-A) without rewriting either side.",
                  "Decorator layers behavior by wrapping — same interface in and out, no class explosion.",
                  "Facade gives one simple door over a messy subsystem; power users can still go direct.",
                  "Proxy stands in with control: lazy loading, auth gates, remote stubs, caching.",
                  "Composite treats leaves and groups uniformly — file/folder, DOM, widget trees."],
                 pg)
    c.save(); print("wrote", path)


def pdf_patterns_3(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Design Patterns III: Behavioral\nVisual Guide",
               "How objects talk —\nfive ways to organize communication.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Observer: Publish / Subscribe",
                       "One subject, many dependents — notify, don't poll.")
    box(c, 216, 490, 180, 60, BOX_BLUE, "Subject", "state + notify()", font_size=12)
    for i, name in enumerate(["EmailView", "SMSView", "LogView"]):
        box(c, 72 + i * 156, 390, 144, 56, BOX_GREEN, name, "update()", font_size=10.5)
        arrow(c, 306, 490, 72 + i * 156 + 72, 446, color=ACCENT, width=1.8)
    y0 = codeblock(c, 72, 350, [
        "  subject.attach(email_view); subject.attach(sms_view)",
        "  subject.set_state('shipped')   # all observers update()",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Subject knows only the OBSERVER interface — observers stay decoupled.",
        "Event buses, reactive UI, model-view: the observer is everywhere.",
        "Lapsed-listener leak: observers that never detach pin memory — unsubscribe!",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Strategy: Swappable Algorithms",
                       "Composition's favorite child — the algorithm becomes a part.")
    box(c, 72, 480, 180, 60, BOX_BLUE, "Navigator", "route()", font_size=12)
    box(c, 300, 480, 110, 60, BOX_GREEN, "Car", "", font_size=10.5)
    box(c, 420, 480, 120, 60, BOX_GREEN, "Bike", "", font_size=10.5)
    arrow(c, 252, 510, 298, 510, color=ACCENT, width=2, label="uses")
    y0 = codeblock(c, 72, 440, [
        "  nav = Navigator(strategy=CarStrategy())   # pick at RUNTIME",
        "  nav.route(a, b)",
        "  nav.strategy = BikeStrategy()             # swap mid-trip",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Kills the if-transport == 'car' chains — new strategy = new class.",
        "Sorting comparators, payment methods, compression choices: all strategies.",
        "Strategy vs State: strategy is CHOSEN by the client; state is DRIVEN by the object.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Command: Requests as Objects",
                       "Encapsulate a call — then queue it, log it, undo it.")
    box(c, 72, 480, 120, 60, BOX_BLUE, "Invoker", "button", font_size=11)
    box(c, 240, 480, 140, 60, BOX_GREEN, "Command", "execute()\nundo()", font_size=11)
    box(c, 420, 480, 120, 60, BOX_ORANGE, "Receiver", "the light", font_size=11)
    arrow(c, 192, 510, 238, 510, color=ACCENT, width=2)
    arrow(c, 380, 510, 418, 510, color=ACCENT, width=2)
    y0 = codeblock(c, 72, 440, [
        "  class LightOn(Command):",
        "      def execute(self): self.light.on()",
        "      def undo(self): self.light.off()     # undo stack = list of commands",
        "  remote.press(LightOn(light))             # invoker never knows 'light'",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Undo/redo, macros, job queues, transactional batches — commands make actions data.",
        "Invoker and receiver never meet: total decoupling of 'who asks' from 'who does'.",
        "Store the inverse (or a snapshot) per command and undo becomes trivial.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "State: Behavior Follows State",
                       "An object that rewrites its own responses as it changes.")
    states = ["Locked", "HasCoin", "Dispensing"]
    for i, s in enumerate(states):
        fill = BOX_ORANGE if i == 1 else BOX_BLUE
        box(c, 72 + i * 156, 480, 144, 60, fill, s, "", font_size=11)
    arrow(c, 216, 510, 226, 510, color=ACCENT, width=2, label="coin")
    arrow(c, 372, 510, 382, 510, color=ACCENT, width=2, label="select")
    arrow(c, 382, 480, 372, 480, color=MUTED, width=1.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawCentredString(377, 462, "dispense")
    y0 = codeblock(c, 72, 420, [
        "  class Vending:                       # delegates to current state",
        "      def insert_coin(self): self.state.insert_coin(self)",
        "  class HasCoin(State):",
        "      def insert_coin(self, ctx): return 'already paid!'  # per-state logic",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Replaces sprawling if-state == X chains — each state is a class with its own rules.",
        "Transitions live in the states: HasCoin.select() moves the context to Dispensing.",
        "TCP sockets, game characters, parsers, workflows — state machines in disguise.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Template Method: Skeleton with Hooks",
                       "The algorithm's SHAPE is fixed; steps are overridden.")
    y0 = codeblock(c, 72, y, [
        "  class DataMiner:                       # the TEMPLATE",
        "      def mine(self):                    # final: do not override",
        "          raw = self.extract()           # hook 1",
        "          clean = self.transform(raw)    # hook 2",
        "          self.load(clean)               # hook 3",
        "  class CSVMiner(DataMiner):",
        "      def extract(self): return read_csv(...)   # fill the hooks",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Hollywood principle: 'don't call us, we'll call you' — the base drives, subclasses fill in.",
        "Hooks with default (do-nothing) implementations make steps optional.",
        "Frameworks are template methods at scale: you fill hooks, the framework runs the show.",
        "Prefer composition + strategy when the skeleton itself might need to vary.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Behavioral Chooser",
                       "Which conversation pattern for which pain?")
    rows = [("One-to-many notifications", "Observer", "subject notifies dependents", BOX_BLUE),
            ("Swappable algorithms", "Strategy", "client picks the variant", BOX_GREEN),
            ("Requests as data (undo/queue)", "Command", "execute() + undo()", BOX_ORANGE),
            ("Behavior depends on state", "State", "object rewrites its responses", BOX_TEAL),
            ("Fixed skeleton, varying steps", "Template Method", "base drives, hooks vary", BOX_PURP)]
    yy = y
    for name, pat, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, pat, f"{name} — {desc}", font_size=11)
        yy -= 70
    note(c, 72, 130, 468, "Strategy vs State vs Template: strategy varies the WHOLE algorithm by client choice; state varies behavior by internal condition; template fixes the skeleton and varies steps.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Behavioral Patterns — Remember",
                 ["Observer: subject notifies dependents via update() — remember to detach (lapsed listeners leak).",
                  "Strategy: swappable algorithm objects, chosen at run time — kills if-chains.",
                  "Command: requests as objects with execute()/undo() — undo stacks, queues, macros.",
                  "State: each state is a class; transitions move the context — replaces state if-chains.",
                  "Template Method: fixed skeleton, overridable hooks — the Hollywood principle."],
                 pg)
    c.save(); print("wrote", path)


def pdf_functional(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Functional Programming\nVisual Guide",
               "Purity, immutability, and functions as data —\na calmer way to reason about code.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Purity: Same Input, Same Output",
                       "No surprises: no hidden reads, no hidden writes.")
    box(c, 72, 460, 220, 70, BOX_GREEN, "pure(x)", "f(2) = 4, always", font_size=12)
    box(c, 320, 460, 220, 70, BOX_RED, "impure()", "reads clock,\nwrites DB...", font_size=11)
    y0 = codeblock(c, 72, 425, [
        "  def pure_add(a, b): return a + b          # PURE: output from inputs only",
        "  total = 0",
        "  def impure_add(a):                       # IMPURE: mutates + reads global",
        "      global total; total += a; return total",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Pure functions are trivially testable: no setup, no mocks, no teardown.",
        "Referential transparency: replace f(x) with its value anywhere — refactoring becomes safe.",
        "Push impurity to the edges: pure core, thin impure shell (I/O, randomness, time).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Immutability: Data That Never Changes",
                       "'Update' means 'derive a new version' — the old one survives.")
    box(c, 72, 480, 150, 60, BOX_BLUE, "[1, 2, 3]", "original", font_size=12)
    arrow(c, 222, 510, 260, 510, color=ACCENT, width=2.5, label="append 4")
    box(c, 262, 480, 150, 60, BOX_GREEN, "[1, 2, 3, 4]", "new list", font_size=12)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 450, "original untouched — no aliasing bugs, safe to share across threads")
    y0 = codeblock(c, 72, 415, [
        "  # persistent structures share unchanged parts (structural sharing)",
        "  # tuple, frozenset, NamedTuple; dataclasses(frozen=True)",
        "  from dataclasses import dataclass",
        "  @dataclass(frozen=True)",
        "  class Point: x: int; y: int",
    ])
    bullet_list(c, 72, y0 - 30, [
        "No defensive copies: share freely — nobody can mutate under you.",
        "Undo/history for free: keep old versions; time-travel debugging.",
        "Cost: allocation churn — persistent structures share structure to stay O(log n).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "First-Class & Higher-Order Functions",
                       "Functions as values: passed, returned, composed.")
    y0 = codeblock(c, 72, y, [
        "  def apply_twice(f, x): return f(f(x))      # takes a FUNCTION",
        "  apply_twice(lambda x: x + 1, 5)            # -> 7",
        "",
        "  def make_adder(n):                        # returns a FUNCTION",
        "      return lambda x: x + n                 # closes over n",
        "  add5 = make_adder(5)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Higher-order: takes or returns functions (map, filter, decorators, callbacks).",
        "Closures capture their defining scope — the adder remembers n=5.",
        "Composition: pipe small functions into pipelines — each stays testable alone.",
        "Callbacks, middleware, and hooks are higher-order functions in production clothes.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "map / filter / reduce",
                       "The three verbs of collection processing.")
    y0 = codeblock(c, 72, y, [
        "  nums = [1, 2, 3, 4, 5]",
        "  map:    [x*2 for x in nums]              # [2,4,6,8,10] transform each",
        "  filter: [x for x in nums if x % 2 == 0] # [2,4]         keep matches",
        "  reduce: functools.reduce(lambda a,b: a+b, nums)  # 15  fold to one",
    ])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y0 - 36, "Pipeline style: read the data flow left to right, no loop bookkeeping.")
    y1 = codeblock(c, 72, y0 - 56, [
        "  # declarative pipeline: what, not how",
        "  total = sum(x*x for x in nums if x % 2 == 1)",
    ])
    bullet_list(c, 72, y1 - 30, [
        "Each stage is pure and independent — trivially parallelizable (map-reduce!).",
        "Lazy variants (generators, streams) process infinite or huge data in O(1) memory.",
        "Prefer comprehensions/pipelines over manual loops for transforms — fewer index bugs.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Monads, Gently: The Maybe Pattern",
                       "Chain operations that might fail — without the if-pyramid.")
    y0 = codeblock(c, 72, y, [
        "  # BEFORE: nested None checks",
        "  user = find(id)",
        "  if user: addr = user.address",
        "  ...",
        "",
        "  # AFTER: Optional chaining / Maybe monad",
        "  city = find(id).map(get_address).map(get_city)  # None short-circuits",
        "  # Haskell: Maybe; Rust: Option; Python: optional chaining (3.10+ match)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "A monad = a wrapper (Maybe, Result, Future) + a way to chain (map/flatMap).",
        "Result types: return Ok(value) or Err(reason) — errors as VALUES, not exceptions.",
        "You already use monads: promises/futures chain async work exactly this way.",
        "Intuition over jargon: 'a box you can map over without opening it'.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Functional Traps",
                       "Purity has prices — know them.")
    bullet_list(c, 72, y, [
        "I/O is inherently impure — isolate it at the edges; don't fight it in the core.",
        "Deep recursion without TCO: Python will RecursionError — use loops or trampolines.",
        "Allocation churn: naive immutable updates copy O(n) — use persistent structures.",
        "Over-abstraction: point-free pipelines that nobody can read are a net loss.",
        "Not all state is evil: local, disciplined mutation inside a pure function is fine.",
        "Hybrid wins: functional core for logic, OO/imperative shell for structure and I/O.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Functional Programming — Remember",
                 ["Pure functions: same input, same output — testable, refactorable, parallelizable.",
                  "Immutability: derive new versions instead of mutating; share freely, keep history.",
                  "First-class functions enable higher-order patterns: map/filter/reduce, closures, composition.",
                  "Monads (Maybe/Result/Future) chain fallible steps without nested checks.",
                  "Push impurity to the edges: pure core, thin impure shell."],
                 pg)
    c.save(); print("wrote", path)


def pdf_concurrency(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Concurrency vs Parallelism\nVisual Guide",
               "Doing many things at once —\nor just appearing to? The distinction that decides design.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Concurrency != Parallelism",
                       "The single most confused pair in systems programming.")
    box(c, 72, 440, 220, 90, BOX_BLUE, "Concurrency", "dealing with many\nthings at once", font_size=12)
    box(c, 320, 440, 220, 90, BOX_GREEN, "Parallelism", "DOING many things\nat once", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "One barista juggling 4 orders = concurrent. Four baristas = parallel.")
    c.drawString(72, 382, "Concurrency is about STRUCTURE (interleaving); parallelism is about EXECUTION (simultaneous).")
    bullet_list(c, 72, 345, [
        "You can have concurrency WITHOUT parallelism: one core interleaving tasks.",
        "Parallelism implies concurrency, not vice versa.",
        "Async I/O is concurrency; multi-core number crunching is parallelism.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Threads: Shared-Memory Concurrency",
                       "Multiple flows, one address space — fast to share, easy to corrupt.")
    for i in range(3):
        box(c, 72 + i * 156, 470, 144, 56, BOX_BLUE, f"Thread {i+1}", "own stack", font_size=11)
    box(c, 72, 380, 468, 56, BOX_ORANGE, "shared heap: counters, caches, queues", "one bad write -> all threads see it", font_size=11)
    arrow(c, 144, 470, 200, 436, color=RED, width=1.8)
    arrow(c, 300, 470, 300, 436, color=RED, width=1.8)
    arrow(c, 456, 470, 400, 436, color=RED, width=1.8)
    bullet_list(c, 72, 330, [
        "Threads share memory: communication is cheap (a pointer), coordination is hard (locks).",
        "Preemptive scheduling: the OS can pause you ANYWHERE — every shared access is a race candidate.",
        "Use for: I/O-bound work, responsive UIs, servers handling many connections.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Async: One Thread, Many Waiters",
                       "Cooperative multitasking — tasks yield instead of being preempted.")
    y0 = codeblock(c, 72, y, [
        "  async def fetch(url):",
        "      resp = await http.get(url)   # YIELD: run others while waiting",
        "      return resp.json()",
        "",
        "  await asyncio.gather(*(fetch(u) for u in urls))  # 1000s of tasks, 1 thread",
    ])
    box(c, 72, y0 - 80, 468, 60, BOX_TEAL, "event loop", "tasks yield at await — no locks between yields", font_size=11)
    bullet_list(c, 72, y0 - 120, [
        "No preemption BETWEEN awaits: shared state is safe until you yield — fewer races by construction.",
        "One blocking call (time.sleep, sync I/O) freezes EVERYTHING — never block the loop.",
        "Scales to 10k+ connections where threads would drown in stack memory.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Parallelism: True Simultaneity",
                       "Multiple cores, real speedup — for CPU-bound work.")
    for i in range(4):
        box(c, 72 + i * 120, 470, 108, 60, BOX_GREEN, f"Core {i+1}", "crunching", font_size=11)
    y0 = codeblock(c, 72, 430, [
        "  # threads won't help CPU-bound Python (GIL!) — use processes",
        "  with ProcessPoolExecutor() as ex:",
        "      results = ex.map(train_model, shards)  # one process per core",
    ])
    bullet_list(c, 72, y0 - 30, [
        "CPU-bound + threads + GIL (Python/Ruby) = no speedup — processes or native code instead.",
        "Data parallelism: split the DATA (map-reduce, SIMD); task parallelism: split the WORK.",
        "Overhead matters: spawning a process per tiny task loses — batch the work.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Amdahl's Law: The Speedup Ceiling",
                       "The sequential fraction caps EVERYTHING.")
    y0 = codeblock(c, 72, y, [
        "  speedup(n) = 1 / (s + (1 - s) / n)",
        "  # s = sequential fraction, n = cores",
        "",
        "  s = 10%, n = 100 cores  ->  speedup ~ 9.2x   (NOT 100x!)",
        "  s = 10%, n = infinity   ->  speedup = 10x max",
    ])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y0 - 36, "Halve the sequential part and you double the ceiling — optimize s before buying cores.")
    bullet_list(c, 72, y0 - 70, [
        "Gustafson's counter: bigger problems parallelize better — scale the WORK, not just cores.",
        "Diminishing returns hit fast: 8 -> 16 cores rarely doubles real throughput.",
        "Measure s by profiling — it hides in startup, I/O, and lock contention.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Model Chooser",
                       "Match the model to the bottleneck.")
    rows = [("I/O-bound, many connections", "async/await", "10k conns, one thread", BOX_TEAL),
            ("I/O-bound, blocking libs", "threads", "simple, OS-scheduled", BOX_BLUE),
            ("CPU-bound, multicore", "processes / threads*", "true parallelism", BOX_GREEN),
            ("CPU-bound, Python", "multiprocessing", "escape the GIL", BOX_ORANGE),
            ("Mixed pipeline", "async + thread pool", "loop for I/O, pool for CPU bursts", BOX_PURP)]
    yy = y
    for name, model, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, model, f"{name} — {desc}", font_size=11)
        yy -= 70
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, 130, "*threads for CPU-bound only where no GIL (Java, Go, Rust) or work is in native code (numpy).")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Concurrency vs Parallelism — Remember",
                 ["Concurrency = dealing with many things (interleaving); parallelism = doing many things (simultaneous).",
                  "Threads share memory: cheap communication, hard coordination — every shared access can race.",
                  "Async: cooperative, one thread, yield at await — massive I/O scale, never block the loop.",
                  "CPU-bound work needs true parallelism: processes (or GIL-free threads); mind Amdahl's ceiling.",
                  "Amdahl: speedup limited by the sequential fraction — 10% serial caps you near 10x forever."],
                 pg)
    c.save(); print("wrote", path)


def pdf_threads(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Threads & Processes\nVisual Guide",
               "Flows of execution —\naddress spaces, switching costs, and talking between processes.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Process vs Thread: Address Spaces",
                       "A process is a container; threads are flows inside it.")
    box(c, 72, 400, 220, 140, BOX_BLUE, "Process A", "own address space\nown heap, fds", font_size=11)
    box(c, 320, 400, 220, 140, BOX_ORANGE, "Process B", "own address space\nisolated", font_size=11)
    for i in range(3):
        box(c, 88 + i * 68, 460, 60, 50, BOX_GREEN, f"T{i+1}", "stack", font_size=9)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawString(330, 370, "X  no shared memory")
    arrow(c, 292, 470, 318, 470, color=RED, width=2.5)
    bullet_list(c, 72, 350, [
        "Process: isolated memory, own file descriptors — crash one, others survive.",
        "Threads in a process share heap/globals; each has its own stack + registers.",
        "Threads are cheap to create; processes pay for fork + separate page tables.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Context Switching: The Hidden Tax",
                       "Swapping what's running costs real time.")
    box(c, 72, 480, 200, 60, BOX_BLUE, "Thread 1 running", "", font_size=11)
    arrow(c, 272, 510, 300, 510, color=RED, width=2.5, label="preempt!")
    box(c, 302, 480, 200, 60, BOX_GREEN, "Thread 2 running", "", font_size=11)
    y0 = codeblock(c, 72, 440, [
        "  # a switch saves/restores:",
        "  # registers, program counter, stack pointer, TLB entries, cache warmth",
        "  # cost: ~1-10 us thread switch; process switch costs MORE (MMU/TLB flush)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Cache pollution: the new thread finds cold caches — the REAL cost dwarfs register saves.",
        "Too many threads -> the OS spends more time switching than working (thrashing).",
        "Rule: ~1-2x CPU cores for CPU work; more only when threads mostly WAIT (I/O).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Thread Lifecycle",
                       "Born, scheduled, blocked, dead — the OS drives the transitions.")
    box(c, 72, 500, 110, 54, BOX_TEAL, "NEW", "", font_size=10.5)
    box(c, 220, 500, 110, 54, BOX_BLUE, "RUNNABLE", "", font_size=10.5)
    box(c, 368, 500, 110, 54, BOX_GREEN, "RUNNING", "", font_size=10.5)
    box(c, 220, 390, 110, 54, BOX_ORANGE, "BLOCKED", "I/O, lock", font_size=10)
    box(c, 368, 390, 110, 54, BOX_RED, "DEAD", "", font_size=10.5)
    arrow(c, 182, 527, 218, 527, color=ACCENT, width=1.8, label="start")
    arrow(c, 330, 527, 366, 527, color=ACCENT, width=1.8, label="schedule")
    arrow(c, 423, 500, 400, 444, color=MUTED, width=1.5)
    arrow(c, 275, 500, 275, 446, color=MUTED, width=1.5)
    arrow(c, 330, 417, 366, 500, color=MUTED, width=1.5)
    arrow(c, 478, 417, 478, 500, color=MUTED, width=1.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(72, 350, "BLOCKED -WAITING-> RUNNABLE: I/O completes, lock frees.  DEAD: return or uncaught exception.")
    note(c, 72, 280, 468, "Join: one thread waits for another's DEATH. Daemon threads die with the process — never put cleanup-only work in them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "IPC: Processes Talking",
                       "No shared memory? These are the channels.")
    rows = [("Pipes", "one-way byte stream, parent-child", "shell pipelines", BOX_BLUE),
            ("Message queues", "OS-buffered datagrams", "decoupled workers", BOX_GREEN),
            ("Shared memory", "fastest; needs manual sync", "video frames, big arrays", BOX_ORANGE),
            ("Sockets", "works across machines too", "network services", BOX_TEAL),
            ("Signals", "tiny async notifications", "Ctrl-C (SIGINT)", BOX_RED)]
    yy = y
    for name, desc, use, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"{desc} — e.g. {use}", font_size=11)
        yy -= 70
    note(c, 72, 130, 468, "Speed ranking: shared memory > pipes/sockets (localhost) > message queues. Pick the weakest channel that does the job.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Shared-Memory Pitfalls",
                       "Threads share everything — including your bugs.")
    y0 = codeblock(c, 72, y, [
        "  # RACE: two threads, one counter",
        "  # T1: read 5 -> add 1 -> write 6",
        "  # T2: read 5 -> add 1 -> write 6     # lost update! expected 7",
        "",
        "  # FIX: lock around read-modify-write, or use atomics",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Race condition: outcome depends on interleaving — passes tests, fails at 3 AM.",
        "False sharing: two threads hammer DIFFERENT fields on one cache line — cache ping-pong.",
        "Visibility: without sync, writes may sit in a core's cache — others read stale values.",
        "Thread-safety is a CONTRACT: document it per class ('thread-safe', 'not thread-safe', 'safe if...').",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Threads vs Processes Chooser",
                       "Isolation or sharing — pick your poison.")
    rows = [("Need crash isolation", "processes", "one dies, rest survive", BOX_BLUE),
            ("Need max sharing speed", "threads", "pointer-speed communication", BOX_GREEN),
            ("CPU-bound in Python", "processes", "dodge the GIL", BOX_ORANGE),
            ("10k concurrent I/O", "async (or threads)", "threads drown in stacks", BOX_TEAL),
            ("Security boundary", "processes", "separate privilege domains", BOX_RED)]
    yy = y
    for name, ans, desc, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, ans, f"{name} — {desc}", font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Threads & Processes — Remember",
                 ["Process = isolated address space; threads = flows sharing one space (own stacks).",
                  "Context switches cost cache warmth more than registers — oversubscription thrashes.",
                  "Thread lifecycle: NEW -> RUNNABLE -> RUNNING -> BLOCKED/WAITING -> DEAD; join waits for death.",
                  "IPC ranked by speed: shared memory, pipes/sockets, message queues, signals.",
                  "Shared memory races are interleaving-dependent — lock read-modify-write or use atomics."],
                 pg)
    c.save(); print("wrote", path)


def pdf_locks(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Locks & Deadlocks\nVisual Guide",
               "Mutual exclusion done right —\nand the four conditions that freeze systems.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Mutex: One at a Time",
                       "Mutual exclusion — the bouncer for critical sections.")
    box(c, 72, 470, 140, 60, BOX_BLUE, "Thread A", "holds lock", font_size=11)
    box(c, 350, 470, 140, 60, BOX_TEAL, "Thread B", "BLOCKED", font_size=11)
    box(c, 231, 470, 100, 60, BOX_RED, "LOCK", "held", font_size=12)
    arrow(c, 212, 500, 229, 500, color=RED, width=2)
    arrow(c, 331, 500, 348, 500, color=MUTED, width=2)
    y0 = codeblock(c, 72, 430, [
        "  with lock:                  # acquire on entry, release on exit",
        "      balance += deposit      # critical section: exactly one thread",
        "  # RAII / context managers: the lock CANNOT be forgotten",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Critical section: code touching shared state — keep it SHORT (contention = serialization).",
        "Always use scoped acquisition (with/lock_guard) — manual unlock on every path is a bug farm.",
        "Recursive mutexes allow re-locking by the owner — a design smell; restructure instead.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Semaphore: N at a Time",
                       "A counter, not a flag — permits for a pool of identical resources.")
    for i in range(5):
        fill = BOX_GREEN if i < 3 else BOX_TEAL
        c.setFillColor(fill); c.circle(120 + i * 80, 500, 26, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(TITLE_FONT, 10)
        c.drawCentredString(120 + i * 80, 496, str(3 - i) if i < 3 else "·")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "DB pool: 3 connections. acquire() decrements; 0 -> wait. release() increments.")
    y0 = codeblock(c, 72, 415, [
        "  sem = Semaphore(3)          # 3 permits",
        "  sem.acquire()              # take one (blocks at 0)",
        "  use_connection(); sem.release()",
        "  # binary semaphore (N=1) ~= mutex, minus ownership tracking",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Counting semaphore: resource pools, rate limiters, bounded buffers.",
        "No owner concept: any thread may release — flexible, and easier to misuse.",
        "Producer/consumer: one semaphore counts items, another counts free slots.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Reader-Writer Locks",
                       "Many readers OR one writer — match the lock to the access pattern.")
    for i in range(4):
        box(c, 72 + i * 118, 480, 108, 54, BOX_GREEN, f"R{i+1}", "reading", font_size=10.5)
    box(c, 72, 390, 200, 54, BOX_RED, "Writer", "waits for readers", font_size=11)
    arrow(c, 300, 417, 540, 417, color=RED, width=2, label="exclusive when held")
    y0 = codeblock(c, 72, 350, [
        "  with rw.read_lock(): return cache[k]     # readers share freely",
        "  with rw.write_lock(): cache[k] = v       # writer excludes everyone",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Read-heavy workloads (caches, configs): big win over plain mutex.",
        "Writer starvation: endless readers can block writers — prefer writer-fair variants.",
        "Upgrade (read -> write) deadlocks naively — release and re-acquire, or use upgradable locks.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Deadlock: The Four Conditions",
                       "All four must hold — break any one and deadlock is impossible.")
    conds = [("Mutual exclusion", "resource can't be shared", BOX_RED),
             ("Hold and wait", "hold one lock, ask for another", BOX_ORANGE),
             ("No preemption", "can't yank a held lock away", BOX_BLUE),
             ("Circular wait", "A waits B waits ... waits A", BOX_PURP)]
    cx, cyy = 306, 480
    for i, (name, desc, fill) in enumerate(conds):
        ang = 3.14159 / 2 - i * 3.14159 / 2
        import math
        bx, by = cx + 150 * math.cos(ang) - 90, cyy + 110 * math.sin(ang) - 28
        box(c, bx, by, 180, 56, fill, name, desc, font_size=10)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(cx, cyy - 4, "DEADLOCK")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(cx, 300, "dining philosophers: 5 forks, each holds left, waits right — forever")
    bullet_list(c, 72, 265, [
        "Coffman conditions (1971): the checklist every deadlock postmortem uses.",
        "Detection: lock-order graphs — a cycle in 'waits-for' means deadlock.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Prevention vs Avoidance vs Detection",
                       "Three strategies, three price tags.")
    rows = [("Prevention", "break a condition: global lock ORDERING", "cheap, sometimes rigid", BOX_GREEN),
            ("Avoidance", "Banker's algorithm: grant only safe states", "costly, needs max claims", BOX_BLUE),
            ("Detection", "let it happen; find cycles, kill a victim", "DBs do this", BOX_ORANGE),
            ("Ignorance", "the ostrich algorithm — most OSes!", "reboot if stuck", BOX_RED)]
    yy = y
    for name, desc, note_, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"{desc} — {note_}", font_size=11)
        yy -= 70
    y0 = codeblock(c, 72, yy - 10, [
        "  # lock ordering: always acquire in ID order — no cycles possible",
        "  first, second = sorted([lock_a, lock_b], key=id)",
        "  with first, second: ...",
    ])
    note(c, 72, y0 - 60, 468, "Lock ordering is the working engineer's answer: simple, provable, and free. Try-lock with backoff is the pragmatic cousin.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Locking Wisdom",
                       "Rules from the trenches.")
    bullet_list(c, 72, y, [
        "Hold locks for the SHORTEST time possible — contention serializes your parallel code.",
        "Never call unknown code (callbacks, virtual methods) while holding a lock — reentrancy deadlock.",
        "Lock granularity: one big lock (simple, serial) vs many fine locks (parallel, deadlock-prone).",
        "Prefer lock-free structures (queues, atomics) on hot paths — then measure.",
        "Document lock order wherever two locks can nest — future you will thank present you.",
        "Livelock: everyone politely backs off forever — randomize backoff to break symmetry.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Locks & Deadlocks — Remember",
                 ["Mutex: one holder; semaphore: N permits; RW-lock: many readers or one writer.",
                  "Deadlock needs all four Coffman conditions — break any one (lock ordering breaks circular wait).",
                  "Strategies: prevention (ordering), avoidance (Banker's), detection (cycle hunt), ostrich.",
                  "Keep critical sections short; never call unknown code while holding a lock.",
                  "Scoped acquisition (with/lock_guard) makes leaks impossible — never hand-unlock."],
                 pg)
    c.save(); print("wrote", path)


def pdf_async(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Async/Await\nVisual Guide",
               "One thread, thousands of tasks —\ncooperative concurrency without the thread tax.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Blocking vs Non-Blocking I/O",
                       "Waiting is the enemy — async refuses to idle.")
    box(c, 72, 470, 220, 70, BOX_RED, "blocking", "thread sleeps\non recv()", font_size=11)
    box(c, 320, 470, 220, 70, BOX_GREEN, "non-blocking", "ask, get EAGAIN,\ndo other work", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "1000 blocking connections = 1000 threads = 1000 stacks (~8MB each) = pain.")
    c.drawString(72, 412, "1000 async connections = 1 thread + 1000 tiny task objects = fine.")
    y0 = codeblock(c, 72, 380, [
        "  # blocking: the OS parks THIS thread until data arrives",
        "  data = sock.recv(1024)          # thread does nothing for 200ms",
        "  # async: park the TASK, keep the thread",
        "  data = await sock.recv(1024)    # loop runs 999 other tasks meanwhile",
    ])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Event Loop",
                       "One scheduler to rule the tasks: run ready ones, park the waiters.")
    box(c, 196, 470, 220, 64, BOX_TEAL, "event loop", "while True:\nrun ready tasks", font_size=11)
    box(c, 72, 370, 140, 56, BOX_BLUE, "task A", "await I/O", font_size=10.5)
    box(c, 236, 370, 140, 56, BOX_BLUE, "task B", "ready!", font_size=10.5)
    box(c, 400, 370, 140, 56, BOX_BLUE, "task C", "await timer", font_size=10.5)
    arrow(c, 142, 370, 250, 470, color=MUTED, width=1.5)
    arrow(c, 470, 370, 360, 470, color=MUTED, width=1.5)
    arrow(c, 306, 426, 306, 470, color=GREEN, width=2.5)
    bullet_list(c, 72, 315, [
        "await = 'I'm stuck; run someone else until my I/O completes'.",
        "Cooperative: tasks yield VOLUNTARILY — no preemption, no races between awaits.",
        "The loop also handles timers, signals, and subprocess I/O — one hub for all waiting.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Promises / Futures: Values from the Future",
                       "A placeholder for a result that hasn't arrived yet.")
    box(c, 72, 480, 140, 60, BOX_BLUE, "pending", "", font_size=11)
    box(c, 252, 480, 140, 60, BOX_GREEN, "fulfilled", "value", font_size=11)
    box(c, 432, 480, 108, 60, BOX_RED, "rejected", "error", font_size=11)
    arrow(c, 212, 510, 250, 510, color=GREEN, width=2, label="resolve")
    arrow(c, 392, 510, 430, 510, color=RED, width=2, label="reject")
    y0 = codeblock(c, 72, 440, [
        "  p = fetch(url)                 # returns IMMEDIATELY: a promise",
        "  p.then(render).catch(show_err) # chain handlers; errors propagate",
        "  # async/await is syntax sugar over the same machinery",
    ])
    bullet_list(c, 72, y0 - 30, [
        "then() chains SEQUENTIALLY; Promise.all / gather runs CONCURRENTLY.",
        "Unhandled rejections crash (Node) or warn — always end chains with catch.",
        "Future vs Promise: naming varies (JS promise, Python future) — the idea is identical.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Microtasks vs Macrotasks",
                       "Two queues, one rule: drain microtasks first.")
    box(c, 72, 470, 220, 64, BOX_ORANGE, "microtask queue", "promise.then\nawait resume", font_size=10.5)
    box(c, 320, 470, 220, 64, BOX_BLUE, "macrotask queue", "timers, I/O\ncallbacks", font_size=10.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Loop tick: run ONE macrotask, then drain ALL microtasks, then render/repeat.")
    y0 = codeblock(c, 72, 400, [
        "  setTimeout(() => console.log('macro'), 0)",
        "  Promise.resolve().then(() => console.log('micro'))",
        "  // prints: micro, THEN macro — always",
    ])
    bullet_list(c, 72, y0 - 30, [
        "await continuations are microtasks — they jump ahead of timers.",
        "Starvation: an infinite microtask chain blocks macrotasks (and rendering) forever.",
        "queueMicrotask vs setTimeout(0): same 'later', very different priority.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Backpressure: When Producers Outrun Consumers",
                       "Fast source + slow sink = unbounded memory — unless you push back.")
    box(c, 72, 470, 150, 60, BOX_RED, "producer", "10k msgs/s", font_size=11)
    arrow(c, 222, 500, 280, 500, color=RED, width=3, label="flood")
    box(c, 282, 470, 150, 60, BOX_ORANGE, "queue", "grows...", font_size=11)
    arrow(c, 432, 500, 470, 500, color=GREEN, width=1.5)
    box(c, 472, 470, 68, 60, BOX_BLUE, "sink", "1k/s", font_size=10)
    y0 = codeblock(c, 72, 430, [
        "  # strategies:",
        "  # 1. bounded queue + await put()  -> producer WAITS (natural throttle)",
        "  # 2. drop newest / oldest         -> lossy, for metrics/logs",
        "  # 3. sample / conflate            -> keep latest, for UI state",
    ])
    bullet_list(c, 72, y0 - 30, [
        "await queue.put() on a FULL bounded queue IS backpressure — the producer slows itself.",
        "Unbounded queues are memory leaks with extra steps — always bound or drop.",
        "Reactive streams (and TCP windows!) are backpressure protocols, not just queues.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Async Traps",
                       "The ways async code bites.")
    bullet_list(c, 72, y, [
        "Blocking the loop: one time.sleep(5) or sync DB call freezes ALL tasks — use run_in_executor.",
        "await in a loop when gather() would do: sequential 100 x 100ms = 10s; gathered = ~100ms.",
        "Fire-and-forget tasks: un-awaited coroutines never run; un-referenced tasks get GC'd mid-flight.",
        "Shared state between awaits is safe; ACROSS awaits another task may have mutated it — re-check.",
        "Mixing threads + async: use loop-safe bridges (call_soon_threadsafe), not raw shared queues.",
        "Async all the way down: one sync function in the chain forces executors or redesign.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Async/Await — Remember",
                 ["Async = cooperative concurrency: tasks yield at await; one thread serves thousands.",
                  "Event loop runs ready tasks and parks waiters — never block it with sync calls.",
                  "Promises/futures are future-values with pending/fulfilled/rejected states; chain with then/catch.",
                  "Microtasks (promise continuations) drain before macrotasks (timers, I/O) every tick.",
                  "Backpressure (bounded queues, drop policies) stops fast producers drowning slow consumers."],
                 pg)
    c.save(); print("wrote", path)


def pdf_memory(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Memory Management\nVisual Guide",
               "Stack vs heap, pointers, and fragmentation —\nwhere your bytes actually live.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Stack vs Heap",
                       "Two regions, opposite trade-offs.")
    box(c, 72, 380, 220, 160, BOX_BLUE, "STACK", "", font_size=13)
    box(c, 320, 380, 220, 160, BOX_ORANGE, "HEAP", "", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(88, 500, "frames push/pop automatically")
    c.drawString(88, 484, "fixed-size locals, LIFO order")
    c.drawString(88, 468, "fast: bump a pointer")
    c.drawString(88, 452, "small (~8 MB), thread-local")
    c.drawString(336, 500, "malloc/new at runtime")
    c.drawString(336, 484, "any size, any lifetime")
    c.drawString(336, 468, "slower: allocator search")
    c.drawString(336, 452, "large, shared, manual/GC'd")
    bullet_list(c, 72, 340, [
        "Stack: compiler-managed, zero-cost cleanup — but fixed at compile time per frame.",
        "Heap: flexible lifetimes (outlive the caller) — but YOU (or GC) manage it.",
        "Escape: returning a stack address is instant undefined behavior — allocate on the heap instead.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Stack Frames Up Close",
                       "Every call gets a frame; returns destroy it.")
    for i, lbl in enumerate(["main()", "parse()", "token()"]):
        yy = 540 - i * 70
        box(c, 200, yy - 56, 220, 60, BOX_BLUE if i < 2 else BOX_GREEN, lbl, "locals + return addr", font_size=11)
    arrow(c, 440, 500, 440, 380, color=ACCENT, width=2.5, label="stack grows")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 300, "token() returns -> its frame pops -> parse() resumes. Locals vanish with the frame.")
    y0 = codeblock(c, 72, 270, [
        "  void f() { int x[1000000]; ... }   # 4MB on the stack: risky!",
        "  void f() { int* x = malloc(...); } # heap: safe, remember free()",
    ])
    note(c, 72, y0 - 60, 468, "Stack overflow = too-deep recursion or too-big locals. The stack is fast because it's dumb: no searching, just push/pop.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Pointers: Addresses as Values",
                       "A pointer is just a number — the address of something.")
    box(c, 72, 470, 120, 60, BOX_BLUE, "ptr", "0x7ff0", font_size=11)
    arrow(c, 192, 500, 240, 500, color=ACCENT, width=2.5, label="points to")
    box(c, 242, 470, 120, 60, BOX_GREEN, "42", "0x7ff0", font_size=12)
    y0 = codeblock(c, 72, 430, [
        "  int x = 42; int* p = &x;   // p holds x's ADDRESS",
        "  *p = 43;                   // dereference: write THROUGH p",
        "  p++;                       // moves by sizeof(int), not 1 byte!",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Pointer arithmetic scales by type size: p+1 on int* jumps 4 bytes.",
        "NULL/dangling/wild: the unholy trinity — check, free once, null after free.",
        "References (C++/Rust) are pointers with guardrails: no arithmetic, no null (mostly).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Manual Allocation: malloc / free",
                       "With great power comes great leak-checking.")
    y0 = codeblock(c, 72, y, [
        "  int* a = malloc(n * sizeof(int));  // request n ints",
        "  if (!a) handle_oom();              // malloc CAN fail",
        "  ... use a[0..n-1] ...",
        "  free(a); a = NULL;                 // release exactly once",
    ])
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y0 - 40, "The four horsemen:")
    rows = [("Leak", "never freed — memory grows until OOM", BOX_RED),
            ("Double free", "freed twice — heap corruption", BOX_ORANGE),
            ("Use after free", "dangling pointer reads garbage", BOX_ORANGE),
            ("Overflow", "write past the end — smashes neighbors", BOX_RED)]
    yy = y0 - 60
    for name, desc, fill in rows:
        box(c, 72, yy - 48, 468, 52, fill, name, desc, font_size=11)
        yy -= 64
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Fragmentation",
                       "Free memory you can't use — the allocator's slow defeat.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "External fragmentation:")
    segs = [(BOX_GREEN, "used"), (BOX_TEAL, "free 8"), (BOX_GREEN, "used"),
            (BOX_TEAL, "free 8"), (BOX_GREEN, "used"), (BOX_TEAL, "free 8")]
    x = 72
    for fill, lbl in segs:
        c.setFillColor(fill); c.roundRect(x, y - 70, 76, 50, 5, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(BODY_FONT, 9); c.drawCentredString(x + 38, y - 44, lbl)
        x += 80
    c.setFillColor(RED); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 100, "24 bytes free total — but no 16-byte CONTIGUOUS block. Allocation fails anyway!")
    bullet_list(c, 72, y - 140, [
        "Internal fragmentation: allocator rounds up (ask 24, get 32) — wasted INSIDE blocks.",
        "Compaction (moving GC) fixes external fragmentation — one reason GCs relocate objects.",
        "Slab allocators: fixed-size pools per type — no fragmentation, O(1) alloc (Linux kernel).",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Memory Wisdom",
                       "Rules that prevent 3 AM pages.")
    bullet_list(c, 72, y, [
        "Ownership: every allocation has ONE owner responsible for freeing it — document it.",
        "RAII / defer / context managers: tie lifetime to scope and leaks become impossible.",
        "Valgrind / AddressSanitizer: run them in CI — they catch what code review misses.",
        "Prefer stack allocation: if it doesn't need to outlive the call, don't heap it.",
        "Arena allocators: free the WHOLE pool at once — perfect for per-request/per-frame data.",
        "Rust's borrow checker is this entire guide as compile errors — ownership made mechanical.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Memory Management — Remember",
                 ["Stack: fast, automatic, LIFO frames; heap: flexible lifetimes, managed allocation.",
                  "Pointers are addresses as values — arithmetic scales by type size; null after free.",
                  "Manual allocation's horsemen: leaks, double-free, use-after-free, overflows.",
                  "Fragmentation (internal rounding, external scattering) wastes memory you technically have.",
                  "Ownership + scoped cleanup (RAII/defer) + sanitizers in CI = memory sanity."],
                 pg)
    c.save(); print("wrote", path)


def pdf_gc(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Garbage Collection\nVisual Guide",
               "Automatic memory reclamation —\nhow runtimes find what's dead.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Why GC Exists",
                       "Manual freeing is correct until it isn't — at scale, humans lose.")
    box(c, 72, 460, 220, 70, BOX_RED, "manual", "fast, precise\n+ leaks/corruption", font_size=11)
    box(c, 320, 460, 220, 70, BOX_GREEN, "GC", "safe by default\n+ pause/throughput cost", font_size=11)
    bullet_list(c, 72, 415, [
        "GC trades CPU cycles and occasional pauses for memory safety.",
        "Roots: globals, stacks, registers — everything reachable FROM roots is alive.",
        "Unreachable = garbage, even if pointers still dangle between dead objects.",
        "No GC prevents LOGICAL leaks: a global list growing forever is still your bug.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Reference Counting",
                       "Count incoming pointers; zero means dead — immediate, no pauses.")
    box(c, 120, 500, 90, 54, BOX_BLUE, "A", "rc=2", font_size=11)
    box(c, 280, 500, 90, 54, BOX_BLUE, "B", "rc=1", font_size=11)
    box(c, 280, 400, 90, 54, BOX_RED, "C", "rc=1", font_size=11)
    arrow(c, 210, 527, 278, 527, color=ACCENT, width=1.8)
    arrow(c, 325, 500, 325, 454, color=ACCENT, width=1.8)
    arrow(c, 280, 427, 210, 500, color=RED, width=2, label="cycle!")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10.5)
    c.drawString(72, 360, "B <-> C reference each other: rc never hits 0 -> LEAKED forever")
    y0 = codeblock(c, 72, 330, [
        "  # CPython: refcounting + a cycle detector bolted on",
        "  import gc; gc.collect()   # hunt the cycles refcounting can't see",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Pros: prompt freeing, no stop-the-world pauses, simple.",
        "Cons: cycles leak; every pointer write pays counter churn (cache traffic).",
        "Weak references break cycles: caches and parent-links should be weak.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Mark-and-Sweep",
                       "Trace from roots, then sweep the unmarked — the classic two-phase GC.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y, "Phase 1 — MARK (trace from roots):")
    box(c, 72, y - 70, 90, 52, BOX_GREEN, "root", "", font_size=10)
    box(c, 200, y - 70, 90, 52, BOX_GREEN, "live", "marked", font_size=10)
    box(c, 328, y - 70, 90, 52, BOX_GREEN, "live", "marked", font_size=10)
    box(c, 456, y - 70, 84, 52, BOX_TEAL, "dead", "unmarked", font_size=10)
    arrow(c, 162, y - 44, 198, y - 44, color=GREEN, width=2)
    arrow(c, 290, y - 44, 326, y - 44, color=GREEN, width=2)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11); c.drawString(72, y - 120, "Phase 2 — SWEEP (reclaim unmarked):")
    box(c, 72, y - 190, 90, 52, BOX_GREEN, "root", "", font_size=10)
    box(c, 200, y - 190, 90, 52, BOX_GREEN, "live", "", font_size=10)
    box(c, 328, y - 190, 90, 52, BOX_GREEN, "live", "", font_size=10)
    box(c, 456, y - 190, 84, 52, BOX_TEAL, "free", "reclaimed", font_size=10)
    bullet_list(c, 72, y - 250, [
        "Handles cycles naturally: unreachable cycles are simply never marked.",
        "Cost: the whole heap is traced — pause scales with LIVE data, not garbage.",
        "Fragmentation: sweeping leaves holes — compacting variants relocate survivors.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Generational GC: The Age Trick",
                       "Most objects die young — collect the nursery often, the elders rarely.")
    box(c, 72, 470, 140, 70, BOX_GREEN, "Young gen", "eden +\nsurvivors", font_size=11)
    box(c, 250, 470, 140, 70, BOX_ORANGE, "Old gen", "tenured", font_size=11)
    box(c, 428, 470, 112, 70, BOX_TEAL, "Perm", "classes", font_size=11)
    arrow(c, 212, 505, 248, 505, color=ACCENT, width=2, label="survive N")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Minor GC: scan young gen only (fast, frequent). Survivors get promoted.")
    c.drawString(72, 412, "Major GC: scan everything (slow, rare) — the pause users feel.")
    bullet_list(c, 72, 375, [
        "Generational hypothesis: 90%+ of objects die in the nursery — bet the GC on it.",
        "Write barriers track old-to-young pointers so minor GCs stay correct.",
        "Tuning = sizing generations: too-small nursery promotes garbage; too-big pauses.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Pauses: The Latency Battle",
                       "Throughput vs latency — pick your GC by your SLA.")
    rows = [("Serial / Parallel", "stop-the-world, max throughput", "batch jobs", BOX_BLUE),
            ("CMS / G1", "mostly concurrent, short pauses", "web services", BOX_GREEN),
            ("ZGC / Shenandoah", "sub-ms pauses, colored pointers", "trading, gaming", BOX_TEAL),
            ("No GC (Rust/ARC)", "zero pauses, compile-time", "systems, real-time", BOX_ORANGE)]
    yy = y
    for name, desc, use, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"{desc} — {use}", font_size=11)
        yy -= 70
    bullet_list(c, 72, yy - 20, [
        "Stop-the-world: every mutator thread halts — simple, but the tail latency spikes.",
        "Concurrent GC trades throughput (barrier overhead) for shorter pauses.",
        "Measure p99, not average: GC pauses live in the tail.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "GC-Friendly Code",
                       "Write so the collector barely notices you.")
    bullet_list(c, 72, y, [
        "Short-lived garbage is FREE in generational GCs — don't pool tiny objects prematurely.",
        "Long-lived caches are expensive: they tenured and get scanned every major GC — bound them.",
        "Avoid finalizers: they resurrect objects and serialize collection — use explicit close().",
        "Null out (or scope-limit) references you no longer need in long-lived structures.",
        "Allocation rate drives GC frequency: fewer temporaries, fewer collections.",
        "Know your flags: -Xmx, G1 regions, ZGC generations — defaults are for average apps, not yours.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Garbage Collection — Remember",
                 ["Roots (stacks, globals) define liveness: unreachable objects are garbage, cycles included.",
                  "Reference counting frees promptly but leaks cycles and churns on every pointer write.",
                  "Mark-and-sweep traces from roots then reclaims unmarked — pause scales with live data.",
                  "Generational GC exploits 'most die young': frequent minor collections, rare major ones.",
                  "Pick collectors by SLA (throughput vs p99 pauses); short-lived garbage is nearly free."],
                 pg)
    c.save(); print("wrote", path)


def pdf_compilers(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Compilers vs Interpreters\nVisual Guide",
               "From source text to running program —\nlexing, parsing, and the JIT middle ground.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Compiler vs Interpreter",
                       "Translate-then-run versus run-as-you-read.")
    box(c, 72, 440, 220, 90, BOX_BLUE, "Compiler", "whole program\n-> machine code", font_size=12)
    box(c, 320, 440, 220, 90, BOX_ORANGE, "Interpreter", "reads + executes\nline by line", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 400, "Compiler: slow build, FAST run (C, Rust, Go). Errors surface before shipping.")
    c.drawString(72, 382, "Interpreter: instant start, slower run (Python, Ruby). Errors surface at runtime.")
    bullet_list(c, 72, 345, [
        "It's a spectrum: bytecode VMs (JVM, CPython) compile to IR, then interpret THAT.",
        "Ahead-of-time (AOT): compile once, ship binary. JIT: compile hot code at runtime.",
        "Transpilers (TypeScript -> JS) are compilers whose target is another language.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Lexing: Text to Tokens",
                       "The scanner chunks characters into meaningful words.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y, "if (x > 3) { y = x + 1; }")
    arrow(c, 300, y - 8, 300, y - 40, color=ACCENT, width=2, label="lexer")
    toks = ["IF", "( ", "x", ">", "3", ")", "{", "y", "=", "x", "+", "1", ";", "}"]
    x = 72
    for t in toks:
        w = max(34, c.stringWidth(t, MONO_FONT, 9) + 12)
        if x + w > 540:
            break
        c.setFillColor(BOX_TEAL); c.roundRect(x, y - 90, w, 34, 5, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(MONO_FONT, 9); c.drawCentredString(x + w / 2, y - 78, t)
        x += w + 6
    bullet_list(c, 72, y - 130, [
        "Tokens: keywords, identifiers, literals, operators, punctuation — whitespace dies here.",
        "Regex-powered: each token type is a regular expression matched longest-first.",
        "Lex errors are the friendliest: 'unexpected character @' points at the exact spot.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Parsing: Tokens to AST",
                       "Grammar rules assemble tokens into a tree of meaning.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y, "tokens:  x  +  3  *  y")
    box(c, 236, y - 80, 140, 50, BOX_BLUE, "+", "BinaryOp", font_size=11)
    box(c, 120, y - 160, 100, 50, BOX_GREEN, "x", "Var", font_size=11)
    box(c, 330, y - 160, 140, 50, BOX_BLUE, "*", "BinaryOp", font_size=11)
    box(c, 280, y - 240, 90, 50, BOX_GREEN, "3", "Lit", font_size=11)
    box(c, 400, y - 240, 90, 50, BOX_GREEN, "y", "Var", font_size=11)
    for x1, y1, x2, y2 in [(306, y - 80, 170, y - 110), (306, y - 80, 400, y - 110),
                           (400, y - 160, 325, y - 190), (400, y - 160, 445, y - 190)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT, width=1.6)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 280, "Precedence encoded in tree SHAPE: * binds tighter, so it sits deeper.")
    bullet_list(c, 72, y - 315, [
        "AST drops punctuation: no parens or semicolons — pure structure.",
        "Recursive descent: one function per grammar rule — hand-written, readable.",
        "Parse errors: 'expected ; at line 12' — the parser knows the grammar you violated.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "IR & Optimization Passes",
                       "Lower to a simple intermediate form, then rewrite it smarter.")
    y0 = codeblock(c, 72, y, [
        "  # source:   result = (a + b) * 2 + (a + b)",
        "  # IR:       t1 = a + b",
        "  #           t2 = t1 * 2",
        "  #           result = t2 + t1",
        "  # passes: constant folding, CSE, dead-code elim, inlining, loop unroll",
    ])
    bullet_list(c, 72, y0 - 30, [
        "IR (LLVM, JVM bytecode): one backend per CPU, one frontend per language — N*M becomes N+M.",
        "Common subexpression elimination: compute (a+b) once, reuse t1.",
        "Optimizers preserve SEMANTICS: -O3 can reorder, but never change what the program means.",
        "SSA form: each variable assigned once — makes dataflow analysis tractable.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "JIT: Compile the Hot Path",
                       "Interpret first, profile, then compile what actually runs hot.")
    box(c, 72, 470, 130, 60, BOX_ORANGE, "interpret", "all code", font_size=11)
    arrow(c, 202, 500, 240, 500, color=ACCENT, width=2, label="profile")
    box(c, 242, 470, 150, 60, BOX_BLUE, "hot detected", "loop runs 10k x", font_size=10.5)
    arrow(c, 392, 500, 430, 500, color=ACCENT, width=2, label="compile")
    box(c, 432, 470, 108, 60, BOX_GREEN, "machine\ncode", "fast!", font_size=11)
    y0 = codeblock(c, 72, 430, [
        "  # tiered JIT (JVM, V8):",
        "  # tier 0: interpret  ->  tier 1: quick baseline JIT",
        "  # -> tier 2: optimizing JIT with speculative inlining",
        "  # deopt: assumption broke? fall back to interpreter, re-profile",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Speculation: 'this is always an int' — compile for ints, guard, deopt on surprise.",
        "Warmup cost: JITs are slow for short scripts — AOT wins CLIs, JIT wins servers.",
        "PyPy, V8, HotSpot: same playbook, different decades.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Compiler Wisdom",
                       "What the pipeline teaches you as a programmer.")
    bullet_list(c, 72, y, [
        "Read error messages bottom-up: lex errors (characters), parse errors (grammar), type errors (meaning).",
        "Write JIT-friendly code: stable types, small functions, predictable loops.",
        "Undefined behavior (C/C++): the optimizer ASSUMES it never happens — and deletes your 'safety' checks.",
        "Interpreted doesn't mean slow: PyPy/JIT and native extensions close the gap for hot code.",
        "Learn one IR (LLVM): it demystifies every 'magic' optimization you've ever benchmarked.",
        "Syntax is the easy 10% — name resolution, types, and codegen are the real compiler.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Compilers vs Interpreters — Remember",
                 ["Pipeline: lex (tokens) -> parse (AST) -> IR -> optimize -> codegen; each stage catches its own errors.",
                  "Compilers: slow build, fast run; interpreters: instant start, slower run; bytecode VMs sit between.",
                  "IR decouples frontends from backends; SSA + optimization passes rewrite without changing meaning.",
                  "JIT profiles real execution, compiles hot paths with speculation, deopts on surprise.",
                  "Write JIT-friendly code: stable types, small functions — and respect undefined behavior."],
                 pg)
    c.save(); print("wrote", path)


def pdf_types(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Type Systems\nVisual Guide",
               "Static vs dynamic, inference, generics —\nwhat types prove before your code runs.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Static vs Dynamic Typing",
                       "WHEN are type errors caught: compile time or run time?")
    box(c, 72, 440, 220, 90, BOX_BLUE, "Static", "checked at\ncompile time", font_size=12)
    box(c, 320, 440, 220, 90, BOX_ORANGE, "Dynamic", "checked at\nrun time", font_size=12)
    y0 = codeblock(c, 72, 400, [
        "  # static (Rust):   let x: i32 = 'hi';   // COMPILE error, ships never",
        "  # dynamic (Python): x = 'hi'; x + 1     // RUNTIME TypeError, ships maybe",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Static: errors caught early, IDE autocompletion, zero-cost abstractions — at the price of ceremony.",
        "Dynamic: fast prototyping, metaprogramming — at the price of runtime surprises and tests-as-types.",
        "Strong vs weak is SEPARATE: strong = no silent coercion; weak = '5' + 5 might 'work'.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Type Inference: Best of Both",
                       "Static checking WITHOUT the annotations — the compiler fills them in.")
    y0 = codeblock(c, 72, y, [
        "  let x = 42;            // Rust: inferred i32, still static!",
        "  auto y = compute();    // C++: deduced",
        "  val z = List(1,2,3)    // Scala/Kotlin: full-program inference",
        "",
        "  # Hindley-Milner: infers the MOST GENERAL type automatically",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Inference != dynamic: types are still fixed at compile time, just unwritten.",
        "Local inference (var/auto) is safe; global inference can produce cryptic errors.",
        "Annotate PUBLIC APIs anyway: inference is for locals, documentation is for humans.",
        "TypeScript: gradual inference over JavaScript — types appear where they pay off.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Generics: Types with Parameters",
                       "Write once, type-check for every contained type.")
    y0 = codeblock(c, 72, y, [
        "  # List of T: one implementation, checked per instantiation",
        "  def first(items: list[T]) -> T: return items[0]",
        "  first([1, 2])      # T = int, returns int",
        "  first(['a'])        # T = str, returns str",
        "  # vs object/dynamic: no casts, no runtime surprises",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Parametric polymorphism: the algorithm doesn't care WHAT T is — only that it's consistent.",
        "Type erasure (Java): generics vanish at runtime — no List-of-int at the bytecode level.",
        "Reified (C#, Rust): types survive to runtime — reflection and specialization work.",
        "Bounds: 'T must be Comparable' — constrain the parameter where the algorithm needs it.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Variance: Subtyping Through Generics",
                       "If Cat is an Animal, is a List of Cat a List of Animal?")
    rows = [("Covariant", "List of Cat IS a List of Animal", "safe for READS (producers)", BOX_GREEN),
            ("Contravariant", "reversed: sinks/consumers", "safe for WRITES (comparators)", BOX_BLUE),
            ("Invariant", "List of Cat is NOT List of Animal", "mutable collections: both read+write", BOX_RED)]
    yy = y
    for name, desc, use, fill in rows:
        box(c, 72, yy - 52, 468, 56, fill, name, f"{desc} — {use}", font_size=11)
        yy -= 70
    y0 = codeblock(c, 72, yy - 10, [
        "  # why mutable lists are invariant:",
        "  # if List[Cat] were a List[Animal]: append(Dog()) compiles... boom.",
    ])
    note(c, 72, y0 - 60, 468, "Mnemonic: producers are covariant (out), consumers contravariant (in) — 'PECS: producer extends, consumer super'.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Gradual Typing Pitfalls",
                       "Half-typed codebases have half the guarantees — mind the gaps.")
    bullet_list(c, 72, y, [
        "Any/Dynamic is contagious: one untyped boundary poisons inference downstream.",
        "Type assertions (casts) are YOU overriding the checker — wrong casts are runtime lies.",
        "None/null: the billion-dollar mistake — Optional types make absence EXPLICIT.",
        "Structural (duck) vs nominal (named) typing: 'has these methods' vs 'IS this class'.",
        "Soundness vs completeness: some checkers reject valid programs to stay sound — learn the trade.",
        "Migrate strategically: type the boundaries and hot paths first, not the tests.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Types as Design Tools",
                       "Let the checker carry what tests can't.")
    bullet_list(c, 72, y, [
        "Make illegal states unrepresentable: enums over booleans, newtypes over raw ints.",
        "Parse, don't validate: convert untrusted input ONCE into strong types at the boundary.",
        "Exhaustiveness: match over enums warns on missing cases — new variant? compiler finds every site.",
        "Phantom types: encode permissions/units in the type, zero runtime cost.",
        "Property tests + types: types prove the shape, tests probe the behavior — complementary.",
        "The type signature is documentation that never rots — read it before the body.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Type Systems — Remember",
                 ["Static catches errors at compile time; dynamic at run time — strong/weak is a separate axis.",
                  "Inference gives static safety without annotation noise — but annotate public APIs.",
                  "Generics (List of T): one implementation, checked per type; erasure vs reification matters.",
                  "Variance: producers covariant, consumers contravariant, mutable collections invariant.",
                  "Make illegal states unrepresentable — types are executable documentation."],
                 pg)
    c.save(); print("wrote", path)


def pdf_git_internals(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Git Internals\nVisual Guide",
               "Blobs, trees, commits, and the DAG —\nwhat actually happens under git's hood.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "Objects: Blob, Tree, Commit",
                       "Everything is a content-addressed object in .git/objects.")
    box(c, 72, 470, 140, 70, BOX_BLUE, "blob", "file CONTENT\nsha1 of bytes", font_size=11)
    box(c, 240, 470, 140, 70, BOX_GREEN, "tree", "dir listing:\nnames -> shas", font_size=11)
    box(c, 408, 470, 132, 70, BOX_ORANGE, "commit", "tree + parent\n+ message", font_size=11)
    arrow(c, 212, 505, 238, 505, color=ACCENT, width=2)
    arrow(c, 380, 505, 406, 505, color=ACCENT, width=2)
    y0 = codeblock(c, 72, 430, [
        "  $ git cat-file -p HEAD        # unpack any object by sha",
        "  $ git hash-object file.txt    # see the blob sha yourself",
        "  # identical content -> identical sha -> stored ONCE (dedup!)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Content addressing: the sha IS the identity — change one byte, new object.",
        "Trees nest: a tree entry can point to a blob (file) or another tree (subdir).",
        "Tags are objects too (annotated); branches are just pointers (next step).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Commit DAG",
                       "History is a directed acyclic graph of commits.")
    box(c, 72, 500, 90, 52, BOX_BLUE, "A", "", font_size=11)
    box(c, 200, 500, 90, 52, BOX_BLUE, "B", "", font_size=11)
    box(c, 328, 500, 90, 52, BOX_GREEN, "C", "", font_size=11)
    box(c, 456, 500, 84, 52, BOX_GREEN, "D", "", font_size=11)
    box(c, 264, 400, 90, 52, BOX_ORANGE, "E", "merge", font_size=11)
    for x1, x2 in [(162, 200), (290, 328), (418, 456)]:
        arrow(c, x1, 526, x2, 526, color=ACCENT, width=1.8)
    arrow(c, 373, 500, 309, 452, color=ACCENT, width=1.8)
    arrow(c, 456, 500, 354, 452, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 360, "A <- B <- C <- D linear; E has TWO parents (C and D) — a merge commit.")
    bullet_list(c, 72, 325, [
        "Each commit points to its parent(s) — history is immutable, only refs move.",
        "'Reachable from X' = ancestors of X — that's what log/fetch/push reason about.",
        "DAG, not a tree: merges give nodes two parents; that's the whole game.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Refs: Branches, Tags, HEAD",
                       "Branches are sticky notes on commits — 41 bytes that move.")
    box(c, 72, 500, 90, 52, BOX_BLUE, "A", "", font_size=11)
    box(c, 200, 500, 90, 52, BOX_BLUE, "B", "", font_size=11)
    box(c, 328, 500, 90, 52, BOX_GREEN, "C", "", font_size=11)
    arrow(c, 162, 526, 198, 526, color=ACCENT, width=1.8)
    arrow(c, 290, 526, 326, 526, color=ACCENT, width=1.8)
    c.setFillColor(ACCENT2); c.setFont(TITLE_FONT, 10)
    c.drawString(340, 566, "main -> C")
    c.drawString(340, 552, "HEAD -> main")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 460, "commit -m: new commit D, main slides forward to D. That's ALL a commit does to branches.")
    y0 = codeblock(c, 72, 425, [
        "  $ cat .git/refs/heads/main      # literally a 40-char sha",
        "  $ git symbolic-ref HEAD         # refs/heads/main",
        "  # detached HEAD: HEAD points at a sha directly — commits can strand",
    ])
    note(c, 72, y0 - 60, 468, "This mental model dissolves 90% of git confusion: commits are frozen, refs are movable labels. Every command just moves labels or makes commits.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Merge: Uniting Histories",
                       "Two parents, one commit — preserving the true story.")
    box(c, 72, 500, 90, 52, BOX_BLUE, "C", "main", font_size=11)
    box(c, 72, 400, 90, 52, BOX_GREEN, "F", "feature", font_size=11)
    box(c, 300, 450, 110, 60, BOX_ORANGE, "M", "merge", font_size=12)
    arrow(c, 162, 526, 298, 480, color=ACCENT, width=1.8)
    arrow(c, 162, 426, 298, 450, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 360, "M's tree = combined result; parents = (C, F). History shows the branch REALLY happened.")
    y0 = codeblock(c, 72, 330, [
        "  $ git merge feature            # fast-forward if linear, else merge commit",
        "  # conflicts: BOTH sides edited same lines — you resolve, then commit",
        "  # octopus: merge 3+ heads at once (rare, satisfying)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Fast-forward: no new commit when one side is strictly ahead — just slide the ref.",
        "Merge commits are documentation: 'feature X landed here, with this context'.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Rebase: Rewriting Onto",
                       "Replay your commits on a new base — linear history, rewritten shas.")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y, "before:            main: A-B-C        feature: A-B-X-Y")
    c.drawString(72, y - 26, "after rebase:      main: A-B-C        feature: A-B-C-X'-Y'  (COPIES!)")
    y0 = codeblock(c, 72, y - 60, [
        "  $ git rebase main              # on feature: replay X,Y onto C",
        "  # X' has new sha (new parent!) — old X,Y still exist until GC",
        "  # GOLDEN RULE: never rebase commits others have pulled",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Rebase = clean linear story; merge = honest branching story — teams pick one.",
        "Interactive rebase (-i): squash, reword, reorder, drop — history as an editable draft.",
        "Rewriting public history strands collaborators — force-push only your own branches.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Reflog: The Safety Net",
                       "Every ref move is logged — nothing is truly lost for ~90 days.")
    y0 = codeblock(c, 72, y, [
        "  $ git reflog                   # HEAD@{0}, HEAD@{1}, ... every move",
        "  $ git reset --hard HEAD@{2}    # undo that bad rebase/merge/reset",
        "  $ git fsck --lost-found        # dangling commits: rescue mission",
    ])
    bullet_list(c, 72, y0 - 30, [
        "'I deleted my branch!': the commits live on — reflog finds the sha, re-create the ref.",
        "reset --soft/--mixed/--hard: move HEAD (and optionally index/worktree) — know which.",
        "GC prunes unreachable objects after ~2 weeks (reflog expiry ~90 days) — rescue promptly.",
        "The index (staging area) is a state between worktree and HEAD — commit snapshots the index.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Git Internals — Remember",
                 ["Objects: blobs (content), trees (directories), commits (snapshot + parents) — all content-addressed.",
                  "History is a DAG; branches/tags are movable refs, HEAD points at your current ref.",
                  "Merge preserves branching truth (two parents); rebase replays as clean linear copies — never rebase public history.",
                  "Fast-forward slides refs with no new commit; conflicts mean both sides touched the same lines.",
                  "Reflog logs every ref move — deleted branches and bad rebases are recoverable."],
                 pg)
    c.save(); print("wrote", path)


def pdf_regex(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Regular Expressions\nVisual Guide",
               "Pattern matching engines —\nNFA vs DFA, backtracking, and the traps.",
               CAT, None); pg += 1

    y = section_header(c, 1, 6, "What a Regex Engine Does",
                       "Compile the pattern once, then simulate a machine over the text.")
    box(c, 72, 470, 150, 60, BOX_BLUE, r"a+b*c", "pattern", font_size=13)
    arrow(c, 222, 500, 260, 500, color=ACCENT, width=2.5, label="compile")
    box(c, 262, 470, 130, 60, BOX_ORANGE, "engine", "NFA/DFA", font_size=11)
    arrow(c, 392, 500, 430, 500, color=ACCENT, width=2.5, label="run")
    box(c, 432, 470, 108, 60, BOX_GREEN, "match?", "yes/no", font_size=11)
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, 430, 'text: "aaabbbbc"  vs  pattern a+ b* c')
    bullet_list(c, 72, 395, [
        "Two phases: COMPILE (pattern -> machine, once) then MATCH (run over text).",
        "Compile outside loops: re.compile() once, match many — don't recompile per call.",
        "Regex flavors differ (PCRE, RE2, .NET) — test on YOUR engine, not a website's.",
    ], font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "NFA vs DFA Engines",
                       "Backtracking search versus precomputed determinism.")
    box(c, 72, 470, 220, 70, BOX_BLUE, "NFA (backtracking)", "Python, JS, Java\nfeatures galore", font_size=11)
    box(c, 320, 470, 220, 70, BOX_GREEN, "DFA (RE2/Go)", "linear time\nguaranteed", font_size=11)
    y0 = codeblock(c, 72, 430, [
        "  # NFA: tries paths, backtracks on failure — supports backrefs, lookaround",
        "  # DFA: one pass, no backtracking — but NO backreferences possible",
        "  # tradeoff: expressive power vs guaranteed linear time",
    ])
    bullet_list(c, 72, y0 - 30, [
        "NFA simulation explores alternatives depth-first — worst case exponential (next steps).",
        "DFA builds all state combos upfront — match time O(n) always, compile can blow up.",
        "Backreferences (\\1) and lookaround NEED backtracking — that's why most engines are NFA.",
        "RE2/Go chose safety: linear-time guarantee, at the cost of those features.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Backtracking, Visualized",
                       "Greedy match, fail, give back one, retry — the NFA's walk.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y, 'pattern: a+ b     text: "aaab"')
    c.drawString(72, y - 30, "1. a+ grabs 'aaa' (greedy!)   ->  b vs end: FAIL")
    c.drawString(72, y - 54, "2. backtrack: a+ gives back one ->  b vs 'b': MATCH")
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y - 84, "match: 'aaab' — the engine tried the WIDEST grab first")
    y0 = codeblock(c, 72, y - 114, [
        "  greedy  a+   : grab max, backtrack as needed",
        "  lazy    a+?  : grab min, expand as needed     # opposite strategy",
        "  # 'a+' on 'aaa': greedy tries 3,2,1; lazy tries 1,2,3",
    ])
    note(c, 72, y0 - 60, 468, "Greedy vs lazy only changes SEARCH ORDER, not what's matchable. Both find a match if one exists — they differ in WHICH match and how fast.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Catastrophic Backtracking",
                       "Nested quantifiers: the regex that hangs your server.")
    y0 = codeblock(c, 72, y, [
        "  pattern: (a+)+b      text: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaac'",
        "  # a+ can split 30 a's in 2^30 ways; each fails on final 'c'...",
        "  # result: BILLIONS of paths before giving up. DoS via regex!",
    ])
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y0 - 40, "2^30 paths ~ 1 billion dead ends — the engine tries them ALL")
    bullet_list(c, 72, y0 - 74, [
        "Smell: quantifier INSIDE a quantified group — (a+)+, (a*)*, (a|a)+.",
        "Overlapping alternatives multiply paths: (a|aa)+ on 'aaaa...' is exponential.",
        "Never run user-supplied regex on user-supplied text without timeouts (or RE2).",
        "Fix: rewrite unambiguously — 'a+b' instead of '(a+)+b'; or use possessive/atomic (next).",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Possessive Quantifiers & Atomic Groups",
                       "Grab and NEVER give back — pruning the search tree by fiat.")
    y0 = codeblock(c, 72, y, [
        "  a++b        # possessive: a+ grabs all, NO backtracking into it",
        "  (?>a+)b    # atomic group: same idea, scoped",
        "  # on 'aaab': a++ takes 'aaa', b matches -> MATCH, zero backtrack steps",
        "  # on 'aaac': a++ takes 'aaa', b fails -> FAIL FAST (no 2^n retry)",
    ])
    bullet_list(c, 72, y0 - 30, [
        "Use when you KNOW the grabbed text can't participate in later matching.",
        "Fail-fast > exponential retry: possessive turns ReDoS patterns into instant no-match.",
        "Not in Python re / JS — available in PCRE, Java, .NET, Onigmo (use the atomic-group spelling).",
        "Alternative: write the pattern unambiguously so backtracking has nothing to explore.",
    ], font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Regex Wisdom",
                       "Power tool, sharp edges.")
    bullet_list(c, 72, y, [
        "Readability: use named capture groups, comment patterns with re.X, split monster patterns.",
        "Validate with tests, not eyeballs: regexes are write-only without a test suite.",
        "Prefer string methods for simple jobs: 'in', startswith, split beat regex on clarity AND speed.",
        "Anchors (^ $): unanchored patterns scan every position — anchor when you mean full-match.",
        "Dot-all and multiline change what . and ^ mean — set flags deliberately.",
        "Two problems joke is real: if the regex needs a regex to explain it, use a parser.",
    ], font_size=11, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Regular Expressions — Remember",
                 ["Engines compile patterns to machines (NFA or DFA), then run them over text.",
                  "NFA backtracks depth-first (expressive: backrefs, lookaround); DFA runs linear-time (RE2/Go).",
                  "Greedy grabs max then backtracks; lazy grabs min then expands — search order, not power.",
                  "Nested quantifiers ((a+)+) cause catastrophic backtracking — exponential ReDoS; rewrite or go possessive.",
                  "Possessive/atomic groups forbid backtracking into the grab — fail fast instead of hanging."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out, exist_ok=True)
    jobs = [
        ("bbg-big-o", pdf_big_o),
        ("bbg-arrays", pdf_arrays),
        ("bbg-linked-lists", pdf_linked_lists),
        ("bbg-stacks-queues", pdf_stacks_queues),
        ("bbg-hash-tables", pdf_hash_tables),
        ("bbg-trees", pdf_trees),
        ("bbg-graphs", pdf_graphs),
        ("bbg-heaps", pdf_heaps),
        ("bbg-sorting", pdf_sorting),
        ("bbg-searching", pdf_searching),
        ("bbg-dp", pdf_dp),
        ("bbg-recursion", pdf_recursion),
        ("bbg-oop", pdf_oop),
        ("bbg-solid", pdf_solid),
        ("bbg-patterns-1", pdf_patterns_1),
        ("bbg-patterns-2", pdf_patterns_2),
        ("bbg-patterns-3", pdf_patterns_3),
        ("bbg-functional", pdf_functional),
        ("bbg-concurrency", pdf_concurrency),
        ("bbg-threads", pdf_threads),
        ("bbg-locks", pdf_locks),
        ("bbg-async", pdf_async),
        ("bbg-memory", pdf_memory),
        ("bbg-gc", pdf_gc),
        ("bbg-compilers", pdf_compilers),
        ("bbg-types", pdf_types),
        ("bbg-git-internals", pdf_git_internals),
        ("bbg-regex", pdf_regex),
    ]
    for slug, fn in jobs:
        fn(os.path.join(out, slug + ".pdf"))
    print(f"done: {len(jobs)} pdfs")
