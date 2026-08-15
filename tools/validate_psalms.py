#!/usr/bin/env python3
"""Validation rules required by the Psalms Resegmentation Audit.

  - scene references must cover each story with no gaps or overlaps
  - chunks must exactly cover their parent scene with no gaps or overlaps
  - chunks may be size-limited for pedagogy (<=6 verses); scenes may not
  - Psalm 119 must validate as 22 eight-verse scenes (44 chunks)
  - canonical psalm/chapter numbers must be preserved (150 psalms, no renumbering)
  - every revised scene must match the audit table exactly
"""
import json, re, sys
sys.path.insert(0, "/home/nigel/memory-method-bible/tools")
from psalms_resegment import REVISED, parse_ref, BASE

def main():
    doc = json.load(open(BASE))
    fail = []
    psalms_seen = {}
    scene_total = chunk_total = 0

    for story in doc["stories"]:
        for sc in story["scenes"]:
            scene_total += 1
            ch, lo, hi = parse_ref(sc["reference"])
            psalms_seen.setdefault(ch, []).append((lo, hi))
            if "chunks" in sc:
                cs = [parse_ref(c["reference"]) for c in sc["chunks"]]
                chunk_total += len(cs)
                if any(c != ch for c, _, _ in cs):
                    fail.append(f"Ps {ch} {sc['reference']}: chunk in another psalm")
                spans = sorted((a, b) for _, a, b in cs)
                if spans[0][0] != lo or spans[-1][1] != hi:
                    fail.append(f"Ps {ch} {sc['reference']}: chunks do not cover the scene")
                for i in range(1, len(spans)):
                    if spans[i][0] != spans[i-1][1] + 1:
                        fail.append(f"Ps {ch} {sc['reference']}: chunk gap/overlap at {spans[i]}")
                for a, b in spans:
                    if b - a + 1 > 6:
                        fail.append(f"Ps {ch} {sc['reference']}: chunk {a}-{b} exceeds 6 verses")

    # coverage: every psalm tiled start-to-finish, no gaps or overlaps
    for ch in sorted(psalms_seen):
        spans = sorted(psalms_seen[ch])
        if spans[0][0] != 1:
            fail.append(f"Ps {ch}: does not start at verse 1")
        for i in range(1, len(spans)):
            if spans[i][0] != spans[i-1][1] + 1:
                fail.append(f"Ps {ch}: gap/overlap between {spans[i-1]} and {spans[i]}")

    if len(psalms_seen) != 150:
        fail.append(f"expected 150 psalms, found {len(psalms_seen)}")
    missing = [n for n in range(1, 151) if n not in psalms_seen]
    if missing:
        fail.append(f"missing psalms: {missing}")

    # the audit table, exactly
    for psalm, ranges in REVISED.items():
        got = sorted((lo, hi) for c, lo, hi in
                     (parse_ref(sc["reference"])
                      for st in doc["stories"] for sc in st["scenes"]) if c == psalm)
        if got != sorted(ranges):
            fail.append(f"Ps {psalm}: scenes {got} != audit {sorted(ranges)}")

    # Psalm 119
    p119 = [sc for st in doc["stories"] for sc in st["scenes"]
            if parse_ref(sc["reference"])[0] == 119]
    n_chunks = sum(len(sc.get("chunks", [])) for sc in p119)
    if len(p119) != 22:
        fail.append(f"Psalm 119 has {len(p119)} scenes, expected 22")
    if n_chunks != 44:
        fail.append(f"Psalm 119 has {n_chunks} chunks, expected 44")
    if any(parse_ref(sc["reference"])[2] - parse_ref(sc["reference"])[1] + 1 != 8 for sc in p119):
        fail.append("Psalm 119 has a stanza that is not eight verses")

    print("scenes by Book:")
    for st in doc["stories"]:
        n = len(st["scenes"])
        c = sum(len(s.get("chunks", [])) for s in st["scenes"])
        print(f"  {st['story_letter']}  {st['story_title'][:40]:<40} {n:>4} scenes  {c:>4} chunks")
    print(f"\ntotal: {scene_total} scenes, {chunk_total} chunks, {len(psalms_seen)} psalms")
    print(f"Psalm 119: {len(p119)} scenes / {n_chunks} chunks")

    if fail:
        print(f"\n!! {len(fail)} FAILURES")
        for f in fail[:40]:
            print("   ", f)
        return 1
    print("\nALL VALIDATION PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
