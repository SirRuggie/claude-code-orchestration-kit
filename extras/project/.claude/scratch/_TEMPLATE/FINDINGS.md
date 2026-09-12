# FINDINGS — <slug>

> **Append-only.** One entry per finding, newest at the bottom. Findings land here **when
> they are discovered**, not at the end of a session — a finding held in a session is a
> finding lost when the session ends.
>
> Every entry cites `file:line` and names what tested it. "Nothing tested this" is a
> valid and required answer when it is true.

---

### F001 — <short title>   <!-- F001, F002, ... in order -->
- **Found by:** <agent / brief file / me>
- **Where:** `path/to/file.ext:LINE`
- **What:** <1–2 sentences. The defect or fact, not the story of finding it.>
- **Evidence:** <exact command and exact output, or the quoted line>
- **Checked by:** <what tested this — a run, a test, a doc, or `nothing tested this`>
- **Class:** STOP | LOG | DEFER
  - `STOP` — can cause a wrong or unsafe result, a false success, silent loss, or an
    unrecorded failure. Blocks release. Must be fixed **and** verified.
  - `LOG` — a real defect that cannot produce a wrong or unrecorded result. Record and
    move on.
  - `DEFER` — real and structural, too large for now. Record the fix shape, its risk, and
    **the condition that would promote it to STOP**.
  - `UNKNOWN` — not yet classified. **Treat as STOP** until classified: an unclassified
    finding cannot be shown harmless. Investigate only far enough to classify it.
- **Sweep:** <a fix in one place is a bug report about everywhere else — what class does
  this belong to, where did you search for the rest of it, and what did you find?
  Including "nothing". An unstated sweep did not happen.>
- **Status:** open | fixed in <commit> | deferred → <backlog ref>
