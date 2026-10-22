---
name: vendor-preferences
description: Record the user's own preferences for contacting a vendor — which channel they prefer for bugs, feature requests or support, channels to avoid, private addresses, and personal contacts at the company (a developer they know, an account manager, a WhatsApp number, someone met in person). Use when the user says "I prefer to email X", "don't post X stuff on Reddit", "I know someone at X", "for X feature requests go to …", or "remember that for X …".
---

# Vendor preferences and contacts

Preferences are private. They live in the user's overlay, never in the plugin repository:

```bash
python3 <plugin-root>/scripts/liaison.py paths    # overlay_dir
```

There's one file per vendor, `<overlay_dir>/<vendor-id>.json`. Create the directory and
the file if they don't exist. Read the file before writing to it, and merge into it;
never replace the whole file.

## Shape

```json
{
  "channels": [
    {"id": "feedback-email", "type": "email", "target": "feedback@example.com",
     "visibility": "private", "purposes": ["feature"], "status": "confirmed",
     "source": "user, YYYY-MM-DD", "notes": "Not published; from the user."}
  ],
  "prefer": {
    "feature": {"channel": "feedback-email", "why": "User prefers email for feature requests."}
  },
  "avoid": ["reddit"],
  "contacts": [
    {"id": "jane", "name": "Jane Doe", "role": "Developer advocate", "organisation": "Example Ltd",
     "methods": [{"type": "whatsapp", "value": "+10000000000"}, {"type": "email", "value": "jane@example.com"}],
     "relationship": "Met at a conference; happy to take product feedback directly.",
     "use_for": ["feature", "bug"],
     "etiquette": "Informal; batch small things rather than messaging often.",
     "last_contact": "YYYY-MM-DD"}
  ],
  "notes": "",
  "vendor": null
}
```

- `prefer.<purpose>.channel` can name a public channel id from `vendors/<id>/vendor.json`,
  a private channel defined in this file, or `contact:<contact id>`.
- `avoid` lists channel ids never to suggest for this vendor.
- `vendor` holds a full private vendor definition (the same shape as `vendor.json`) for
  a vendor that isn't in the public data. Leave it out otherwise.
- Contacts are personal data. They stay in this file and are never copied into the repo,
  a public post or a log line.

## After writing

Run `python3 <plugin-root>/scripts/liaison.py validate <vendor-id>`, then
`route <vendor-id> <purpose>`. Show the user that the preference now ranks first, or the
warning that explains why it doesn't (for example, a public channel preferred for
security).
