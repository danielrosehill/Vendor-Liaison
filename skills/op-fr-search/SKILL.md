---
name: op-fr-search
description: Search the 1Password Community and release notes for an existing feature request or answer before posting a new one.
---

# Search 1Password feature requests

Run this before every new 1Password feature request, and when the user asks "has anyone
asked 1Password for X", "is there a thread about X", or "does 1Password do X yet".

## Inputs

- The capability in plain words (e.g. "per-app SSH agent approval").
- Optional product area: home, work, developers.

## Steps

1. **Shipped already?** Check release notes. Fetch
   `https://releases.1password.com/index.xml` (or the product section in
   `${CLAUDE_PLUGIN_ROOT}/vendors/1password/channels.json`) and look for the capability. Also check the product's
   support docs with a web search scoped to `support.1password.com` /
   `developer.1password.com`. If it shipped, stop and say where.
2. **Title search, no browser.** Run the helper from the plugin root:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/vendors/1password/scripts/community.py search <2-4 keywords> [--category developers]
   ```

   Try two or three phrasings with synonyms (`autofill`/`fill`, `passkey`/`webauthn`,
   `cli`/`op`). Slugs are titles only, so a miss here is not proof of absence.
3. **Read the top candidates.** For up to five plausible hits:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/vendors/1password/scripts/community.py topic <url>
   ```

   This gives the opening post, date, likes and reply count. It does not include replies
   or tags.
4. **Browser search for body text and tags.** The forum search runs client-side, so use
   Claude in Chrome (open your own tab). Open
   `https://www.1password.community/search/index?q=Feature%20Request&search_type=tag`
   for the Feature Request tag, and `https://www.1password.community/search?q=<terms>`
   for keywords. Read the result list; open a thread to see replies, staff responses and
   whether it is locked.
5. **The user's own topics.** Open the user's profile activity
   (`/members/<handle>-<id>`, linked from the avatar) and check they haven't asked this
   already. Their earlier topics can be filed as *Question* with a non-standard title,
   which the sitemap search misses (2026-10-22: topic 25245 duplicated 24516).
6. **Optional: GitHub.** For SDK, Terraform, Connect, operator or shell-plugin requests,
   search issues in the matching `github.com/1Password/<repo>`.

## Output

Report as JSON-shaped lines, most relevant first:

```json
{"verdict": "shipped | existing-thread | none-found",
 "matches": [{"url": "...", "title": "...", "created": "...", "likes": 0, "replies": 0,
              "staff_replied": true, "locked": false, "fit": "exact | partial"}],
 "searched": ["release notes", "sitemap: <terms>", "forum tag search", "forum keyword search"]}
```

Then one line of advice: reply to the existing thread (hand off to
`op-community-engage`), or post new (hand off to `op-feature-request`). An exact match
means a supportive reply that adds the user's use case, posted by default, not a
dead end.

## Notes

- Do not report "none found" from the sitemap step alone. The browser search is what
  covers post bodies.
- The `/ideas` board is empty and unused; ignore it.
