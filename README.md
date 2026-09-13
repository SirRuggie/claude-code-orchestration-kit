# Claude Code orchestration kit

## What this is

By default, every subagent runs on the same model as your main session, inherits its
effort level, and can spawn subagents of its own. Fable spawning Fable to run a grep is
how a week of quota disappears in a day.

This kit fixes that. The main session is the orchestrator: it plans, writes briefs,
reviews, and verifies. It never edits code. Five subagents do the work. Each one has a
pinned model, a pinned effort level, and a fixed tool list, and none of them can spawn
another subagent.

A **brief** is the written task each subagent receives: what to do, what not to do, and
the exact condition that means it is done.

A **bucket** is the folder that holds everything about one task: its briefs, reports,
findings, and decisions. Its name is a **slug**: a short name with no spaces, only
lowercase letters, numbers, and hyphens, so it is safe as a folder name. Example: `bug-42`.

## Install

```bash
mkdir -p ~/.claude/agents ~/.claude/commands
cp core/CLAUDE.md     ~/.claude/CLAUDE.md      # ⚠ replaces your existing file. Compare first.
cp core/agents/*.md   ~/.claude/agents/
cp core/commands/*.md ~/.claude/commands/
```

| File | What it is |
|---|---|
| `core/CLAUDE.md` | The rules. This is the only place that defines the brief format (six sections), the bucket, and the rule that every agent has a pinned model. |
| `core/agents/` | The five agents, one file each: scout `haiku`, researcher `sonnet`, builder `sonnet`, refuter `opus`, debugger `opus`. Each file pins the model, the **effort**, and the tools. |
| `core/commands/task.md` | `/task` shows every open task. `/task <sentence>` continues one or starts a new one. |

The **Response contract** section at the top of `core/CLAUDE.md` is one person's reply
preferences (answer length, troubleshooting order). Edit it to match yours.

## The five agents

| Agent | Model | What it does | What it cannot do |
|---|---|---|---|
| scout | haiku, `effort: low` | Finds where things are in the code. | Cannot edit. Returns file paths only, never file contents. |
| researcher | sonnet, `effort: medium` | Answers a question from docs or source, with citations. | Cannot edit. |
| builder | sonnet, `effort: medium` | Writes the code and runs the tests. | The only agent with Edit and Write. |
| refuter | opus, `effort: high` | Reviews the builder's change and tries to find what is wrong with it. | Has no Edit or Write tool. It reports problems, it does not fix them. |
| debugger | opus, `effort: high` | Finds the real cause of a hard bug and proves it. | Has no Edit or Write tool. It explains, it does not fix. |

The normal loop is: **you plan → builder builds → refuter checks → you decide.**

**None of the five can spawn a subagent.** The `Agent` tool is not in any of their
tool lists, so it does not exist for them. This is enforced, not just requested. For any
other subagent you start, set this once so it cannot spawn either. In a terminal:

```bash
export CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1
```

In the desktop app there is no terminal, so put it in `~/.claude/settings.json` instead:

```json
{ "env": { "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1" } }
```

The extras `settings.json` sets the same value for a repo. After installing, test it once:
spawn a subagent and ask it whether it has the `Agent` tool. It should say no.

## Your first task

You do not name tasks or run a command for each step. You say what you want, and Claude
keeps the bookkeeping.

1. In your repo, type `/task fix the broken menu on the settings page`. Claude opens a
   bucket for it, names it `broken-settings-menu`, shows the scope, and waits for your go.
2. Claude writes a brief for the builder and spawns it. You do not see the brief unless you
   ask. The builder makes the change, runs the tests, and writes a report.
3. Claude spawns the refuter with the same brief. The refuter reads the code change, reruns
   the tests, and answers ACCEPT or REWORK with a list of must-fix items.
4. On REWORK, Claude writes a new brief with the must-fix list and goes back to step 2.
   On ACCEPT, Claude closes the bucket and tells you in one line.
5. Say the next thing: "now the time display is wrong". Claude sees it is a different
   task, opens a new bucket, and starts again. Ten tasks in a day means ten buckets. You
   named none of them.

Tomorrow, type `/task` with nothing after it. Claude lists every bucket, what is open,
what is blocked on you, and the next action for each.

## Where the files go

There are two places. The rule: **your personal habits go in your home folder. Facts
about a project go in that project's repo.**

### Home folder: `~/.claude/` (only you, every project)

| File | Why here |
|---|---|
| `CLAUDE.md` | Loaded automatically in every session and into every subagent. Your rules follow you to every repo. |
| `agents/*.md` | The five agents from the table above. One file each, so each one's tool list is enforced. |
| `commands/task.md` | Defines `/task`. The dashboard for every bucket. |

These files describe how *you* like to work. They say nothing about any codebase, so they
do not belong in a repo.

### The repo: `<project>/`

| File | Why here | Commit it? |
|---|---|---|
| `CLAUDE.md` | How to build and test this code, its layout, and what is dangerous in it. Every teammate and every agent needs this. | **Yes** |
| `.claude/settings.json` | Permission rules for this repo. | **Yes** |
| `.claude/scratch/<task>/` | Working notes for one task. Nobody else needs them. | **No — add it to .gitignore** |

Simple test: if a new teammate would need the file, commit it. If it only describes how you
like your answers, keep it in your home folder.

### Desktop app or terminal?

**Same thing.** Both read the same `~/.claude/` folder, which holds `CLAUDE.md`,
`settings.json`, `plugins/`, and `sessions/`. The folder `AppData/Roaming/Claude` belongs
to the separate chat app and holds no settings. Install once and both apps use it.

## Why each agent has its own file

Three reasons:

- **The tool list is a real limit.** In an agent file, `tools:` lists the only tools that
  agent gets. A tool that is not on the list does not exist for that agent. This is why
  the refuter cannot use Edit or Write. Leave `tools:` out and the agent gets every tool.
  If all five were described in one text file, that would only be a request. In
  separate files it is enforced.
- **The file is only loaded when that agent runs.** One big file with all five agents
  would have to be read by your expensive main chat every time. That is the opposite of
  saving money.
- **The `description:` line is how Claude picks an agent.** It compares your task to each
  agent's description and chooses. No guessing.

## Two things to know about subagents

- **Subagents get your CLAUDE.md files.** Both the home one and the project one. So agent
  files can say "follow the rules" instead of repeating them. It also means **every subagent
  pays for every line of both CLAUDE.md files, every time it starts.** Keep them short.
  That is about cost, not style.
- **Subagents do not see your conversation.** They get the text you send them, the CLAUDE.md
  files, and a snapshot of `git status`. Nothing else. So the brief must contain
  everything. "As we discussed" in a brief is a mistake.

## The three rules that do the real work

1. **Every agent has a pinned model.** Without one, a subagent uses your main session's
   model, and so do any subagents it spawns. That is what burns quota, not "using
   subagents". If you spawn an agent that is not one of the five, pass a model yourself.
2. **The brief is a file. Write it before you spawn the agent. Never change it after.**
   The refuter checks the work against those exact words. If the words can change, the
   review means nothing.
3. **The refuter never reads what the builder said.** It reads the brief, the code
   change, and its own test run. Builders describe their own work as better than it is.
   The code cannot do that.

## Why CLAUDE.md is so short

Every subagent loads all of CLAUDE.md, so **every line costs money every time one
starts.** About 60% of this kit's first `CLAUDE.md` was instructions only the main chat
could use. A subagent paid for those lines and could do nothing with them. You cannot move
them somewhere else, because CLAUDE.md is the only file that loads automatically.

So the split is: **CLAUDE.md holds the rules, this README holds the reasons.** Reasons do
not change what Claude does, and nothing loads this README while Claude runs. So reasons
are free here and cost money there. This kit's `CLAUDE.md` went from 2,258 to 1,324
tokens, a 41% cut, and kept all 16 rules that matter. That is about 23k tokens saved over
25 spawns.

If you add something to `CLAUDE.md`, add the rule, not the reason.

## The bucket

Each task gets one bucket inside the repo you are working in. Claude opens it when a new
task starts and closes it when the refuter accepts. A file called `INDEX.md` next to the
buckets lists all of them with status and next action. Agents share information through
these files instead of through your chat:

```
.claude/scratch/<slug>/
  STATE.md       replaced each update — what is true NOW
  FINDINGS.md    append-only — evidence, file:line
  DECISIONS.md   append-only — what changed and WHY   ← the loop-breaker
  briefs/        orders, written before spawn, then read-only
  reports/       one per brief
```

`DECISIONS.md` is the most useful file. **Every agent reads it before changing anything.
If a change would undo a decision written there, the agent stops and reports instead.**
This ends the problem where round two undoes round one, and round three undoes round two.
Add `.claude/scratch/` to `.gitignore`.

---

## extras: install only if you need them

```bash
cp extras/project/CLAUDE.md             <repo>/CLAUDE.md            # then fill in the placeholders
cp extras/project/.claude/settings.json <repo>/.claude/settings.json
cat extras/project/.gitignore-snippet  >> <repo>/.gitignore
cp -r extras/project/.claude/scratch/_TEMPLATE <repo>/.claude/scratch/_TEMPLATE
```

Start Claude Code from the repo root. The paths in `settings.json` are matched from the
folder you start in, so starting from a subfolder turns those rules off.

| | |
|---|---|
| `project/CLAUDE.md` | A template for a repo's own CLAUDE.md: commands table, layout, danger list, list of past defects. |
| `project/.claude/settings.json` | Blocks Edit/Write on `briefs/**`. Asks before `push`, `reset --hard`, and removing the read-only flag. Stops subagents spawning subagents. |
| `project/.claude/scratch/_TEMPLATE/` | Longer versions of the bucket files, with STOP/LOG/DEFER classes for findings. |
| `project/.gitignore-snippet` | The two lines that keep buckets out of git. |

## Facts from the official docs

- **The `model:` line in an agent file is respected.** Order of priority: a model you pass
  when spawning → the agent file's `model:` → `CLAUDE_CODE_SUBAGENT_MODEL` →
  your main chat's model. So the five agents really are pinned. Pass a model yourself only
  for an agent that is not one of the five. This order needs Claude Code 2.1.251 or newer.
  Older versions put the environment variable first.
- **`haiku` is an official short name.** So is `fable`. Never put `fable` on a subagent.
- **A tool missing from `tools:` is denied.** The list is "only these". That is why the
  refuter has no Edit or Write. A file with no `tools:` line gets all tools.
- **Subagents load every CLAUDE.md**: `~/.claude/CLAUDE.md`, the project CLAUDE.md,
  `CLAUDE.local.md`, and any company policy file. Only the built-in Explore and Plan
  agents skip this. Your main session's memory is NOT passed to subagents.
- **If two agents have the same name, the project one wins.** For skills and commands it
  is the other way round: `~/.claude/commands/` beats `.claude/commands/`. Do not use the
  same name twice.
- **`$1` means the SECOND word**, because counting starts at 0. Every command in this kit
  uses `$ARGUMENTS` and splits the words itself, so this does not affect them.
- **Subagents can spawn subagents**, three levels deep by default. The five kit agents
  cannot, because `Agent` is not in their tool lists. `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`
  closes it for every other subagent.

## Agent file settings worth knowing

The docs list 17 settings for an agent file, not just the usual 5 (`name`, `description`,
`model`, `tools`, `color`). These matter:

| Setting | Why |
|---|---|
| `effort` | `low` to `max`. **If you leave it out, the agent inherits your session's level**, so a cheap model can still be told to think hard. Set on all five agents here. |
| `disallowedTools` | A block list, for when "only these tools" is too strict. |
| `isolation: worktree` | Gives the agent its own git worktree, started from your default branch, not your current branch. Use it when two agents must write at the same time. |
| `permissionMode` | Permission behavior for that agent only. |
| `skills`, `hooks`, `memory`, `maxTurns` | Exist, not used here. |

## The one-line quota fix

If you only want one thing from this kit, use this:

```bash
export CLAUDE_CODE_SUBAGENT_MODEL=sonnet
export CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1
```

Every subagent becomes Sonnet, and **every agent file's `model:` is ignored.** You also
cannot pass a model when spawning. This turns off the five-agent setup completely. Use
it when quota matters more than choosing the right agent for each job.
