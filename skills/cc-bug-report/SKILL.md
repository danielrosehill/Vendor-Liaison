---
name: cc-bug-report
description: File a bug report against Claude Code (anthropics/claude-code on GitHub), after checking that it hasn't already been reported. Use when the user wants to "report a Claude Code bug", "file an issue with Anthropic", "open a bug on claude-code", or describes Claude Code (the CLI, harness, tools, hooks, plugins, MCP handling) misbehaving. Searches open and closed issues first, offers to comment on a match, and files the issue through Anthropic's live bug_report form only when nothing matches. Not for complaints about what the model said; that is a model-behavior report.
---

# Claude Code bug report

Target: `anthropics/claude-code`. Read `${CLAUDE_PLUGIN_ROOT}/vendors/claude-code/reporting.md`
first. It covers the channels, the form fields and how the repo's duplicate bot behaves.
If `CLAUDE_PLUGIN_ROOT` is unset (the skill was loaded on its own), the same facts are
summarised here.

## 1. Pin down the bug

From the conversation, get:
- the symptom;
- what should have happened;
- steps to reproduce;
- any exact error text.

Ask only for what is missing, in one batch. If the user has described more than one bug,
each one gets its own report.

Collect the environment yourself rather than asking:

```bash
claude --version
npm view @anthropic-ai/claude-code version   # latest release
uname -srm; echo "$SHELL"; echo "${TERM_PROGRAM:-$TERM}"
```

If the installed version is behind, say so. The form's preflight asks you to confirm you're
on the latest version, so suggest updating and reproducing again before filing.

## 2. Search for duplicates (always, before drafting)

Search open **and** closed issues, without a label filter. Run at least three phrasings:
the symptom, the feature or setting involved, and the exact error string.

```bash
gh search issues --repo anthropics/claude-code "<keywords>" --limit 20 \
  --json number,title,state,url,updatedAt,commentsCount
```

Open the most likely two or three (`gh issue view <n> --repo anthropics/claude-code
--comments`) and compare their bodies, not just the titles. `gh` doesn't show why a closed
issue was closed; get that with `gh api repos/anthropics/claude-code/issues/<n> -q .state_reason`
(`completed`, `not_planned` or `duplicate`). Then decide:

| Finding | Action |
|---|---|
| An open issue describes the same bug | Don't file. Give the link and offer a comment adding what is new: version, platform, reproduction, impact. A 👍 on the issue alone is also fine. |
| Closed as completed, but the bug is back | File a new issue that links the old one and says it's a regression. |
| Closed as a duplicate | Follow the link to the issue it was closed in favour of, and treat that one as the match. |
| Closed as not planned | Show it to the user. Re-filing usually goes nowhere. |
| Nothing matches | Go on to step 3. |

When the user says "file it", that covers the text of the report, not filing a duplicate.
If a match exists, show it before doing anything.

## 3. Draft from the live form

```bash
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/.github/ISSUE_TEMPLATE/bug_report.yml
```

Build the body from whatever fields the form declares now:
- Skip `type: markdown` items.
- Each other item becomes `### {label}` followed by its value, in the form's order.
- Checkboxes are written `- [x] text`.
- Use the option text verbatim for dropdowns.
- Write `_No response_` for optional fields left empty.
- Wrap anything with `render: shell` in a code fence.

The title is `[BUG] ` plus a specific one-line summary, under about 90 characters.

Only tick a preflight box if it's true. The search in step 2 makes the first one true.

Before showing the draft, remove secrets and personal detail:
- tokens and keys;
- email addresses;
- internal hostnames and IPs;
- home-directory usernames (write `~/`).

Tell the user what you removed.

## 4. Confirm, then file

Show the title, the full body and the target repo, and wait for approval. Then:

```bash
gh issue create --repo anthropics/claude-code --title "$TITLE" --body-file "$BODY_FILE"
```

The form adds the `bug` label. Don't pass `--label`, because outside contributors can't
set labels. Report the issue URL.

## 5. After filing

The repo's bot may post a "possible duplicate" comment within minutes. It closes the issue
after 3 days unless someone comments afterwards or the issue's author puts a 👎 on the bot
comment. Tell the user this. If they think the flag is wrong, the 👎 and a short comment
explaining the difference keep the issue open.
