# Vendor Feedback

Bug reports and feature requests to the vendors of software I use, from one plugin.

Every vendor takes reports differently: GitHub issue forms, a community forum, email or
an in-app form. Instead of maintaining one plugin per vendor, each vendor gets:

- a folder under `vendors/<vendor>/` describing how that vendor takes bug reports and
  feature requests (`reporting.md`), plus any helper scripts and references;
- skills with a vendor prefix (`cc-` for Claude Code, `op-` for 1Password) that read
  that folder.

The same rule applies to every vendor: **search for an existing report before filing**,
and show the draft to the user before it's posted.

## Vendors and skills

| Vendor | Notes | Skill | Does |
|---|---|---|---|
| Claude Code | `vendors/claude-code/` | `cc-bug-report` | Searches open and closed issues on `anthropics/claude-code`, offers a comment on a match, otherwise files through Anthropic's live `bug_report.yml` form |
| 1Password | `vendors/1password/` | `op-fr-search` | Checks release notes, the forum sitemap and forum search for an existing request |
| | | `op-feature-request` | Drafts and posts a `Feature Request:` topic on the 1Password Community, after approval |
| | | `op-bug-report` | Checks the installed version against the latest release, searches for duplicates, posts a `[Bug]` topic |
| | | `op-community-engage` | Adds use cases to existing requests, replies, likes |
| | | `op-fr-tracker` | Logs posted threads and checks for staff replies or a shipped feature |

## Adding a vendor

See `vendors/README.md`.

## History

The 1Password skills came from `Claude-1Password-Feedback-Plugin` (`onepassword-feedback`),
which was retired on 2026-10-22 and folded in here. One plugin covering several vendors
replaces one plugin per vendor. The skills are unchanged apart from file paths, and their
local data directory keeps the old name (`…/claude-plugins/onepassword-feedback/`) so
existing request logs still work.

## Requirements

- `gh`, authenticated, for GitHub-based vendors.
- Claude in Chrome, signed in to the forum, for forum-based vendors (1Password).
