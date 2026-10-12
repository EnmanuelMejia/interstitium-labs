"""IL-15 retrofit: Machine Learning track (6 modules)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, apply_all

CONTENT = {
    "ml-interview-prep--ml-theory-iv": {
        "summary": (
            "Welcome to the Machine Learning Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to go "
            "past the buzzwords into the theory interviewers actually probe: why regularization works, what the "
            "loss is really optimizing, and where each model class breaks — derived, not recited."
        ),
        "concepts": (
            "- **bias-variance tradeoff** — Expected error = bias² + variance + irreducible noise; simple models "
            "underfit (high bias), complex models overfit (high variance) — the sweet spot minimizes the total.\n"
            "- **L1 (lasso)** — Penalizes |w|: drives weights to exactly zero — feature selection, sparse "
            "solutions; 'L1 selects.'\n"
            "- **L2 (ridge)** — Penalizes w²: shrinks weights smoothly, handles correlated features; 'L2 shrinks.'\n"
            "- **maximum likelihood (MLE)** — Choose parameters maximizing P(data|θ); least squares is MLE under "
            "Gaussian noise, cross-entropy is MLE for classification — 'most loss functions are MLE in disguise.'\n"
            "- **gradient descent** — Batch (exact, slow), SGD (noisy, fast, escapes shallow minima), mini-batch "
            "(the practical default).\n"
            "- **learning rate** — The step size; 'the most important hyperparameter': too large diverges "
            "(NaN/inf), too small crawls.\n"
            "- **decision boundary** — The surface separating predicted classes: linear (logistic regression), "
            "axis-aligned boxes (trees), smooth nonlinear (RBF SVM), learned hierarchical (neural nets) — 'the "
            "boundary shape tells you the model's inductive bias.'\n"
            "- **inductive bias** — The assumptions a model class bakes in about the world; what it can and "
            "cannot learn.\n"
            "- **derivation over recitation** — Working from definitions on the board: checkable, recoverable "
            "when memory fails mid-step."
        ),
        "procedure_intro": (
            "The theory drill: every concept is derived on paper or a whiteboard from its definition, then "
            "stress-tested with 'where does this break?' Recitation is untestable until it breaks; derivations "
            "are checkable all the way down."
        ),
        "procedure_steps": [
            "State the definition precisely (bias-variance decomposition, MLE objective) before any intuition.",
            "Derive the key result on the board: squared error from the Gaussian log-likelihood, the L1 sparsity intuition, the boundary shape from the model form.",
            "Name the failure mode unprompted: where the assumption breaks (non-independent data for MLE-style losses, correlated features for L1).",
            "Connect to practice: which interview question this answers ('why does regularization help?', 'what is the loss optimizing?').",
            "Red-team with numbers: a tiny worked example showing the tradeoff (e.g., variance exploding with model complexity on fixed data).",
            "Close with the one-sentence interview version — the line you deliver before the derivation, not instead of it.",
        ],
        "project_brief": (
            "Build a theory reference notebook: the bias-variance decomposition derived and simulated (error vs "
            "complexity curves), L1 vs L2 geometry shown on a toy problem, MLE derived for linear regression and "
            "logistic regression, gradient-descent variants compared on a ravine-shaped loss, and decision "
            "boundaries plotted for five model classes. Each section ends with the interview one-liner and the "
            "'where it breaks' note. Derive, don't recite — the notebook is your pre-interview review."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Theory here is interview-depth — precise but not a substitute for a full machine-learning education. "
            "Derivations are standard results; if you deploy these ideas, validate on real data, not on the "
            "notebook's toy examples."
        ),
        "new_card": {
            "front": "What's the interview line for the loss function?",
            "back": "'Most loss functions are MLE in disguise': least squares is maximum likelihood under Gaussian noise, cross-entropy under categorical outcomes. The loss isn't arbitrary — it's a probabilistic assumption about the world, and naming it shows you know what you're optimizing.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Expected test error decomposes into:",
                "choices": [
                    "Training error plus luck",
                    "Bias² + variance + irreducible noise",
                    "Bias plus regularization",
                    "Loss plus learning rate",
                ],
                "answer": 1,
                "explain": "The decomposition names the tradeoff: complexity trades bias for variance. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "With highly correlated features, prefer L2 over L1 because:",
                "choices": [
                    "It's faster",
                    "L2 shrinks correlated weights together; L1 arbitrarily keeps one and zeroes the rest",
                    "L1 is deprecated",
                    "L2 needs less data",
                ],
                "answer": 1,
                "explain": "'L1 selects, L2 shrinks' — the penalty geometry decides. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "NaN loss mid-training most likely means:",
                "choices": [
                    "Too little data",
                    "Learning rate too large for the loss curvature — reduce it (or schedule/clip) first",
                    "Too many epochs",
                    "Wrong optimizer brand",
                ],
                "answer": 1,
                "explain": "Overshooting the minimum repeatedly: the step size is the first suspect. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Mini-batch gradient descent is the practical default because:",
                "choices": [
                    "It's exact",
                    "It balances gradient noise (which helps escape shallow minima) against compute efficiency",
                    "It's simplest",
                    "Batch is banned",
                ],
                "answer": 1,
                "explain": "Noise plus speed: the tradeoff batch and SGD sit at opposite ends of. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "An RBF-kernel SVM's decision boundary is:",
                "choices": ["Linear", "Axis-aligned boxes", "Smooth and nonlinear — local influence around support vectors", "Random"],
                "answer": 2,
                "explain": "The boundary shape reveals the inductive bias — that's the interview point. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Deriving beats reciting in theory rounds because:",
                "choices": [
                    "It's longer",
                    "It's checkable reasoning — recoverable when memory fails mid-step",
                    "It impresses",
                    "It's traditional",
                ],
                "answer": 1,
                "explain": "A derivation can be followed and fixed; a recitation can only be right or wrong. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
    "ml-interview-prep--deep-learning-iv": {
        "summary": (
            "Welcome to the Machine Learning Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to open "
            "up deep learning at interview depth: backprop and the chain rule, why activations and initialization "
            "matter, what makes convolutions fit images, the RNN-to-attention handoff — and reading a training "
            "curve like a diagnostic."
        ),
        "concepts": (
            "- **backpropagation** — The chain rule applied to the computation graph: forward pass computes "
            "values, backward pass propagates gradients from loss to parameters — 'every framework is chain rule "
            "+ bookkeeping.'\n"
            "- **activation function** — The nonlinearity (ReLU and variants) that stops deep nets collapsing into "
            "linear models; saturating activations stall gradients.\n"
            "- **initialization (He/Xavier)** — Weight scales that keep signal and variance stable across layers; "
            "bad init means vanishing or exploding gradients before training starts.\n"
            "- **vanishing / exploding gradients** — Gradients shrinking to zero or blowing up across many layers; "
            "the reason for careful init, normalization, and gated architectures.\n"
            "- **convolution** — Local connectivity plus weight sharing: filters detect local patterns anywhere in "
            "the image with far fewer parameters than dense layers.\n"
            "- **translation equivariance** — A cat is a cat wherever it appears: shared filters respond to "
            "patterns independent of position.\n"
            "- **RNN** — Sequential processing with hidden state; vanishing gradients over long sequences limit "
            "its memory.\n"
            "- **LSTM** — Gated cells preserving long-term state; better than vanilla RNNs, still sequential.\n"
            "- **attention** — All-pairs interactions computed in parallel, no recurrence; 'attention replaced "
            "recurrence because parallelism won' — the handoff that enabled transformers.\n"
            "- **dropout** — Randomly zeroing activations in training so the network can't rely on any single "
            "unit; trains an implicit ensemble of subnetworks.\n"
            "- **batch / layer normalization** — Stabilizing layer input distributions during training; faster, "
            "more reliable convergence.\n"
            "- **training curve diagnosis** — Train loss falling while validation rises: overfitting. Both "
            "plateaued high: underfitting. Divergence: learning-rate trouble."
        ),
        "procedure_intro": (
            "The deep-learning drill: mechanisms first, architectures second. Every architecture question is "
            "answered by naming what problem it solves — interviewers probe the 'why this structure,' not the "
            "parameter count."
        ),
        "procedure_steps": [
            "Derive backprop for a two-layer net on paper: forward values, then the chain rule backward — once, by hand, so it's yours.",
            "Explain each architecture as a fix: CNNs fix dense layers' parameter explosion on images; LSTMs fix RNN memory; attention fixes sequential bottlenecks.",
            "Name the failure mode per component: saturating activations, bad init, unnormalized training — and the standard remedy.",
            "Practice curve diagnosis: given six train/val curve pairs, name overfitting, underfitting, divergence, and the prescribed fix.",
            "Compare regularization tools (dropout, weight decay, augmentation, early stopping) by what variance they remove and what they cost.",
            "Close with the handoff narrative: recurrence → gating → attention, told as a sequence of solved bottlenecks.",
        ],
        "project_brief": (
            "Build a deep-learning diagnostics notebook: backprop derived by hand for a tiny net and verified "
            "against autograd, activation/init ablations showing the gradient pathology each fixes, a CNN vs dense "
            "parameter-count comparison on images, and a training-curve gallery (healthy, overfit, underfit, "
            "divergent) with the diagnosis and prescription for each. Every section ends with the interview "
            "one-liner. Mechanisms, not benchmarks."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Deep learning here is interview-depth mechanisms, not research training — architectures evolve "
            "quickly, so date your claims and verify current best practice before building. Toy experiments "
            "illustrate principles; they don't transfer as production recipes."
        ),
        "new_card": {
            "front": "What's the interview line for attention's win over RNNs?",
            "back": "'Attention replaced recurrence because parallelism won': RNNs process tokens one at a time — a sequential bottleneck — while attention computes all pairwise interactions at once, which is GPU-friendly. Tell architectures as solved bottlenecks.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Without nonlinear activations, a deep network:",
                "choices": [
                    "Trains faster",
                    "Collapses to a linear model no matter how many layers it has",
                    "Overfits less",
                    "Needs no init",
                ],
                "answer": 1,
                "explain": "Compositions of linear maps are linear — depth without nonlinearity adds nothing. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "He/Xavier initialization exists to:",
                "choices": [
                    "Speed up data loading",
                    "Keep activation variance stable across layers so gradients neither vanish nor explode at start",
                    "Reduce parameters",
                    "Pick the learning rate",
                ],
                "answer": 1,
                "explain": "Bad init breaks training before it begins; scaled init preserves signal depth-wise. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Both train and validation loss plateau at a high value. Diagnosis:",
                "choices": ["Overfitting", "Underfitting — the model can't capture the pattern; add capacity or features", "Divergence", "Perfect fit"],
                "answer": 1,
                "explain": "Converged-but-bad means capacity or features, not more training. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Dropout's 'implicit ensemble' means:",
                "choices": [
                    "Many models are saved",
                    "Each training step samples a different subnetwork; inference uses the full net (scaled) — averaging their behavior",
                    "Dropout picks the best layer",
                    "It's only for CNNs",
                ],
                "answer": 1,
                "explain": "Forcing redundancy across units prevents co-adaptation. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "LSTMs improve on vanilla RNNs by:",
                "choices": [
                    "Adding layers",
                    "Gating that preserves long-term cell state — though processing stays sequential",
                    "Removing recurrence",
                    "Using attention",
                ],
                "answer": 1,
                "explain": "Gates fix the memory problem; attention later fixed the sequential bottleneck. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A CNN needs far fewer parameters than a dense net on images because:",
                "choices": [
                    "Images are small",
                    "Weight sharing: one filter reused across positions — parameters scale with filter size, not image size",
                    "GPUs are fast",
                    "Pooling removes layers",
                ],
                "answer": 1,
                "explain": "Local connectivity plus sharing is the whole efficiency story. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "ml-interview-prep--ml-system-design": {
        "summary": (
            "Welcome to the Machine Learning Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to do the "
            "round that decides senior ML loops: ML system design. Frame the business goal as a prediction "
            "problem, design the training-to-serving path, name the failure modes — and keep the complexity honest."
        ),
        "concepts": (
            "- **framing** — Translating the business decision into prediction: what's predicted, for whom, at "
            "what moment, with what latency, measured how — 'framing is the highest-leverage ML skill.'\n"
            "- **training/serving skew** — Feature or label computation differing between training and "
            "production; caught by logging serving-time features and comparing distributions.\n"
            "- **feature store** — One home for feature definitions shared by training and serving: consistent "
            "computation (kills skew), point-in-time correctness, online/offline serving — 'where features become "
            "contracts.'\n"
            "- **point-in-time correctness** — Training features computed as of the prediction moment, never with "
            "future knowledge; the anti-leakage guarantee.\n"
            "- **data drift** — Input feature distributions shifting vs training; the early warning before "
            "performance visibly decays.\n"
            "- **prediction drift** — Output distribution shifting; detectable without labels — a leading "
            "indicator when labels lag.\n"
            "- **champion/challenger** — Safe rollout: the new model serves a slice of traffic against the "
            "incumbent, promoted on evidence.\n"
            "- **retraining triggers** — Schedule-based or drift-threshold-based; the policy that keeps the model "
            "fresh without churn.\n"
            "- **simple-model-first** — A linear model or heuristic sets the baseline: ships fast, debugs easily, "
            "forces complexity to prove its value — 'I scale complexity with evidence, not enthusiasm.'\n"
            "- **latency/cost budget** — The serving constraints (p99 latency, cost per prediction) that bound "
            "model choice before accuracy does."
        ),
        "procedure_intro": (
            "The system-design drill: 40 minutes, one vague prompt ('design recommendations for...'), narrated "
            "end to end. The grading lens is coverage of the full system — data, training, serving, monitoring — "
            "not the cleverness of the model."
        ),
        "procedure_steps": [
            "Frame first (5 min): decision → prediction target → latency → success metric in business terms. Write the framing down; everything references it.",
            "Sketch data: sources, labels and their lag, feature computation — and mark where skew can enter between training and serving.",
            "Choose the baseline: the simplest model that could work; state what evidence would justify more complexity.",
            "Design serving: online vs batch, latency budget, the feature path (feature store for consistency), fallback when the model is down.",
            "Design monitoring: input drift, prediction drift, performance proxies while labels lag, data-quality gates on the pipeline.",
            "Set retraining policy: schedule vs drift triggers, champion/challenger rollout, rollback criteria.",
            "Name failure modes aloud: skew, drift, feedback loops, cold start, cost blowout — and the mitigation for each. Close by re-checking the framing.",
        ],
        "project_brief": (
            "Design reviews for two systems: real-time fraud scoring (60-second latency budget) and batch churn "
            "prediction (daily). For each deliver: the framing doc, data/label analysis with lag noted, the "
            "baseline and complexity-justification bar, serving design with latency budget, the feature-store "
            "contract, monitoring (drift, proxies, gates), retraining policy with rollout plan, and the failure-"
            "mode table. Present one as a 40-minute whiteboard; the other as a written design doc."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Whiteboard designs are judged on systems thinking — failure modes, monitoring, honest complexity — "
            "not on matching any company's stack. Production ML adds organizational constraints (cost, "
            "compliance, on-call) this module sketches but doesn't simulate."
        ),
        "new_card": {
            "front": "What's the interview line for training/serving skew?",
            "back": "Skew is when production computes features differently than training did — and it's silent until metrics decay. The defenses: one feature definition (feature store), point-in-time correctness in training, and serving-time feature logging compared against the training baseline.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Labels that arrive weeks late make model monitoring rely on:",
                "choices": [
                    "Accuracy",
                    "Proxies: input drift, prediction drift, and business-metric guardrails — leading indicators",
                    "Retraining daily",
                    "Manual review of everything",
                ],
                "answer": 1,
                "explain": "When ground truth lags, distribution signals warn first. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Champion/challenger deployment is safer than big-bang because:",
                "choices": [
                    "It's faster",
                    "The new model proves itself on a traffic slice against the incumbent — evidence before full rollout",
                    "It's cheaper",
                    "It's traditional",
                ],
                "answer": 1,
                "explain": "Gradual, measured promotion bounds the blast radius of a bad model. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A feedback loop in production ML (predictions influencing future training data) is dangerous because:",
                "choices": [
                    "It's slow",
                    "The model trains on its own past outputs — bias amplifies and the system drifts from reality",
                    "It needs GPUs",
                    "Labels disappear",
                ],
                "answer": 1,
                "explain": "Self-reinforcing systems need explicit detection and correction design. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Point-in-time correctness prevents:",
                "choices": [
                    "Slow training",
                    "Leakage — features computed with knowledge from after the prediction moment",
                    "Drift",
                    "High cost",
                ],
                "answer": 1,
                "explain": "Training on the future makes evaluation fiction; as-of semantics keep it honest. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The latency budget should be set:",
                "choices": [
                    "After model selection",
                    "Before — from the product requirement; it bounds which models are even candidates",
                    "By the ML team alone",
                    "As low as possible",
                ],
                "answer": 1,
                "explain": "Serving constraints are requirements, not optimizations; they shape the design. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "A design covering only the model is weak because:",
                "choices": [
                    "Models don't matter",
                    "Production value lives in data, serving, and monitoring — the model is one piece",
                    "It's too short",
                    "Interviewers are bored",
                ],
                "answer": 1,
                "explain": "Most ML failures are systems failures: skew, drift, latency — not the algorithm. See the 'Honesty note' in this module.",
            },
        ],
    },
    "ml-interview-prep--ml-coding": {
        "summary": (
            "Welcome to the Machine Learning Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this module we're going to do "
            "whiteboard coding for ML roles: implementing k-means and gradient descent from scratch, vectorized "
            "NumPy under time pressure, and debugging shape mismatches fast — narrated aloud, the whole way."
        ),
        "concepts": (
            "- **k-means (Lloyd's algorithm)** — Alternate: assign points to the nearest centroid, recompute "
            "centroids as means, repeat until stable; converges to local optima — hence k-means++ seeding and "
            "restarts.\n"
            "- **k-means++** — Seeding that spreads initial centroids; mitigates the bad-local-optima problem of "
            "random init.\n"
            "- **vectorized NumPy** — Whole-array ops in compiled C; no Python loops — the speed and clarity "
            "answer for ML coding.\n"
            "- **shape discipline** — Asserting array shapes at each step; mismatches are the #1 time sink — 'I "
            "assert shapes the way others assert types.'\n"
            "- **broadcasting** — NumPy's implicit shape alignment; powerful, and the source of silent "
            "wrong-shape bugs when misunderstood.\n"
            "- **gradient descent by hand** — Deriving the update from the loss (e.g., w -= lr * X^T(Xw - y)/n "
            "for least squares) and coding the loop.\n"
            "- **decision-tree split** — Choosing the split maximizing impurity reduction (Gini/entropy); the "
            "coding exercise behind 'implement a tree.'\n"
            "- **narration** — Verbalizing what each block computes and why; 'my narration is the proof I'd "
            "write this the same way at 2am.'"
        ),
        "procedure_intro": (
            "The coding drill: 25 minutes per algorithm, vectorized NumPy, shapes asserted, narration "
            "continuous. The interviewer grades method — derivation, shape discipline, error recovery — as much "
            "as the final code."
        ),
        "procedure_steps": [
            "State the algorithm in one breath (k-means: assign → recompute → repeat) before writing anything.",
            "Derive the update from the definition: write the loss, differentiate, state the vectorized update — on the board, aloud.",
            "Set up shapes first: comment the expected shape of every array (X: (n,d), w: (d,)) before the loop.",
            "Write vectorized: no Python loops over data; broadcasting where shapes align, with a comment where it's subtle.",
            "Assert shapes after each operation; when a mismatch appears, the first surprising shape is the bug — don't reshape randomly.",
            "Test on a tiny hand-computable case: verify the first iteration's numbers by hand.",
            "Narrate continuously: what each block computes, why this formulation, what could go wrong — silence scores zero on method.",
        ],
        "procedure_code": (
            "import numpy as np\n"
            "\n"
            "def kmeans(X, k, iters=100, seed=0):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    C = X[rng.choice(len(X), k, replace=False)]  # (k, d)\n"
            "    for _ in range(iters):\n"
            "        d2 = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)  # (n, k)\n"
            "        a = d2.argmin(1)                                      # (n,)\n"
            "        new_C = np.array([X[a == j].mean(0) for j in range(k)])\n"
            "        if np.allclose(new_C, C):\n"
            "            break\n"
            "        C = new_C\n"
            "    assert C.shape == (k, X.shape[1])\n"
            "    return a, C"
        ),
        "procedure_lang": "python",
        "project_brief": (
            "Build an ML-from-scratch library: k-means (with k-means++ seeding), gradient descent for least "
            "squares and logistic regression (derived updates), a decision-tree split finder (Gini/entropy), "
            "all vectorized NumPy with shape assertions and docstrings stating the math. Include a test file "
            "verifying each against a hand-computed tiny case and against a reference implementation's outputs. "
            "The README derives each update in three lines. This is the code you re-read before ML coding rounds."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "From-scratch implementations are interview exercises — production uses tested libraries; never ship "
            "hand-rolled optimizers. Timed coding reps measure fluency under pressure, not engineering judgment "
            "at large."
        ),
        "new_card": {
            "front": "What's the interview line for shape mismatches?",
            "back": "'The first surprising shape is the bug': print or assert shapes at every operation, and when one surprises you, that's where the fix lives. Random reshaping is flailing; shape discipline is debugging.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "k-means++ improves on random initialization by:",
                "choices": [
                    "Running faster",
                    "Spreading initial centroids apart — reducing the chance of bad local optima",
                    "Choosing k automatically",
                    "Removing the need for restarts",
                ],
                "answer": 1,
                "explain": "Better seeds, better optima: initialization is part of the algorithm. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The vectorized least-squares gradient step is:",
                "choices": [
                    "w -= lr * (Xw - y)",
                    "w -= lr * X^T(Xw - y)/n — derived from differentiating the MSE",
                    "w += lr * Xy",
                    "w = X^{-1}y always",
                ],
                "answer": 1,
                "explain": "Derive from the loss: the transpose appears because w multiplies X on the right. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Broadcasting (3,) with (4, 3) gives:",
                "choices": ["An error", "(4, 3) — the row vector stretches across rows", "(3, 4)", "(7, 3)"],
                "answer": 1,
                "explain": "Trailing dimensions align; size-1 (or missing) dims stretch. Know it cold — it's the silent-bug source. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A decision-tree split is chosen to maximize:",
                "choices": [
                    "Depth",
                    "Impurity reduction (Gini or entropy gain) — the split that best separates classes",
                    "Speed",
                    "Balance only",
                ],
                "answer": 1,
                "explain": "Greedy impurity reduction is the whole splitting criterion. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Narrating while coding catches bugs because:",
                "choices": [
                    "Interviewers help",
                    "Verbalized logic is checkable logic — most caught bugs are caught mid-sentence",
                    "It's required",
                    "It's slower",
                ],
                "answer": 1,
                "explain": "Saying the invariant aloud exposes the violated one. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Multiple random restarts in k-means address:",
                "choices": [
                    "Slow convergence",
                    "Local optima — keep the run with the best final objective",
                    "Choosing k",
                    "High dimensions",
                ],
                "answer": 1,
                "explain": "Lloyd's algorithm is local; restarts sample the optima landscape. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "ml-interview-prep--ml-capstone-project": {
        "summary": (
            "Welcome to the Machine Learning Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this capstone module you're going "
            "to build one model like a professional: framed problem, honest metric, tracked experiments, "
            "ablations, error analysis, documented limits — and a five-minute story that fits the interview."
        ),
        "concepts": (
            "- **problem framing** — Business decision → prediction task (what, for whom, when); 'the metric is "
            "the business objective, mathematized.'\n"
            "- **baseline** — The simple model every fancier model must beat to justify its cost; also debugs the "
            "pipeline early — 'complexity must earn its keep.'\n"
            "- **experiment tracking** — Params, data version, code hash, metrics per run; 'an untracked "
            "experiment is an anecdote.'\n"
            "- **ablation** — Removing a component and measuring the drop; credit assignment for features and "
            "design choices.\n"
            "- **error analysis** — Slicing failures by subgroup, examining actual examples; 'metrics tell me I'm "
            "wrong; error analysis tells me why.'\n"
            "- **model card** — Intended use, training data, evaluation, limitations, ethical considerations — "
            "'a model without a card is a black box I'm asking others to trust.'\n"
            "- **five-minute narrative** — Framing → approach → key result → limits → what you'd do next; the "
            "interview-length story of the project.\n"
            "- **scope honesty** — Claiming only what the artifact demonstrates; the limits section is a feature, "
            "not an apology."
        ),
        "procedure_intro": (
            "The capstone build order: frame, baseline, iterate with tracking, analyze errors, document limits. "
            "The experiment log is written as you go — reconstruction after the fact is fiction."
        ),
        "procedure_steps": [
            "Frame the problem: translate the business decision into a prediction task; derive the metric from error costs.",
            "Establish the baseline first: simple model, honest evaluation — if it fails, the problem is the data, not the model.",
            "Set up experiment tracking before iterating: every run logs params, data version, code hash, and metrics.",
            "Iterate one change at a time; ablate to assign credit for each improvement — no stacked changes.",
            "Run error analysis: slice failures by subgroup, look at actual examples, let the pattern choose the next move.",
            "Write the model card: intended use, data, evaluation, limitations — especially where the model shouldn't be trusted.",
            "Rehearse the five-minute narrative: framing, approach, key result, limits, what you'd do next — timed.",
        ],
        "project_brief": (
            "Deliver the ML capstone: a framed problem on a real dataset with a cost-derived metric, a baseline "
            "that later models must beat, a tracked experiment log (one change per run, ablations for credit), "
            "error analysis that drove at least one iteration, a model card with honest limitations, and the "
            "five-minute interview narrative recorded or written. The repository is the link you send when they "
            "ask about ML project experience — and the limits section is what makes it believable."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. A "
            "capstone demonstrates professional process on one problem — it doesn't replicate production "
            "constraints (scale, latency, compliance) or team dynamics. The model card's limits section exists "
            "precisely so nobody mistakes the artifact for more than it is."
        ),
        "new_card": {
            "front": "What's the interview line for experiment tracking?",
            "back": "'An untracked experiment is an anecdote': log params, data version, code hash, and metrics for every run, change one thing at a time, and ablate for credit. Without tracking, 'it got better' is unfalsifiable.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "Changing three things between runs and seeing improvement tells you:",
                "choices": [
                    "All three helped",
                    "Nothing about credit — confounded changes are unfalsifiable; change one thing at a time",
                    "The best one",
                    "To ship it",
                ],
                "answer": 1,
                "explain": "Credit assignment needs isolation; stacked changes teach nothing. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Error analysis should drive the next iteration by:",
                "choices": [
                    "Suggesting a bigger model always",
                    "Revealing which errors dominate — the pattern (data? features? labels?) chooses the fix",
                    "Confirming the metric",
                    "Adding hyperparameters",
                ],
                "answer": 1,
                "explain": "'Metrics tell me I'm wrong; error analysis tells me why.' See the 'Concepts' glossary in this module.",
            },
            {
                "q": "The model card's limitations section prevents:",
                "choices": ["Use", "Misuse — downstream users know where the model shouldn't be trusted", "Evaluation", "Training"],
                "answer": 1,
                "explain": "Documented limits turn unknown unknowns into known ones. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A baseline that beats your fancy model means:",
                "choices": [
                    "The project failed",
                    "The complexity hasn't earned its keep — simplify, or find the real bottleneck (often data)",
                    "Baselines are bad",
                    "More tuning needed always",
                ],
                "answer": 1,
                "explain": "Baselines bound the problem; losing to one is information, not failure. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Logging the data version per experiment matters because:",
                "choices": [
                    "It's tidy",
                    "Data changes silently invalidate comparisons — the version is part of the experiment's identity",
                    "It's required",
                    "Storage is cheap",
                ],
                "answer": 1,
                "explain": "Reproducibility needs the full tuple: code, params, and data. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Ending the narrative with 'what you'd do next' is strong because:",
                "choices": [
                    "It's humble",
                    "It shows scope awareness — you see the work's frontier, not just its interior",
                    "It fills time",
                    "It excuses gaps",
                ],
                "answer": 1,
                "explain": "Knowing the next step proves you owned the problem, not just the implementation. See the 'Concepts' glossary in this module.",
            },
        ],
    },
    "ml-interview-prep--ml-mock": {
        "summary": (
            "Welcome to the Machine Learning Interview Prep track of the IL-15 Data Engineering & Analytics "
            "Interview Prep course. I'm your instructor for this track, and in this final track module we're going "
            "to run full ML-loop simulations — timed theory deep-dives, live ML coding, system-design whiteboards, "
            "paper-discussion questions — scored the way hiring committees score them."
        ),
        "concepts": (
            "- **ML loop** — The standard sequence: theory deep-dive, live coding, system design, paper "
            "discussion, behavioral — each round with its own shape.\n"
            "- **theory shape** — Derive, don't recite: start from definitions, work forward on the board; "
            "'derivations prove understanding.'\n"
            "- **coding shape** — Vectorized NumPy, shape asserts, narrate as you go; 'narration proves method.'\n"
            "- **system-design shape** — Frame → data → baseline → serving → monitoring → failure modes; coverage "
            "of the full system, not model cleverness.\n"
            "- **paper-discussion shape** — Problem, key idea, why it works, limitations, then the practice "
            "connection: 'I read for the idea and its failure modes, not the leaderboard number.'\n"
            "- **failed-experiment story** — Hypothesis, what the data said, the kill/pivot decision with numbers, "
            "the process lesson — 'a clean kill is a success; the failure is in not learning.'\n"
            "- **scored review** — Rubric per round immediately after; misses verbatim.\n"
            "- **redrill plan** — Misses to specific, dated tasks; the loop-closing mechanism."
        ),
        "procedure_intro": (
            "The ML mock protocol: one full loop per session, real timing, derivations on the board. Rotate the "
            "weakest round forward — pressure training targets the gap."
        ),
        "procedure_steps": [
            "Assemble the loop: 20-min theory deep-dive, 25-min live coding, 40-min system design, 15-min paper discussion, 10-min failed-experiment story.",
            "Run theory as derivation: definitions first, board work, the 'where it breaks' unprompted.",
            "Run coding vectorized with shape asserts and continuous narration; test on a tiny hand-computed case.",
            "Run system design with the full coverage checklist; name failure modes and mitigations aloud.",
            "Run paper discussion: idea, mechanism, limitations, practice connection — never the leaderboard number.",
            "Tell the failed-experiment story: hypothesis, evidence, the kill decision, the captured learning.",
            "Score every round against the rubric immediately; convert each miss to a dated redrill task.",
        ],
        "project_brief": (
            "Run and document three full ML mock loops over two weeks. Per loop deliver the prompts per round, "
            "rubric scores with verbatim misses, the dated redrill plan, and a trend summary. Close with a "
            "readiness self-assessment: strongest round shape, costliest remaining miss, the plan to close it — "
            "and one paper-discussion answer written out in full as the exemplar."
        ),
        "honesty": (
            "Preparation, not a credential: this module confers no certificate and makes no placement claims. "
            "Mocks simulate the loop's shapes under pressure; real loops vary by team, and research taste is "
            "scored beyond any rubric. Use scores to aim redrills, not to predict offers."
        ),
        "new_card": {
            "front": "What's the interview line for paper discussions?",
            "back": "'I read for the idea and its failure modes, not the leaderboard number': problem, key idea, why it works, limitations — then when you'd actually use it. Understanding means grasping the mechanism and its boundaries.",
        },
        "explain_pointer": "Covered in this module's 'Concepts' note.",
        "new_quiz": [
            {
                "q": "In a theory deep-dive, the strongest opening is:",
                "choices": [
                    "The final formula",
                    "The definition, then working forward — derivation, not recitation",
                    "A joke",
                    "The paper citation",
                ],
                "answer": 1,
                "explain": "Derivations are checkable and recoverable; recitations are brittle. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "A killed experiment told as a 'clean kill' works when:",
                "choices": [
                    "Always",
                    "The decision was evidence-driven and the learning was captured — killing well is the skill",
                    "Never mention failures",
                    "It's trendy",
                ],
                "answer": 1,
                "explain": "Experimentation's product is learning; a well-killed test delivered it. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Quoting a paper's benchmark number without the idea:",
                "choices": [
                    "Shows diligence",
                    "Scores nothing — understanding means the mechanism, limitations, and practice connection",
                    "Is sufficient",
                    "Impresses",
                ],
                "answer": 1,
                "explain": "Leaderboard numbers age; ideas and failure modes transfer. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "Rotating the weakest round to the front:",
                "choices": [
                    "Builds confidence",
                    "Trains the gap while fresh — deliberate practice targets misses",
                    "Is traditional",
                    "Saves time",
                ],
                "answer": 1,
                "explain": "Pressure training is for the miss, not the strength. See the 'Hands-on procedure' in this module.",
            },
            {
                "q": "In system-design rounds, the most common miss is:",
                "choices": [
                    "Wrong model choice",
                    "Covering only the model — production value lives in data, serving, monitoring",
                    "Going too slow",
                    "Asking questions",
                ],
                "answer": 1,
                "explain": "Coverage of the full system is the grading lens. See the 'Concepts' glossary in this module.",
            },
            {
                "q": "Scoring immediately after each round (not later) matters because:",
                "choices": [
                    "It's faster",
                    "Fresh misses are verbatim and specific — delayed review smooths them vague",
                    "Rubrics expire",
                    "Memory is perfect",
                ],
                "answer": 1,
                "explain": "Specific misses become specific redrills. See the 'Hands-on procedure' in this module.",
            },
        ],
    },
}

if __name__ == "__main__":
    apply_all(load(), CONTENT)
