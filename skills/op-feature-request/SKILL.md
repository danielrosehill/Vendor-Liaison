---
name: op-feature-request
description: Draft and submit a feature request to 1Password as a Community topic tagged Feature Request, after a duplicate check and approval.
---

# Submit a 1Password feature request

Use when the user says "request a feature from 1Password", "file a 1Password FR", "tell
1Password they should…", or "post this to the 1Password community".

Read `${CLAUDE_PLUGIN_ROOT}/vendors/1password/posting-guide.md` and `${CLAUDE_PLUGIN_ROOT}/vendors/1password/channels.json` first.

## Inputs

- What the user wants and why, in their words (a voice note transcript is fine).
- Product/platform if known.

## Steps

1. **Duplicate check.** Run `op-fr-search`. If it finds an exact match, recommend a
   reply on that thread (`op-community-engage`) instead and stop unless the user insists.
   A partial match gets linked in the new post.
2. **Gather facts.** Fill gaps the request needs: platform, plan, app or CLI version.
   Get versions from the machine where possible (`op --version`, the app's About
   screen) rather than asking. Ask the user only for the use case if it is missing.
3. **Pick the route.**
   - Default: Community topic, category home (`fid=31`), work (`fid=58`) or
     developers (`fid=69`).
   - SDK / Terraform / Connect / operator / shell-plugin: offer a GitHub issue on the
     matching `1Password/<repo>` using its feature-request template as an alternative
     or addition.
4. **Draft** with the template in `posting-guide.md`. Title starts
   `Feature Request: `. Strip any account email, vault or item names, Secret Key,
   order numbers.
5. **Post by default.** Asking for a feature request is permission to post it. Go
   straight to step 6, and show the final category, tags, title and body in the
   report afterwards. Stop at the draft and wait for approval only when the user asks
   for that ("draft it", "let me see it first", "pause before posting"), or when the
   duplicate check found an exact match.
6. **Post** with Claude in Chrome (open your own tab):
   1. Open `https://www.1password.community/topic/new?fid=<31|58|69>`.
   2. If the page shows a login prompt, stop and ask the user to sign in to the
      community account in that window. It is a separate account from 1Password
      itself. Do not type credentials.
   3. **Topic type:** the form opens on *Question*. Select **Conversation** for a
      feature request.
   4. **Title:** plain text input (`placeholder="Enter title here"`); click and type.
      Typing it makes the form show a *Related topics* list: one last duplicate check.
   5. **Body:** a CKEditor 4 instance (`editor1`). Typing loses structure; set HTML
      instead, with `javascript_tool`:
      `Object.values(CKEDITOR.instances)[0].setData(html)`. Use `<p><strong>` for
      headings and `<ul><li><a>` for related links.
   6. **Category** is preselected from `?fid=`.
   7. **Tags:** click *Add tags*, type `Feature Request`, then click the dropdown
      suggestion (Enter alone does not add it). Product tags then appear as
      `<Tag> +` chips under the field; click the right one. Read the chips back before
      submitting.
   8. Click **Create**. The page redirects to the new topic.
7. **Verify.** Read back the published topic URL. Confirm title, body and tags render.
   Run `python3 ${CLAUDE_PLUGIN_ROOT}/vendors/1password/scripts/community.py topic <url>` once it is in the
   sitemap (can lag).
8. **Log** via `op-fr-tracker` (add entry).

## Data storage

Logged requests live in
`${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/onepassword-feedback/data/requests.json`.
Nothing is written elsewhere.

## Notes

- Posting is public and attributed to the user's community account. Default is to post;
  pause at the draft only when the user asks.
- If the tag picker, URL or form layout differs from this file, finish the job, then
  update this skill and `channels.json` with what you found and the date.
