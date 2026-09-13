# <PROJECT NAME> — working rules

Repo-specific rules only. General orchestration, model routing, agent roster, brief
format and reporting rules live in `~/.claude/CLAUDE.md` and apply here too.

Keep this file about **this codebase**: how to build it, how to test it, what is
dangerous in it, and what it has already got wrong.

---

## Commands

Fill these in. Agents run exactly what is written here, so a wrong command becomes a
false pass.

| Purpose | Command |
|---|---|
| Install | `<...>` |
| Build | `<...>` |
| Full test suite | `<...>` |
| Single test | `<...>` |
| Lint / format | `<...>` |
| Type check | `<...>` |

- The **full test suite** is what a refuter reruns. It must be runnable from a clean
  checkout with no manual setup.
- If a command needs credentials or network access an agent does not have, say so here
  and name what the agent should report instead of a pass.

## Layout

```
<dir>/     <one line — what lives here>
<dir>/     <one line>
```

Name the three or four files most changes touch, so scouts start in the right place.

## Conventions

- <language/version, formatter, import style — only where it is not obvious from the code>
- New code matches the file it lands in: naming, idiom, comment density.

## Danger list

The things in this repo that cause real damage. One line each, direct.

- `<path>` — <what goes wrong if this is changed carelessly>
- <any command that writes to a live system, and who must authorize it>
- <any generated file that must not be hand-edited>

## Authorization

- I authorize: deploys, production writes, migrations, anything touching a live system.
  An agent that believes it needs one of these **stops and reports**.

## Task buckets

Multi-agent work in this repo uses buckets under `.claude/scratch/<slug>/`, opened by
Claude when a new task starts, or by `/task <sentence>`. Buckets are git-ignored; nothing operational, no credentials
and no production data goes in them, or in any tracked doc.

## Handoff

`docs/HANDOFF.md` (create it if it does not exist) is the current session state — **read
it at session start and verify it before relying on it.** Check its recorded branch, HEAD and dirty-tree state against the
repo, and spot-check the claims you are about to act on. Where the handoff and the repo
disagree, **the repo is right**: correct the handoff and say plainly that you corrected it.

Replace stale state; do not append a session log. Keep it under ~100 lines — a handoff
nobody finishes reading is a handoff nobody reads.

Record: timestamp, branch, exact HEAD, dirty-tree state, current objective, material
changes, verification that actually ran with its real numbers, checks that did not run or
failed, unresolved decisions, known risks, the recommended next action, and what needs a
human.

## Backlog

Before ending any response, every newly identified later action, deferred fix,
investigation or dependency goes in `docs/BACKLOG.md` (create it if it does not exist).
Update the existing entry rather
than duplicating it. A chat message is not a record. Confirm to me that it was recorded;
if recording failed, say that instead of claiming it is saved.

## Past defects — what this repo has already got wrong

Every entry is a rule added after a real defect, not a principle someone liked. Add to it whenever
a defect escapes review; the refuter reads this list.

| # | Defect | Rule it earned |
|---|---|---|
| 1 | <what happened> | <the check that now catches it> |
