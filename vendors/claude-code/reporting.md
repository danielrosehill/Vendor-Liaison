# Claude Code — how to report bugs and request features

Verified 2026-10-22 against `anthropics/claude-code` (Claude Code 2.1.308).

## Channels

| Channel | Use for | Notes |
|---|---|---|
| GitHub issue on `anthropics/claude-code` | Bugs, feature requests, model behaviour, docs | Public. The only channel that gives you a link to follow. |
| `/feedback` in Claude Code (alias `/bug`) | Quick private report with session context attached | Goes straight to Anthropic. Doesn't search for duplicates and doesn't give you a public link. |
| Discord (`anthropic.com/discord`) | Questions and support | Not a bug tracker. |

Blank issues are disabled (`blank_issues_enabled: false`). Every issue has to use one of
the forms in `.github/ISSUE_TEMPLATE/`:

| File | Title prefix | Purpose |
|---|---|---|
| `bug_report.yml` | `[BUG] ` | CLI and harness bugs |
| `feature_request.yml` | `[FEATURE] ` | Enhancements |
| `model_behavior.yml` | — | What Claude said or did, not the tool |
| `documentation.yml` | — | Missing or wrong docs |
| `github_connection.yml` | — | The GitHub app integration |

Fetch the live form every time, because the fields change:
`https://raw.githubusercontent.com/anthropics/claude-code/main/.github/ISSUE_TEMPLATE/<file>`

## Bug report form (as of 2026-10-22)

Submitted in the browser, the form applies the `bug` label. Submitted with `gh issue create`,
no label is applied (observed 2026-10-22, #104378), and outside contributors can't add one.
Required fields:

- **Preflight** (three checkboxes): the issue was searched for first, the report covers
  one bug, and you're on the latest version
- **What's Wrong?** and **What Should Happen?**
- **Steps to Reproduce**
- **Is this a regression?**
- **Claude Code Version**
- **Platform**, **Operating System** and **Terminal/Shell**

Optional fields: Error Messages/Logs, Claude Model, Last Working Version, Additional
Information.

To check the "latest version" box, compare `claude --version` with
`npm view @anthropic-ai/claude-code version`.

## Duplicate handling on Anthropic's side

The repo has a duplicate bot, so a careless report gets closed:

- `claude-dedupe-issues.yml` runs on every new issue. If it finds matches, a bot posts a
  comment containing "Found … possible duplicate".
- `auto-close-duplicates.yml` runs daily at 09:00 UTC through
  `scripts/auto-close-duplicates.ts`. It closes an issue when the bot comment is more than
  3 days old, unless one of these is true:
  1. someone has commented since the bot's comment;
  2. the issue's author has put a 👎 reaction on the bot's comment.

So search first. If the bot flags a report that is not a duplicate, add a 👎 to its
comment from the author's account and explain the difference in a comment.

## Searching for existing issues

The repo has more than 15,000 open issues. Search open **and** closed issues, without a
label filter, because many reports never get a label:

```bash
gh search issues --repo anthropics/claude-code "<3-6 keywords>" --limit 20 \
  --json number,title,state,url,updatedAt,commentsCount
```

Run two or three phrasings: the symptom, the feature or setting involved, and the exact
error text. A closed issue whose bug has come back is a reason to file a new issue that
links to it, not to post on the closed one.
