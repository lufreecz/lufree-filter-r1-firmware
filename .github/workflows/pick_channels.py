"""Write channels/stable.json and channels/beta.json from the release list.

usage: pick_channels.py releases.json OUT_DIR
releases.json is the REST answer of GET /repos/{owner}/{repo}/releases.
Each release carries a manifest.json asset written by the build workflow.
"""
import json
import os
import re
import sys
import urllib.request


def key(version):
    m = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-beta\.(\d+))?$", version or "")
    if not m:
        return None
    x, y, z, beta = m.groups()
    return (int(x), int(y), int(z), int(beta) if beta else 10**6)  # release above its betas


best = {"stable": None, "beta": None}
for rel in json.load(open(sys.argv[1], encoding="utf-8")):
    if rel.get("draft"):
        continue
    asset = next((a for a in rel.get("assets", []) if a["name"] == "manifest.json"), None)
    if not asset:
        continue
    with urllib.request.urlopen(asset["browser_download_url"]) as r:
        manifest = json.load(r)
    k = key(manifest.get("version"))
    if k is None:
        continue
    for ch in (["beta"] if rel.get("prerelease") else ["beta", "stable"]):
        if best[ch] is None or k > best[ch][0]:
            best[ch] = (k, manifest)

for ch, item in best.items():
    out = os.path.join(sys.argv[2], ch + ".json")
    if item is None:
        if os.path.exists(out):
            os.remove(out)
        print(ch, "-> none")
    else:
        json.dump(item[1], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(ch, "->", item[1]["version"])
