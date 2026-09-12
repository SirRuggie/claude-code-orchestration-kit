---
description: Write a scoped agent brief into the task bucket and dispatch the agent
argument-hint: <task-slug> <agent> <objective>
allowed-tools: Bash, Read, Write, Glob, Agent
---

Write and dispatch a brief for: **$ARGUMENTS**

First word is the task slug (the bucket's folder name), second is the agent (`scout`, `researcher`, `builder`,
`refuter`, `debugger`), the rest is the objective.

## 1. Write the brief file first

Save to `.claude/scratch/<slug>/briefs/<agent>-NN.md` (NN = next unused number).
The file is the agent's authoritative scope. **It is written before the agent is
spawned and it is never edited afterwards** — the reviewer grades against these exact
words, so a brief that moves is a review that means nothing.

Create it with a Bash heredoc, then make it read-only, so no agent can quietly change
its own instructions:

```bash
mkdir -p .claude/scratch/<slug>/briefs
cat > .claude/scratch/<slug>/briefs/<agent>-NN.md <<'BRIEF'
...content...
BRIEF
# Windows:
attrib +R ".claude\scratch\<slug>\briefs\<agent>-NN.md"
# macOS / Linux:
# chmod a-w .claude/scratch/<slug>/briefs/<agent>-NN.md
```

The Write and Edit tools are denied on `briefs/**` by `.claude/settings.json`, and
removing the read-only flag needs approval. The flag stops accidental edits. If the brief
genuinely has to change, that is a **new numbered brief**, never an edit to the old one.

Use the six-section brief format defined in `~/.claude/CLAUDE.md` — CURRENT STATE /
DO NEXT / DO NOT / CONTEXT / SUCCESS / STOP, plus the output budget. That file is the
single definition; do not restate it here.

## 2. Show me the brief

Print it and wait for my go, unless I have already approved this exact scope.

## 3. Dispatch

Spawn with the agent type from the roster; its model is pinned in its file. Pass a model
explicitly only for an off-roster agent — never inherit the orchestrator's model. Pass the
brief file path plus the brief body.

Record the launch in `STATE.md` under **Active agents**: agent, brief file, launch time,
what ends it.

## 4. On return

- Write `reports/<agent>-NN.md` if the agent did not.
- Mark the agent terminal in `STATE.md`.
- **Every brief must end with a report.** A brief with no report is UNKNOWN, never zero —
  that check never happened and nobody was told.
