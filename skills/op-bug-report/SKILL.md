---
name: op-bug-report
description: Report a 1Password bug on the Community — version check against latest release, duplicate search, environment details, tagged topic.
---

# Report a 1Password bug

Use when the user says "report a 1Password bug", "1Password isn't syncing / filling /
unlocking", "file this with 1Password", or describes 1Password misbehaving.

Read `${CLAUDE_PLUGIN_ROOT}/vendors/1password/posting-guide.md` and `${CLAUDE_PLUGIN_ROOT}/vendors/1password/channels.json` first.

## Inputs

- What happened, what was expected, how often (always / intermittent), since when.
- Product and platform, if the user knows.

## Steps

1. **Collect the environment from the machine, not the user.** Every bug report needs:
   - desktop app version (`1password --version` on Linux; About screen elsewhere);
   - browser extension version (Chromium: the version directory under
     `<profile>/Extensions/aeblfdkhhhdcdjpifhhbdiojplfjncoa/`);
   - browser and version (`google-chrome --version`, etc.);
   - OS and version (`lsb_release -ds`, `sw_vers`), and on Linux the session type
     (`$XDG_SESSION_TYPE`);
   - `op --version` if the CLI is involved.
2. **Version currency check, before anything else.** Compare the installed versions to
   the latest stable in `https://releases.1password.com/<platform>/index.xml` (items are
   oldest-first; sort by `pubDate`). If the installed app is behind:
   - search the release notes between the two versions for a fix (grep the item
     descriptions for the symptom's keywords);
   - find out why it is behind. On Debian/Ubuntu: check
     `/etc/apt/sources.list.d/` for a `1password.list`. A `1password.list.save` with no
     `.list` means a distro release upgrade disabled the repo, and the app silently stopped
     updating; `apt-cache policy 1password` then shows the old version as "Candidate".
     Compare with the repo's real
     `https://downloads.1password.com/linux/debian/amd64/dists/stable/main/binary-amd64/Packages`;
     the fix is to restore the source (`mv 1password.list.save 1password.list`), `apt-get
     update`, `apt-get install --only-upgrade 1password`. Recent packages (seen on
     8.12.42, 2026-10-21) then write their own deb822 `1password.sources` ("Installing the
     debian auto-update channel"); move the restored `.list` back to `.save` so the source
     is not configured twice. The upgrade stops the app; relaunch with `1password --silent`;
   - tell the user, and ask to update and re-test before filing. Staff will ask for this
     first, and a report against an old version is usually closed as fixed. Updating
     changes the system, so get a yes; do not do it silently.
3. **Duplicate search.** Run `op-fr-search` with the symptom's keywords (both the
   sitemap helper and the browser keyword search). For a matching open thread on a
   current version, add the user's environment and observations there
   (`op-community-engage`) instead of opening a new topic.
4. **Gather reproduction detail.** Steps, frequency, timing (e.g. "item appears after
   2–5 minutes"), what does and does not fix it (lock/unlock, restarting the app,
   manual sync), and relevant settings (e.g. desktop app integration on/off). Get
   timings by testing when possible, not from memory.
5. **Draft** using the bug template below. Title starts `[Bug] ` and names the platform.
   No account email, vault or item names, Secret Key, or screenshots that show them.
6. **Post by default**, as in `op-feature-request` step 6, with these differences:
   - topic type **Question** (so staff or others can mark a solution);
   - category home (`fid=31`), work (`fid=58`) or developers (`fid=69`);
   - tags: the platform (`Linux`, `Windows`, `macOS`, `iOS`, `Android`), plus
     `Browser Extension` or `CLI` when involved. Do not add `Feature Request`.
   Stop at the draft only if the user asks.
7. **Mention the diagnostics route** in the report to the user: staff often ask for a
   diagnostics report sent privately to `support@1password.com` with a link to the
   thread. Never attach diagnostics to the public post.
8. **Log** via `op-fr-tracker` with `"kind": "bug"`.

## Bug template

```
Title: [Bug] <Platform>: <symptom in one line>

What happens
<observed behaviour, with frequency and timing>

Expected
<what should happen>

Steps to reproduce
1. ...

Environment
- 1Password app: <version> (<channel>)
- Browser extension: <version> in <browser> <version>
- OS: <distro/version>, <session type>
- Desktop app integration: on/off

Already tried
<lock/unlock, restart, manual sync, update ...>

Related
<links to related threads, if any>
```
