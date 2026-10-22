# Vendors

One folder per vendor, named with its lower-case kebab-case id (`claude-code`,
`1password`, `whisperian`). The folder holds:

- `vendor.json` (required): the vendor's channels and routing, in the shape below.
- `reporting.md` (optional): long-form notes, such as form fields, how duplicate
  handling works, and anything that doesn't fit in a field.
- Anything else the vendor needs: helper scripts, a drafting guide, a verification log.

Check every change with `python3 scripts/liaison.py validate`.

## vendor.json

```json
{
  "id": "example",
  "name": "Example",
  "maker": "Example Ltd",
  "products": ["Example for Android"],
  "homepage": "https://example.com",
  "verified": "YYYY-MM-DD",
  "channels": [
    {
      "id": "support-email",
      "type": "email",
      "target": "support@example.com",
      "visibility": "private",
      "purposes": ["bug", "feature", "support", "security"],
      "dedupe": "how to search for an existing report on this channel (optional)",
      "status": "confirmed",
      "source": "where this was found, with date",
      "notes": "optional"
    }
  ],
  "routing": { "bug": ["support-email"], "security": ["support-email"] },
  "skills": { "bug": "a-vendor-specific-skill" },
  "rules": ["Imperative sentences the agent must follow for this vendor."]
}
```

| Field | Values |
|---|---|
| `type` | `github-issues`, `github-discussions`, `gitlab-issues`, `issue-tracker`, `email`, `contact-form`, `in-app`, `forum`, `reddit`, `discord`, `slack`, `feature-board`, `app-store-review`, `bug-bounty`, `social`, `whatsapp`, `signal`, `telegram`, `phone`, `in-person`, `contact`, `other` |
| `visibility` | `public`: what you post is visible to anyone. `private`: only the vendor sees it. |
| `purposes` | `bug`, `feature`, `security`, `support`, `question`, `feedback`, `docs` |
| `status` | `confirmed` (loaded or seen published), `inferred` (secondary source), `dead` (kept so nobody re-adds it) |
| `routing` | Per purpose, the recommended order of channel ids. Every id must exist and list that purpose. |

Hard rule, enforced by the validator and the resolver: `routing.security` may only
contain `private` channels, and the resolver never offers a public channel for `security`.

## Private data

The user's preferences, unpublished addresses, personal contacts and private vendors live
outside the repo, in `<overlay_dir>/<vendor-id>.json` (see the `vendor-preferences`
skill). `liaison.py paths` shows where that is. Never commit overlay content.
