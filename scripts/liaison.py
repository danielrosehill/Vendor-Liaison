#!/usr/bin/env python3
"""Vendor channel data and the user's private overlay, merged into a route.

Subcommands (all print JSON):
  paths                      where vendor data and the user overlay are read from
  vendors                    every known vendor (public and private)
  show VENDOR                the merged record for one vendor
  route VENDOR PURPOSE       ranked channels for one purpose, with the reason for each
  validate [VENDOR ...]      check vendor files and overlays against the rules below

Public vendor data: <repo>/vendors/<id>/vendor.json
User overlay:       <data-root>/vendor-liaison/<id>.json   (never in the repo)

Standard library only.
"""
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VENDOR_DIR = REPO / "vendors"
TOOL = "vendor-liaison"

PURPOSES = {"bug", "feature", "security", "support", "question", "feedback", "docs"}
CHANNEL_TYPES = {
    "github-issues", "github-discussions", "gitlab-issues", "issue-tracker",
    "email", "contact-form", "in-app", "forum", "reddit", "discord", "slack",
    "feature-board", "app-store-review", "bug-bounty", "social",
    "whatsapp", "signal", "telegram", "phone", "in-person", "contact", "other",
}
VISIBILITY = {"public", "private"}
STATUS = {"confirmed", "inferred", "dead"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def data_root():
    """Resolve the user-data root. Returns (path, rule that fired)."""
    if os.environ.get("VENDOR_LIAISON_DATA"):
        return Path(os.environ["VENDOR_LIAISON_DATA"]).expanduser(), "VENDOR_LIAISON_DATA"
    if os.environ.get("CLAUDE_USER_DATA"):
        return Path(os.environ["CLAUDE_USER_DATA"]).expanduser() / TOOL, "CLAUDE_USER_DATA"
    xdg = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share") / "claude-plugins"
    for root in (Path.home() / ".claude-user-data", xdg):
        if root.is_dir():
            return root / TOOL, f"existing root {root}"
    return Path.home() / ".claude-user-data" / TOOL, "default"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def public_vendor(vid):
    p = VENDOR_DIR / vid / "vendor.json"
    return load_json(p) if p.is_file() else None


def overlay(vid):
    p = data_root()[0] / f"{vid}.json"
    return load_json(p) if p.is_file() else None


def all_vendor_ids():
    ids = {p.parent.name for p in VENDOR_DIR.glob("*/vendor.json")}
    root = data_root()[0]
    if root.is_dir():
        for p in root.glob("*.json"):
            try:
                if "vendor" in load_json(p) or p.stem in ids:
                    ids.add(p.stem)
            except (OSError, json.JSONDecodeError):
                pass
    return sorted(ids)


def contact_channels(ov):
    """Each private contact becomes a channel, id 'contact:<id>'."""
    out = []
    for c in (ov or {}).get("contacts", []):
        out.append({
            "id": f"contact:{c['id']}",
            "type": "contact",
            "target": c.get("name", c["id"]),
            "visibility": "private",
            "purposes": c.get("use_for", []),
            "status": "confirmed",
            "source": "user",
            "contact": c,
        })
    return out


def merged(vid):
    pub = public_vendor(vid)
    ov = overlay(vid)
    if pub is None and not (ov and "vendor" in ov):
        raise SystemExit(json.dumps({"error": f"unknown vendor '{vid}'", "known": all_vendor_ids()}))
    base = dict(pub) if pub else dict(ov["vendor"])
    base["origin"] = "public" if pub else "private"
    channels = [dict(c, source=c.get("source", "vendor data")) for c in base.get("channels", [])]
    if ov:
        for c in ov.get("channels", []):
            channels.append(dict(c, source=c.get("source", "user")))
        channels += contact_channels(ov)
    base["channels"] = channels
    base["overlay"] = {
        "path": str(data_root()[0] / f"{vid}.json"),
        "exists": ov is not None,
        "prefer": (ov or {}).get("prefer", {}),
        "avoid": (ov or {}).get("avoid", []),
        "notes": (ov or {}).get("notes"),
    }
    if pub and (VENDOR_DIR / vid / "reporting.md").is_file():
        base["notes_file"] = str(VENDOR_DIR / vid / "reporting.md")
    return base


def route(vid, purpose):
    if purpose not in PURPOSES:
        raise SystemExit(json.dumps({"error": f"unknown purpose '{purpose}'", "purposes": sorted(PURPOSES)}))
    v = merged(vid)
    by_id = {c["id"]: c for c in v["channels"]}
    avoid = set(v["overlay"]["avoid"])
    warnings = []

    def usable(c):
        if c.get("status") == "dead" or c["id"] in avoid:
            return False
        if purpose not in c.get("purposes", []):
            return False
        # Hard rule: an undisclosed vulnerability never goes to a public channel.
        if purpose == "security" and c.get("visibility") != "private":
            return False
        return True

    ranked, seen = [], set()

    def add(cid, reason):
        c = by_id.get(cid)
        if c is None:
            warnings.append(f"'{cid}' is referenced but not defined")
            return
        if cid in seen:
            return
        if not usable(c):
            if reason == "user preference":
                why = "it is public" if purpose == "security" and c.get("visibility") != "private" else \
                      "it is dead, avoided, or not listed for this purpose"
                warnings.append(f"preferred channel '{cid}' skipped: {why}")
            return
        seen.add(cid)
        ranked.append(dict(c, reason=reason))

    pref = v["overlay"]["prefer"].get(purpose)
    if pref:
        add(pref["channel"], "user preference")
        if ranked and pref.get("why"):
            ranked[0]["why"] = pref["why"]
    for cid in v.get("routing", {}).get(purpose, []):
        add(cid, "vendor routing")
    for c in v["channels"]:
        if c["id"] not in seen and usable(c):
            add(c["id"], "also accepts this purpose")

    if not ranked:
        warnings.append(f"no usable channel for '{purpose}'"
                        + ("; for security, look for /.well-known/security.txt or a security@ address"
                           if purpose == "security" else ""))
    for i, c in enumerate(ranked, 1):
        c["rank"] = i
    return {
        "vendor": vid,
        "name": v.get("name"),
        "purpose": purpose,
        "route": ranked,
        "skill": v.get("skills", {}).get(purpose),
        "rules": v.get("rules", []),
        "notes_file": v.get("notes_file"),
        "verified": v.get("verified"),
        "overlay": v["overlay"]["path"] if v["overlay"]["exists"] else None,
        "warnings": warnings,
    }


def check_channel(c, where, errs):
    for k in ("id", "type", "target", "visibility", "purposes", "status"):
        if k not in c:
            errs.append(f"{where}: channel {c.get('id', '?')} missing '{k}'")
    if c.get("type") not in CHANNEL_TYPES:
        errs.append(f"{where}: channel {c.get('id')} type '{c.get('type')}' not in {sorted(CHANNEL_TYPES)}")
    if c.get("visibility") not in VISIBILITY:
        errs.append(f"{where}: channel {c.get('id')} visibility must be public|private")
    if c.get("status") not in STATUS:
        errs.append(f"{where}: channel {c.get('id')} status must be confirmed|inferred|dead")
    for p in c.get("purposes", []):
        if p not in PURPOSES:
            errs.append(f"{where}: channel {c.get('id')} purpose '{p}' unknown")


def validate(ids):
    errs = []
    for vid in ids or all_vendor_ids():
        pub = public_vendor(vid)
        if pub:
            where = f"vendors/{vid}/vendor.json"
            if pub.get("id") != vid:
                errs.append(f"{where}: id '{pub.get('id')}' does not match folder")
            if not DATE.match(str(pub.get("verified", ""))):
                errs.append(f"{where}: 'verified' must be YYYY-MM-DD")
            ids_seen = set()
            for c in pub.get("channels", []):
                check_channel(c, where, errs)
                if c.get("id") in ids_seen:
                    errs.append(f"{where}: duplicate channel id {c.get('id')}")
                ids_seen.add(c.get("id"))
            for purpose, order in pub.get("routing", {}).items():
                if purpose not in PURPOSES:
                    errs.append(f"{where}: routing purpose '{purpose}' unknown")
                for cid in order:
                    c = next((x for x in pub.get("channels", []) if x.get("id") == cid), None)
                    if c is None:
                        errs.append(f"{where}: routing.{purpose} names unknown channel '{cid}'")
                    elif purpose not in c.get("purposes", []):
                        errs.append(f"{where}: routing.{purpose} uses '{cid}', which does not list that purpose")
                    elif purpose == "security" and c.get("visibility") != "private":
                        errs.append(f"{where}: routing.security uses public channel '{cid}'")
        ov = overlay(vid)
        if ov:
            where = f"overlay {vid}.json"
            for c in ov.get("channels", []):
                check_channel(c, where, errs)
            for c in ov.get("contacts", []):
                if "id" not in c:
                    errs.append(f"{where}: contact without 'id'")
            if "vendor" in ov:
                for c in ov["vendor"].get("channels", []):
                    check_channel(c, where + " (vendor)", errs)
        if not pub and not (ov and "vendor" in ov):
            errs.append(f"{vid}: no public vendor.json and no private vendor definition")
    return {"ok": not errs, "errors": errs}


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    if cmd == "paths":
        root, rule = data_root()
        out = {"vendors": str(VENDOR_DIR), "overlay_dir": str(root), "rule": rule, "overlay_dir_exists": root.is_dir()}
    elif cmd == "vendors":
        out = [{"id": v, "name": merged(v).get("name"), "origin": merged(v)["origin"],
                "has_overlay": overlay(v) is not None} for v in all_vendor_ids()]
    elif cmd == "show" and len(args) == 1:
        out = merged(args[0])
    elif cmd == "route" and len(args) == 2:
        out = route(*args)
    elif cmd == "validate":
        out = validate(args)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0 if out["ok"] else 1
    else:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
