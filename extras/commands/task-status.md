---
description: Compare a task bucket against the repo and the agent list, and report the true state
argument-hint: [task-slug]
allowed-tools: Bash, Read, Glob
---

Compare and report the real state of: **$ARGUMENTS**

With no slug, do this for every folder under `.claude/scratch/` whose `STATE.md` says
`OPEN`.

## Compare — in this order

1. **Repo vs. record.** Compare `STATE.md`'s recorded branch, HEAD and dirty-tree state
   against `git rev-parse --abbrev-ref HEAD`, `git rev-parse --short HEAD`,
   `git status --short`. **The repo wins.** Correct the file and say that you corrected
   it — a silent fix hides how long the wrong claim was relied on.
2. **Briefs vs. reports.** Every file in `briefs/` must have a matching file in
   `reports/`. List any brief without a report as **UNREPORTED**.
3. **Agents launched vs. agents terminal.** The identity must balance and the buckets
   must be disjoint:

   ```
   launched = terminal + running + unknown
   ```

   Take `launched` from `STATE.md`'s Active agents list — the **declared** population.
   Never infer it from what happens to have reported: "zero observed" is the exact shape
   of "the record never got written." Anything you cannot place is **unknown**, never
   zero.
4. **Decisions vs. code.** Spot-check the two most recent entries in `DECISIONS.md`
   against the current code. Report any that no longer hold.

## Report — under 150 words

```
## STATUS
- Objective: <one line>
- Repo: branch <x> @ <sha>, tree <clean|N dirty> — record was <accurate|corrected>
- Agents: launched N = terminal N + running N + unknown N   <balances / DOES NOT BALANCE>
- Unreported briefs: <list, or none>
- Settled: <bullets>
- Open: <bullets>

## NEXT
- <the single next action>

## NEEDS ME
- <human decisions or authorizations, or none>
```

If the accounting does not balance, say `INCOMPLETE` and put it first. Do not round an
unknown down to zero to make it balance.
