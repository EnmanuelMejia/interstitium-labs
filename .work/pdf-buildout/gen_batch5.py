"""Batch 5: AI/ML PDFs — Neural Networks, Transformers, Training Pipelines."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def _neuron(c, x, y, r=16, fill=BOX_BLUE, label=None):
    c.setFillColor(fill); c.circle(x, y, r, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.circle(x, y, r, fill=0, stroke=1)
    if label:
        c.setFillColor(INK); c.setFont(BODY_FONT, 8); c.drawCentredString(x, y - 3, label)


def pdf_neural_nets(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Neural Networks\nVisual Guide",
               "Neurons, layers, and learning —\nhow machines learn from examples.",
               "AI / ML", None); pg += 1

    y = section_header(c, 1, 6, "The Neuron: Weighted Sum + Nonlinearity",
                       "Biology-inspired math: combine inputs, squash, pass on.")
    _neuron(c, 306, 400, 34, BOX_BLUE)
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    for i, (yy2, lbl) in enumerate([(470, "x1"), (430, "x2"), (390, "x3")]):
        c.drawString(150, yy2, lbl)
        arrow(c, 180, yy2, 272, 400, color=ACCENT, width=1.5)
        c.setFont(BODY_FONT, 9); c.setFillColor(MUTED)
        c.drawString(200, (yy2 + 400) / 2 + 6, f"w{i+1}")
        c.setFont(BODY_FONT, 11); c.setFillColor(INK)
    c.drawString(360, 400, "+ b")
    arrow(c, 344, 400, 420, 400, color=ACCENT, label="σ(z)")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(430, 396, "a")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 330, "z = w1·x1 + w2·x2 + w3·x3 + b  →  a = σ(z)")
    c.drawCentredString(306, 312, "σ = activation: ReLU, sigmoid, tanh — the nonlinearity that makes depth powerful")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Layers: From Pixels to Concepts",
                       "Stack neurons; each layer learns richer features.")
    layers_x = [120, 260, 400, 520]
    labels = ["input\n784 px", "hidden 1\nedges", "hidden 2\nshapes", "output\n10 digits"]
    for lx, lbl in zip(layers_x, labels):
        for i in range(4):
            _neuron(c, lx, 480 - i * 44, 14, BOX_BLUE if i == 0 else BOX_GREEN)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8)
        for j, ln in enumerate(lbl.split("\n")):
            c.drawCentredString(lx, 270 - j * 12, ln)
    c.setStrokeColor(MUTED); c.setLineWidth(0.7)
    for a in range(3):
        for i in range(4):
            for j in range(4):
                c.line(layers_x[a] + 14, 480 - i * 44, layers_x[a+1] - 14, 480 - j * 44)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 220, "Depth builds hierarchy: pixels → edges → shapes → objects → decisions.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Forward Pass: Prediction",
                       "Data flows left to right; out pops a prediction.")
    for lx in [120, 280, 440]:
        _neuron(c, lx, 420, 18, BOX_BLUE)
    arrow(c, 140, 420, 260, 420, color=ACCENT, width=2.5, label="W1")
    arrow(c, 300, 420, 420, 420, color=ACCENT, width=2.5, label="W2")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 360, "Input image → multiply by weights, add biases, activate → ... → output scores:")
    c.setFont(MONO_FONT, 10)
    c.drawString(72, 336, "[0.01, 0.02, 0.90, 0.01, …]  →  predicts '2' with 90% confidence")
    note(c, 72, 240, 468, "Softmax turns raw scores into probabilities that sum to 1. The highest wins.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Loss: How Wrong Were We?",
                       "One number summarizing prediction error — the thing we minimize.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, y, "True label: '2'  →  one-hot: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]")
    c.drawString(72, y - 26, "Predicted:                [0.01, 0.02, 0.90, 0.01, …]")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 13)
    c.drawString(72, y - 60, "Cross-entropy loss = −log(0.90) ≈ 0.105")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 100,
        ["Confident + correct → tiny loss. Confident + WRONG → huge loss.",
         "Loss is differentiable — we can compute how each weight contributed (that's next).",
         "Training = find weights that minimize average loss over the dataset."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Backpropagation: Blame Assignment",
                       "Chain rule from calculus, applied at scale.")
    for lx in [440, 280, 120]:
        _neuron(c, lx, 420, 18, BOX_RED if lx == 440 else BOX_BLUE)
    arrow(c, 420, 420, 300, 420, color=RED, width=2.5, label="∂L/∂W2")
    arrow(c, 260, 420, 140, 420, color=RED, width=2.5, label="∂L/∂W1")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 360, "Gradients flow RIGHT to LEFT — the reverse of prediction.")
    yy = bullet_list(c, 72, 330,
        ["Each weight gets a gradient: 'nudge me this way to reduce loss.'",
         "Gradient descent: w ← w − η · ∂L/∂w  (η = learning rate).",
         "Too big η: diverge. Too small η: train forever. Schedules + Adam help."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Training Loop & Overfitting",
                       "Epochs, batches, and the generalization gap.")
    box(c, 72, 430, 468, 60, BOX_TEAL, "Loop", "for epoch: shuffle → mini-batches → forward → loss → backward → update", font_size=10)
    # loss curves
    c.setStrokeColor(MUTED); c.line(90, 200, 540, 200); c.line(90, 200, 90, 380)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(90, 388, "loss"); c.drawString(500, 188, "epochs")
    import math
    c.setStrokeColor(GREEN); c.setLineWidth(2.5)
    p = c.beginPath()
    p.moveTo(90, 360 - 140 * (1 - math.exp(0)))
    for i in range(90, 541, 8):
        t = (i - 90) / 450
        p.lineTo(i, 360 - 140 * (1 - math.exp(-t * 5)))
    c.drawPath(p)
    c.setStrokeColor(RED); c.setLineWidth(2.5)
    p = c.beginPath()
    p.moveTo(90, 360 - 140 * (1 - math.exp(0)))
    for i in range(90, 541, 8):
        t = (i - 90) / 450
        p.lineTo(i, 360 - 140 * (1 - math.exp(-t * 5)) + 60 * t * t)
    c.drawPath(p)
    c.setFillColor(GREEN); c.setFont(BODY_FONT, 10); c.drawString(400, 340, "train loss ↓")
    c.setFillColor(RED); c.drawString(400, 300, "val loss ↑ = overfitting")
    c.setFillColor(INK); c.drawString(72, 150, "Cures: more data, regularization (dropout, weight decay), early stopping, simpler models.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Neural Networks — Remember",
                 ["Neuron: z = Σw·x + b, then a = σ(z). Nonlinearity makes depth meaningful.",
                  "Forward pass predicts; loss (cross-entropy) scores the prediction.",
                  "Backprop sends gradients backward; gradient descent nudges weights downhill.",
                  "Watch the validation curve — when it rises while training falls, you're overfitting.",
                  "Depth learns hierarchy: pixels → edges → shapes → concepts."],
                 pg)
    c.save(); print("wrote", path)


def pdf_transformers(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Transformers &\nAttention",
               "The architecture behind GPT, BERT, and modern AI.\n'Attention is all you need' — explained visually.",
               "AI / ML", None); pg += 1

    y = section_header(c, 1, 6, "The Problem Attention Solves",
                       "Old RNNs read word-by-word and forgot the beginning. Attention looks at everything at once.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 12)
    words = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "too", "tired"]
    bx = 72
    for w in words:
        box(c, bx, 440, 44, 36, BOX_BLUE if w != "it" else BOX_RED, w, "", font_size=10)
        bx += 48
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, 400, "What does 'it' refer to? → the ANIMAL (not the street).")
    c.drawString(72, 380, "Attention lets 'it' directly query every other word — no forgetting.")
    note(c, 72, 280, 468, "Swap 'tired' → 'wide' and 'it' now means the STREET. Attention resolves this dynamically per context.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Q, K, V: Queries, Keys, Values",
                       "Borrowed from databases: query the keys, get weighted values.")
    box(c, 72, 420, 140, 70, BOX_BLUE, "Query (Q)", "'what am I looking for?'")
    box(c, 246, 420, 140, 70, BOX_GREEN, "Key (K)", "'what do I contain?'")
    box(c, 420, 420, 120, 70, BOX_ORANGE, "Value (V)", "'what do I actually say?'")
    c.setFillColor(INK); c.setFont(MONO_FONT, 12)
    c.drawCentredString(306, 350, "Attention(Q,K,V) = softmax(QKᵀ/√d) · V")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    yy = bullet_list(c, 72, 310,
        ["Score = how well each query matches each key (dot product).",
         "Softmax → weights summing to 1.  Output = weighted mix of values.",
         "√d scaling keeps gradients stable as dimensions grow."],
        font_size=10, gap=22)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Attention Heatmap",
                       "Darker = stronger attention. See what the model 'looks at.'")
    words = ["it", "animal", "street", "tired"]
    # grid
    gx, gy, cell = 150, 420, 70
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    for j, w in enumerate(words):
        c.drawCentredString(gx + j * cell + cell/2, gy + 18, w)
        c.drawString(gx - 60, gy - j * cell - cell/2 + 4, w)
    heats = [[0.9, 0.05, 0.02, 0.03], [0.1, 0.7, 0.1, 0.1],
             [0.05, 0.1, 0.75, 0.1], [0.6, 0.15, 0.05, 0.2]]
    for i in range(4):
        for j in range(4):
            v = heats[i][j]
            col = HexColor(f"#{int(255-(255-67)*v):02x}{int(255-(255-97)*v):02x}{int(255-(255-238)*v):02x}")
            c.setFillColor(col)
            c.rect(gx + j * cell, gy - (i+1) * cell, cell, cell, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 100, "Row 'it' attends mostly to 'animal' (0.9) — the model resolved the pronoun correctly.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Multi-Head Attention",
                       "Not one attention — many, in parallel, each learning different relations.")
    for i in range(4):
        bx = 72 + i * 120
        box(c, bx, 400, 104, 70, [BOX_BLUE, BOX_GREEN, BOX_ORANGE, BOX_TEAL][i],
            f"Head {i+1}", ["syntax", "coreference", "position", "semantics"][i], font_size=10)
    box(c, 186, 300, 240, 56, BOX_PURP, "Concatenate + project", "combine all heads' views", font_size=10)
    for i in range(4):
        arrow(c, 72 + i * 120 + 52, 398, 306, 358, color=ACCENT, width=1.2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 250, "Each head learns a different lens; together they see the whole picture.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "The Full Block: Attention + Feed-Forward",
                       "Repeated N times (GPT-3: 96×). Residuals + normalization keep it trainable.")
    box(c, 216, 480, 180, 50, BOX_BLUE, "Input embeddings", "+ positional encoding")
    arrow(c, 306, 478, 306, 452, color=ACCENT)
    box(c, 216, 400, 180, 50, BOX_GREEN, "Multi-head attention", "")
    arrow(c, 306, 398, 306, 372, color=ACCENT)
    box(c, 216, 320, 180, 50, BOX_ORANGE, "Feed-forward network", "per position")
    arrow(c, 306, 318, 306, 292, color=ACCENT)
    box(c, 216, 240, 180, 50, BOX_PURP, "Layer norm", "")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 190, "Residual connections (x + sublayer(x)) let gradients flow through 100+ layers.")
    c.drawString(72, 172, "Positional encoding injects order — attention itself is order-blind.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Why Transformers Won",
                       "Parallelism changed everything.")
    rows = [("Parallel training", "RNNs: sequential. Transformers: all positions at once → GPUs fully fed.", BOX_GREEN),
            ("Long context", "Attention reaches across thousands of tokens (and growing).", BOX_BLUE),
            ("Scale laws", "Bigger models + more data + more compute = predictably better. No plateau yet.", BOX_ORANGE),
            ("Transfer learning", "Pre-train once on the internet; fine-tune for anything.", BOX_TEAL)]
    yy = y
    for name, desc, fill in rows:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Transformers — Remember",
                 ["Attention(Q,K,V) = softmax(QKᵀ/√d)·V — queries match keys, values get mixed by weight.",
                  "Multi-head = parallel attentions, each learning different linguistic relations.",
                  "Blocks stack attention + feed-forward with residuals and layer norm, repeated N×.",
                  "Parallelism over sequence positions is why transformers train at supercomputer scale.",
                  "Pre-train broadly, fine-tune narrowly — the modern recipe."],
                 pg)
    c.save(); print("wrote", path)


def pdf_training_pipelines(path):
    c = new_canvas(path); pg = 1
    title_page(c, "ML Training\nPipelines",
               "From raw data to deployed model:\nthe production machine-learning lifecycle.",
               "AI / ML", None); pg += 1

    y = section_header(c, 1, 6, "The Pipeline at a Glance",
                       "ML systems are software systems — with data as a first-class citizen.")
    stages = ["Data\nIngest", "Validate\n& Clean", "Feature\nStore", "Train", "Evaluate", "Deploy", "Monitor"]
    bx = 40
    for i, s in enumerate(stages):
        c.setFillColor([BOX_BLUE, BOX_TEAL, BOX_GREEN, BOX_ORANGE, BOX_PURP, ACCENT, BOX_RED][i])
        c.roundRect(bx, 430, 68, 68, 10, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(TITLE_FONT, 8.5)
        yy2 = 468
        for ln in s.split("\n"):
            c.drawCentredString(bx + 34, yy2, ln); yy2 -= 11
        if i < len(stages) - 1:
            arrow(c, bx + 68, 464, bx + 80, 464, color=INK, width=1.5)
        bx += 80
    arrow(c, 520, 430, 120, 380, color=RED, width=1.5, label="retrain loop")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 330, "Monitoring closes the loop — drift triggers retraining, not a pager at 3am.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Data Validation: Garbage In, Garbage Out",
                       "Validate data like you validate code.")
    checks = [("Schema", "Columns, types, ranges match expectations", BOX_BLUE),
              ("Distribution", "No sudden shifts in feature stats (mean, nulls, cardinality)", BOX_GREEN),
              ("Anomalies", "Outliers quarantined, not silently trained on", BOX_ORANGE),
              ("Lineage", "Every row traceable to its source + transform version", BOX_TEAL)]
    yy = y
    for name, desc, fill in checks:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    note(c, 72, yy - 30, 468, "Tools: Great Expectations, TFDV. A broken upstream column shouldn't silently poison your model.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Feature Stores: One Definition of 'User Age'",
                       "Train and serve must compute features IDENTICALLY — or you get skew.")
    box(c, 72, 430, 200, 60, BOX_BLUE, "Offline store", "training (batch)")
    box(c, 340, 430, 200, 60, BOX_GREEN, "Online store", "serving (low-latency)")
    box(c, 216, 320, 180, 60, BOX_ORANGE, "Feature definitions", "single source of truth")
    arrow(c, 306, 318, 172, 428, color=ACCENT, width=1.5)
    arrow(c, 306, 318, 440, 428, color=ACCENT, width=1.5)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(306, 270, "Training-serving skew kills models silently")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 250, "Same code, same features, both paths. Point-in-time correctness for training.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Experiment Tracking",
                       "If it isn't logged, it didn't happen.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y, "Log per run: code commit • data version • hyperparams • metrics • artifacts")
    # fake experiment table
    headers = ["Run", "LR", "Batch", "Val Acc"]
    rows = [["a3f9", "3e-4", "256", "0.941"], ["b7c1", "1e-4", "512", "0.937"], ["d2e8", "3e-4", "512", "0.948 ✓"]]
    yy = y - 40
    c.setFont(TITLE_FONT, 10)
    for j, h in enumerate(headers):
        c.drawString(90 + j * 110, yy, h)
    yy -= 20
    c.setFont(MONO_FONT, 10)
    for r in rows:
        c.setFillColor(BOX_GREEN if "✓" in r[-1] else BG)
        c.rect(72, yy - 16, 460, 24, fill=1, stroke=0)
        c.setFillColor(INK)
        for j, val in enumerate(r):
            c.drawString(90 + j * 110, yy, val)
        yy -= 28
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, yy - 20, "Tools: MLflow, Weights & Biases. Compare apples to apples — same data split, same metric.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Deployment Patterns",
                       "Getting the model to users — safely.")
    pats = [("Batch inference", "Score millions of rows overnight. Simple, cheap, high latency.", BOX_BLUE),
            ("Real-time API", "Model behind REST/gRPC. Milliseconds matter; autoscale it.", BOX_GREEN),
            ("Shadow mode", "New model scores live traffic silently — compare before promoting.", BOX_ORANGE),
            ("Canary", "5% of traffic to v2; watch metrics; roll forward or back.", BOX_TEAL)]
    yy = y
    for name, desc, fill in pats:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Monitoring: Models Rot",
                       "The world changes; your model doesn't — unless you watch.")
    drifts = [("Data drift", "Input distribution shifts (new users, seasonality). Detect with PSI/KS tests.", BOX_ORANGE),
              ("Concept drift", "The RULES change (fraud patterns evolve). Labels needed to detect.", BOX_RED),
              ("Feedback loops", "Model's outputs become its future inputs — bias amplifies.", BOX_PURP),
              ("SLOs for ML", "Latency, throughput, prediction quality — alert like any service.", BOX_BLUE)]
    yy = y
    for name, desc, fill in drifts:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "ML Pipelines — Remember",
                 ["Treat data as code: version it, validate it, track its lineage.",
                  "Feature stores kill training-serving skew — one definition, two stores.",
                  "Log every experiment: code + data + params + metrics, or it didn't happen.",
                  "Deploy progressively: shadow, canary, then full rollout.",
                  "Monitor for drift and decay — retraining is a loop, not an event."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_neural_nets(os.path.join(out, "bbg-neural-networks.pdf"))
    pdf_transformers(os.path.join(out, "bbg-transformers.pdf"))
    pdf_training_pipelines(os.path.join(out, "bbg-ml-pipelines.pdf"))
