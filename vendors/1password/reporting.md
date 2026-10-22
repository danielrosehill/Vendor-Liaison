# 1Password — how to report bugs and request features

Verified 2026-10-21. See `verification-log.md` for the record.

## Channels

- **Feature requests**: an ordinary Community topic at
  `https://www.1password.community/topic/new`, tagged **Feature Request** plus a product
  tag. It goes in one of three categories: *1Password at home* (`fid=31`), *1Password at
  work* (`fid=58`) or *Developers* (`fid=69`). The `/ideas` board exists but is empty.
  Votes don't set priority; staff log requests internally.
- **Bugs**: a Community topic titled `[Bug] …`, posted after checking the installed
  version against the latest release. Skill: `op-bug-report`.
- The Community account is separate from the 1Password account. Posting needs the user
  signed in in Chrome. The agent never types credentials.
- The forum runs on Gainsight (formerly inSided) since 2026-07-02. Its search runs in the
  browser, so there's no API and no RSS. `scripts/community.py` reads the two sources
  that work without a browser: the topic sitemap and each topic's QAPage JSON-LD.

## Files here

| File | What it holds |
|---|---|
| `channels.json` | Every channel, the secondary routes (GitHub repos, Slack, support) and URLs known to be dead |
| `posting-guide.md` | Drafting rules for topics and replies |
| `verification-log.md` | What was tested and when |
| `scripts/community.py` | Read-only helper (standard library only): `search`, `topic`, `recent` |

Local data keeps the old plugin's directory name, so earlier logs still work:
`${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/onepassword-feedback/`.
That holds `cache/` (the sitemap, refreshed every 6 hours) and `data/requests.json`
(the request log).
