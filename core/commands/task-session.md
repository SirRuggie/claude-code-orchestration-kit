---
description: Create or resume a task context bucket that every agent on this task reads and updates
argument-hint: <task-slug> [one-line objective]
allowed-tools: Bash, Read, Write, Glob
---

Open a task context bucket for: **$ARGUMENTS**

First word is the slug (a short folder-safe name: lowercase, numbers, hyphens, no spaces).
The rest is the objective.

## If `.claude/scratch/<slug>/` does not exist — create it

```
.claude/scratch/<slug>/
  STATE.md        replaced each update — what is true NOW
  FINDINGS.md     append-only — evidence, file:line
  DECISIONS.md    append-only — what changed and WHY
  briefs/         orders given to agents; written once, never edited
  reports/        one per brief
```

Seed the three files with exactly these headings and nothing else:

**STATE.md**
```markdown
# STATE — <slug>
<!-- REPLACED, never appended. History lives in FINDINGS/DECISIONS and git. -->
Updated: <date>   Status: OPEN
## Objective
## Repo
branch <x> @ <sha>, tree clean|N dirty
## Scope — in
## Scope — out
## Current subtask
## Next action
## Active agents
| agent | brief | launched | ends when | running/terminal/unknown |
## Open questions
## Blockers
```

**FINDINGS.md**
```markdown
# FINDINGS — <slug>
<!-- Append-only. Land here WHEN DISCOVERED, not at end of session. -->
<!-- Each: what · file:line · evidence · what tested it (or "nothing tested this") -->
```

**DECISIONS.md**
```markdown
# DECISIONS — <slug>
<!-- Append-only. READ BEFORE ANY CHANGE. -->
<!-- Each: chose · rejected · WHY · reverses D0NN (an earlier decision's number) or nothing · files touched -->
```

Then show me the bucket path, the objective, and your proposed scope in/out. **Stop and
wait for me to confirm the scope** before spawning anything.

## If it already exists — resume it

1. Read `STATE.md`, the tail of `DECISIONS.md`, then `FINDINGS.md`.
2. **Verify before trusting.** It is a report, not proof — check its branch/HEAD against
   `git rev-parse --abbrev-ref HEAD`, `git rev-parse --short HEAD`, `git status --short`.
   Where the file and the repo disagree, **the repo is right**: correct the file and say
   plainly that you corrected it.
3. Check `briefs/` against `reports/`. **Every brief must have a report.** One without a
   report means that agent never reported — list it as UNKNOWN, never as nothing found.
4. Report under 120 words: objective, what is settled, what is open, unreported briefs,
   and the single next action.

## While this bucket is open

Every brief you write must name the bucket and require the agent to:
- **Read `DECISIONS.md` before changing anything.** If a change would reverse a decision
  recorded there, **stop and report the conflict** — do not reverse it.
- Update `FINDINGS.md`, `DECISIONS.md`, `STATE.md` and write `reports/<agent>-NN.md`
  (NN = the brief's number) before it stops.
- Never edit anything under `briefs/`.

Write each brief to `briefs/<agent>-NN.md` **before** spawning, using a Bash heredoc
(the optional project `settings.json` denies the Write tool there). Then make it read-only
(`attrib +R` on Windows, `chmod a-w` elsewhere) to stop accidental edits.

If two rounds start swapping between the same two fixes, **stop the loop**, read
`DECISIONS.md` yourself, and sort it out with me. Do not let it run.
