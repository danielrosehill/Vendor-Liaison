# Verification log

## 2026-10-21 — initial build

Confirmed (loaded and read):
- `https://www.1password.community/`, `/search/index?q=Feature%20Request&search_type=tag`,
  `/topic/new` — all HTTP 200, inSided/Gainsight markup. URLs supplied by the plugin author.
- `/sitemap.xml` is an index of two files: `sitemap-structure.xml` and
  `sitemap-topics-1.xml` (~25.8k `<url><loc>…</loc><lastmod>YYYY-MM-DD</lastmod>` entries;
  path = `<category-slug>-<id>/<title-slug>-<topic-id>`).
- Topic pages embed two JSON-LD blocks: `BreadcrumbList` (Home > Discussions > Topics >
  category > title) and `QAPage` with `mainEntity` {name, text, dateCreated, upvoteCount,
  author{name,url}, answerCount, acceptedAnswer}. Replies and tags are not in JSON-LD.
- Feature requests are normal topics: e.g. `developers-69/feature-request-per-application-
  authorization-policy-for-the-ssh-agent-25530` (title prefix "Feature Request:").
- `/ideas` loads with 0 ideas. `/api/v2/`, `/rss`, `/categories` → 404.
- `vendors/1password/scripts/community.py search|topic|recent` tested against the live site.

Inferred / not confirmed:
- Category `fid` values (31/58/69) come from category slugs and `?fid=` links; the
  new-topic form with those params has not been submitted.
- Product tag names beyond "Feature Request"; the tag picker was not opened logged in.
- Productboard as the internal tracker (from a `PB-` reference and a page-config flag).

Wrong turns worth not repeating:
- `community.1password.com` is a 1Password sign-in page, not the forum.
- Plain fetch of `/search?q=` returns the shell only; results load by JavaScript.
- `/ideas` looks like the FR board and is not.

## 2026-10-21 — first live post

Posted `1password-at-home-31/feature-request-default-save-vault-per-item-type-e-g-api-credentials-25878`.
Confirmed: `?fid=31` preselects the category; form opens with topic type *Question*
(switched to *Conversation*); body editor is CKEditor 4 and accepts `setData(html)`;
tag field needs the dropdown suggestion clicked, after which suggested product tags
appear as `+` chips. Create redirects to the topic. Sitemap and JSON-LD for the new
topic not yet checked (sitemap can lag).
