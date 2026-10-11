module = {
  "id": "IL28-M17",
  "code": "IL-28",
  "title": "Branching Workflows: Rebase vs Merge, Code Review & MRs",
  "summary": "Master Git branching workflows — when to merge, when to rebase, how to resolve conflicts — and how to run rigorous merge-request reviews, including the dependency-pinning requirements.txt review exercise drawn from real panel interviews.",
  "objectives": [
    "Explain the difference between merge and rebase and choose the right one for shared versus private branches.",
    "Resolve merge conflicts during both merges and rebases using the standard edit-stage-continue workflow.",
    "Describe fast-forward merges and decide when to preserve topology with --no-ff.",
    "Conduct a merge-request review that checks correctness, scope, tests, secrets, and dependency hygiene.",
    "Review a requirements.txt change and justify an approve versus request-changes verdict based on version pinning."
  ],
  "notes": [
    {
      "title": "Merge: joining two histories with a merge commit",
      "body": """A merge takes the tips of two branches, finds their common ancestor (the merge base), combines the changes from both sides, and records the result as a merge commit — a commit with two parents. That two-parent commit is the permanent record that \"these two lines of work came together here.\" Worked example: you branched feature/login off main, and while you worked, main also moved forward, so the histories diverged. You finish and run:

$ git checkout main
$ git merge feature/login

Git cannot fast-forward (covered in the next note), so it creates a merge commit. `git log --graph --oneline` now shows:

*   9f3a2c1 Merge branch 'feature/login'
|\\
| * 7b1e04d Add login form
| * 2c8f9aa Validate email input
|/
* 4d5aa10 Deploy pipeline fix

Solution walkthrough: main sat at 4d5aa10 while feature/login added 2c8f9aa and 7b1e04d on its own line. The merge commit 9f3a2c1 has two parents — 4d5aa10 and 7b1e04d — and its content is the union of both sides. If both sides touched the same lines, Git stops and asks you to resolve conflicts (see the conflicts note). Merging never rewrites existing commits: every commit keeps its original hash, which is why merge is always safe on shared branches. The trade-off is a busier graph — long-lived projects accumulate many merge commits, which is exactly the problem rebasing solves."""
    },
    {
      "title": "Rebase: replaying your commits onto a new base",
      "body": """Rebasing takes your branch's commits, temporarily sets them aside, moves your branch pointer to the tip of the target branch, then re-applies your commits one by one on top — as if you had started your work from the latest main all along. The result is a perfectly linear history with no merge commit. Worked example: your private branch feature/login is three commits behind a fast-moving main:

$ git checkout feature/login
$ git fetch origin
$ git rebase origin/main

If main added commits A and B while you added X and Y, your history goes from `...-A-B` plus a side line `X-Y` to a single line `...-A-B-X'-Y'`. The primes matter: X' and Y' are NEW commits with new hashes, because their parent changed. That rewriting is the whole point and the whole danger. Solution check: after rebasing, run `git log --oneline --graph` and confirm a single straight line, then run your tests — rebased code can break if main changed an API you depend on. Because hashes change, anyone else holding the old X and Y now has divergent history. Hence the golden rule of rebasing: never rebase commits that exist on a shared branch other people may have pulled. Rebase private branches freely; merge shared ones. A common safe pattern is `git pull --rebase`, which rebases only your own unpushed commits on top of what you just fetched."""
    },
    {
      "title": "Fast-forward merges: when history is already linear",
      "body": """A fast-forward is not really a merge at all — it happens when the branch you are merging is directly ahead of your current branch with no divergence. Git simply slides the branch pointer forward; no merge commit is created and no conflict is possible. Worked example: you cut a hotfix branch from main, committed one fix, and main has not moved since:

$ git checkout main
$ git log --oneline -2
4d5aa10 Deploy pipeline fix
$ git merge hotfix/timeout
Updating 4d5aa10..a91c3e2
Fast-forward
 app.py | 2 +-

Solution walkthrough: hotfix/timeout's tip a91c3e2 is a direct descendant of 4d5aa10, so Git just moves the main pointer to a91c3e2. `git log --graph` stays a straight line — there is no evidence a branch ever existed. That cleanliness is sometimes exactly what you do NOT want: for release branches or long-running feature branches, teams often prefer a merge commit marking the integration point, so the branch's scope stays visible. That is what `git merge --no-ff` is for — it forces a merge commit even when a fast-forward is possible:

$ git merge --no-ff hotfix/timeout -m "Merge hotfix/timeout: raise API timeout"

Many teams set branch policies (GitHub \"require merge commit\" or squash policies) to standardize this. Panel tip: if asked \"what is a fast-forward,\" answer with the condition — the target branch contains your branch's tip as an ancestor — not just \"it moves the pointer.\""""
    },
    {
      "title": "Resolving conflicts: one workflow for merge and rebase",
      "body": """A conflict means both sides changed the same lines (or one side deleted what the other edited) and Git cannot choose for you. The resolution workflow is identical in spirit for merges and rebases; only the command that resumes differs. Worked example: main sets `timeout = 30` while your branch sets `timeout = 60` on the same line. During `git merge`, Git stops and marks the file:

<<<<<<< HEAD
timeout = 30
=======
timeout = 60
>>>>>>> feature/login

Solution, step by step. First, `git status` to see which files are conflicted — never guess. Second, open each file and decide the correct content; here the right answer might be neither literal value but `timeout = 45` with a comment, or keeping one side. Delete the marker lines entirely. Third, `git add` the resolved files to mark them resolved. Fourth, finish: for a merge, run `git commit` (Git pre-fills the merge message — keep it); for a rebase, run `git rebase --continue` to replay the remaining commits. If you get lost, `git merge --abort` or `git rebase --abort` restores everything to the pre-operation state — aborting is always safe and is the correct answer when a rebase conflict spirals. Two professional habits: resolve conflicts in small chunks (rebase one commit at a time with `git rebase -i` when the branch is long), and after resolving, run the test suite before continuing — a \"resolved\" conflict that breaks tests is worse than an unresolved one."""
    },
    {
      "title": "Code review that catches real problems",
      "body": """A merge-request review is a correctness gate, not a style debate. Work through this checklist on every MR, in order. One: does the change do what the title claims, and nothing more? Scope creep — a \"fix timeout\" MR that also refactors logging — gets sent back. Two: are there tests, and do they fail without the fix? Three: are secrets, tokens, or credentials anywhere in the diff, including in test fixtures and config examples? A leaked secret means blocking the MR and rotating the secret, not just deleting the line. Four: dependencies — every new package needs a pinned version and a reason (see the next note). Five: backwards compatibility — does this break existing callers, configs, or stored data? Worked example of review infrastructure: a CODEOWNERS file auto-assigns the right reviewers so security-sensitive paths never slip through unreviewed:

# CODEOWNERS
/terraform/      @platform-team
/docker/         @platform-team @security-team
/requirements*.txt @platform-team

With this file, any MR touching /terraform/ automatically requests the platform team. The review verdicts are approve (ship it), comment (feedback, author decides), and request changes (do not merge until addressed) — requesting changes on an unpinned dependency or a hardcoded secret is the panel-expected answer, and you should be able to defend it out loud in under a minute."""
    },
    {
      "title": "Panel exercise: review this requirements.txt MR",
      "body": """This is the dependency-review exercise panels actually give: an MR adds a requirements.txt and you must approve or request changes. Here is an original example in that spirit. The MR adds:

requests
flask
flask-cors
asyncio
setuptools
pandas
pytest

Verdict: request changes — and here is the full solution with reasoning for each line. First, every production dependency is unpinned. Unpinned installs resolve to whatever is newest on install day, so builds are not reproducible: the artifact you tested is not the artifact you deploy. Pin with == after verifying the versions work (example pins: requests==2.32.3, flask==3.1.0, flask-cors==5.0.0, pandas==2.2.3). Second, asyncio is part of the Python standard library — listing it in requirements.txt is wrong; remove the line (pip will simply fail to find it or confuse readers). Third, setuptools is a build backend, not a runtime dependency of the application — remove it from the runtime file. Fourth, pytest is a test dependency and does not belong in the production install; move it to a separate requirements-test.txt (example pin: pytest==8.3.3) so production images stay lean and the attack surface stays small. The corrected requirements.txt is four pinned runtime lines, and the review comment lists each finding with its fix. In the panel, say the verdict first, then walk the lines — verdict-first is what interviewers score."""
    }
  ],
  "cards": [
    {"front": "What is the fundamental difference between git merge and git rebase?", "back": "Merge preserves both histories and records the join with a merge commit (two parents); rebase rewrites your commits as new commits replayed linearly on top of the target branch, producing straight-line history but changing commit hashes."},
    {"front": "State the golden rule of rebasing.", "back": "Never rebase commits that have been pushed to a shared branch other people may have pulled — rewriting public history orphans everyone else's copies."},
    {"front": "When does git merge do a fast-forward instead of creating a merge commit?", "back": "When the branch being merged is directly ahead of the current branch (your tip is an ancestor of its tip) — Git just slides the pointer forward with no new commit."},
    {"front": "How do you force a merge commit when a fast-forward is possible?", "back": "git merge --no-ff <branch> — used to keep an explicit integration marker for release or feature branches."},
    {"front": "What do the <<<<<<<, =======, >>>>>>> markers in a conflicted file mean?", "back": "They delimit the two competing versions: content between <<<<<<< HEAD and ======= is your current branch's version; between ======= and >>>>>>> is the incoming branch's version."},
    {"front": "After resolving rebase conflicts, which command continues the rebase? How do you bail out?", "back": "git rebase --continue resumes replaying commits; git rebase --abort restores the branch to its pre-rebase state safely."},
    {"front": "What is a CODEOWNERS file and why does it matter?", "back": "It maps file paths to owning teams/users so the right reviewers are auto-requested on every MR — ensuring security-sensitive paths (Terraform, Docker, dependencies) are never merged unreviewed."},
    {"front": "An MR adds unpinned dependencies (e.g. a bare 'flask' line). Approve or request changes?", "back": "Request changes — unpinned versions make builds non-reproducible; pin every runtime dependency with == after verifying."},
    {"front": "An MR's requirements.txt lists 'asyncio'. What is your review finding?", "back": "asyncio is in the Python standard library and must not be a pip requirement — remove the line."},
    {"front": "An MR puts pytest in the production requirements.txt. What do you require?", "back": "Move it to a separate test requirements file — test tooling does not belong in the production install (leaner images, smaller attack surface)."},
    {"front": "What does git pull --rebase do, and why is it safe?", "back": "It fetches, then replays only your own unpushed local commits on top of the fetched tip — safe because it never rewrites commits anyone else has."},
    {"front": "You find a hardcoded API secret in an MR diff. What are the correct actions?", "back": "Block the MR (request changes), rotate/revoke the exposed secret immediately, and purge it from history — deleting the line alone is not enough since history retains it."}
  ],
  "quiz": [
    {"q": "Panel question: what is the biggest difference between rebase and merge?", "choices": ["Rebase is faster because it skips conflict detection", "Merge rewrites commit hashes while rebase preserves them", "Rebase replays commits as new commits for linear history; merge preserves both histories with a merge commit", "They are identical; rebase is just an alias for merge"], "answer": 2, "explain": "Rebase rewrites your commits (new hashes) onto the target tip for a straight line; merge keeps every original commit and records the join point with a two-parent merge commit."},
    {"q": "Which statement about the golden rule of rebasing is correct?", "choices": ["Never rebase on Fridays", "Never rebase commits pushed to a shared branch others may have pulled", "Always rebase main into your branch before pushing", "Rebase is only allowed with --force"], "answer": 1, "explain": "Rewriting public history orphans collaborators' copies; rebase is for private branches, merge is for shared ones."},
    {"q": "git merge reports 'Fast-forward'. What does that tell you?", "choices": ["A merge commit was created", "There were conflicts auto-resolved", "Your branch tip was an ancestor of the merged branch, so Git just moved the pointer", "The merge was rejected by branch policy"], "answer": 2, "explain": "Fast-forward means no divergence existed — the merged branch was directly ahead, so no merge commit was needed."},
    {"q": "During a rebase you hit a conflict, resolve the file, and stage it. What next?", "choices": ["git commit to finish", "git rebase --continue to replay remaining commits", "git push --force immediately", "git merge --abort"], "answer": 1, "explain": "Staging marks the conflict resolved; --continue resumes replaying the rest of your commits onto the new base."},
    {"q": "What is the purpose of a CODEOWNERS file?", "choices": ["To list who wrote each line of code", "To auto-request the right reviewers for sensitive paths on every MR", "To assign merge permissions in the CI pipeline", "To document the team's on-call rotation"], "answer": 1, "explain": "CODEOWNERS maps paths to owning teams so Terraform, Docker, and dependency changes always get expert review."},
    {"q": "An MR adds requirements.txt containing a bare 'requests' line with no version. Your verdict?", "choices": ["Approve — pip always picks the safest version", "Approve with a comment suggesting a version someday", "Request changes — pin with == for reproducible builds", "Request changes — requests is deprecated"], "answer": 2, "explain": "Unpinned dependencies resolve differently on different days, so the tested artifact may not match the deployed one; pin versions."},
    {"q": "The same MR lists 'asyncio' as a requirement. What do you tell the author?", "choices": ["Pin it like the others", "Remove it — asyncio ships with Python's standard library", "Move it to the test requirements", "Approve — explicit is better than implicit"], "answer": 1, "explain": "asyncio is stdlib; listing it as a pip dependency is incorrect and will confuse or break installs."},
    {"q": "The MR includes 'pytest' in the production requirements.txt. What is the right fix?", "choices": ["Pin pytest and keep it — tests run in production", "Remove pytest entirely — testing is optional", "Move pytest to a separate test requirements file", "Replace pytest with unittest"], "answer": 2, "explain": "Test dependencies belong in a separate requirements-test.txt so production images stay lean with a smaller attack surface."},
    {"q": "Your teammate rebased the shared main branch and force-pushed. What is the consequence?", "choices": ["Nothing — Git auto-heals on the next pull", "Everyone else's local main now diverges; they must recover (e.g. re-clone or reset to the new upstream)", "The old commits are permanently deleted from the server", "CI pipelines run twice as fast"], "answer": 1, "explain": "Rewriting shared history orphans every collaborator's copy — this is exactly what the golden rule forbids."}
  ],
  "weight": 1,
  "prerequisiteFor": ["IL28-M37"],
  "drills": [
    {
      "id": "il28-m17-rebase-merge-panel",
      "title": "Rebase vs merge — panel drill",
      "items": [
        {"prompt": "Panel: 'Explain rebase versus merge to me.' Give the 60-second answer.", "answer": "Merge joins two histories with a merge commit that has two parents, preserving every original commit and hash — safe for shared branches but leaves a busier graph. Rebase replays my commits as brand-new commits on top of the target branch, giving linear history, but it rewrites hashes, so it is only for private branches.", "explain": "Hits the four scoring points: merge commit/two parents, hash preservation, rebase replay/new hashes, and the private-vs-shared rule."},
        {"prompt": "State the golden rule of rebasing and the reason behind it.", "answer": "Never rebase commits pushed to a shared branch others may have pulled, because rewriting public history orphans every collaborator's copy and forces painful recovery.", "explain": "The rule plus the mechanism (orphaned copies) is the complete panel answer."},
        {"prompt": "When is git merge a fast-forward, and when would you use --no-ff?", "answer": "Fast-forward happens when the merged branch is directly ahead with no divergence — Git just moves the pointer. Use --no-ff to force a merge commit that marks the integration point, e.g. for release branches where you want the branch scope visible in history.", "explain": "Condition first (ancestor check), then the deliberate --no-ff use case."},
        {"prompt": "What does git pull --rebase do, and why is it considered safe?", "answer": "It fetches remote changes, then replays only my own unpushed local commits on top of the fetched tip. It is safe because it never rewrites commits anyone else has — only my private, unpushed work.", "explain": "Distinguishes private unpushed commits (safe to rewrite) from public ones."},
        {"prompt": "Mid-rebase you hit a conflict. List the exact recovery commands.", "answer": "git status to identify conflicted files, edit and resolve, git add to mark resolved, git rebase --continue to resume — or git rebase --abort at any point to restore the pre-rebase state.", "explain": "The full loop including the abort escape hatch shows practiced experience."},
        {"prompt": "Your feature branch is private and main moved ahead. Rebase or merge main in — and why?", "answer": "Rebase the private branch onto the updated main: it keeps history linear, surfaces integration issues against the latest code, and the golden rule is satisfied because the branch is private.", "explain": "Applies the decision rule rather than reciting definitions."},
        {"prompt": "Why do many teams merge (not rebase) release branches into main?", "answer": "The merge commit permanently marks where the release line integrated, preserving the true topology of what shipped together — rebasing would flatten that record away.", "explain": "Shows judgment about history as documentation, not just mechanics."}
      ]
    },
    {
      "id": "il28-m17-mr-review",
      "title": "MR review drill",
      "items": [
        {"prompt": "What does a CODEOWNERS entry '/terraform/ @platform-team' guarantee?", "answer": "Every MR touching /terraform/ automatically requests review from the platform team, so infrastructure changes cannot merge without expert eyes.", "explain": "The value is automatic, path-scoped reviewer assignment."},
        {"prompt": "MR adds requirements.txt with unpinned 'flask'. Verdict and reason?", "answer": "Request changes: unpinned versions make builds non-reproducible — pin with == after verifying the versions.", "explain": "Reproducibility is the core argument panels expect."},
        {"prompt": "The same file lists 'asyncio'. Your review comment?", "answer": "Remove it — asyncio is part of the Python standard library, not a pip package.", "explain": "Tests whether the reviewer knows stdlib from third-party."},
        {"prompt": "The file lists 'setuptools' as a runtime dependency. Your finding?", "answer": "Remove it from the runtime file — setuptools is a build backend, not something the application needs at runtime.", "explain": "Distinguishes build-time from runtime dependencies."},
        {"prompt": "Where should 'pytest' live, and why not in production requirements?", "answer": "In a separate requirements-test.txt — test tooling in the production install bloats images and widens the attack surface for no runtime benefit.", "explain": "Separation of test and runtime dependency sets."},
        {"prompt": "You spot a hardcoded AWS secret key in the MR diff. Exact actions?", "answer": "Request changes to block the merge, rotate/revoke the exposed key immediately, and purge it from Git history — deleting the line is insufficient.", "explain": "Block + rotate + purge; history retains anything merely deleted."},
        {"prompt": "When do you choose 'request changes' over 'comment' on an MR?", "answer": "Request changes when the MR must not merge as-is — unpinned dependencies, secrets, missing tests, scope creep. Comment when the feedback is advisory and the author can decide.", "explain": "Shows the reviewer understands the verdict as a merge gate."}
      ]
    }
  ],
  "handsOnLab": {
    "id": "il28-m17-lab",
    "title": "Branch, conflict, rebase, and review",
    "brief": "You will build a small Git repository from scratch, create a merge conflict and resolve it, rebase a private branch onto a moved main, enforce review ownership with CODEOWNERS, and produce a pinned requirements.txt from an unpinned MR-style starting point.",
    "steps": [
      "Create the lab repo: run mkdir branching-lab && cd branching-lab && git init -b main, then git config user.name 'Lab Learner' and git config user.email 'learner@example.com'.",
      "Commit a starting point: create app.py containing 'timeout = 30' on one line, then git add app.py && git commit -m 'Set default API timeout'.",
      "Create a feature branch: git checkout -b feature/timeout, change the line to 'timeout = 60', commit with message 'Raise timeout for slow endpoint'.",
      "Divert main: git checkout main, change the same line to 'timeout = 45  # tuned per load test', commit as 'Tune timeout per load test'.",
      "Merge and resolve: run git merge feature/timeout, observe the conflict, open app.py, replace the marker block with your chosen final value, git add app.py, then git commit (accept the default merge message).",
      "Verify the merge commit: run git log --graph --oneline and confirm a merge commit with two parents exists.",
      "Rebase exercise: git checkout -b feature/retry, add a line 'retries = 3' to app.py and commit; then git checkout main, append '# main moved' comment line and commit; then git checkout feature/retry && git rebase main, and confirm git log --oneline --graph shows a straight line.",
      "Force a merge commit: git checkout main && git merge --no-ff feature/retry -m 'Merge feature/retry', then confirm the merge commit exists even though fast-forward was possible.",
      "Add review ownership: create a CODEOWNERS file mapping '/app.py' to your username and any '*.txt' to a second reviewer name.",
      "Produce the pinned file: write requirements-v1.txt with unpinned lines (requests, flask, flask-cors, asyncio, setuptools, pandas, pytest), then write the corrected requirements.txt (pinned runtime deps only) and requirements-test.txt, and save a diff or notes file review-notes.md with your verdict and per-line reasoning."
    ],
    "deliverable": "A local Git repo containing the merge commit, the rebased linear section, the --no-ff merge commit, a CODEOWNERS file, requirements-v1.txt, the corrected requirements.txt + requirements-test.txt, and review-notes.md with the verdict.",
    "checkpoint": "git log --graph --oneline shows both a merge commit and a straight rebased section; requirements.txt has no asyncio/setuptools/pytest lines and every runtime dep is pinned with ==; review-notes.md states 'request changes' with per-line reasons."
  },
  "mockTask": {
    "id": "il28-m17-mock",
    "type": "choice",
    "q": "Panel: your feature branch is private, main has moved ahead, and you are about to open an MR. What do you do?",
    "choices": ["Merge main into the branch to keep all history, then open the MR", "Rebase the branch onto the updated main, run tests, then open the MR", "Force-push the branch onto main and skip the MR", "Open the MR first and let CI resolve the divergence"],
    "answer": 1,
    "explain": "The branch is private so the golden rule is satisfied; rebasing gives a clean linear history and validates the code against the latest main before review. Merging main in is for shared branches; force-pushing to main and skipping review are both disqualifying answers."
  },
  "crossLinks": [],
  "videos": [
    {"title": "Git and GitHub for Beginners – Crash Course", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "source": "freeCodeCamp.org (YouTube)", "durationMin": 68, "order": 1, "watchBefore": "notes", "blurb": "Full beginner-to-productive Git course covering branching, merging, and the GitHub pull-request workflow this module builds on."}
  ],
  "estimatedMinutes": 0
}
