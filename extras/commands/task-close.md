---
description: Close a task bucket — roll its durable content into the project handoff and archive it
argument-hint: <task-slug>
allowed-tools: Bash, Read, Write, Glob
---

Close the task bucket: **$ARGUMENTS**

## 1. Refuse to close a bucket that is not finished

Run `/task-status` first. **Do not close** if any of these is true —
report which one and stop:

- The agent accounting does not balance (`launched ≠ terminal + running + unknown`).
- Any brief has no report.
- `STATE.md` lists an open question or blocker that has not been answered.
- The last refuter verdict was `REWORK` and no later `ACCEPT` exists.

## 2. Roll forward what outlives the task

Into the project handoff (`docs/HANDOFF.md`, or the project's equivalent):
- What changed and why — one or two lines, not a session log.
- Decisions that constrain future work.
- Anything left unresolved, with its evidence and the next concrete action.
- Verification that actually ran, **with its real numbers**, and anything SKIPPED.

Into the project's backlog:
- Every deferred fix, investigation, verification and user dependency found during the
  task. Update an existing entry rather than creating a duplicate.
- Each entry carries: scope, current evidence, one concrete next action, and its closure
  condition or blocker.

**Recording is not execution.** Writing a deferred action down never authorizes doing it.

## 3. Archive

- Set `STATE.md` status to `CLOSED <date>` with a two-line outcome summary.
- Move `.claude/scratch/<slug>/` to `.claude/scratch/_closed/<slug>/`.
- Never delete a bucket — the reports are how anyone later reconstructs what was checked.

## 4. Confirm

Tell me in one line that the follow-ups were recorded and where. **If any write failed,
say so** — never claim it is saved when it is not.
