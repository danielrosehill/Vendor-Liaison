---
name: security-disclosure
description: Disclose a security vulnerability to a software vendor responsibly, through a private channel only — bug-bounty program, security.txt contact, security@ address, or a trusted contact at the company — never a public tracker, forum or social post. Use when the user has found a vulnerability, data exposure, auth bypass, secret leak or other security flaw in someone else's product and wants to report it.
---

# Security disclosure

An undisclosed vulnerability must not appear anywhere public until the vendor has fixed
it or the agreed embargo has ended. The rule applies at every step below.

## 1. Find the private channel

```bash
python3 <plugin-root>/scripts/liaison.py route <vendor-id> security
```

The resolver already drops public channels. If it returns nothing usable, or the vendor
is unknown:

1. Fetch `https://<vendor-domain>/.well-known/security.txt`, then `/security.txt`. Use
   its `Contact`, `Policy`, `Encryption` and `Expires` fields, and ignore it if it has
   expired.
2. Look for a vendor security page or a bug-bounty listing (HackerOne, Bugcrowd,
   Intigriti).
3. For an open-source project, look for `SECURITY.md` and GitHub private vulnerability
   reporting (the "Report a vulnerability" button under the repo's Security tab).
4. Failing all of those, write to a `security@` address, or ask a personal contact from
   the overlay who the right recipient is, without giving details.

Record any new channel with the `add-vendor` skill so the next disclosure is quicker.

## 2. Before writing

- Don't search public trackers using words that describe the vulnerability. A public
  search for "auth bypass in X" can itself leak it. Searching the vendor's published
  advisories is fine.
- Read the vendor's policy for scope, safe harbour and disclosure timeline, and tell the
  user about anything that limits what they may test or say.
- Collect: affected product and versions, impact, the minimum reproduction, and when and
  how it was found. Don't run further tests against systems the user doesn't own.

## 3. Draft

- A factual summary of the impact and the affected versions.
- Reproduction steps, with no working exploit beyond what is needed to show the issue.
- The user's contact details and preferred disclosure timeline. The common default is 90
  days, or the vendor's policy if that says otherwise.
- If the channel offers encryption (a PGP key in security.txt), encrypt, or tell the user
  to.
- If the first contact goes to a person rather than a security channel, ask only for the
  right channel. Send no details yet.

## 4. Approve, send, track

Show the draft and the destination, and send only after approval. Log it in
`<overlay_dir>/reports.jsonl` with purpose `security` and a summary that doesn't describe
the flaw (for example "disclosure sent, awaiting acknowledgement"). Remind the user of
the disclosure date. Nothing about the issue goes public before then, including commit
messages, notes in public repos, and posts.
