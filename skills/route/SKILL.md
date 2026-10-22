---
name: route
description: Work out where to send something to a software vendor — a bug report, feature request, security vulnerability, support question or general feedback — taking the vendor's own channels and the user's personal preferences and contacts into account. Use when the user asks "where do I report this to X", "how do I request a feature from X", "who do I tell about this bug", or before any of the report, security-disclosure or vendor-specific filing skills.
---

# Route a message to a vendor

The resolver merges the vendor's public channel data with the user's private overlay and
ranks the channels:

```bash
python3 <plugin-root>/scripts/liaison.py route <vendor-id> <purpose>
```

`<plugin-root>` is `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In other agents it's the folder
that contains `vendors/` and `scripts/`. The purpose is one of `bug`, `feature`,
`security`, `support`, `question`, `feedback` or `docs`. Run
`python3 <plugin-root>/scripts/liaison.py vendors` for the vendor ids.

## Reading the result

- `route` lists channels best first, each with a `reason`:
  - `user preference`: the user chose this channel, and `why` says why. It wins.
  - `vendor routing`: the order the vendor data recommends.
  - `also accepts this purpose`: the channel is valid but not recommended.
- Channels with ids beginning `contact:` are named people the user knows. The
  `contact` object holds how to reach them and any etiquette notes.
- `skill`: a vendor-specific skill exists for this purpose (for example `cc-bug-report`).
  Hand off to it.
- `rules`: the vendor's own requirements, such as searching first or using a template.
  Follow them.
- `warnings`: always tell the user about these, especially a preference that was skipped.

Security reports are never routed to a public channel, whatever the preference says. The
resolver enforces this, and you must not work around it.

## When the vendor isn't known

If the vendor isn't in the list, use the `add-vendor` skill to research its channels
first. Don't guess an address.

## Answer

Give the top channel, its address or URL, why it ranks first, and what to check before
using it (the `dedupe` field). Mention the runner-up. If the user wants to go ahead,
continue with `report`, `security-disclosure`, or the vendor skill named in `skill`.
