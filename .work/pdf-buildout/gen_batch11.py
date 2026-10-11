"""Batch 11: AI/ML PDFs — backprop, CNNs, RNNs/LSTM, attention, BERT vs GPT."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_backprop(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Backpropagation\nVisual Guide",
               "How neural networks learn:\nforward pass, loss, chain rule, gradient descent.",
               "Machine Learning", None); pg += 1

    y = section_header(c, 1, 6, "The Forward Pass",
                       "Input flows one way: the network makes a prediction.")
    box(c, 72, 480, 130, 70, BOX_BLUE, "Input", "x: features")
    box(c, 244, 480, 130, 70, BOX_PURP, "Hidden", "weights W, bias b")
    box(c, 416, 480, 124, 70, BOX_GREEN, "Output", "prediction")
    arrow(c, 202, 515, 242, 515, color=ACCENT, width=2.5)
    arrow(c, 374, 515, 414, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Each neuron: z = W dot x + b, then a = activation(z). Prediction flows left to right.")
    note(c, 72, 300, 468, "Forward pass = the network making a guess. Nothing is learned yet — learning comes from the error.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Measuring Error with Loss",
                       "One number says how wrong the prediction was.")
    box(c, 72, 480, 140, 70, BOX_GREEN, "Prediction", "what the net said")
    box(c, 254, 480, 140, 70, BOX_BLUE, "Target", "ground truth label")
    box(c, 414, 480, 126, 70, BOX_RED, "Loss L", "how wrong it was")
    arrow(c, 212, 515, 252, 515, color=ACCENT, width=2)
    arrow(c, 394, 515, 412, 515, color=ACCENT, width=2)
    box(c, 72, 350, 220, 64, BOX_ORANGE, "MSE", "regression: mean squared error", font_size=11)
    box(c, 320, 350, 220, 64, BOX_TEAL, "Cross-entropy", "classification: penalizes wrong confidence", font_size=11)
    note(c, 72, 230, 468, "Pick the loss that matches the task. The loss is the single number training tries to minimize.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Chain Rule, Backwards",
                       "Blame is assigned layer by layer, in reverse.")
    box(c, 408, 480, 132, 70, BOX_RED, "dL/dy", "error at output")
    box(c, 240, 480, 130, 70, BOX_ORANGE, "dL/dz", "times local grad")
    box(c, 72, 480, 130, 70, BOX_BLUE, "dL/dW", "final gradient")
    arrow(c, 406, 515, 372, 515, color=RED, width=2.5)
    arrow(c, 238, 515, 204, 515, color=RED, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "dL/dW = dL/dy x dy/dz x dz/dW — multiply local derivatives back through every layer.")
    note(c, 72, 300, 468, "The chain rule turns 'how wrong was I' into 'which weight caused it'. Gradients flow opposite to the forward pass.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Gradient Descent: The Update",
                       "Nudge every weight a little, opposite the gradient.")
    box(c, 72, 480, 140, 70, BOX_ORANGE, "Old weights W", "before the step")
    box(c, 254, 480, 140, 70, BOX_RED, "Gradient", "points uphill")
    box(c, 414, 480, 126, 70, BOX_GREEN, "W - lr x grad", "one step downhill")
    arrow(c, 212, 515, 252, 515, color=ACCENT, width=2)
    arrow(c, 394, 515, 412, 515, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Update rule: W := W - lr * dL/dW. Subtract because the gradient points toward higher loss.")
    note(c, 72, 300, 468, "Repeat millions of times: forward, loss, backward, update. That loop IS training.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "The Learning Rate",
                       "The single most influential training knob.")
    box(c, 72, 440, 140, 80, BOX_BLUE, "Too small", "lr = 0.0001: crawls, may stall")
    box(c, 246, 440, 140, 80, BOX_GREEN, "Just right", "lr = 0.01: steady descent")
    box(c, 420, 440, 120, 80, BOX_RED, "Too large", "lr = 1.0: overshoots, diverges")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 390, "Step size = learning rate x gradient. Too big bounces out of the valley; too small never arrives.")
    note(c, 72, 270, 468, "Start moderate (Adam default ~1e-3). Use a schedule: warm up, then decay as the loss plateaus.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Training in Practice",
                       "What the loop looks like at scale.")
    yy = bullet_list(c, 72, y,
        ["Minibatches: update on 32-512 examples at a time — noisy gradients escape sharp minima.",
         "Epochs: one full pass over the data. Watch train AND validation loss — divergence means overfitting.",
         "Optimizers: SGD with momentum is simple; Adam/AdamW adapt the step per weight and are the default.",
         "Gradient clipping: cap gradient norms to stop explosions in deep or recurrent nets.",
         "Shuffle every epoch. Never tune hyperparameters on the test set."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "If training is unstable: lower the learning rate first, check the data pipeline second, blame the architecture last.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Backpropagation — Remember",
                 ["Forward pass makes a prediction; loss measures the error as one number.",
                  "The chain rule sends gradients backward, assigning blame to each weight.",
                  "Gradient descent subtracts the gradient: W := W - lr * dL/dW.",
                  "Learning rate controls step size — too large diverges, too small stalls.",
                  "Minibatches + epochs + Adam is the standard training recipe; watch validation loss for overfitting."],
                 pg)
    c.save(); print("wrote", path)


def pdf_cnns(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Convolutional Neural Networks\nVisual Guide",
               "How CNNs see:\nconvolutions, pooling, receptive fields, skip connections.",
               "Deep Learning", None); pg += 1

    y = section_header(c, 1, 6, "The Convolution Operation",
                       "A small learned kernel slides across the image.")
    box(c, 72, 470, 150, 90, BOX_BLUE, "Image", "e.g. 28x28 pixels")
    box(c, 262, 470, 118, 90, BOX_ORANGE, "Kernel 3x3", "learned weights")
    box(c, 420, 470, 120, 90, BOX_GREEN, "Feature map", "one response map")
    arrow(c, 222, 515, 260, 515, color=ACCENT, width=2.5)
    arrow(c, 380, 515, 418, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "At each position the kernel computes a weighted sum. One kernel = one feature detector.")
    note(c, 72, 290, 468, "Weight sharing: the same kernel is reused everywhere — far fewer parameters than a dense layer.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Filters Learn a Hierarchy",
                       "Simple features compose into complex ones.")
    box(c, 156, 500, 300, 60, BOX_BLUE, "Layer 1: edges & colors", "oriented edges, color blobs")
    box(c, 156, 410, 300, 60, BOX_TEAL, "Layer 2: textures & shapes", "corners, curves, patterns")
    box(c, 156, 320, 300, 60, BOX_PURP, "Layer 3+: object parts", "wheels, eyes, faces")
    arrow(c, 306, 498, 306, 472, color=ACCENT, width=2.5)
    arrow(c, 306, 408, 306, 382, color=ACCENT, width=2.5)
    note(c, 72, 200, 468, "Visualize the filters to audit what the network 'sees'. Early layers are generic; late layers are task-specific.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Pooling: Shrink and Summarize",
                       "Keep the strongest signal, drop the resolution.")
    box(c, 72, 470, 150, 90, BOX_GREEN, "Feature map", "high resolution")
    box(c, 268, 470, 118, 90, BOX_ORANGE, "Max pool 2x2", "keep the max")
    box(c, 432, 470, 108, 90, BOX_TEAL, "Smaller map", "1/4 the size")
    arrow(c, 222, 515, 266, 515, color=ACCENT, width=2.5)
    arrow(c, 386, 515, 430, 515, color=ACCENT, width=2.5)
    note(c, 72, 300, 468, "Pooling buys translation invariance and cuts compute. Modern nets often use strided convolutions instead of pooling.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Receptive Fields Grow",
                       "Deeper neurons see more of the image.")
    box(c, 72, 470, 130, 80, BOX_BLUE, "Layer 1", "sees 3x3 px")
    box(c, 244, 470, 130, 80, BOX_TEAL, "Layer 3", "sees 11x11 px")
    box(c, 416, 470, 124, 80, BOX_PURP, "Layer 5", "sees 35x35 px")
    arrow(c, 202, 510, 242, 510, color=ACCENT, width=2.5)
    arrow(c, 374, 510, 414, 510, color=ACCENT, width=2.5)
    note(c, 72, 300, 468, "The receptive field is why deep CNNs understand context: late neurons integrate the whole scene.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Skip Connections (ResNet)",
                       "A shortcut lets gradients flow through 100+ layers.")
    box(c, 72, 460, 120, 70, BOX_BLUE, "x", "block input")
    box(c, 246, 460, 140, 70, BOX_ORANGE, "F(x)", "conv layers")
    box(c, 430, 460, 110, 70, BOX_GREEN, "F(x) + x", "residual")
    arrow(c, 192, 495, 244, 495, color=ACCENT, width=2)
    arrow(c, 386, 495, 428, 495, color=ACCENT, width=2)
    arrow(c, 132, 560, 484, 560, color=GREEN, width=2.5, label="skip path")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 410, "The network learns the residual F(x) instead of the full mapping — much easier to optimize.")
    note(c, 72, 290, 468, "Residual nets made very deep CNNs trainable and are the backbone of most vision systems.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "CNN Design Rules",
                       "Defaults that work.")
    yy = bullet_list(c, 72, y,
        ["3x3 kernels, stacked deep, beat one big kernel: same receptive field, fewer params, more nonlinearity.",
         "Stride 2 (or pooling) halves resolution each stage while doubling channels: 64 -> 128 -> 256 -> 512.",
         "Batch normalization after convolutions stabilizes training and allows higher learning rates.",
         "Data augmentation (crops, flips, color jitter) is free training data — almost always worth it.",
         "For a new vision task, fine-tune a pretrained ResNet/EfficientNet before training from scratch."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "CNNs — Remember",
                 ["Convolution = learned kernel sliding over the image; weight sharing keeps params low.",
                  "Filters form a hierarchy: edges -> textures -> object parts.",
                  "Pooling/striding downsamples for invariance and efficiency; receptive fields grow with depth.",
                  "Skip connections (ResNet) let gradients flow through very deep networks.",
                  "Start from a pretrained backbone and fine-tune; augment aggressively."],
                 pg)
    c.save(); print("wrote", path)


def pdf_rnns(path):
    c = new_canvas(path); pg = 1
    title_page(c, "RNNs & LSTMs\nVisual Guide",
               "Networks with memory:\nsequence processing, vanishing gradients, LSTM gates.",
               "Deep Learning", None); pg += 1

    y = section_header(c, 1, 5, "Sequences, One Step at a Time",
                       "The hidden state carries memory forward.")
    box(c, 72, 460, 120, 70, BOX_BLUE, "h(t-1)", "previous memory")
    box(c, 246, 460, 120, 70, BOX_PURP, "h(t)", "updated memory")
    box(c, 420, 460, 120, 70, BOX_BLUE, "h(t+1)", "next memory")
    arrow(c, 192, 495, 244, 495, color=ACCENT, width=2.5)
    arrow(c, 366, 495, 418, 495, color=ACCENT, width=2.5)
    box(c, 246, 360, 120, 60, BOX_GREEN, "x(t)", "input at step t")
    box(c, 246, 560, 120, 60, BOX_ORANGE, "y(t)", "output at step t")
    arrow(c, 306, 420, 306, 458, color=ACCENT, width=2)
    arrow(c, 306, 532, 306, 558, color=ACCENT, width=2)
    note(c, 72, 240, 468, "Same weights reused at every timestep. The network's memory IS the hidden state h.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Unrolled Through Time",
                       "The loop becomes a very deep feedforward net.")
    xs = [72, 182, 292, 402]
    for i, xx in enumerate(xs):
        box(c, xx, 470, 96, 70, BOX_PURP, "h%d" % (i + 1), "t = %d" % (i + 1))
        if i > 0:
            arrow(c, xs[i-1] + 96, 505, xx, 505, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Unrolling exposes the loop as a chain. Backprop through it is called backprop-through-time (BPTT).")
    note(c, 72, 290, 468, "A 100-step sequence unrolls into a 100-layer network — which is exactly why gradients misbehave.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "The Vanishing Gradient Problem",
                       "Gradients shrink (or explode) across many steps.")
    box(c, 420, 470, 120, 70, BOX_RED, "grad = 1.0", "at the end")
    box(c, 246, 470, 120, 70, BOX_ORANGE, "grad = 0.01", "midway back")
    box(c, 72, 470, 120, 70, BOX_BLUE, "grad ~ 0", "at the start")
    arrow(c, 418, 505, 368, 505, color=RED, width=4)
    arrow(c, 244, 505, 194, 505, color=RED, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Each step multiplies the gradient by the recurrent weights. Values < 1 decay to zero exponentially.")
    note(c, 72, 290, 468, "Result: plain RNNs cannot learn long-range dependencies. Gradient clipping tames explosions; LSTMs fix vanishing.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "LSTM Gates",
                       "Three gates guard a protected cell state.")
    box(c, 72, 560, 120, 60, BOX_RED, "Forget", "erase old memory?")
    box(c, 216, 560, 120, 60, BOX_GREEN, "Input", "store new info?")
    box(c, 360, 560, 120, 60, BOX_BLUE, "Output", "reveal what?")
    box(c, 72, 450, 408, 56, BOX_PURP, "Cell state C(t)", "the protected conveyor belt — gradients flow undiminished")
    arrow(c, 132, 558, 132, 508, color=RED, width=1.5)
    arrow(c, 276, 558, 276, 508, color=GREEN, width=1.5)
    arrow(c, 420, 558, 420, 508, color=ACCENT, width=1.5)
    note(c, 72, 320, 468, "Gates are sigmoids (0-1) learned from data. The cell state is an additive highway — the fix for vanishing gradients.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "RNNs vs Transformers",
                       "When each architecture wins.")
    box(c, 72, 430, 220, 120, BOX_PURP, "RNN / LSTM", "sequential, O(n) memory,")
    box(c, 320, 430, 220, 120, BOX_BLUE, "Transformer", "parallel, O(n^2) attention,")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "great for streaming,")
    c.drawString(92, 486, "tiny models, low latency.")
    c.drawString(340, 500, "dominant for language —")
    c.drawString(340, 486, "sees all positions at once.")
    yy = bullet_list(c, 72, 380,
        ["RNNs process step-by-step: slow to train, but constant memory and natural for streaming.",
         "Transformers attend to everything in parallel: fast to train on GPUs, but memory grows quadratically.",
         "For long text, transformers won. For tiny on-device streaming models, RNNs/LSTMs still ship."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "RNNs & LSTMs — Remember",
                 ["RNNs reuse weights across timesteps; the hidden state is the memory.",
                  "Unrolling gives backprop-through-time (BPTT) — a very deep chain.",
                  "Vanishing gradients kill long-range learning in plain RNNs.",
                  "LSTM gates (forget/input/output) protect a cell-state highway for gradients.",
                  "Transformers dominate language; RNNs still win for streaming and tiny models."],
                 pg)
    c.save(); print("wrote", path)


def pdf_attention(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Attention\nDeep Dive",
               "The mechanism behind transformers:\nscaled dot-product attention, Q/K/V, masking, heatmaps.",
               "Deep Learning", None); pg += 1

    y = section_header(c, 1, 5, "Why Attention",
                       "Let every position look at every other position.")
    box(c, 72, 480, 130, 70, BOX_BLUE, "Query", "what am I looking for?")
    box(c, 244, 480, 130, 70, BOX_ORANGE, "Keys", "what do I contain?")
    box(c, 416, 480, 124, 70, BOX_GREEN, "Values", "what do I pass on?")
    arrow(c, 202, 515, 242, 515, color=ACCENT, width=2)
    arrow(c, 374, 515, 414, 515, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Attention = weighted lookup. The query scores every key; the scores weight the values.")
    note(c, 72, 300, 468, "Unlike RNNs, attention sees the whole sequence at once — fully parallel, no forgetting curve.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Scaled Dot-Product Attention",
                       "Four operations, one formula.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(306, 590, "Attention(Q, K, V) = softmax( Q K^T / sqrt(d_k) ) V")
    box(c, 72, 440, 100, 64, BOX_ORANGE, "Scores", "Q dot K")
    box(c, 188, 440, 100, 64, BOX_TEAL, "Scale", "/ sqrt(d_k)")
    box(c, 304, 440, 100, 64, BOX_BLUE, "Softmax", "weights sum to 1")
    box(c, 420, 440, 120, 64, BOX_GREEN, "Mix", "weighted sum of V")
    arrow(c, 172, 472, 186, 472, color=ACCENT, width=1.5)
    arrow(c, 288, 472, 302, 472, color=ACCENT, width=1.5)
    arrow(c, 404, 472, 418, 472, color=ACCENT, width=1.5)
    note(c, 72, 300, 468, "Scaling by sqrt(d_k) keeps dot products small so softmax stays in its sensitive range — without it, attention saturates.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Q, K, V Matrices",
                       "Three learned projections of the same embeddings.")
    box(c, 196, 500, 220, 60, BOX_PURP, "Token embeddings", "input sequence")
    box(c, 72, 380, 130, 70, BOX_BLUE, "Q = X Wq", "queries")
    box(c, 241, 380, 130, 70, BOX_ORANGE, "K = X Wk", "keys")
    box(c, 410, 380, 130, 70, BOX_GREEN, "V = X Wv", "values")
    arrow(c, 260, 498, 137, 452, color=ACCENT, width=1.5)
    arrow(c, 306, 498, 306, 452, color=ACCENT, width=1.5)
    arrow(c, 352, 498, 475, 452, color=ACCENT, width=1.5)
    note(c, 72, 260, 468, "Wq, Wk, Wv are learned. Multi-head attention runs several Q/K/V sets in parallel — each head learns a different relation.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Causal Masking",
                       "Decoders must not peek at the future.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 600, "Attention grid: rows = current position, columns = positions it may attend to.")
    box(c, 72, 480, 130, 60, BOX_GREEN, "Position 1: 'The'", "attends to: The")
    box(c, 241, 480, 130, 60, BOX_GREEN, "Position 2: 'cat'", "attends to: The, cat")
    box(c, 410, 480, 130, 60, BOX_RED, "'sat' blocked", "future is masked")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Before softmax, future scores are set to -infinity. After softmax they become exactly zero.")
    note(c, 72, 300, 468, "Masking is what makes next-token prediction honest: the model predicts each token from earlier positions only.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Reading Attention Heatmaps",
                       "Bright cells show strong attention weights.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Diagonal band", "local attention:")
    box(c, 320, 470, 220, 90, BOX_ORANGE, "Vertical stripe", "global hub token:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 510, "each word attends to neighbors —")
    c.drawString(92, 496, "syntax lives here.")
    c.drawString(340, 510, "many words attend to one token —")
    c.drawString(340, 496, "often punctuation or [SEP]-like anchors.")
    yy = bullet_list(c, 72, 400,
        ["Rows sum to 1: a row spread thin means diffuse attention; one bright cell means focus.",
         "Different heads specialize: some track syntax, some track coreference, some track position.",
         "Caution: high attention weight does not prove causation — treat heatmaps as hints, not explanations."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Attention — Remember",
                 ["Attention = softmax(QK^T / sqrt(d_k)) V: queries score keys, weights mix values.",
                  "Q, K, V are learned projections; multi-head runs several in parallel.",
                  "Scaling prevents softmax saturation; masking enforces causality in decoders.",
                  "Heatmaps reveal patterns (diagonal = local, stripes = hubs) but are not proof of reasoning.",
                  "Parallel over the sequence is why transformers train so much faster than RNNs."],
                 pg)
    c.save(); print("wrote", path)


def pdf_bert_gpt(path):
    c = new_canvas(path); pg = 1
    title_page(c, "BERT vs GPT\nVisual Guide",
               "Two pretraining philosophies:\nmasked language modeling vs next-token prediction.",
               "NLP", None); pg += 1

    y = section_header(c, 1, 5, "Encoder vs Decoder",
                       "Same transformer blocks, opposite information flow.")
    box(c, 72, 430, 220, 120, BOX_BLUE, "BERT: encoder", "bidirectional — sees")
    box(c, 320, 430, 220, 120, BOX_ORANGE, "GPT: decoder", "causal — sees only")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "left AND right context.")
    c.drawString(92, 486, "Reads the whole sentence.")
    c.drawString(340, 500, "the past.")
    c.drawString(340, 486, "Generates left to right.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 380, "Encoders understand; decoders generate. The masking pattern is the entire difference.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Masked LM: BERT's Pretraining",
                       "Hide words, predict them from both sides.")
    toks = ["The", "[MASK]", "sat", "on", "the", "[MASK]"]
    xx = 72
    for t in toks:
        fill = BOX_RED if t == "[MASK]" else BOX_BLUE
        box(c, xx, 480, 68, 56, fill, t, "")
        xx += 76
    arrow(c, 306, 478, 306, 430, color=ACCENT, width=2)
    box(c, 196, 350, 220, 64, BOX_GREEN, "Predict: 'cat', 'mat'", "cross-entropy on masks")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 300, "Mask ~15% of tokens at random. Loss is computed ONLY on the masked positions.")
    note(c, 72, 200, 468, "Bidirectional context makes BERT superb at understanding — classification, NER, QA span extraction.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Next-Token: GPT's Pretraining",
                       "Predict the next word, forever.")
    toks = ["The", "cat", "sat", "on", "the", "?"]
    xx = 72
    for i, t in enumerate(toks):
        fill = BOX_GREEN if t == "?" else BOX_ORANGE
        box(c, xx, 480, 68, 56, fill, t, "")
        if i < len(toks) - 1:
            arrow(c, xx + 68, 508, xx + 76, 508, color=ACCENT, width=1.5)
        xx += 76
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 410, "Every position predicts the next token. The entire internet becomes a self-supervised dataset.")
    note(c, 72, 290, 468, "Simple objective, staggering scale: next-token prediction at trillion-token scale yields general capabilities.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Fine-tuning BERT",
                       "Add a small head, train on labeled data.")
    box(c, 72, 470, 200, 70, BOX_BLUE, "Pretrained BERT", "frozen or lightly tuned")
    box(c, 320, 470, 200, 70, BOX_GREEN, "Task head", "classifier / span layer")
    arrow(c, 272, 505, 318, 505, color=ACCENT, width=2.5)
    yy = bullet_list(c, 72, 400,
        ["Classification: feed the [CLS] embedding into a linear layer (sentiment, intent, topic).",
         "QA: two heads predict answer start/end spans over the passage.",
         "Fine-tune all layers with a small learning rate (2e-5) for a few epochs — watch for overfitting on small sets."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Adapting GPT",
                       "Prompt it, or fine-tune it.")
    box(c, 72, 480, 220, 70, BOX_ORANGE, "Prompting", "zero/few-shot + instructions")
    box(c, 320, 480, 220, 70, BOX_TEAL, "Fine-tuning", "train on your Q/A pairs")
    yy = bullet_list(c, 72, 400,
        ["Prompting first: cheapest adaptation. Good prompts often beat small fine-tunes.",
         "Fine-tune when you need a stable style, domain vocabulary, or structured outputs at scale.",
         "RLHF/DPO aligns the model with human preferences after pretraining — the chat behavior you know.",
         "Rule of thumb: prompt for behavior, fine-tune for knowledge and format reliability."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "BERT vs GPT — Remember",
                 ["BERT = bidirectional encoder trained with masked LM: best for understanding tasks.",
                  "GPT = causal decoder trained with next-token prediction: best for generation.",
                  "Masking pattern is the core difference; architecture is otherwise similar.",
                  "Fine-tune BERT with a task head; adapt GPT via prompting first, fine-tuning second.",
                  "Both benefit from domain-adaptive pretraining before task fine-tuning."],
                 pg)
    c.save(); print("wrote", path)


def pdf_embeddings(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Embeddings\nVisual Guide",
               "Turning words into vectors:\nword2vec, analogies, cosine similarity, sentence embeddings.",
               "NLP", None); pg += 1

    y = section_header(c, 1, 5, "Words as Vectors",
                       "Dense vectors carry meaning; one-hot vectors don't.")
    box(c, 72, 470, 220, 90, BOX_RED, "One-hot", "50,000 dims, all zeros")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Embedding", "300 dense dims,")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "but one 1. No notion")
    c.drawString(92, 501, "of similarity.")
    c.drawString(340, 515, "learned from context.")
    c.drawString(340, 501, "Similar words sit close.")
    note(c, 72, 320, 468, "Distributional hypothesis: words appearing in similar contexts get similar vectors. Geometry becomes semantics.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Skip-gram vs CBOW",
                       "Word2vec's two training games.")
    box(c, 72, 440, 220, 110, BOX_BLUE, "Skip-gram", "center word ->")
    box(c, 320, 440, 220, 110, BOX_TEAL, "CBOW", "context -> center")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "predicts surrounding")
    c.drawString(92, 486, "words. Better for rare words.")
    c.drawString(340, 500, "word. Faster, better")
    c.drawString(340, 486, "for frequent words.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 390, "Both train a shallow network whose hidden weights BECOME the embeddings. The task is a pretext.")
    note(c, 72, 270, 468, "Negative sampling makes training tractable: contrast the true context word against a few random impostors.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Analogies in Vector Space",
                       "Relationships become directions.")
    box(c, 72, 500, 110, 60, BOX_BLUE, "king", "")
    box(c, 216, 500, 110, 60, BOX_RED, "- man", "")
    box(c, 360, 500, 110, 60, BOX_GREEN, "+ woman", "")
    arrow(c, 182, 530, 214, 530, color=ACCENT, width=2)
    arrow(c, 326, 530, 358, 530, color=ACCENT, width=2)
    box(c, 216, 400, 180, 64, BOX_PURP, "= queen (nearest)", "vector arithmetic works")
    arrow(c, 306, 498, 306, 466, color=GREEN, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 350, "king - man + woman lands nearest to 'queen'. Gender, tense, and capital-of become consistent offsets.")
    note(c, 72, 240, 468, "Analogies are a diagnostic, not a guarantee — they also surface the biases baked into the training corpus.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Cosine Similarity",
                       "Angle, not distance, measures relatedness.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "cos = A dot B / (|A||B|)", "1 = same direction")
    box(c, 320, 470, 220, 90, BOX_GREEN, "0 = unrelated", "orthogonal vectors")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Cosine similarity ranges from -1 to 1. Normalizing vectors makes dot product equal cosine.")
    note(c, 72, 300, 468, "This one formula powers semantic search: embed the query, find stored vectors with the highest cosine similarity.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Sentence Embeddings",
                       "From word vectors to whole-text vectors.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Tokens", "word pieces")
    box(c, 256, 500, 140, 70, BOX_PURP, "Encoder", "transformer")
    box(c, 430, 500, 110, 70, BOX_GREEN, "Pooling", "mean / CLS")
    arrow(c, 212, 535, 254, 535, color=ACCENT, width=2)
    arrow(c, 396, 535, 428, 535, color=ACCENT, width=2)
    yy = bullet_list(c, 72, 420,
        ["Mean-pool token embeddings, or train a dedicated sentence model (SBERT, E5, BGE).",
         "Contrastive training: pull paraphrases together, push unrelated texts apart.",
         "One vector per document unlocks semantic search, clustering, dedup, and recommendations."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Embeddings — Remember",
                 ["Dense vectors encode meaning; one-hot vectors cannot.",
                  "Skip-gram predicts context from a word; CBOW predicts the word from context.",
                  "Analogies (king - man + woman = queen) reveal semantic directions — and corpus bias.",
                  "Cosine similarity turns angle into a relatedness score for search and clustering.",
                  "Sentence embeddings power semantic search, dedup, and recommendations."],
                 pg)
    c.save(); print("wrote", path)


def pdf_finetuning(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Fine-tuning LLMs\nVisual Guide",
               "Adapting big models cheaply:\nfull tuning, LoRA/QLoRA, instruction tuning, RLHF.",
               "LLM Engineering", None); pg += 1

    y = section_header(c, 1, 6, "Full Fine-tuning",
                       "Update every weight. Powerful, expensive.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Pretrained model", "all weights trainable")
    box(c, 320, 470, 220, 90, BOX_ORANGE, "Your dataset", "thousands of examples")
    arrow(c, 292, 515, 318, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Every parameter updates. Needs serious GPU memory — optimizer states can triple the footprint.")
    note(c, 72, 300, 468, "Risks: catastrophic forgetting of general ability, and overfitting on small datasets. Small learning rate, few epochs.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "LoRA: Low-Rank Adapters",
                       "Freeze the giant; train a tiny side-path.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Base weights W", "FROZEN — no updates")
    box(c, 320, 470, 220, 90, BOX_GREEN, "LoRA: A x B", "tiny rank-r matrices,")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(340, 500, "trainable. W + AB is")
    c.drawString(340, 486, "the effective weight.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Rank r (8-64) controls capacity. Adapters are <1% of parameters — mergeable at inference for zero overhead.")
    note(c, 72, 300, 468, "LoRA adapters are swappable: one base model, many task adapters. The standard efficient fine-tuning method.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "QLoRA: Quantize the Base",
                       "Fine-tune a 65B model on one GPU.")
    box(c, 72, 470, 150, 90, BOX_PURP, "Base model", "quantized to 4-bit")
    box(c, 262, 470, 150, 90, BOX_GREEN, "LoRA", "in higher precision")
    box(c, 452, 470, 88, 90, BOX_BLUE, "1 GPU", "fits!")
    arrow(c, 222, 515, 260, 515, color=ACCENT, width=2)
    arrow(c, 412, 515, 450, 515, color=ACCENT, width=2)
    note(c, 72, 320, 468, "4-bit NormalFloat quantization shrinks the frozen base ~8x. Quality stays close to full fine-tuning on most tasks.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Instruction Tuning",
                       "Teach the model to follow instructions.")
    box(c, 72, 500, 468, 64, BOX_BLUE, "Instruction: 'Summarize this report in 3 bullets'", "input")
    box(c, 72, 410, 468, 64, BOX_GREEN, "Response: '- Revenue up 12% ...'", "target output")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 360, "Train on (instruction, response) pairs — FLAN, Alpaca-style datasets. The model learns the follow-instructions behavior.")
    note(c, 72, 240, 468, "Instruction tuning is what turns a raw next-token model into a helpful assistant. Quality and diversity of examples matter most.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "The RLHF Pipeline",
                       "Align with human preferences in three stages.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "1. SFT", "supervised fine-tune")
    box(c, 246, 470, 140, 80, BOX_ORANGE, "2. Reward model", "learns human prefs")
    box(c, 420, 470, 120, 80, BOX_GREEN, "3. PPO/DPO", "optimize vs reward")
    arrow(c, 212, 510, 244, 510, color=ACCENT, width=2.5)
    arrow(c, 386, 510, 418, 510, color=ACCENT, width=2.5)
    note(c, 72, 330, 468, "Humans rank pairs of responses; the reward model generalizes those rankings; PPO/DPO steers the policy toward them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Evaluating After Tuning",
                       "Prove the tune helped — and didn't break anything.")
    yy = bullet_list(c, 72, y,
        ["Hold out a test set BEFORE tuning. Report task metrics (accuracy, F1) plus a general benchmark (MMLU-lite).",
         "Regression-test old capabilities: fine-tunes can silently degrade general knowledge.",
         "Check for overfitting: huge train/test gaps, or the model parroting training phrasing.",
         "Human spot-checks on 50-100 outputs catch what metrics miss — tone, format, refusal behavior."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "If evals don't move, the bottleneck is data quality — not rank, not epochs. Curate harder examples.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Fine-tuning LLMs — Remember",
                 ["Full fine-tuning updates everything: powerful but GPU-hungry and forgetful.",
                  "LoRA trains tiny rank-r adapters on a frozen base — swappable, mergeable, standard.",
                  "QLoRA quantizes the base to 4-bit so huge models fit on one GPU.",
                  "Instruction tuning teaches follow-instructions behavior; RLHF/DPO aligns with human preference.",
                  "Evaluate on held-out tests AND general benchmarks to catch regressions."],
                 pg)
    c.save(); print("wrote", path)


def pdf_rag(path):
    c = new_canvas(path); pg = 1
    title_page(c, "RAG: Retrieval-Augmented\nGeneration",
               "Grounding LLMs in your data:\nchunking, retrieval, reranking, cited answers.",
               "LLM Engineering", None); pg += 1

    y = section_header(c, 1, 6, "Chunking Strategies",
                       "Split documents into retrievable pieces.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "Fixed-size", "500 tokens + overlap")
    box(c, 246, 470, 140, 80, BOX_TEAL, "Recursive", "split on paragraphs,")
    box(c, 420, 470, 120, 80, BOX_GREEN, "Semantic", "split on topic shifts")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(266, 500, "then sentences.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Chunks must be self-contained enough to make sense alone, small enough to rank precisely.")
    note(c, 72, 300, 468, "Include metadata (title, page, date) per chunk — it powers filtering and citations later.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Embed and Index",
                       "Turn chunks into searchable vectors.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "Chunks", "text pieces")
    box(c, 256, 470, 140, 80, BOX_PURP, "Embedder", "text -> vector")
    box(c, 430, 470, 110, 80, BOX_GREEN, "Index", "vector DB")
    arrow(c, 212, 510, 254, 510, color=ACCENT, width=2.5)
    arrow(c, 396, 510, 428, 510, color=ACCENT, width=2.5)
    note(c, 72, 330, 468, "Index once, query many times. Re-embed only when documents change — version your embeddings with your data.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Retrieval",
                       "Find the chunks that answer the query.")
    box(c, 72, 500, 200, 70, BOX_ORANGE, "Query", "'refund policy for Pro plan?'")
    box(c, 320, 500, 220, 70, BOX_BLUE, "Top-k chunks", "k = 5-20 by similarity")
    arrow(c, 272, 535, 318, 535, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "Embed the query with the SAME model, run nearest-neighbor search, apply metadata filters.")
    note(c, 72, 320, 468, "Retrieval quality dominates RAG quality. If the right chunk isn't retrieved, the LLM cannot invent it — it will hallucinate instead.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Reranking",
                       "A second, smarter pass over candidates.")
    box(c, 72, 470, 220, 80, BOX_BLUE, "Stage 1: recall", "fast bi-encoder, top 50")
    box(c, 320, 470, 220, 80, BOX_GREEN, "Stage 2: rerank", "cross-encoder, top 5")
    arrow(c, 292, 510, 318, 510, color=ACCENT, width=2.5)
    note(c, 72, 330, 468, "Cross-encoders read query+chunk together — slower but far more accurate. The classic recall-then-precision tradeoff.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Generate with Citations",
                       "Answer ONLY from retrieved context.")
    box(c, 72, 500, 220, 70, BOX_BLUE, "Context chunks", "the evidence")
    box(c, 320, 500, 220, 70, BOX_PURP, "LLM", "strict system prompt")
    arrow(c, 292, 535, 318, 535, color=ACCENT, width=2.5)
    box(c, 196, 390, 220, 64, BOX_GREEN, "Cited answer", "'... [doc 3, p.12]'")
    arrow(c, 306, 498, 306, 456, color=GREEN, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "System prompt: answer from context only; cite sources; say 'I don't know' when context is insufficient.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Evaluating RAG",
                       "Faithfulness first.")
    yy = bullet_list(c, 72, y,
        ["Faithfulness: is every claim supported by a retrieved chunk? (LLM-judge or entailment model).",
         "Answer relevance: does the answer actually address the question asked?",
         "Retrieval metrics: recall@k and MRR on a labeled Q/A set — fix retrieval before the prompt.",
         "Build a golden Q/A set from real user questions; re-run it on every pipeline change."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "Most RAG failures are retrieval failures. Log queries with zero good hits — they reveal chunking and coverage gaps.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "RAG — Remember",
                 ["Chunk for self-containment; attach metadata for filtering and citations.",
                  "Embed once with a consistent model; retrieval quality dominates final quality.",
                  "Rerank with a cross-encoder: recall first, precision second.",
                  "Generate with a strict grounded prompt and require citations; allow 'I don't know'.",
                  "Evaluate faithfulness and retrieval recall on a golden Q/A set, continuously."],
                 pg)
    c.save(); print("wrote", path)


def pdf_prompt_engineering(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Prompt Engineering\nVisual Guide",
               "Getting reliable behavior from LLMs:\nshots, chain-of-thought, structure, defense.",
               "LLM Engineering", None); pg += 1

    y = section_header(c, 1, 6, "Zero-shot vs Few-shot",
                       "Examples are the cheapest fine-tune.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Zero-shot", "instruction only:")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Few-shot", "instruction +")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "'Classify this review.'")
    c.drawString(340, 515, "3-5 input/output")
    c.drawString(340, 501, "examples. Anchors format.")
    note(c, 72, 320, 468, "Few-shot examples fix output format and edge-case behavior. Pick diverse, representative examples — order matters.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Chain-of-Thought",
                       "Make the model show its work.")
    box(c, 72, 500, 130, 70, BOX_BLUE, "Problem", "the question")
    box(c, 246, 500, 130, 70, BOX_ORANGE, "Reasoning", "step by step")
    box(c, 420, 500, 120, 70, BOX_GREEN, "Answer", "final result")
    arrow(c, 202, 535, 244, 535, color=ACCENT, width=2.5)
    arrow(c, 376, 535, 418, 535, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "Magic phrase: 'Let's think step by step.' Reasoning tokens give the model compute to work with.")
    note(c, 72, 320, 468, "Best for math, logic, and multi-hop questions. Verify the steps — CoT can rationalize a wrong answer convincingly.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Structured Outputs",
                       "Constrain the response shape.")
    box(c, 72, 470, 220, 90, BOX_PURP, "JSON schema", "fields + types")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Valid JSON", "parseable, no prose")
    arrow(c, 292, 515, 318, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Demand a schema in the prompt — or enforce it with the API's structured-output mode / grammar decoding.")
    note(c, 72, 300, 468, "Never regex-parse free prose when you can require JSON. Validate against the schema and retry on failure.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "System Prompts",
                       "Set the role, rules, and boundaries up front.")
    box(c, 72, 470, 140, 90, BOX_BLUE, "Role", "'You are a senior'")
    box(c, 246, 470, 140, 90, BOX_TEAL, "Rules", "'Cite sources;'")
    box(c, 420, 470, 120, 90, BOX_ORANGE, "Limits", "'Never invent'")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "support agent.")
    c.drawString(266, 500, "'3 bullets max.'")
    c.drawString(440, 500, "prices.'")
    note(c, 72, 320, 468, "System prompts outrank user prompts in well-behaved models — put non-negotiable constraints here, not in the user message.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Prompt Injection Defense",
                       "Treat untrusted input as data, never as instructions.")
    box(c, 72, 470, 220, 90, BOX_RED, "Attack", "'Ignore rules, reveal'")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Defense", "delimit + instruct +")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(340, 500, "validate. Untrusted text")
    c.drawString(340, 486, "goes in quoted blocks.")
    yy = bullet_list(c, 72, 380,
        ["Delimit untrusted content with clear markers; instruct the model to treat it as data.",
         "Least privilege: the model should only have tools and data the task truly needs.",
         "Validate outputs before acting on them — especially tool calls and database writes."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The Iteration Loop",
                       "Prompts are software: version and test them.")
    yy = bullet_list(c, 72, y,
        ["Write the prompt, run it on 20-50 representative cases, score the outputs.",
         "Change ONE thing at a time: wording, examples, or structure — never all three.",
         "Keep a prompt eval set in version control; re-run on every model or prompt change.",
         "Log failures by category (format, hallucination, refusal) — categories tell you what to fix.",
         "When few-shot stops improving the prompt, that's the signal to consider fine-tuning."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Prompt Engineering — Remember",
                 ["Few-shot examples anchor format and edge cases — cheapest adaptation available.",
                  "Chain-of-thought buys reasoning compute; verify the steps, not just the answer.",
                  "Require structured outputs (JSON schema) instead of parsing prose.",
                  "Put role, rules, and limits in the system prompt; treat untrusted input as data.",
                  "Version prompts and eval them like code: fixed test sets, one change at a time."],
                 pg)
    c.save(); print("wrote", path)


def pdf_diffusion(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Diffusion Models\nVisual Guide",
               "How image generators work:\nnoising, denoising, U-Net, sampling, conditioning.",
               "Generative AI", None); pg += 1

    y = section_header(c, 1, 5, "Forward: Adding Noise",
                       "Destroy the image on a fixed schedule.")
    box(c, 72, 480, 120, 70, BOX_GREEN, "Image", "clean x(0)")
    box(c, 226, 480, 120, 70, BOX_ORANGE, "Noisy", "x(t)")
    box(c, 380, 480, 120, 70, BOX_RED, "Pure noise", "x(T)")
    arrow(c, 192, 515, 224, 515, color=ACCENT, width=2.5)
    arrow(c, 346, 515, 378, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Each step adds a little Gaussian noise. After T steps the image is pure static — a known distribution.")
    note(c, 72, 300, 468, "The forward process needs no learning — it is a fixed recipe. All the intelligence lives in the reverse process.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Reverse: Denoising",
                       "Learn to remove the noise, one step at a time.")
    box(c, 72, 480, 120, 70, BOX_RED, "Pure noise", "x(T)")
    box(c, 226, 480, 120, 70, BOX_ORANGE, "Denoise", "predict noise")
    box(c, 380, 480, 120, 70, BOX_GREEN, "Image", "clean x(0)")
    arrow(c, 192, 515, 224, 515, color=GREEN, width=2.5)
    arrow(c, 346, 515, 378, 515, color=GREEN, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "The model predicts the noise added at step t, subtracts it, and repeats — walking noise back into an image.")
    note(c, 72, 300, 468, "Training: take a clean image, add known noise, ask the model to predict that noise. Simple MSE loss.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "The U-Net",
                       "The denoiser's architecture.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "Encoder", "downsample,")
    box(c, 256, 470, 140, 80, BOX_PURP, "Bottleneck", "global context")
    box(c, 430, 470, 110, 80, BOX_TEAL, "Decoder", "upsample back")
    arrow(c, 212, 510, 254, 510, color=ACCENT, width=2)
    arrow(c, 396, 510, 428, 510, color=ACCENT, width=2)
    arrow(c, 142, 560, 484, 560, color=GREEN, width=2, label="skip connections")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "capture context.")
    note(c, 72, 300, 468, "Skip connections carry fine detail past the bottleneck — sharp edges survive the round trip.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Sampling: Steps vs Speed",
                       "Fewer steps, faster images — with tradeoffs.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "DDPM: 1000 steps", "slow, highest quality")
    box(c, 320, 470, 220, 90, BOX_GREEN, "DDIM: 20-50 steps", "fast, near-equal quality")
    arrow(c, 292, 515, 318, 515, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "DDIM skips steps deterministically. Distilled models (few-step) push generation to 1-8 steps.")
    note(c, 72, 300, 468, "The sampler is swappable after training — upgrade speed without retraining the model.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Text Conditioning",
                       "Steering generation with words.")
    box(c, 72, 480, 200, 70, BOX_BLUE, "Text prompt", "'a red fox in snow'")
    box(c, 320, 480, 220, 70, BOX_PURP, "Text encoder", "CLIP / T5 embeddings")
    arrow(c, 272, 515, 318, 515, color=ACCENT, width=2.5)
    box(c, 196, 370, 220, 64, BOX_GREEN, "Cross-attention", "U-Net attends to text")
    arrow(c, 306, 478, 306, 436, color=GREEN, width=2.5)
    note(c, 72, 250, 468, "Classifier-free guidance: blend conditional and unconditional predictions — higher guidance = stronger prompt adherence.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Diffusion Models — Remember",
                 ["Forward process adds noise on a fixed schedule; no learning needed there.",
                  "The model learns reverse denoising: predict the noise, subtract, repeat.",
                  "U-Net with skip connections is the classic denoiser architecture.",
                  "DDIM and distilled samplers cut 1000 steps to dozens with little quality loss.",
                  "Text encoders + cross-attention + classifier-free guidance steer generation."],
                 pg)
    c.save(); print("wrote", path)


def pdf_gans(path):
    c = new_canvas(path); pg = 1
    title_page(c, "GANs: Generative Adversarial\nNetworks",
               "Two networks, one game:\ngenerator vs discriminator, training dynamics, failure modes.",
               "Generative AI", None); pg += 1

    y = section_header(c, 1, 5, "The Adversarial Game",
                       "A forger and a detective, locked in competition.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Generator", "noise -> fake image.")
    box(c, 320, 470, 220, 90, BOX_RED, "Discriminator", "real or fake?")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "Tries to fool the")
    c.drawString(92, 501, "discriminator.")
    c.drawString(340, 515, "Tries to catch the")
    c.drawString(340, 501, "generator.")
    arrow(c, 292, 540, 318, 540, color=ACCENT, width=2, label="fake images")
    arrow(c, 318, 490, 292, 490, color=RED, width=2, label="real/fake signal")
    note(c, 72, 320, 468, "Minimax game: the generator minimizes what the discriminator maximizes. Equilibrium = fakes indistinguishable from real.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Training Dynamics",
                       "Alternate updates; balance is everything.")
    box(c, 72, 480, 130, 70, BOX_RED, "Train D", "on real + fake")
    box(c, 246, 480, 130, 70, BOX_BLUE, "Train G", "fool frozen D")
    box(c, 420, 480, 120, 70, BOX_GREEN, "Repeat", "thousands of")
    arrow(c, 202, 515, 244, 515, color=ACCENT, width=2.5)
    arrow(c, 376, 515, 418, 515, color=ACCENT, width=2.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(440, 500, "rounds.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Freeze one network while updating the other. If D gets too strong, G gets no useful gradient.")
    note(c, 72, 300, 468, "GAN training is famously unstable: learning rates, update ratios, and architectures must be tuned together.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Mode Collapse",
                       "The generator finds one trick and repeats it.")
    box(c, 72, 470, 220, 90, BOX_GREEN, "Healthy GAN", "diverse outputs:")
    box(c, 320, 470, 220, 90, BOX_RED, "Collapsed GAN", "one output,")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "many faces, poses,")
    c.drawString(92, 501, "styles.")
    c.drawString(340, 515, "repeated endlessly.")
    c.drawString(340, 501, "D is fooled; diversity dies.")
    note(c, 72, 320, 468, "Fixes: minibatch discrimination, unrolled GANs, Wasserstein loss, or simply better architectures (StyleGAN). Diversity metrics catch it early.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Evaluating GANs",
                       "No loss curve tells you the images are good.")
    yy = bullet_list(c, 72, y,
        ["FID (Frechet Inception Distance): compares feature distributions of real vs generated images — lower is better.",
         "Inception Score: rewards sharp, diverse classifications — higher is better, but gameable.",
         "Precision/Recall for GANs: precision = quality of fakes, recall = coverage of real diversity.",
         "Human eval still matters: show raters mixed real/fake grids and measure fool rate.",
         "Track FID through training; stop or roll back when it degrades — GANs can collapse late."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Modern Variants",
                       "Where GAN ideas live on.")
    variants = [("StyleGAN", "Style-based generator: control pose, texture, identity separately. Photoreal faces.", BOX_BLUE),
                ("CycleGAN", "Unpaired image-to-image translation: horses to zebras, summer to winter.", BOX_TEAL),
                ("Conditional GANs", "Feed the label in: generate 'a cat', not just 'an image'.", BOX_GREEN),
                ("Diffusion era", "Diffusion models largely replaced GANs for quality — GANs still win on single-step speed.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in variants:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "GANs — Remember",
                 ["Generator forges, discriminator detects: a minimax game toward indistinguishability.",
                  "Train by alternating updates; keep the two networks balanced.",
                  "Mode collapse = one repeated output; watch diversity metrics, not just loss.",
                  "Evaluate with FID + precision/recall + human fool rates.",
                  "StyleGAN/CycleGAN/conditional variants; diffusion now leads on quality, GANs on speed."],
                 pg)
    c.save(); print("wrote", path)


def pdf_rl(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Reinforcement Learning\nVisual Guide",
               "Learning by doing:\nagents, rewards, Q-learning, policy gradients.",
               "Machine Learning", None); pg += 1

    y = section_header(c, 1, 6, "The Agent-Environment Loop",
                       "Act, observe, get rewarded, repeat.")
    box(c, 196, 480, 220, 80, BOX_BLUE, "Agent", "the decision maker")
    box(c, 196, 350, 220, 80, BOX_GREEN, "Environment", "the world")
    arrow(c, 280, 478, 280, 432, color=ACCENT, width=2.5, label="action")
    arrow(c, 352, 432, 352, 478, color=GREEN, width=2.5, label="state + reward")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 300, "At each step the agent sees a state, takes an action, and receives a reward. Goal: maximize total reward.")
    note(c, 72, 200, 468, "No labeled data — the reward signal IS the supervision. Sparse or delayed rewards make RL hard.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Rewards and Returns",
                       "Not just now — the whole future, discounted.")
    box(c, 72, 480, 140, 80, BOX_ORANGE, "Reward r(t)", "immediate")
    box(c, 256, 480, 140, 80, BOX_TEAL, "Return G(t)", "sum of future")
    box(c, 430, 470, 110, 90, BOX_PURP, "Discount", "gamma < 1:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(276, 500, "rewards, discounted.")
    c.drawString(450, 510, "future rewards")
    c.drawString(450, 496, "worth less.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "G(t) = r(t) + gamma*r(t+1) + gamma^2*r(t+2) + ... — discounting prefers sooner rewards and bounds infinity.")
    note(c, 72, 300, 468, "Reward shaping (small hints along the way) speeds learning — but a misshaped reward teaches the wrong behavior.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Exploration vs Exploitation",
                       "Try new things, or milk what works?")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Explore", "random actions:")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Exploit", "best known action:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "discover better")
    c.drawString(92, 501, "strategies.")
    c.drawString(340, 515, "collect reliable")
    c.drawString(340, 501, "reward.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Epsilon-greedy: act randomly with probability epsilon, greedily otherwise. Decay epsilon over training.")
    note(c, 72, 300, 468, "Too much exploration never converges; too little gets stuck in a local optimum. The central tension of RL.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Q-Learning",
                       "Learn the value of every action in every state.")
    box(c, 72, 480, 220, 70, BOX_BLUE, "Q(s, a)", "expected future reward")
    box(c, 320, 480, 220, 70, BOX_GREEN, "Policy", "pick argmax Q")
    arrow(c, 292, 515, 318, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Update: Q(s,a) += alpha * [r + gamma*max Q(s',a') - Q(s,a)]. Bootstrap from your own estimates.")
    note(c, 72, 300, 468, "Deep Q-Networks replace the table with a neural net. Use a frozen target network and experience replay for stability.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Policy Gradients",
                       "Optimize the policy directly.")
    box(c, 72, 480, 140, 80, BOX_PURP, "Policy net", "state -> action")
    box(c, 256, 480, 140, 80, BOX_ORANGE, "Rollout", "collect episodes")
    box(c, 430, 470, 110, 90, BOX_GREEN, "Reinforce", "upweight winners")
    arrow(c, 212, 520, 254, 520, color=ACCENT, width=2)
    arrow(c, 396, 520, 428, 520, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Increase the probability of actions that led to high reward. REINFORCE, PPO, and actor-critic refine this idea.")
    note(c, 72, 300, 468, "PPO (clipped updates) is the workhorse — including inside RLHF for language models.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "RL in Practice",
                       "Where it shines — and what to watch.")
    yy = bullet_list(c, 72, y,
        ["Games and robotics: simulators give unlimited cheap episodes — the ideal RL setting.",
         "RLHF: human preference becomes the reward; PPO/DPO aligns language models.",
         "Sample inefficiency is the tax: millions of episodes for what a human learns in minutes.",
         "Always try supervised or imitation learning first — reach for RL when no labels exist.",
         "Evaluate on held-out environments: RL agents overfit to their simulators."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Reinforcement Learning — Remember",
                 ["Agent acts, environment returns state + reward; maximize discounted return.",
                  "Discount factor gamma trades off immediate vs future reward.",
                  "Epsilon-greedy balances exploration (discover) vs exploitation (harvest).",
                  "Q-learning values state-action pairs; policy gradients optimize the policy directly (PPO).",
                  "RL needs simulators or cheap episodes; prefer imitation learning when labels exist."],
                 pg)
    c.save(); print("wrote", path)


def pdf_feature_engineering(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Feature Engineering\nVisual Guide",
               "The highest-ROI step in ML:\nencoding, scaling, selection, leakage traps.",
               "Machine Learning", None); pg += 1

    y = section_header(c, 1, 5, "Encoding Categoricals",
                       "Turn labels into numbers without inventing order.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "One-hot", "'red','blue' ->")
    box(c, 246, 470, 140, 80, BOX_TEAL, "Ordinal", "only if truly")
    box(c, 420, 470, 120, 80, BOX_GREEN, "Target", "mean target per")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "binary columns.")
    c.drawString(266, 500, "ordered: S<M<L.")
    c.drawString(440, 500, "category — with")
    c.drawString(440, 486, "cross-validation!")
    note(c, 72, 330, 468, "Label-encoding 'red'=1,'blue'=2' invents an order the model will believe. High-cardinality IDs? Hash them or embed them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Scaling",
                       "Put features on comparable footing.")
    box(c, 72, 470, 220, 90, BOX_ORANGE, "Standardize", "(x - mean) / std")
    box(c, 320, 470, 220, 90, BOX_TEAL, "Normalize", "(x - min) / (max - min)")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "zero mean, unit variance.")
    c.drawString(92, 501, "For gradient methods, SVMs.")
    c.drawString(340, 515, "range [0,1]. For neural")
    c.drawString(340, 501, "nets, kNN, images.")
    note(c, 72, 320, 468, "Fit scalers on TRAIN only, then apply to test — fitting on all data leaks test statistics into training.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Feature Selection",
                       "Fewer, better features beat more features.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "Filter", "correlation,")
    box(c, 246, 470, 140, 80, BOX_GREEN, "Wrapper", "search subsets,")
    box(c, 420, 470, 120, 80, BOX_PURP, "Embedded", "L1, tree")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "mutual info.")
    c.drawString(266, 500, "keep winners.")
    c.drawString(440, 500, "importance.")
    yy = bullet_list(c, 72, 380,
        ["Drop constant and near-constant features first — they carry no signal.",
         "Drop one of each highly-correlated pair; trees don't care, linear models do.",
         "L1 regularization selects features automatically during training."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Target Leakage Traps",
                       "The silent killer of ML projects.")
    box(c, 72, 470, 220, 90, BOX_RED, "Leak example", "'days_in_hospital'")
    box(c, 320, 470, 220, 90, BOX_RED, "Leak example", "'approved' flag in")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "predicting readmission —")
    c.drawString(92, 501, "known only AFTER.")
    c.drawString(340, 515, "loan data — recorded")
    c.drawString(340, 501, "after the decision.")
    note(c, 72, 320, 468, "Leakage test: could this feature exist at prediction time in production? If not, drop it. Great validation scores + leakage = worthless model.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Feature Engineering Workflow",
                       "A repeatable recipe.")
    yy = bullet_list(c, 72, y,
        ["Start with domain features: ratios, differences, and aggregates a human expert would check.",
         "Add time features: hour, weekday, days-since-event, rolling averages with proper cutoffs.",
         "Create interactions the model can't easily learn: price_per_sqft beats price + sqft for linear models.",
         "Build everything inside a pipeline (fit on train, transform both) so leakage can't creep in.",
         "Version features in a feature store — training/serving skew starts as a notebook shortcut."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Feature Engineering — Remember",
                 ["One-hot nominal categories; never invent order with label encoding.",
                  "Scale for gradient/kNN/neural models; fit scalers on train only.",
                  "Select features: drop constants, dedupe correlates, let L1 help.",
                  "Leakage = features unavailable at prediction time; it fakes great scores.",
                  "Pipelines + feature stores keep train/serve consistent and leakage out."],
                 pg)
    c.save(); print("wrote", path)


def pdf_model_serving(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Model Serving\nVisual Guide",
               "From trained model to production:\nbatch vs real-time, vLLM, batching, autoscaling.",
               "MLOps", None); pg += 1

    y = section_header(c, 1, 6, "Batch vs Real-time",
                       "Two serving patterns, different SLOs.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Batch", "score millions")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Real-time", "score one request")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "overnight. Throughput")
    c.drawString(92, 501, "matters; latency doesn't.")
    c.drawString(340, 515, "in milliseconds. Latency")
    c.drawString(340, 501, "SLOs dominate.")
    note(c, 72, 320, 468, "Default to batch when the decision isn't needed instantly — it is 10-100x cheaper per prediction.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Model Servers",
                       "Purpose-built inference runtimes.")
    srvs = [("NVIDIA Triton", "Multi-framework server: TensorRT, ONNX, PyTorch — dynamic batching built in.", BOX_BLUE),
            ("vLLM", "The LLM server: PagedAttention + continuous batching for high-throughput generation.", BOX_GREEN),
            ("ONNX / TensorRT", "Optimized runtimes: graph fusion and kernel autotuning cut latency sharply.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in srvs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Don't serve from a Flask app wrapping torch.load — you lose batching, caching, and GPU utilization.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Continuous Batching",
                       "The trick behind fast LLM APIs.")
    box(c, 72, 500, 110, 60, BOX_BLUE, "req A", "")
    box(c, 206, 500, 110, 60, BOX_BLUE, "req B", "")
    box(c, 340, 500, 110, 60, BOX_BLUE, "req C", "")
    box(c, 196, 380, 220, 70, BOX_GREEN, "One GPU batch", "mixed requests, one pass")
    arrow(c, 127, 498, 220, 452, color=ACCENT, width=1.5)
    arrow(c, 261, 498, 280, 452, color=ACCENT, width=1.5)
    arrow(c, 395, 498, 392, 452, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 330, "Requests join and leave the batch token-by-token — no waiting for the slowest request to finish.")
    note(c, 72, 220, 468, "Static batching wastes GPU on padding and stragglers. Continuous batching keeps utilization near 100%.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "The KV Cache",
                       "Why the first token is slow and the rest are fast.")
    box(c, 72, 470, 220, 90, BOX_ORANGE, "Prefill", "process the whole prompt:")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Decode", "one token at a time,")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "compute-bound, caches")
    c.drawString(92, 501, "keys and values.")
    c.drawString(340, 515, "reading the cache —")
    c.drawString(340, 501, "memory-bandwidth bound.")
    note(c, 72, 320, 468, "Long contexts explode KV-cache memory. PagedAttention (vLLM) manages it like OS virtual memory.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Autoscaling Inference",
                       "Scale on the right signal.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Metrics", "queue depth,")
    box(c, 256, 480, 140, 70, BOX_ORANGE, "Scaler", "add/remove")
    box(c, 430, 470, 110, 80, BOX_GREEN, "Replicas", "GPU pods")
    arrow(c, 212, 515, 254, 515, color=ACCENT, width=2)
    arrow(c, 396, 515, 428, 515, color=ACCENT, width=2)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "p99 latency.")
    c.drawString(276, 500, "replicas.")
    note(c, 72, 330, 468, "GPU cold starts take minutes — keep a warm minimum and scale on queue depth, not CPU.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Latency vs Throughput",
                       "You can usually have one.")
    yy = bullet_list(c, 72, y,
        ["Latency: time per request. Throughput: requests per second. Batching trades the first for the second.",
         "Quantization (FP16/INT8) cuts both latency and memory — nearly free speedup for inference.",
         "Speculative decoding: a small model drafts, the big model verifies — faster without quality loss.",
         "Set SLOs first (p99 < 200ms?), then choose batching, precision, and replicas to meet them."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Model Serving — Remember",
                 ["Batch when you can (cheap); serve real-time only when latency SLOs demand it.",
                  "Use a real inference server (Triton, vLLM) — not a bare web framework.",
                  "Continuous batching + PagedAttention unlock high-throughput LLM serving.",
                  "KV cache makes decode memory-bound; long contexts need cache management.",
                  "Autoscale on queue depth/latency with warm minimums; quantize for free speed."],
                 pg)
    c.save(); print("wrote", path)


def pdf_mlops(path):
    c = new_canvas(path); pg = 1
    title_page(c, "MLOps\nVisual Guide",
               "Operating ML in production:\ntracking, registry, CI/CD, feature stores.",
               "MLOps", None); pg += 1

    y = section_header(c, 1, 6, "Experiment Tracking",
                       "Every run recorded, comparable, reproducible.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "Params", "lr, depth, seed")
    box(c, 246, 470, 140, 80, BOX_GREEN, "Metrics", "loss, F1, AUC")
    box(c, 420, 470, 120, 80, BOX_PURP, "Artifacts", "models, plots")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "MLflow / Weights & Biases: log everything per run. 'Best model' must be a query, not a memory.")
    note(c, 72, 300, 468, "Log the git hash, data version, and environment with every run — otherwise results aren't reproducible.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Model Registry",
                       "From experiment to governed artifact.")
    box(c, 72, 470, 130, 80, BOX_ORANGE, "Staging", "candidate")
    box(c, 246, 470, 130, 80, BOX_BLUE, "Production", "live model")
    box(c, 420, 470, 120, 80, BOX_RED, "Archived", "retired")
    arrow(c, 202, 510, 244, 510, color=ACCENT, width=2.5)
    arrow(c, 376, 510, 418, 510, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Promotion is a gated decision: champion/challenger tests, sign-offs, and automatic rollback on regression.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "CI/CD for ML",
                       "Test the pipeline, not just the code.")
    box(c, 72, 480, 120, 70, BOX_BLUE, "Train", "on commit")
    box(c, 226, 480, 120, 70, BOX_ORANGE, "Evaluate", "vs baseline")
    box(c, 380, 480, 120, 70, BOX_GREEN, "Deploy", "if better")
    arrow(c, 192, 515, 224, 515, color=ACCENT, width=2.5)
    arrow(c, 346, 515, 378, 515, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Unit-test data schemas and feature code; integration-test the training pipeline on a data sample.")
    note(c, 72, 300, 468, "ML CI is slower than software CI — cache datasets and use small representative samples for fast feedback.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Feature Stores",
                       "One definition of each feature, everywhere.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Offline store", "training: point-in-")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Online store", "serving: low-latency")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "time-correct joins for")
    c.drawString(92, 501, "training sets.")
    c.drawString(340, 515, "lookups for live")
    c.drawString(340, 501, "predictions.")
    note(c, 72, 320, 468, "Training/serving skew — features computed differently in prod — is a top silent model killer. Feature stores prevent it.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Data in the Pipeline",
                       "Models are downstream of data.")
    box(c, 72, 480, 140, 70, BOX_TEAL, "Versioned data", "DVC / LakeFS")
    box(c, 256, 480, 140, 70, BOX_BLUE, "Validated", "schema + drift")
    box(c, 430, 470, 110, 80, BOX_PURP, "Lineage", "data -> model")
    arrow(c, 212, 515, 254, 515, color=ACCENT, width=2)
    arrow(c, 396, 515, 428, 515, color=ACCENT, width=2)
    note(c, 72, 330, 468, "Every training run must record exactly which data snapshot it used — 'the latest CSV' is not a version.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The MLOps Loop",
                       "Monitor, trigger, retrain, redeploy.")
    box(c, 196, 500, 220, 60, BOX_GREEN, "Serve & monitor", "metrics, drift")
    box(c, 196, 400, 220, 60, BOX_BLUE, "Retrain", "on trigger")
    arrow(c, 306, 498, 306, 462, color=ACCENT, width=2.5)
    arrow(c, 196, 430, 130, 430, color=ACCENT, width=2)
    arrow(c, 130, 430, 130, 530, color=ACCENT, width=2)
    arrow(c, 130, 530, 194, 530, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 350, "Retraining triggers: schedule, drift detection, or performance decay — never 'vibes'.")
    note(c, 72, 240, 468, "Close the loop with automated rollback: a worse challenger must never silently become champion.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "MLOps — Remember",
                 ["Track every experiment: params, metrics, artifacts, git hash, data version.",
                  "The registry governs promotion: staging -> production -> archived, with gates.",
                  "CI/CD for ML tests data and pipelines, not just code.",
                  "Feature stores kill training/serving skew with one feature definition.",
                  "Monitor in prod; retrain on triggers; roll back automatically on regression."],
                 pg)
    c.save(); print("wrote", path)


def pdf_data_versioning(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Data Versioning\nVisual Guide",
               "Reproducible ML starts with data:\nDVC, LakeFS, snapshots, lineage.",
               "MLOps", None); pg += 1

    y = section_header(c, 1, 5, "Why Version Data",
                       "Code versioning alone can't reproduce a model.")
    box(c, 72, 470, 220, 90, BOX_RED, "Without", "'train.csv' changed")
    box(c, 320, 470, 220, 90, BOX_GREEN, "With", "data@a3f9c1 ->")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "under you. Results")
    c.drawString(92, 501, "unreproducible.")
    c.drawString(340, 515, "model v2.1. Exact")
    c.drawString(340, 501, "snapshot, every time.")
    note(c, 72, 320, 468, "The number-one reproducibility failure: the same code, 'the same data', different results — because the data wasn't the same.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "The DVC Model",
                       "Git for code, pointers for data.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Git repo", "code + .dvc")
    box(c, 256, 480, 140, 70, BOX_TEAL, "Pointer", "hash of data")
    box(c, 430, 470, 110, 80, BOX_GREEN, "Remote", "S3 / GCS data")
    arrow(c, 212, 515, 254, 515, color=ACCENT, width=2)
    arrow(c, 396, 515, 428, 515, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "DVC stores tiny pointer files in git; the bytes live in remote storage, fetched by hash on demand.")
    note(c, 72, 300, 468, "Checking out a commit checks out the data pointer too — code and data stay in lockstep.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "LakeFS: Git for Data Lakes",
                       "Branches and merges, but for datasets.")
    box(c, 72, 470, 140, 80, BOX_BLUE, "main", "production data")
    box(c, 246, 470, 140, 80, BOX_ORANGE, "experiment", "branch: try a")
    box(c, 420, 470, 120, 80, BOX_GREEN, "merge", "promote the")
    arrow(c, 212, 510, 244, 510, color=ACCENT, width=2)
    arrow(c, 386, 510, 418, 510, color=ACCENT, width=2)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(266, 500, "new labeling.")
    c.drawString(440, 500, "winner.")
    note(c, 72, 330, 468, "Zero-copy branches: experimenting on a data branch doesn't duplicate terabytes — until you commit changes.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "The Reproducibility Recipe",
                       "Four ingredients, all pinned.")
    ings = [("Code", "git commit hash", BOX_BLUE),
            ("Data", "snapshot hash / version", BOX_TEAL),
            ("Environment", "container image + lockfile", BOX_ORANGE),
            ("Config", "hyperparams + seeds", BOX_PURP)]
    yy = y
    for name, desc, fill in ings:
        box(c, 72, yy - 46, 468, 50, fill, name, desc, font_size=11)
        yy -= 62
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, yy - 10, "Miss one ingredient and the result is folklore, not science.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Data Lineage",
                       "Trace every model back to its raw sources.")
    box(c, 72, 500, 120, 60, BOX_TEAL, "Raw sources", "")
    box(c, 236, 500, 120, 60, BOX_BLUE, "Cleaned", "")
    box(c, 400, 500, 120, 60, BOX_GREEN, "Features", "")
    box(c, 236, 390, 140, 60, BOX_PURP, "Model v2.1", "")
    arrow(c, 192, 530, 234, 530, color=ACCENT, width=1.5)
    arrow(c, 356, 530, 398, 530, color=ACCENT, width=1.5)
    arrow(c, 306, 498, 306, 452, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "Lineage answers: which data trained this model? A bad upstream fix becomes a targeted retrain, not a panic.")
    note(c, 72, 230, 468, "Regulators increasingly demand lineage for high-stakes models. Build it before you're asked.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Data Versioning — Remember",
                 ["Version data alongside code, or results aren't reproducible.",
                  "DVC: git pointers + content-addressed remote storage.",
                  "LakeFS: branch/merge workflows for data lakes, zero-copy branches.",
                  "Reproducibility = pinned code + data + environment + config.",
                  "Lineage traces models to sources — essential for debugging and compliance."],
                 pg)
    c.save(); print("wrote", path)


def pdf_model_drift(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Model Monitoring & Drift\nVisual Guide",
               "Catching decay before users do:\ndata drift, concept drift, PSI/KS, retraining triggers.",
               "MLOps", None); pg += 1

    y = section_header(c, 1, 5, "Two Kinds of Drift",
                       "Inputs shift, or the world changes meaning.")
    box(c, 72, 470, 220, 90, BOX_ORANGE, "Data drift", "P(X) changes:")
    box(c, 320, 470, 220, 90, BOX_RED, "Concept drift", "P(y|X) changes:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "customers get younger,")
    c.drawString(92, 501, "sensors recalibrated.")
    c.drawString(340, 515, "what 'fraud' means")
    c.drawString(340, 501, "evolves over time.")
    note(c, 72, 320, 468, "Data drift is detectable without labels. Concept drift needs ground truth — the harder, more dangerous kind.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Detecting Drift",
                       "Compare live distributions to training.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "PSI", "Population Stability")
    box(c, 320, 470, 220, 90, BOX_TEAL, "KS test", "Kolmogorov-Smirnov:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "Index: binned distance")
    c.drawString(92, 501, "between distributions.")
    c.drawString(340, 515, "max gap between CDFs;")
    c.drawString(340, 501, "p-value for 'same?'.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "PSI > 0.25 or KS p < 0.05 on key features = investigate. Track per-feature, not just globally.")
    note(c, 72, 300, 468, "Monitor the features the model actually depends on (top SHAP features) — drift elsewhere may not matter.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Label-Free Monitoring",
                       "Watch the model when ground truth is slow.")
    yy = bullet_list(c, 72, y,
        ["Prediction distribution: a fraud model suddenly approving 40% more transactions is screaming.",
         "Confidence/entropy: rising uncertainty often precedes accuracy drops.",
         "Input schema checks: new categories, null spikes, unit changes — catch pipeline breaks first.",
         "Shadow labels: sample predictions for human review weekly to estimate true accuracy cheaply."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "Labels can lag by weeks (did the loan default?). Label-free signals are your early warning system.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Retraining Triggers",
                       "Decide in advance when to retrain.")
    trigs = [("Schedule", "Retrain weekly/monthly — simple, predictable, sometimes wasteful.", BOX_BLUE),
             ("Drift threshold", "PSI breach on key features fires a retraining pipeline automatically.", BOX_ORANGE),
             ("Performance decay", "Live accuracy / business KPI drops below the agreed floor.", BOX_RED),
             ("Data event", "New product launch, regulation change, or upstream schema migration.", BOX_TEAL)]
    yy = y
    for name, desc, fill in trigs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "The Drift Response Playbook",
                       "From alert to action.")
    yy = bullet_list(c, 72, y,
        ["1. Triage: is it a pipeline bug (null spike) or real drift? Check data quality first.",
         "2. Scope: which features drifted, and does the model depend on them?",
         "3. Decide: retrain on recent data, reweight, or fix the upstream source.",
         "4. Validate the challenger against the champion on recent labeled data before promoting.",
         "5. Post-mortem: log the drift event — patterns across incidents reveal systemic issues."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Model Monitoring & Drift — Remember",
                 ["Data drift = inputs shift (detectable without labels); concept drift = meaning shifts (needs labels).",
                  "PSI and KS tests compare live vs training distributions per feature.",
                  "Monitor prediction distributions and confidence when labels lag.",
                  "Set retraining triggers in advance: schedule, drift threshold, or performance floor.",
                  "Triage pipeline bugs first; validate challengers before promoting."],
                 pg)
    c.save(); print("wrote", path)


def pdf_quantization(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Quantization & Pruning\nVisual Guide",
               "Smaller, faster models:\nINT8/FP16, PTQ vs QAT, pruning, distillation, edge.",
               "ML Optimization", None); pg += 1

    y = section_header(c, 1, 6, "The Precision Ladder",
                       "Fewer bits per weight: smaller, faster, nearly as good.")
    box(c, 72, 470, 130, 80, BOX_BLUE, "FP32", "4 bytes:")
    box(c, 236, 470, 130, 80, BOX_TEAL, "FP16", "2 bytes:")
    box(c, 400, 470, 140, 80, BOX_GREEN, "INT8", "1 byte:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "training default.")
    c.drawString(256, 500, "2x smaller, 2x")
    c.drawString(256, 486, "faster on GPUs.")
    c.drawString(420, 500, "4x smaller, integer")
    c.drawString(420, 486, "math on edge chips.")
    arrow(c, 202, 510, 234, 510, color=ACCENT, width=2)
    arrow(c, 366, 510, 398, 510, color=ACCENT, width=2)
    note(c, 72, 330, 468, "Memory bandwidth — not FLOPs — usually limits inference. Halving precision roughly doubles speed.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "PTQ vs QAT",
                       "Quantize after training, or train quantization-aware.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "PTQ", "post-training: quantize")
    box(c, 320, 470, 220, 90, BOX_ORANGE, "QAT", "quantization-aware:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "a finished model with")
    c.drawString(92, 501, "calibration data. Fast.")
    c.drawString(340, 515, "simulate quantization")
    c.drawString(340, 501, "during training. Slower, better.")
    note(c, 72, 320, 468, "Start with PTQ — it recovers most of the accuracy for free. Reach for QAT when PTQ degrades quality.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Magnitude Pruning",
                       "Delete the weights that matter least.")
    box(c, 72, 500, 130, 70, BOX_BLUE, "Dense", "all weights")
    box(c, 246, 500, 130, 70, BOX_ORANGE, "Prune", "zero the smallest")
    box(c, 420, 500, 120, 70, BOX_GREEN, "Sparse", "50-90% zeros")
    arrow(c, 202, 535, 244, 535, color=ACCENT, width=2)
    arrow(c, 376, 535, 418, 535, color=ACCENT, width=2)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(266, 530, "magnitudes.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "Iterative prune-and-fine-tune beats one-shot pruning. Unstructured sparsity needs special kernels to pay off.")
    note(c, 72, 320, 468, "Structured pruning (whole channels/filters) gives real speedups on standard hardware; unstructured needs sparse libraries.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Knowledge Distillation",
                       "A small student learns from a big teacher.")
    box(c, 72, 470, 200, 90, BOX_PURP, "Teacher", "large, accurate, slow")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Student", "small, fast — trained")
    arrow(c, 272, 515, 318, 515, color=ACCENT, width=2.5, label="soft targets")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(340, 515, "on teacher's soft")
    c.drawString(340, 501, "probabilities, not hard labels.")
    note(c, 72, 320, 468, "Soft targets carry 'dark knowledge' — which wrong answers were almost right. Students often beat same-size models trained from scratch.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Edge Deployment Stack",
                       "From cloud model to on-device.")
    box(c, 72, 480, 130, 70, BOX_BLUE, "Quantize", "INT8 / FP16")
    box(c, 246, 480, 130, 70, BOX_ORANGE, "Compile", "TFLite, ONNX,")
    box(c, 420, 480, 120, 70, BOX_GREEN, "Deploy", "phone, camera,")
    arrow(c, 202, 515, 244, 515, color=ACCENT, width=2)
    arrow(c, 376, 515, 418, 515, color=ACCENT, width=2)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(266, 500, "CoreML, TensorRT.")
    c.drawString(440, 500, "sensor.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Measure on the actual device — desktop benchmarks lie about mobile NPUs and DSPs.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The Accuracy Tradeoff",
                       "How much quality does compression cost?")
    yy = bullet_list(c, 72, y,
        ["FP16: essentially free — do it always for inference.",
         "INT8 PTQ: usually <1% accuracy loss on vision and many NLP tasks.",
         "Aggressive pruning/distillation: expect 1-3% loss; validate on YOUR data, not the paper's.",
         "Combine techniques: distill, then quantize — the gains stack.",
         "Always keep the full-precision model as the reference for regression tests."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Quantization & Pruning — Remember",
                 ["FP16 is free; INT8 gives 4x compression with tiny accuracy cost.",
                  "PTQ first (fast); QAT when PTQ isn't enough.",
                  "Prune small magnitudes iteratively; prefer structured pruning for real speedups.",
                  "Distillation transfers dark knowledge from teacher soft targets to a small student.",
                  "Measure on the target device; keep full-precision as the regression reference."],
                 pg)
    c.save(); print("wrote", path)


def pdf_distributed_training(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Distributed Training\nVisual Guide",
               "Training across many GPUs:\ndata parallelism, all-reduce, ZeRO, pipeline parallelism.",
               "ML Systems", None); pg += 1

    y = section_header(c, 1, 5, "Data Parallelism",
                       "Same model, different data, on every GPU.")
    box(c, 72, 500, 120, 60, BOX_BLUE, "GPU 0", "batch shard")
    box(c, 226, 500, 120, 60, BOX_BLUE, "GPU 1", "batch shard")
    box(c, 380, 500, 120, 60, BOX_BLUE, "GPU 2", "batch shard")
    box(c, 196, 380, 220, 64, BOX_GREEN, "Average gradients", "all-reduce")
    arrow(c, 132, 498, 240, 446, color=ACCENT, width=1.5)
    arrow(c, 286, 498, 286, 446, color=ACCENT, width=1.5)
    arrow(c, 440, 498, 392, 446, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 330, "Each GPU computes gradients on its shard; gradients are averaged; every replica applies the same update.")
    note(c, 72, 220, 468, "The default strategy. Effective batch size = per-GPU batch x GPU count — scale the learning rate accordingly.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "All-Reduce",
                       "Every GPU ends up with the same averaged gradient.")
    box(c, 72, 480, 120, 70, BOX_BLUE, "GPU 0", "grad g0")
    box(c, 226, 480, 120, 70, BOX_BLUE, "GPU 1", "grad g1")
    box(c, 380, 480, 120, 70, BOX_BLUE, "GPU 2", "grad g2")
    box(c, 196, 370, 220, 60, BOX_GREEN, "g = mean(g0, g1, g2)", "on every GPU")
    arrow(c, 306, 478, 306, 432, color=GREEN, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 320, "Ring all-reduce: each GPU exchanges chunks with neighbors — bandwidth-optimal, no central bottleneck.")
    note(c, 72, 220, 468, "Communication overlaps with backward-pass computation (gradient bucketing) so GPUs rarely sit idle.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Model & Pipeline Parallelism",
                       "Split the MODEL when it doesn't fit on one GPU.")
    box(c, 72, 470, 220, 90, BOX_PURP, "Model parallel", "layers split across")
    box(c, 320, 470, 220, 90, BOX_TEAL, "Pipeline parallel", "stages process")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "GPUs; activations")
    c.drawString(92, 501, "flow between them.")
    c.drawString(340, 515, "micro-batches in a")
    c.drawString(340, 501, "pipeline; some idle bubbles.")
    note(c, 72, 320, 468, "Pipeline bubbles waste compute — interleaved schedules and more micro-batches shrink them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "ZeRO: Sharding the Optimizer",
                       "The optimizer states are the real memory hog.")
    box(c, 72, 470, 140, 80, BOX_RED, "Problem", "Adam states = 2x")
    box(c, 246, 470, 140, 80, BOX_GREEN, "ZeRO-1/2/3", "shard optimizer,")
    box(c, 420, 470, 120, 80, BOX_BLUE, "Result", "train 10x")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "model size in FP32.")
    c.drawString(266, 500, "gradients, params")
    c.drawString(266, 486, "across GPUs.")
    c.drawString(440, 500, "bigger models.")
    note(c, 72, 330, 468, "ZeRO-3 shards everything; each GPU gathers what it needs just in time. The enabler of hundred-billion-param training.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Choosing a Strategy",
                       "Match the parallelism to the bottleneck.")
    yy = bullet_list(c, 72, y,
        ["Model fits on one GPU? Data parallelism (+ larger batches) is all you need.",
         "Optimizer memory explodes? Add ZeRO-1/2 — nearly free with data parallelism.",
         "Model doesn't fit at all? ZeRO-3, or tensor/pipeline parallelism for the biggest models.",
         "Network slow? Gradient compression and accumulation cut communication.",
         "Profile first: the bottleneck is usually memory, communication, or data loading — in that order."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Distributed Training — Remember",
                 ["Data parallelism: replicate the model, shard the data, average gradients.",
                  "Ring all-reduce synchronizes gradients with no central bottleneck.",
                  "Model/pipeline parallelism splits layers across GPUs when one GPU can't hold the model.",
                  "ZeRO shards optimizer states (and more) to train far bigger models.",
                  "Choose by bottleneck: fit -> data parallel; memory -> ZeRO; huge -> pipeline."],
                 pg)
    c.save(); print("wrote", path)


def pdf_federated(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Federated Learning\nVisual Guide",
               "Training without collecting data:\nrounds, secure aggregation, non-IID challenges.",
               "ML Systems", None); pg += 1

    y = section_header(c, 1, 5, "Federated Rounds",
                       "The model travels; the data stays home.")
    box(c, 196, 520, 220, 60, BOX_BLUE, "Server", "holds global model")
    box(c, 72, 400, 120, 60, BOX_GREEN, "Phone A", "trains locally")
    box(c, 246, 400, 120, 60, BOX_GREEN, "Phone B", "trains locally")
    box(c, 420, 400, 120, 60, BOX_GREEN, "Phone C", "trains locally")
    arrow(c, 280, 518, 132, 462, color=ACCENT, width=1.5)
    arrow(c, 306, 518, 306, 462, color=ACCENT, width=1.5)
    arrow(c, 352, 518, 480, 462, color=ACCENT, width=1.5)
    arrow(c, 160, 430, 260, 500, color=GREEN, width=1.5)
    arrow(c, 340, 430, 320, 500, color=GREEN, width=1.5)
    arrow(c, 480, 430, 380, 500, color=GREEN, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 350, "Round: server sends model -> devices train on local data -> server averages updates (FedAvg) -> repeat.")
    note(c, 72, 230, 468, "Raw data never leaves the device. Only model updates travel — the core privacy promise.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Secure Aggregation",
                       "The server learns the sum, never the parts.")
    box(c, 72, 470, 140, 80, BOX_GREEN, "Masked update", "update + random")
    box(c, 246, 470, 140, 80, BOX_GREEN, "Masked update", "masks cancel in")
    box(c, 420, 470, 120, 80, BOX_BLUE, "Server", "sees only the")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "mask.")
    c.drawString(266, 500, "aggregation.")
    c.drawString(440, 500, "total.")
    note(c, 72, 330, 468, "Cryptographic masking means even a curious server can't reconstruct any single device's update.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "The Non-IID Challenge",
                       "Every device's data looks different.")
    box(c, 72, 470, 220, 90, BOX_RED, "Non-IID reality", "one user types in")
    box(c, 320, 470, 220, 90, BOX_ORANGE, "IID fantasy", "every device sees")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "Spanish, another in")
    c.drawString(92, 501, "emoji. Skewed labels.")
    c.drawString(340, 515, "the same distribution.")
    c.drawString(340, 501, "Algorithms assume this.")
    note(c, 72, 320, 468, "Non-IID data slows convergence and can diverge FedAvg. Fixes: proximal terms (FedProx), personalization layers, more rounds.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Privacy Techniques",
                       "Defense in depth for updates.")
    yy = bullet_list(c, 72, y,
        ["Differential privacy: add calibrated noise to updates so no single user is identifiable.",
         "Secure aggregation: cryptography hides individual updates from the server.",
         "Update clipping: bound each device's influence — also blunts poisoning attacks.",
         "On-device personalization: keep a private head locally; share only the base model."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "Model updates can leak training data (inversion attacks) — 'we never saw the data' is not the whole story.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "When Federated Fits",
                       "The right tool for sensitive, distributed data.")
    yy = bullet_list(c, 72, y,
        ["Keyboards, voice assistants, health apps: data users won't (or can't) upload.",
         "Hospitals collaborating without sharing patient records across institutions.",
         "Requirements: many clients, intermittent connectivity, tolerance for slow convergence.",
         "Skip it when data CAN be centralized — federated is always harder than centralized training.",
         "Watch for: stragglers, dropped devices, and adversarial clients poisoning the global model."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Federated Learning — Remember",
                 ["Federated rounds: server broadcasts model, devices train locally, server averages (FedAvg).",
                  "Data stays on device; only updates travel — with secure aggregation hiding individuals.",
                  "Non-IID data is the core challenge: skewed clients slow or break convergence.",
                  "Add differential privacy and clipping; updates can leak data without them.",
                  "Use when data can't be centralized; prefer centralized training otherwise."],
                 pg)
    c.save(); print("wrote", path)


def pdf_xai(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Explainable AI\nVisual Guide",
               "Opening the black box:\nSHAP, LIME, saliency maps — and their limits.",
               "Responsible AI", None); pg += 1

    y = section_header(c, 1, 5, "Global vs Local Explanations",
                       "Two questions, two tool families.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Global", "'what does the model")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Local", "'why THIS prediction")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "rely on overall?' —")
    c.drawString(92, 501, "feature importance.")
    c.drawString(340, 515, "for THIS input?' —")
    c.drawString(340, 501, "per-decision reasons.")
    note(c, 72, 320, 468, "Global explanations audit the model; local explanations justify individual decisions. You usually need both.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "SHAP Values",
                       "Fair credit assignment from game theory.")
    box(c, 72, 500, 130, 70, BOX_BLUE, "income +", "pushes approval")
    box(c, 216, 500, 130, 70, BOX_RED, "debt -", "pushes denial")
    box(c, 360, 500, 130, 70, BOX_ORANGE, "age ~", "neutral")
    box(c, 196, 390, 220, 64, BOX_PURP, "Sum = prediction", "additive explanation")
    arrow(c, 306, 498, 306, 456, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "Each feature gets a Shapley value: its marginal contribution averaged over all feature orderings.")
    note(c, 72, 230, 468, "SHAP is consistent and theoretically grounded — but expensive on large models; use sampling or tree-specific fast paths.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "LIME",
                       "Explain locally with a simple surrogate.")
    box(c, 72, 480, 140, 70, BOX_PURP, "Complex model", "black box")
    box(c, 256, 480, 140, 70, BOX_ORANGE, "Perturb", "tweak the input,")
    box(c, 430, 470, 110, 80, BOX_GREEN, "Simple model", "linear fit on")
    arrow(c, 212, 515, 254, 515, color=ACCENT, width=2)
    arrow(c, 396, 515, 428, 515, color=ACCENT, width=2)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(276, 500, "watch outputs.")
    c.drawString(450, 510, "neighbors.")
    note(c, 72, 330, 468, "LIME fits an interpretable model on perturbed samples near the input. Fast and model-agnostic — but sampling noise makes explanations jittery.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Saliency and Attention Maps",
                       "Show WHERE the model looked.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Saliency", "gradient of output")
    box(c, 320, 470, 220, 90, BOX_TEAL, "Attention", "weight heatmaps in")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "w.r.t. input pixels —")
    c.drawString(92, 501, "highlights influential regions.")
    c.drawString(340, 515, "transformers — which")
    c.drawString(340, 501, "tokens the model used.")
    note(c, 72, 320, 468, "Great for debugging ('the model looked at the watermark, not the tumor'). Smooth with Grad-CAM or integrated gradients for stability.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "When Explanations Mislead",
                       "Explanations are models too — they can be wrong.")
    yy = bullet_list(c, 72, y,
        ["Attention is not explanation: high weight does not prove the token caused the output.",
         "Surrogates approximate: LIME/SHAP explain the neighborhood, not the true decision boundary.",
         "Explanations can be gamed: adversarial models can hide bias while producing innocent-looking SHAP plots.",
         "Confirmation bias: humans accept explanations that match their priors and ignore the rest.",
         "Use explanations to generate hypotheses, then verify with ablations and counterfactuals."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Explainable AI — Remember",
                 ["Global explanations audit the model; local ones justify single decisions.",
                  "SHAP gives principled additive credit per feature; LIME fits local surrogates fast.",
                  "Saliency/attention maps show where the model looked — great for debugging.",
                  "Explanations can mislead: attention isn't proof, surrogates approximate, plots can be gamed.",
                  "Treat explanations as hypotheses; verify with ablations and counterfactuals."],
                 pg)
    c.save(); print("wrote", path)


def pdf_fairness(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Bias & Fairness\nVisual Guide",
               "Measuring and mitigating unfairness:\nmetrics, sources, and fixes across the pipeline.",
               "Responsible AI", None); pg += 1

    y = section_header(c, 1, 5, "Fairness Metrics",
                       "Different definitions — pick deliberately.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Demographic parity", "equal approval rates")
    box(c, 320, 470, 220, 90, BOX_GREEN, "Equalized odds", "equal true/false")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "across groups.")
    c.drawString(92, 501, "Simple, often too strict.")
    c.drawString(340, 515, "positive rates across")
    c.drawString(340, 501, "groups. Respects base rates.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Impossibility result: you cannot satisfy all fairness definitions at once when base rates differ.")
    note(c, 72, 300, 468, "Choose the metric with stakeholders BEFORE modeling. The metric choice is a values decision, not a math one.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Sources of Bias",
                       "Bias enters long before the model.")
    srcs = [("Historical bias", "Training data reflects past discrimination (hiring, lending, policing).", BOX_RED),
            ("Representation bias", "Some groups are under-sampled; the model learns them poorly.", BOX_ORANGE),
            ("Measurement bias", "Proxies mismeasure: 'arrests' is not 'crime', 'clicks' is not 'satisfaction'.", BOX_BLUE),
            ("Deployment bias", "A fair model used in an unfair workflow still produces unfair outcomes.", BOX_PURP)]
    yy = y
    for name, desc, fill in srcs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Pre-processing Mitigation",
                       "Fix the data before training.")
    yy = bullet_list(c, 72, y,
        ["Reweighting: upweight underrepresented groups so the loss can't ignore them.",
         "Resampling: over/undersample to balance group representation in training.",
         "Disparate-impact remover: repair features to reduce group correlation while keeping rank order.",
         "Audit labels: have diverse reviewers check whether 'ground truth' encodes past bias."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "Pre-processing is model-agnostic — one fix benefits every model trained on the data.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "In-processing Mitigation",
                       "Build fairness into training.")
    box(c, 72, 470, 220, 90, BOX_PURP, "Fairness constraints", "optimize accuracy")
    box(c, 320, 470, 220, 90, BOX_TEAL, "Adversarial debiasing", "a second network")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "subject to a fairness")
    c.drawString(92, 501, "bound. Explicit tradeoff.")
    c.drawString(340, 515, "tries to predict the")
    c.drawString(340, 501, "protected attribute — penalize it.")
    note(c, 72, 320, 468, "Removing the protected column is NOT enough — proxies (zip code, name) carry the signal. Measure, don't assume.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Post-processing and Auditing",
                       "Fix decisions and keep watching.")
    yy = bullet_list(c, 72, y,
        ["Threshold tuning: set per-group decision thresholds to equalize the chosen metric.",
         "Reject option: route low-confidence, high-disparity cases to human review.",
         "Continuous auditing: recompute fairness metrics on live decisions — drift breaks fairness too.",
         "Document everything: model cards should state metrics, limitations, and intended use."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Bias & Fairness — Remember",
                 ["Pick a fairness metric deliberately — no model satisfies all definitions at once.",
                  "Bias sources: historical, representation, measurement, and deployment.",
                  "Mitigate at three stages: pre-process the data, constrain training, adjust decisions.",
                  "Dropping the protected attribute doesn't work — proxies leak it.",
                  "Audit continuously and document in model cards; fairness decays with drift."],
                 pg)
    c.save(); print("wrote", path)


def pdf_llm_eval(path):
    c = new_canvas(path); pg = 1
    title_page(c, "LLM Evaluation\nVisual Guide",
               "Proving a model works:\nbenchmarks, LLM judges, human eval, red teaming.",
               "LLM Engineering", None); pg += 1

    y = section_header(c, 1, 5, "Benchmarks",
                       "Standardized tests — with known limits.")
    bms = [("Knowledge: MMLU", "57 subjects, multiple choice — tests breadth of pretraining knowledge.", BOX_BLUE),
           ("Reasoning: GSM8K / MATH", "Grade-school to competition math — tests step-by-step reasoning.", BOX_GREEN),
           ("Code: HumanEval", "Write functions that pass hidden tests — tests practical coding.", BOX_ORANGE),
           ("Chat: MT-Bench / Arena", "Multi-turn quality judged comparatively — closest to real use.", BOX_PURP)]
    yy = y
    for name, desc, fill in bms:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Benchmarks saturate and leak into training data. They rank models; they don't certify YOUR use case.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "LLM-as-Judge",
                       "A strong model grades the weaker one.")
    box(c, 72, 480, 200, 70, BOX_BLUE, "Candidate answers", "A and B")
    box(c, 320, 480, 220, 70, BOX_PURP, "Judge model", "rubric + blind")
    arrow(c, 272, 515, 318, 515, color=ACCENT, width=2.5)
    box(c, 196, 370, 220, 64, BOX_GREEN, "Verdict + rationale", "'B wins: clearer steps'")
    arrow(c, 306, 478, 306, 436, color=GREEN, width=2.5)
    note(c, 72, 250, 468, "Calibrate the judge against humans first. Watch for position bias (prefers answer A) and verbosity bias (prefers longer).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Human Evaluation",
                       "The gold standard — expensive and slow.")
    yy = bullet_list(c, 72, y,
        ["Preference ranking: raters pick the better of two responses — simple, reliable, powers RLHF.",
         "Rubric scoring: rate helpfulness, accuracy, tone on 1-5 scales — more diagnostic.",
         "Inter-rater agreement (Cohen's kappa): low agreement means the task or rubric is underspecified.",
         "Blind the raters to which model produced what — branding bias is real.",
         "Use humans to calibrate automated evals, then scale with the automation."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Red Teaming",
                       "Adversarially probe for failures.")
    yy = bullet_list(c, 72, y,
        ["Jailbreaks: prompt-injection and roleplay attacks that bypass safety behavior.",
         "Harmful outputs: disallowed content, biased decisions, dangerous instructions.",
         "Hallucination probes: obscure facts and edge cases where the model confidently invents.",
         "Track attack success rate per category; fix, then re-attack — red teaming is iterative.",
         "Include domain experts: generic testers miss failures only practitioners would catch."],
        font_size=10.5, gap=30)
    note(c, 72, 150, 468, "Red team BEFORE launch, and after every major model or system-prompt change.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Eval Harnesses in CI",
                       "Evals as regression tests.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Prompt/model", "change")
    box(c, 256, 480, 140, 70, BOX_ORANGE, "Harness", "lm-eval-harness,")
    box(c, 430, 470, 110, 80, BOX_GREEN, "Gate", "block on")
    arrow(c, 212, 515, 254, 515, color=ACCENT, width=2)
    arrow(c, 396, 515, 428, 515, color=ACCENT, width=2)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(276, 500, "Ragas, custom.")
    c.drawString(450, 500, "regression.")
    note(c, 72, 330, 468, "Pin eval versions and seeds. A flaky eval suite teaches the team to ignore it.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "LLM Evaluation — Remember",
                 ["Benchmarks rank models but don't certify your use case; build task-specific evals.",
                  "LLM-as-judge scales grading — calibrate against humans and correct for biases.",
                  "Human eval is the gold standard: blind, rubric-driven, agreement-measured.",
                  "Red team adversarially and iteratively, with domain experts included.",
                  "Run evals in CI as regression gates on every prompt or model change."],
                 pg)
    c.save(); print("wrote", path)


def pdf_vector_db(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Vector Databases\nVisual Guide",
               "Search by meaning at scale:\nANN, HNSW, IVF, and vector DB architecture.",
               "LLM Engineering", None); pg += 1

    y = section_header(c, 1, 6, "The ANN Problem",
                       "Exact search doesn't scale; approximate does.")
    box(c, 72, 470, 220, 90, BOX_RED, "Brute force", "compare query to")
    box(c, 320, 470, 220, 90, BOX_GREEN, "ANN", "99% of accuracy at")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "ALL 100M vectors.")
    c.drawString(92, 501, "Accurate, impossibly slow.")
    c.drawString(340, 515, "1% of the cost.")
    c.drawString(340, 501, "The recall/latency tradeoff.")
    note(c, 72, 320, 468, "ANN = Approximate Nearest Neighbor. Nobody needs the mathematically closest vector — the 10th-closest is just as useful.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "IVF: Clustering the Space",
                       "Search the right neighborhood, not the whole city.")
    box(c, 72, 500, 140, 70, BOX_BLUE, "Cluster 1", "centroid c1")
    box(c, 256, 500, 140, 70, BOX_TEAL, "Cluster 2", "centroid c2")
    box(c, 430, 470, 110, 80, BOX_PURP, "Cluster N", "...")
    box(c, 196, 380, 220, 64, BOX_GREEN, "Query -> nearest clusters", "probe nprobe of them")
    arrow(c, 306, 498, 306, 446, color=GREEN, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 330, "Train k-means centroids; assign each vector to a cluster. Query only the closest nprobe clusters.")
    note(c, 72, 220, 468, "Tuning: more clusters = finer partitions; higher nprobe = better recall, slower search.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "HNSW: The Graph Index",
                       "Navigate a layered highway of vectors.")
    box(c, 72, 500, 220, 60, BOX_BLUE, "Top layer: sparse", "long jumps")
    box(c, 320, 500, 220, 60, BOX_TEAL, "Bottom layer: dense", "local links")
    arrow(c, 306, 498, 306, 462, color=ACCENT, width=2)
    box(c, 196, 380, 220, 64, BOX_GREEN, "Greedy walk", "descend layers to target")
    arrow(c, 306, 428, 306, 446, color=GREEN, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 330, "Hierarchical Navigable Small World: enter at the top, greedily walk toward the query, refine downward.")
    note(c, 72, 220, 468, "HNSW is the default high-recall index. Cost: significant RAM — the graph lives in memory.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Metadata Filtering",
                       "Vectors plus structured filters.")
    box(c, 72, 470, 220, 90, BOX_BLUE, "Vector search", "top-k by similarity")
    box(c, 320, 470, 220, 90, BOX_ORANGE, "Filter", "date > 2024 AND")
    arrow(c, 292, 515, 318, 515, color=ACCENT, width=2.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(340, 515, "lang = 'en'")
    c.drawString(340, 501, "Pre- or post-filter.")
    note(c, 72, 320, 468, "Pre-filtering is exact but can starve ANN; post-filtering is fast but may return too few. Hybrid indexes balance both.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Vector DB Architecture",
                       "What Pinecone / Weaviate / Qdrant provide.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Write path", "embed, index,")
    box(c, 256, 480, 140, 70, BOX_GREEN, "Query path", "ANN + filter +")
    box(c, 430, 470, 110, 80, BOX_PURP, "Ops", "replicas,")
    arrow(c, 212, 515, 254, 515, color=ACCENT, width=1.5)
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 500, "store, replicate.")
    c.drawString(276, 500, "rerank.")
    c.drawString(450, 510, "backups,")
    c.drawString(450, 496, "namespaces.")
    note(c, 72, 330, 468, "Managed (Pinecone) vs self-hosted (Weaviate, Qdrant, Milvus): tradeoff is operational burden against control and cost.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Tuning Recall vs Latency",
                       "The knobs that matter.")
    yy = bullet_list(c, 72, y,
        ["HNSW: ef_search higher = better recall, slower queries. Build once with high ef_construction.",
         "IVF: nprobe higher = better recall, more clusters scanned.",
         "Quantize vectors (PQ/SQ) to fit bigger indexes in RAM — small recall cost.",
         "Measure recall@k against brute-force ground truth on YOUR data, not vendor benchmarks.",
         "Set an SLO (p99 < 50ms at recall 0.95?) then tune the index to meet it."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Vector Databases — Remember",
                 ["ANN trades a little accuracy for massive speed — the 10th-closest vector is fine.",
                  "IVF clusters the space and probes nearby clusters; HNSW walks a layered graph.",
                  "Combine vector search with metadata filters for real applications.",
                  "Managed vs self-hosted is an ops-burden vs control tradeoff.",
                  "Tune ef_search/nprobe against recall@k measured on your own data."],
                 pg)
    c.save(); print("wrote", path)


def pdf_semantic_search(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Semantic Search\nVisual Guide",
               "Finding meaning, not just keywords:\ndense vs sparse, hybrid, rerankers.",
               "LLM Engineering", None); pg += 1

    y = section_header(c, 1, 5, "Dense vs Sparse Retrieval",
                       "Meaning vectors vs keyword matching.")
    box(c, 72, 470, 220, 90, BOX_GREEN, "Dense", "embeddings + ANN:")
    box(c, 320, 470, 220, 90, BOX_BLUE, "Sparse", "BM25 keywords:")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9.5)
    c.drawString(92, 515, "finds paraphrases,")
    c.drawString(92, 501, "misses exact terms.")
    c.drawString(340, 515, "finds exact terms,")
    c.drawString(340, 501, "misses paraphrases.")
    note(c, 72, 320, 468, "They fail in opposite ways — which is exactly why combining them works so well.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Hybrid Search",
                       "Fuse both signals.")
    box(c, 72, 500, 130, 70, BOX_GREEN, "Dense", "top 100")
    box(c, 246, 500, 130, 70, BOX_BLUE, "Sparse", "top 100")
    box(c, 410, 500, 130, 70, BOX_PURP, "Fusion", "RRF merge")
    arrow(c, 202, 535, 244, 535, color=ACCENT, width=1.5)
    arrow(c, 376, 535, 408, 535, color=ACCENT, width=1.5)
    arrow(c, 475, 535, 500, 535, color=ACCENT, width=1.5)
    box(c, 196, 390, 220, 64, BOX_ORANGE, "Fused ranking", "reciprocal rank fusion")
    arrow(c, 475, 498, 350, 456, color=GREEN, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 340, "RRF: score = sum over lists of 1/(k + rank). No score normalization needed — ranks only.")
    note(c, 72, 230, 468, "Hybrid is the production default: dense for semantics, sparse for names, codes, and rare terms.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Query Understanding",
                       "Fix the query before searching.")
    yy = bullet_list(c, 72, y,
        ["Query expansion: add synonyms and related terms ('car' -> 'automobile, vehicle').",
         "HyDE: have an LLM draft a hypothetical answer, then search with its embedding.",
         "Query rewriting: turn a vague question into a precise search query with an LLM.",
         "Spell correction and entity recognition: 'iphon 15' should still find iPhone 15.",
         "Decompose multi-hop questions into sub-queries; search each, then synthesize."],
        font_size=10.5, gap=30)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Rerankers",
                       "A careful second look at the top candidates.")
    box(c, 72, 470, 220, 80, BOX_BLUE, "Stage 1", "hybrid recall: top 100")
    box(c, 320, 470, 220, 80, BOX_GREEN, "Stage 2", "cross-encoder: top 10")
    arrow(c, 292, 510, 318, 510, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Cross-encoders score query+document jointly — far more accurate than bi-encoder similarity.")
    note(c, 72, 300, 468, "Reranking is the highest-ROI upgrade for most search systems: keep recall broad, let the reranker be picky.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "End-to-End Pipeline",
                       "The full semantic search stack.")
    box(c, 72, 520, 120, 60, BOX_ORANGE, "Query", "")
    box(c, 226, 520, 130, 60, BOX_BLUE, "Understand", "rewrite/expand")
    box(c, 390, 520, 120, 60, BOX_GREEN, "Hybrid", "dense+sparse")
    arrow(c, 192, 550, 224, 550, color=ACCENT, width=1.5)
    arrow(c, 356, 550, 388, 550, color=ACCENT, width=1.5)
    box(c, 140, 410, 150, 60, BOX_PURP, "Rerank", "top 10")
    box(c, 340, 410, 150, 60, BOX_TEAL, "Results", "with snippets")
    arrow(c, 450, 518, 215, 472, color=ACCENT, width=1.5)
    arrow(c, 290, 440, 338, 440, color=ACCENT, width=1.5)
    note(c, 72, 290, 468, "Instrument every stage: log queries, retrieved sets, and clicks. Search quality is measured, not assumed.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Semantic Search — Remember",
                 ["Dense finds paraphrases; sparse finds exact terms — they fail in opposite ways.",
                  "Hybrid search with RRF fusion is the production default.",
                  "Understand the query first: expand, rewrite, or HyDE before retrieving.",
                  "Rerankers are the highest-ROI upgrade: broad recall, picky precision.",
                  "Measure with labeled relevance judgments; log everything to improve."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    jobs = [
        (pdf_backprop, "bbg-backprop.pdf"),
        (pdf_cnns, "bbg-cnns.pdf"),
        (pdf_rnns, "bbg-rnns.pdf"),
        (pdf_attention, "bbg-attention-deep.pdf"),
        (pdf_bert_gpt, "bbg-bert-gpt.pdf"),
        (pdf_embeddings, "bbg-embeddings.pdf"),
        (pdf_finetuning, "bbg-finetuning.pdf"),
        (pdf_rag, "bbg-rag.pdf"),
        (pdf_prompt_engineering, "bbg-prompt-engineering.pdf"),
        (pdf_diffusion, "bbg-diffusion.pdf"),
        (pdf_gans, "bbg-gans.pdf"),
        (pdf_rl, "bbg-rl.pdf"),
        (pdf_feature_engineering, "bbg-feature-engineering.pdf"),
        (pdf_model_serving, "bbg-model-serving.pdf"),
        (pdf_mlops, "bbg-mlops.pdf"),
        (pdf_data_versioning, "bbg-data-versioning.pdf"),
        (pdf_model_drift, "bbg-model-drift.pdf"),
        (pdf_quantization, "bbg-quantization.pdf"),
        (pdf_distributed_training, "bbg-distributed-training.pdf"),
        (pdf_federated, "bbg-federated.pdf"),
        (pdf_xai, "bbg-xai.pdf"),
        (pdf_fairness, "bbg-fairness.pdf"),
        (pdf_llm_eval, "bbg-llm-eval.pdf"),
        (pdf_vector_db, "bbg-vector-db.pdf"),
        (pdf_semantic_search, "bbg-semantic-search.pdf"),
    ]
    for fn, name in jobs:
        fn(os.path.join(out, name))
    print("done:", len(jobs), "pdfs")
