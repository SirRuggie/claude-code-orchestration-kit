# REPORT <agent>-NN — <slug>   <!-- NN = the brief's number -->

**Brief:** `briefs/<agent>-NN.md`
**Agent / model:** <name> / <model>
**Outcome:** SUCCESS | REWORK | BLOCKED | FAILED

> Every brief must end with one of these files. A brief with no report is **UNKNOWN**,
> never zero — it means that check never happened and nobody was told.

## VERDICT
<one line. A failure is never buried under completed work.>

## FOUND / CHANGED
- `path:LINE` — <what, one line>

## VERIFICATION
| Check | Command | Result |
|---|---|---|
| <name> | `<exact command>` | `<exact counts>` / SKIPPED — <why> |

- A check that did not run is **SKIPPED**, never passed.
- "Executed" is not "correct" — say which one you have.
- Every number states what it counts.

## NOT DONE
- <anything in scope left incomplete, and why>

## DEVIATIONS
- <anywhere this differs from the brief, and why>

## NEED-TO-KNOW
- <at most 3 things the orchestrator must know that it did not ask for>

## OPERATOR ACTIONS
- <what needs a human, or `none`>

## BLOCKERS
- <what stopped you, or `none`>
