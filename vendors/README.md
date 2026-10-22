# Vendors

One folder per vendor, named in lower-case kebab-case (`claude-code`, `1password`).

## What goes in a vendor folder

- `reporting.md` (required). How the vendor takes **bug reports** and **feature
  requests**: the channel (GitHub issue form, forum, email, in-app form), the URL, any
  required fields or template, how to search for existing reports, and any duplicate or
  auto-close behaviour on the vendor's side. Record the date you verified it and what
  you confirmed versus inferred.
- Optional: helper scripts (`scripts/`), machine-readable channel data
  (`channels.json`), a drafting guide, a verification log.

## Skills

Skills live in the top-level `skills/` folder with a short vendor prefix (`cc-`, `op-`).
Each one reads `${CLAUDE_PLUGIN_ROOT}/vendors/<vendor>/reporting.md` first. Add a skill
only for what the vendor actually needs: a vendor with a single channel and no tooling
can get by with notes alone, used through a general flow.

Every filing skill has to:
1. search for an existing report before drafting, and offer to add to it instead;
2. show the full draft and get approval before posting;
3. strip secrets and personal detail from logs and reproduction steps.

When a vendor is added, add a row to the table in the top-level `README.md`.
