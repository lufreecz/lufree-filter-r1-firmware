"""Pick the newest manifest for each channel.

usage: pick_channels.py releases.json MANIFEST_DIR OUT_DIR
"""
import json
import os
import re
import sys


def key(version):
    m = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-beta\.(\d+))?$", version)
    if not m:
        return None
    x, y, z, beta = m.groups()
    # a release ranks above its own betas
    return (int(x), int(y), int(z), int(beta) if beta else 10**6)


releases = json.load(open(sys.argv[1]))
best = {"stable": None, "beta": None}
for r in releases:
    if r.get("isDraft"):
        continue
    path = os.path.join(sys.argv[2], r["tagName"] + ".json")
    if not os.path.exists(path):
        continue
    manifest = json.load(open(path, encoding="utf-8"))
    k = key(manifest.get("version", ""))
    if k is None:
        continue
    channels = ["beta"] if r["isPrerelease"] else ["beta", "stable"]
    for ch in channels:
        if best[ch] is None or k > best[ch][0]:
            best[ch] = (k, manifest)

for ch, item in best.items():
    out = os.path.join(sys.argv[3], ch + ".json")
    if item is None:
        if os.path.exists(out):
            os.remove(out)
        print(ch, "-> none")
        continue
    json.dump(item[1], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(ch, "->", item[1]["version"])
