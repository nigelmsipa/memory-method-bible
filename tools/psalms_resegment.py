#!/usr/bin/env python3
"""Apply the Psalms Resegmentation Audit (2026-08-14) to psalms-base.json.

The audit's finding: the existing 748 units are a memorization-chunk map, not a
literary-scene map. Every unit is <=6 verses, which conflicts with the repo's
locked rule that boundaries come from the text, not a verse-count target.

The fix is hierarchical, not destructive:
    Book -> Psalter Book -> Psalm -> poetic scene/strophe -> memorization chunk
Revised scenes come from the audit table. The existing ranges survive underneath
as an optional `chunks` array. Psalms not named in the audit are untouched.

Run with --write to modify the file; default is a dry run.
"""
import json, sys, re
from collections import OrderedDict

BASE = "/home/nigel/memory-method-bible/data/base-structure/psalms-base.json"

# --- the audit's high-confidence boundary changes, verbatim -------------------
# psalm -> revised poetic scene ranges as (first_verse, last_verse)
def R(spec):
    out = []
    for part in spec.split(";"):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-"); out.append((int(a), int(b)))
        else:
            out.append((int(part), int(part)))
    return out

REVISED = {
    18:  R("1-3;4-6;7-15;16-19;20-24;25-29;30-36;37-42;43-45;46-50"),
    19:  R("1-6;7-11;12-14"),
    22:  R("1-5;6-11;12-18;19-21;22-26;27-31"),
    45:  R("1-2;3-9;10-15;16-17"),
    51:  R("1-2;3-6;7-12;13-17;18-19"),
    59:  R("1-5;6-10;11-13;14-17"),
    69:  R("1-6;7-12;13-18;19-21;22-28;29-33;34-36"),
    71:  R("1-6;7-11;12-16;17-21;22-24"),
    73:  R("1-3;4-12;13-17;18-20;21-26;27-28"),
    77:  R("1-3;4-9;10-15;16-20"),
    78:  R("1-8;9-16;17-31;32-39;40-55;56-64;65-72"),
    89:  R("1-4;5-14;15-18;19-29;30-37;38-45;46-51;52"),
    90:  R("1-6;7-12;13-17"),
    91:  R("1-2;3-8;9-13;14-16"),
    102: R("1-2;3-11;12-17;18-22;23-28"),
    103: R("1-5;6-10;11-14;15-18;19-22"),
    104: R("1-4;5-9;10-18;19-23;24-30;31-35"),
    105: R("1-6;7-15;16-22;23-36;37-41;42-45"),
    106: R("1-5;6-12;13-18;19-23;24-27;28-31;32-33;34-39;40-46;47-48"),
    107: R("1-3;4-9;10-16;17-22;23-32;33-38;39-43"),
    109: R("1-5;6-20;21-25;26-29;30-31"),
    116: R("1-4;5-9;10-14;15-19"),
    118: R("1-4;5-9;10-14;15-18;19-21;22-24;25-27;28-29"),
    119: [(i, i + 7) for i in range(1, 177, 8)],   # 22 alphabetic stanzas of 8
    121: R("1-8"),
    132: R("1-5;6-10;11-12;13-18"),
    136: R("1-3;4-9;10-15;16-22;23-26"),
    139: R("1-6;7-12;13-18;19-24"),
    147: R("1-6;7-11;12-14;15-18;19-20"),
}

# audit "Reason" text -> recorded on the revised scene so the rationale survives
REASON = {
    18: "Theophany, rescue, vindication, divine character, battle, and doxology are broader completed movements; several three-verse cuts merely interrupt one image or action.",
    19: "The classic creation / Torah / prayer structure. The former 7-9 and 10-14 cut broke the Torah movement between description and value-response.",
    22: "Complaint alternates with remembered trust, reaches its animal-encirclement climax, pivots to urgent petition, then to public and worldwide praise.",
    45: "Prologue and address to the king, royal portrait, address to the bride, dynastic conclusion. The former two- and three-verse cuts over-segmented each address.",
    51: "Cleansing and renewal at 7-12 form one sustained petition; teaching, praise, and acceptable sacrifice at 13-17 form one response.",
    59: "Repeated dog imagery and fortress refrains organize the poem more strongly than the former short cuts.",
    69: "Lament, reproach, rescue petition, poisonous treatment, imprecation, personal praise, cosmic and Zion conclusion.",
    71: "Lifelong trust, public reproach, renewed plea, old-age vocation, and final praise.",
    73: "Envy, portrait of the wicked, sanctuary hinge, their end, restored perspective, conclusion.",
    77: "Selah and the turn from sleepless questioning to remembrance, then Exodus theophany, give four coherent movements.",
    78: "Prologue; Ephraim and Exodus memory; wilderness food rebellion; shallow repentance and mercy; plagues-to-land deliverance; apostasy and Shiloh; Judah-Zion-David resolution.",
    89: "Covenant opening; cosmic kingship; blessed people; Davidic grant; covenant discipline and immutability; apparent rejection; lament; Book III doxology. Verse 52 remains a separate editorial doxology.",
    90: "God's eternity against human transience; wrath and numbered days; plea for compassion and established work.",
    91: "The former 1-4 range crossed the voice and stance change after the personal confession in verse 2. The divine oracle at 14-16 is unmistakably separate.",
    102: "Invocation; personal wasting; Zion hope; future generations and nations; mortal weakness against God's permanence.",
    103: "Self-exhortation and benefits; justice and mercy; fatherly compassion; mortal grass against enduring covenant love; cosmic summons.",
    104: "Robed Creator; earth and water boundaries; provision and habitats; ordered times; sea and dependent creatures; closing praise.",
    105: "Summons; patriarchal covenant; Joseph; Egypt and the plagues; Exodus and wilderness provision; covenant-purpose conclusion.",
    106: "Opening prayer followed by the poem's successive rebellion episodes, judgment and mercy synthesis, and Book IV doxology.",
    107: "Introduction; four complete distress-cry-deliverance-thanks cycles; providential reversal; wisdom conclusion. The refrains at 8, 15, 21 and 31 close rather than bisect the four central scenes.",
    109: "Complaint; sustained curse speech; afflicted petition; plea for public vindication; praise. Smaller rehearsal chunks are kept inside 6-20.",
    116: "Heard prayer; gracious deliverance and rest; faith and vows; precious death, service and thanksgiving.",
    118: "Liturgical calls, testimony, the nations' attack, victory song, gates, cornerstone and day, festal procession, final thanks.",
    119: "Non-negotiable formal structure: 22 Hebrew-letter stanzas of eight lines each. The alphabetic marker, not an imposed verse count, fixes both boundaries.",
    121: "A compact Song of Ascents unified by the repeated root shamar (keep, watch) across the whole psalm.",
    132: "David's oath; procession and prayer; covenant condition; Zion election and promises.",
    136: "Opening thanksgiving; creation; Exodus; wilderness and conquest; remembered low estate and universal provision. The recurring response binds the litany and is not 26 separate scenes.",
    139: "God's exhaustive knowledge, inescapable presence, creative formation, and the psalmist's final alignment and search prayer. One of the clearest cases of over-segmentation.",
    147: "Two praise summons (verses 1 and 12) and their internal developments. The Greek tradition's division between verses 11 and 12 is structurally informative though canonical numbering remains 147.",
}

HEBREW_LETTERS = ["Aleph","Beth","Gimel","Daleth","He","Vau","Zain","Cheth","Teth","Jod",
                  "Caph","Lamed","Mem","Nun","Samech","Ain","Pe","Tzaddi","Koph","Resh",
                  "Schin","Tau"]

# Psalms 42-43 are one poetic complex; canonical numbering is untouched.
LINKED_COMPLEX = {42: "Psalms 42-43", 43: "Psalms 42-43"}


def parse_ref(ref):
    m = re.match(r"^\s*(\d+):(\d+)(?:\s*-\s*(?:(\d+):)?(\d+))?\s*$", ref)
    if not m:
        raise ValueError(f"unparseable reference: {ref!r}")
    ch = int(m.group(1)); v1 = int(m.group(2))
    v2 = int(m.group(4)) if m.group(4) else v1
    return ch, v1, v2


KJV = "/home/nigel/memory-method-bible/source-texts/KJV.txt"
_kjv = None

def kjv_verse(chapter, verse):
    """KJV.txt is 'Psalm C:V<TAB>text' (singular 'Psalm'), with supplied words in
    [brackets] per the KJV italics convention. Edition 2 drops the brackets in its
    incipits, so do the same here."""
    global _kjv
    if _kjv is None:
        _kjv = {}
        with open(KJV, encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.startswith("Psalm "):
                    continue
                ref, _, text = line.partition("\t")
                m = re.match(r"^Psalm (\d+):(\d+)$", ref.strip())
                if m:
                    _kjv[(int(m.group(1)), int(m.group(2)))] = \
                        text.strip().replace("[", "").replace("]", "")
    return _kjv.get((chapter, verse), "")


def incipit(chapter, verse, lo=4, hi=12):
    """Title a re-cut continuation the way edition 2 does: the opening words of
    its first verse, 4-12 words of KJV, no invention."""
    words = kjv_verse(chapter, verse).split()
    if not words:
        return None
    take = words[:hi]
    for n in range(lo, len(take) + 1):          # stop at the first clause boundary
        if take[n - 1].endswith((",", ";", ":", ".", "?", "!")):
            take = take[:n]
            break
    return " ".join(take).rstrip(",;:.!?").rstrip()


def make_chunks(scene_lo, scene_hi, source_scenes):
    """Existing ranges become chunks. They must tile the parent exactly, so cut on
    every existing boundary falling inside the scene and clamp the ends. A scene
    already small enough (<=6 verses) with no internal boundary gets no chunks."""
    cuts = sorted({lo for (lo, hi, name) in source_scenes if scene_lo < lo <= scene_hi})
    if not cuts:
        return []
    bounds = [scene_lo] + cuts + [scene_hi + 1]
    chunks = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1] - 1
        if lo > hi:
            continue
        src = next(((a, b, n) for (a, b, n) in source_scenes if a <= lo <= b), None)
        # A source unit clamped by a new scene boundary is now two pieces. Only the
        # piece that still opens where the source opened may keep its title; giving
        # both the same name would put two identical footholds in one psalm.
        title = src[2] if src and src[0] == lo else None
        chunks.append((lo, hi, title))
    # a chunk may not exceed the memorisation ceiling of 6 verses; split evenly
    out = []
    for lo, hi, title in chunks:
        n = hi - lo + 1
        if n <= 6:
            out.append((lo, hi, title)); continue
        parts = -(-n // 6)
        size = -(-n // parts)
        v = lo
        while v <= hi:
            out.append((v, min(v + size - 1, hi), title if v == lo else None))
            v += size
    return out


def main(write=False):
    doc = json.load(open(BASE))
    # NOT idempotent: it expects the pre-audit 748-scene file as input. Running it
    # against its own output would treat coarse literary scenes as source units.
    if any("chunks" in sc for st in doc["stories"] for sc in st["scenes"]):
        sys.exit("psalms-base.json already carries `chunks` — the audit has been applied.\n"
                 "To re-run, restore the pre-audit file first:\n"
                 "  git -C ~/memory-method-bible show 84cbc48^:data/base-structure/psalms-base.json"
                 " > data/base-structure/psalms-base.json")
    report = []
    total_before = total_after = 0
    chunk_total = 0

    for story in doc["stories"]:
        rebuilt = []
        # group this Book's scenes by psalm, preserving order
        by_psalm = OrderedDict()
        for sc in story["scenes"]:
            ch, v1, v2 = parse_ref(sc["reference"])
            by_psalm.setdefault(ch, []).append((v1, v2, sc))

        for psalm, entries in by_psalm.items():
            total_before += len(entries)
            if psalm not in REVISED:
                for _, _, sc in entries:                      # untouched
                    sc.pop("chunks", None)
                    if psalm in LINKED_COMPLEX:
                        sc["linked_complex"] = LINKED_COMPLEX[psalm]
                    rebuilt.append(sc)
                    total_after += 1
                continue

            src = [(v1, v2, sc["scene_name"]) for v1, v2, sc in entries]
            src_lo = min(a for a, _, _ in src); src_hi = max(b for _, b, _ in src)
            new_ranges = REVISED[psalm]
            if (new_ranges[0][0], new_ranges[-1][1]) != (src_lo, src_hi):
                report.append(f"  !! Psalm {psalm}: revised span {new_ranges[0][0]}-{new_ranges[-1][1]}"
                              f" != current span {src_lo}-{src_hi}")

            for idx, (lo, hi) in enumerate(new_ranges):
                if psalm == 119:
                    name = f"Psalm 119 – {HEBREW_LETTERS[idx]}"
                else:
                    # Preserve the in-house title of the movement's opening unit —
                    # but only when the movement actually opens where that unit
                    # opened. Where a new boundary cuts into the middle of an old
                    # unit, reusing its title would repeat a name inside the psalm,
                    # so label from the text instead (edition 2's incipit rule).
                    opener = next(((a, b, n) for (a, b, n) in src if a <= lo <= b), None)
                    if opener and opener[0] == lo:
                        name = opener[2]
                    else:
                        name = f"Psalm {psalm} – {incipit(psalm, lo) or f'{lo}-{hi}'}"
                ref = f"{psalm}:{lo}-{hi}" if hi > lo else f"{psalm}:{lo}"
                scene = {
                    "scene_number": None,
                    "scene_name": name,
                    "reference": ref,
                    "why_start_end_and_devices": REASON[psalm],
                }
                if psalm in LINKED_COMPLEX:
                    scene["linked_complex"] = LINKED_COMPLEX[psalm]
                chunks = make_chunks(lo, hi, src)
                if chunks:
                    scene["chunks"] = [
                        {"chunk_number": i + 1,
                         "chunk_name": t or f"Psalm {psalm} – {incipit(psalm, a) or f'{a}-{b}'}",
                         "reference": f"{psalm}:{a}-{b}" if b > a else f"{psalm}:{a}"}
                        for i, (a, b, t) in enumerate(chunks)
                    ]
                    chunk_total += len(chunks)
                rebuilt.append(scene)
                total_after += 1

        for i, sc in enumerate(rebuilt, 1):                   # renumber within Book
            sc["scene_number"] = str(i)
            if "chunks" in sc:                                # keep key order tidy
                ch = sc.pop("chunks"); sc["chunks"] = ch
        story["scenes"] = rebuilt
        report.append(f"  Book {story['story_letter']} {story['story_title'][:38]:<38} "
                      f"scenes -> {len(rebuilt)}")

    doc["big_picture_notes"] = doc["big_picture_notes"].replace(
        "For memorization, each psalm is a complete literary unit (scene).",
        "Each psalm is a complete poem and may contain one or more poetic scenes "
        "(strophes); a scene may in turn carry smaller memorization chunks.")

    print("\n".join(report))
    print(f"\nscenes {total_before} -> {total_after}   (audit expects 748 -> 609)")
    print(f"chunks created: {chunk_total}")
    if write:
        json.dump(doc, open(BASE, "w"), indent=2, ensure_ascii=False)
        print(f"WROTE {BASE}")
    return doc


if __name__ == "__main__":
    main(write="--write" in sys.argv)
