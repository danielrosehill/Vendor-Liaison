---
name: report
description: Send a bug report, feature request, support question or feedback to a software vendor through the right channel — email, GitHub issue, forum or subreddit post, contact form, in-app form, or a message to a personal contact at the company — after checking it hasn't already been reported. Use when the user says "report this to X", "send X a feature request", "email the developer about this bug", "tell my contact at X". For security vulnerabilities use security-disclosure instead.
---

# Report to a vendor

## 1. Route

Run the `route` skill, which calls `scripts/liaison.py route <vendor> <purpose>`. If the
result names a vendor-specific `skill`, hand off to it and stop here. Otherwise use the
top channel, unless the user picks another.

If the purpose is `security`, stop and use `security-disclosure`.

## 2. Check it hasn't been reported

Run this on every channel, including private ones: a private email about a problem that
is already on the public tracker wastes the vendor's time.

- Follow the channel's `dedupe` instruction where it has one.
- Otherwise search the vendor's public channels from its data (issue tracker, forum,
  subreddit) with two or three short phrasings, and check its release notes or changelog
  in case the problem is already fixed or the feature already shipped.
- If an existing report matches, show it. Offer to add to it (comment, reply or vote)
  instead of filing a new one. When you send privately anyway, reference the public
  thread.

## 3. Collect what the vendor needs

Use the vendor's `rules` for which fields it needs. For a bug, the usual set is:
- product and version;
- OS or device;
- steps to reproduce;
- what should happen and what actually happens;
- exact error text.

Collect environment facts by running commands rather than asking. Ask for anything still
missing in a single batch.

## 4. Draft for the channel

| Channel type | Draft |
|---|---|
| `email` | Subject line that says what's wrong or what's wanted ("Bug: …", "Feature request: …"); short body; product and version near the top |
| `github-issues`, `issue-tracker` | Fetch and follow the repo's issue template; one problem per issue |
| `forum`, `reddit`, `discord`, `slack` | Follow the community's posting rules and flair; a title that matches what someone else would search for |
| `contact-form`, `in-app` | Text sized to the form; tell the user which fields to fill if you can't drive it |
| `contact`, `whatsapp`, `signal`, `telegram` | A personal, short message in the register of the relationship; follow the contact's `etiquette` notes |
| `in-person`, `phone` | Talking points for the user, not a script |
| `app-store-review` | Only when the user wants a public rating; never as a substitute for a bug report |

Remove secrets and personal detail before showing the draft:
- tokens and keys;
- account IDs;
- other people's data;
- internal hostnames.

Tell the user what you removed.

## 5. Approve, send, log

Show the exact text, the destination and the sender. Send only after the user approves.
Use whatever tool the environment provides for that channel type:
- `gh` for GitHub;
- the user's email tool for email;
- a signed-in browser for forums and forms;
- a messaging tool for chat apps.

If no tool can send it, give the user the text and the destination to send themselves.

After sending, add one line to `<overlay_dir>/reports.jsonl` (the path comes from
`liaison.py paths`):

```json
{"date": "YYYY-MM-DD", "vendor": "<id>", "purpose": "<purpose>", "channel": "<channel id>", "ref": "<URL, message id or ''>", "summary": "<one line>"}
```
