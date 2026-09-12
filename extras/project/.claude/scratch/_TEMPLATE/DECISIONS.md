# DECISIONS — <slug>

> **Append-only, and read before any change.** This file exists to stop the loop where
> two rounds keep reversing each other's fix.
>
> **Every agent reads this before editing anything.** If a change would reverse a decision
> recorded here, the agent **stops and reports the conflict** instead of reversing it.
> Sorting out contradictory decisions is the orchestrator's job, together with you.

---

### D001 — <the decision, as an imperative>   <!-- D001, D002, ... in order -->
- **When:** <YYYY-MM-DD HH:MM>
- **Decided by:** <me / orchestrator / brief <file>>
- **Chose:** <what we are doing>
- **Rejected:** <the alternative that was actually on the table>
- **Why:** <the reason — this is the part that stops it being undone by accident>
- **Reverses:** <the number of an earlier decision, or `nothing`>
- **Touches:** `path/to/file.ext`
- **Would be wrong if:** <the condition that should make someone reopen this>

---

<!--
Loop-breaker rule:
If a decision reverses an earlier one, and a later decision reverses it back, STOP. Do not
write a third.
Two reversals of the same question means the question was never settled — take it to the
operator with both reasons side by side.
-->
