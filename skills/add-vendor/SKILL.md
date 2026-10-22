---
name: add-vendor
description: Research how a software vendor takes bug reports, feature requests, security reports and support, and record it as structured channel data (vendor.json) so routing works for that vendor. Use when a vendor isn't known yet, when the user says "add X to vendor liaison", "find out how X takes feedback", or when a vendor's channels have changed or died.
---

# Add or update a vendor

## 1. Research the channels

Check each of these for the vendor, and record where each fact came from:

- The website's footer, contact, support and help pages.
- `/.well-known/security.txt`, a security page or bug-bounty listing, and `SECURITY.md`.
- App store listings. These usually give the developer's contact email.
- Public issue trackers: GitHub or GitLab issues and their issue templates, and whether
  blank issues are allowed.
- Community spaces: the forum, subreddit, Discord or Slack. Note any flair or tag used
  for feature requests and bugs.
- Feature boards (Canny, Productboard portal, UserVoice, and so on), and whether they are
  actually in use.
- In-app feedback.
- Release notes or a changelog, for checking against before reporting.

For each channel, test the address or URL where you can. Mark the channel `confirmed`
only if you loaded the page or saw the address published; mark it `inferred` if it came
from a secondary source; mark it `dead` (and keep it) if it's gone, so nobody adds it
again.

Also find out how each public channel can be searched for duplicates, and record the
working method in `dedupe`. For example, Reddit's `.json` endpoints refuse anonymous
requests but `search.rss` works.

## 2. Write the record

Public vendor: `vendors/<id>/vendor.json` in the plugin repo. The field reference is in
`vendors/README.md`, and existing vendors are examples. Required fields:
- `id`, `name` and `verified` (YYYY-MM-DD);
- `channels`, each with `id`, `type`, `target`, `visibility`, `purposes` and `status`;
- `routing`: the recommended channel order per purpose;
- `rules`: the vendor's requirements, in imperative sentences.

Optional: a `reporting.md` for long-form notes, and `skills` when a vendor-specific skill
exists.

Anything personal to the user (unpublished addresses, contacts, preferences) goes in
their overlay through `vendor-preferences`, never here. A vendor the user doesn't want
published goes under `vendor` in their overlay file.

## 3. Validate

```bash
python3 <plugin-root>/scripts/liaison.py validate <id>
python3 <plugin-root>/scripts/liaison.py route <id> bug
```

The validator rejects routing that points at undefined channels, a channel that doesn't
list the purpose it's routed for, and any public channel in `routing.security`. A public
vendor file is a change to the plugin repository: commit it there (or open a pull
request upstream) and add a row to the vendor table in the top-level README.
