---
description: Task dashboard. With no words, lists every bucket and its next action. With a sentence, continues the matching bucket or opens a new one.
argument-hint: [what you want to do, in one sentence]
allowed-tools: Bash, Read, Write, Glob
---

Task request: **$ARGUMENTS**

A bucket is the folder `.claude/scratch/<slug>/` for one task. The index file
`.claude/scratch/INDEX.md` lists every bucket. Rules for buckets are in `CLAUDE.md`.

## 1. Read the index

If `.claude/scratch/INDEX.md` does not exist, create it with exactly this content:

```markdown
# Task index
<!-- One line per bucket. Claude updates this whenever a bucket changes. -->
| slug | status | updated | next action |
|---|---|---|---|
```

Status is one of: OPEN, BLOCKED (waiting on me), DONE.

## 2. No words given: show the dashboard

Read the index. Report under 120 words:
- OPEN buckets with their next action.
- BLOCKED buckets and what they wait for.
- Anything marked DONE since the last session.

Then ask: continue one of these, or start something new?

## 3. A sentence given: continue or open

Compare the sentence to the OPEN and BLOCKED buckets.
- Same objective as an existing bucket: continue it (step 5).
- A different objective: open a new bucket (step 4), even if it touches the same files.
- Not sure: ask one question, "New task, or part of <slug>?", and wait.

## 4. Open a new bucket

1. Make the slug from the sentence: 2 to 4 words, lowercase, digits and hyphens only.
   "fix the ACL permission on the share page" becomes `acl-share-permission`.
2. Create `.claude/scratch/<slug>/` with these files and folders:

```
.claude/scratch/<slug>/
  STATE.md        replaced each update — what is true NOW
  FINDINGS.md     append-only — evidence, file:line
  DECISIONS.md    append-only — what changed and WHY
  briefs/         orders given to agents; written once, never edited
  reports/        one per brief
```

3. Seed the three files with exactly these headings and nothing else:

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

4. Add one line for the bucket to the index.
5. Tell me in one line: "Opened bucket <slug>." Then show the objective and the proposed
   scope in and out. **Wait for me to confirm the scope** before spawning anything.

## 5. Continue a bucket

1. Read `STATE.md`, the tail of `DECISIONS.md`, then `FINDINGS.md`.
2. **Verify before trusting.** Check the recorded branch and HEAD against
   `git rev-parse --abbrev-ref HEAD`, `git rev-parse --short HEAD`, `git status --short`.
   Where the file and the repo disagree, **the repo is right**: correct the file and say
   that you corrected it.
3. Check `briefs/` against `reports/`. **Every brief must have a report.** A brief with no
   report means that agent never reported. List it as UNKNOWN, never as "nothing found".
4. Report under 120 words: objective, what is settled, what is open, unreported briefs,
   and the single next action. Then do the next action.

## While a bucket is open

- Write every brief to `briefs/<agent>-NN.md` before spawning, using a Bash heredoc
  (the optional project `settings.json` denies the Write tool there). NN counts up from 01.
  Make it read-only (`attrib +R` on Windows, `chmod a-w` elsewhere). Do not show me
  briefs unless I ask.
- Every brief must name the bucket and require the agent to read `DECISIONS.md` before
  changing anything, update `FINDINGS.md`, `DECISIONS.md` and `STATE.md`, write
  `reports/<agent>-NN.md` before it stops, and never edit anything under `briefs/`.
- Record the launch in `STATE.md` under Active agents. When the agent returns, mark it
  terminal. If it left no report, write `reports/<agent>-NN.md` yourself and say so.
- Update the bucket's line in the index whenever its status or next action changes.
- If two rounds start swapping between the same two fixes, **stop the loop**, read
  `DECISIONS.md` yourself, and sort it out with me. Do not let it run.

## Closing

When the objective is met (last refuter verdict is ACCEPT and nothing is open in
`STATE.md`), or I say the task is abandoned:

1. Set `STATE.md` status to `CLOSED <date>` with a two-line outcome summary.
2. Write anything that outlives the task into the project's handoff note and backlog
   (see the project `CLAUDE.md`). Recording a follow-up never authorizes doing it.
3. Move `.claude/scratch/<slug>/` to `.claude/scratch/_closed/<slug>/`. Never delete a
   bucket.
4. Mark the bucket DONE in the index. Tell me in one line.

Do not close if any brief has no report, or if the agent count in `STATE.md` does not
balance (`launched = terminal + running + unknown`). Say which, and stop.
