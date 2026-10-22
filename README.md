# Vendor Liaison

Agent skills for reporting bugs, requesting features, disclosing security issues and
asking for support from software vendors, each through the vendor's own channel.

Every vendor takes reports differently: GitHub issue forms, forums, subreddits, Discord,
feature boards, a support address, a bug-bounty program. On top of that, you may have
your own preferences ("email them, don't post on Reddit") or know someone at the company.
This plugin keeps both kinds of information as data and merges them into a ranked route:

- **Vendor data (public, in this repo):** `vendors/<id>/vendor.json`, holding the
  channels, what each one is for, whether it's public or private, how to search it for
  duplicates, the recommended order per purpose, and the vendor's rules.
- **Your overlay (private, never in the repo):** `<overlay_dir>/<id>.json`, holding your
  preferred channel per purpose, channels to avoid, unpublished addresses, and personal
  contacts (WhatsApp, email, phone, someone you met in person) with notes on the
  relationship.
- **Resolver:** `scripts/liaison.py route <vendor> <purpose>` merges the two. A
  preference comes first, then the vendor's order, and every channel comes with the
  reason it ranks where it does. A security report is never routed to a public channel.

Every filing flow searches for an existing report first and shows the draft for approval
before anything is sent.

## Skills

| Skill | Does |
|---|---|
| `route` | Ranks where to send something for a vendor and purpose |
| `report` | Duplicate check, draft for the channel type, approve, send, log |
| `security-disclosure` | Private channels only (security.txt, bug bounty, security@), embargo-safe drafting |
| `vendor-preferences` | Records preferred channels, avoided channels and personal contacts in the private overlay |
| `add-vendor` | Researches a vendor's channels and writes `vendor.json` |
| `cc-bug-report` | Claude Code: searches `anthropics/claude-code` issues, files through the live bug form |
| `op-fr-search`, `op-feature-request`, `op-bug-report`, `op-community-engage`, `op-fr-tracker` | 1Password Community: duplicate search, posting, replies, tracking |

## Vendors

| Vendor | Bugs | Feature requests | Security | Data |
|---|---|---|---|---|
| Claude Code | GitHub issues (`cc-bug-report`) | GitHub issues | HackerOne (security.txt) | `vendors/claude-code/` |
| 1Password | Community forum (`op-bug-report`) | Community forum (`op-feature-request`) | HackerOne, security@agilebits.com | `vendors/1password/` |
| Whisperian (Android dictation) | support@whisperian.app | support@whisperian.app, r/Whisperian | support@whisperian.app (no security.txt) | `vendors/whisperian/` |

To add a vendor, use the `add-vendor` skill or see `vendors/README.md`.

## Resolver

```bash
python3 scripts/liaison.py paths                 # where vendor data and your overlay are read from
python3 scripts/liaison.py vendors
python3 scripts/liaison.py route whisperian feature
python3 scripts/liaison.py validate
```

Standard library only, with JSON output. The overlay directory resolves in this order:
1. `$VENDOR_LIAISON_DATA`;
2. `$CLAUDE_USER_DATA/vendor-liaison`;
3. the first existing folder of `~/.claude-user-data` and
   `${XDG_DATA_HOME:-~/.local/share}/claude-plugins`, plus `vendor-liaison`;
4. otherwise `~/.claude-user-data/vendor-liaison`.

Sent reports are logged one per line to `<overlay_dir>/reports.jsonl`.

## Using it outside Claude Code

The skills are plain `SKILL.md` files and the resolver is a Python script, so any agent
that reads skills can use them. Where a skill says `<plugin-root>`, use the folder that
holds `vendors/` and `scripts/` (`${CLAUDE_PLUGIN_ROOT}` in Claude Code).

## History

- 2026-10-22: created as `vendor-feedback`, then widened and renamed `vendor-liaison`,
  with structured channel data, a private overlay and security disclosure.
- It replaces two single-vendor plugins, retired to consolidate:
  - `onepassword-feedback` (repo `Claude-1Password-Feedback-Plugin`). Its `op-*` skills
    are here unchanged apart from paths, and their local data keeps the old folder name
    (`…/claude-plugins/onepassword-feedback/`).
  - `feedback-filer` (repo `Claude-Code-Feedback`). Replaced by `cc-bug-report` and the
    generic `report` flow.
