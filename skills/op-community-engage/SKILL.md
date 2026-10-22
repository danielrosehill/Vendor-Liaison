---
name: op-community-engage
description: Engage in the 1Password Community — +1 or add a use case to a feature request, reply to threads, answer questions, browse new topics.
---

# Engage with the 1Password Community

Use when the user says "+1 that 1Password request", "reply on the 1Password forum",
"what's new on the 1Password community", "answer that 1Password thread", or when
`op-fr-search` found an existing thread to join.

Read `${CLAUDE_PLUGIN_ROOT}/vendors/1password/posting-guide.md` before drafting any reply.

## Modes

### Browse

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/vendors/1password/scripts/community.py recent --days 7 [--category developers]
```

Summarise by category. Flag `Feature Request` titles and topics touching the user's stated
interests. Pull the opening post of anything they pick with `community.py topic <url>`.

### Support an existing feature request

1. Read the full thread in Chrome (open your own tab):
   staff replies, whether it is locked, what use cases are already stated.
2. If the user's use case is already there, the action is a Like only. Say so.
3. Otherwise draft a short reply that adds their **new** use case or detail. Do not write
   "+1" alone.
4. Locked thread: offer a new topic that links it (`op-feature-request`).

### Reply or answer

Draft a reply that answers the question asked, with version numbers and steps the user
can vouch for. If unsure, say what to test rather than guessing.

## Posting (all modes)

1. Post by default; asking for a reply or +1 is permission. Stop at the draft and wait
   for approval only if the user asks to see it first. Report the posted text afterwards.
2. In Chrome, open the thread. If not signed in, ask the user to sign in to the community
   account (separate from 1Password). Never type credentials.
3. Click **Reply** under the post. The editor is CKEditor 4 (`editor1`); set the body with
   `CKEDITOR.instances.editor1.setData(html)` and read it back with `getData()`. The
   submit button is labelled **Send**. For a Like, click it and confirm the count moved.
4. Read back the post's permalink. After Send the URL gains `?postid=<n>#post<n>`, but
   the reply may not show on the thread or in the profile's Replies count straight away
   (seen 2026-10-22, postid 140559, likely held for moderation). Don't resubmit: record
   the postid and check again later via `op-fr-tracker`.
5. If it relates to a logged request, update the entry via `op-fr-tracker`.

## Notes

- Do not cross-post the same content to Reddit or Mastodon.
- Never include account emails, vault/item names, Secret Key or order numbers.
