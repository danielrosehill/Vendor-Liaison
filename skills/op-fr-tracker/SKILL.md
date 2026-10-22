---
name: op-fr-tracker
description: Log 1Password feature requests and threads the user posted or joined, and check them for staff replies or shipped features.
---

# Track 1Password feature requests

Use when the user asks "what have I asked 1Password for", "any reply on my 1Password
request", "did 1Password ship X", or after `op-feature-request` / `op-community-engage`
posts something.

## Data storage

`${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/onepassword-feedback/data/requests.json`.
Create it as `{"requests": []}` on first use. Never write elsewhere.

Entry shape:

```json
{"id": "2026-10-21-ssh-agent-per-app-policy",
 "title": "Feature Request: ...",
 "url": "https://www.1password.community/developers-69/...-25530",
 "kind": "feature-request | bug",
 "route": "community | github | support",
 "role": "author | replied | liked",
 "category": "developers",
 "tags": ["Feature Request", "SSH"],
 "posted": "2026-10-21",
 "status": "open | staff-acknowledged | shipped | declined | locked",
 "staff_reference": null,
 "last_checked": "2026-10-21",
 "notes": ""}
```

## Steps

### Add

Append an entry with the values from the post just made. Use an id of
`<date>-<short-slug>`.

### Check

For each entry not `shipped` or `declined`:

1. `python3 ${CLAUDE_PLUGIN_ROOT}/vendors/1password/scripts/community.py topic <url>` for reply count and likes.
   If `replies` grew since `last_checked`, open the thread in Chrome and read the new
   replies. Mark `staff-acknowledged` when a `1P_` / employee account replied, and copy
   any reference number (e.g. `PB-…`).
2. Search `https://releases.1password.com/index.xml` for the capability. If it shipped,
   set `shipped` and note the release.
3. Update `last_checked`.

Report a short table: title, status, what changed since last check, link. List anything
that needs the user's reply first.

## Notes

- The sitemap `lastmod` changes on any edit, so it is a hint to re-read a thread, not
  evidence of a staff reply.
