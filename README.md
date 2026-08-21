# The Memory Method Bible

A version-agnostic, text-driven biblical literary analysis framework for Scripture memorization optimized for structural integrity and cognitive retention.

## What Is This?

The Memory Method Bible divides Scripture into **scenes**—complete thoughts identified from the text's own internal structure—that serve as memorizable pericopes. Each scene is:

- **A complete thought** (defined by text boundaries, not arbitrary chapter breaks)
- **Text-driven** (boundaries justified by oracle formulas, speaker changes, narrative turns, location shifts)
- **Memorizable** (naturally small when correctly identified, typically a few verses)
- **Literarily justified** (organized into larger narrative stories with explicit literary glue)

This framework rejects arbitrary verse count targets and theological imposition, instead deriving all structure from **what the text itself shows**.

## Books Completed (66 — Full Canon)

All 66 books of the Bible have been converted: 296 stories, 7,962 scenes.

**OLD TESTAMENT** (39 books)

*LAW (Torah)*: Genesis (11 stories, 363 scenes), Exodus (5, 289), Leviticus (6, 207), Numbers (3, 297), Deuteronomy (5, 237)

*HISTORY*: Joshua (3, 153), Judges (10, 141), Ruth (4, 19), 1 Samuel (6, 192), 2 Samuel (5, 160), 1 Kings (10, 189), 2 Kings (5, 177), 1 Chronicles (4, 225), 2 Chronicles (8, 196), Ezra (2, 76), Nehemiah (4, 95), Esther (2, 39)

*POETRY & WISDOM*: Job (7, 229), Psalms (5, 609), Proverbs (6, 208), Ecclesiastes (5, 57), Song of Songs (5, 45), Lamentations (5, 39)

*MAJOR PROPHETS*: Isaiah (8, 449), Jeremiah (7, 505), Ezekiel (8, 476), Daniel (2, 104)

*MINOR PROPHETS*: Hosea (5, 60), Joel (2, 21), Amos (4, 46), Obadiah (1, 6), Jonah (2, 15), Micah (3, 26), Nahum (3, 13), Habakkuk (3, 16), Zephaniah (3, 13), Haggai (4, 7), Zechariah (4, 56), Malachi (4, 12)

**NEW TESTAMENT** (27 books)

*GOSPELS*: Matthew (7, 250), Mark (4, 156), Luke (6, 277), John (4, 197)

*ACTS*: Acts (7, 226)

*PAULINE EPISTLES*: Romans (7, 100), 1 Corinthians (5, 101), 2 Corinthians (3, 64), Galatians (4, 35), Ephesians (3, 40), Philippians (4, 24), Colossians (4, 22), 1 Thessalonians (3, 20), 2 Thessalonians (3, 11), 1 Timothy (4, 27), 2 Timothy (4, 20), Titus (3, 13), Philemon (1, 7)

*GENERAL EPISTLES*: Hebrews (5, 88), James (4, 28), 1 Peter (5, 27), 2 Peter (3, 15), 1 John (3, 21), 2 John (1, 4), 3 John (1, 4), Jude (1, 8)

*APOCALYPSE*: Revelation (8, 110)

---

## Project Structure

```
memory-method-bible/
├── data/base-structure/
│   ├── genesis-base.json
│   ├── exodus-base.json
│   ├── [64 additional books — full canon]
│   └── jeremiah-base.json
├── data/title-overlays/
│   ├── plain/          # Straightforward scene titles
│   ├── evocative/      # Vivid, memorable scene titles
│   └── archaic/        # Archaic/literary scene titles
├── source-texts/       # KJV, WEB, BSB, Majority text
├── exports/            # Markdown exports (e.g., Jeremiah)
├── tools/              # Validation & resegmentation scripts
├── CONVERSION_GUIDE.md # Master Specification & JSON conversion process
├── BIBLE-BOOK-ANALYSIS-SPEC-V1.md  # Analysis spec
├── IDEAS.md
├── JEREMIAH-V1-GUIDE.md
└── README.md           # This file
```

**Base structure JSON format:**
- `book_name` - Book title
- `hebrew_name` - Original Hebrew/Aramaic name
- `canonical_grouping` - Position in Hebrew Tanakh or Christian canon
- `big_picture_notes` - Literary and structural overview
- `stories` - Array of narrative/literary units with:
  - `story_letter` - A, B, C, etc.
  - `story_title` - Name of the unit
  - `why_start_end_and_literary_glue` - Justification and literary devices
  - `reference` - Verse range (e.g., "1:1 - 4:22")
  - `scenes` - Array of scenes (each scene = complete thought with text-driven boundaries)

## How It Works

### The Master Specification
**See `CONVERSION_GUIDE.md` for the authoritative specification.**

A **scene** is identified by:
1. **Text-driven boundaries** - Each scene begins and ends at a natural break marked by the text itself:
   - Oracle formulas ("The word of the LORD came...")
   - Speaker changes ("Then Elijah said...")
   - Location shifts ("When they came to...")
   - Time shifts ("At evening..." / "The next day...")
   - Narrative turns ("So the matter was settled...")
2. **Single complete thought** - Each scene develops ONE narrative or textual idea
3. **Self-containment** - A reader could understand the scene in isolation
4. **Memorable** - When boundaries are correctly identified from text, scenes naturally become small enough to memorize (typically a few verses)

### Example: Ruth 1:6-14 ("The Debate on the Road")
```json
{
  "scene_number": 2,
  "scene_name": "Naomi Urges Her Daughters-in-Law Home",
  "reference": "1:6-1:9",
  "why_start_end_and_devices": "Starts with new action: 'Then she arose with her daughters-in-law to return...' (1:6). Ends with Naomi's blessing and release of her daughters-in-law (1:9). Verse 10 begins the daughters' resistance, a new movement in the dialogue."
}
```

**Why these boundaries?**
- Starts: "Then she arose" = narrative turn, new action begins
- Ends: Naomi's blessing completes her first attempt to send them away
- Literary device: Repetition of "return" (shuv) throughout the chapter

## Using This Framework

### For Memorization
1. Open the **base structure** file (e.g., `ruth-base.json`)
2. Read the **story** title and **why_start_end_and_literary_glue** to understand the narrative arc
3. For each **scene**, read the **scene_name** and **why_start_end_and_devices** to understand:
   - Where the scene begins (what text marker triggers it)
   - Where it ends (what completion it reaches)
   - What literary devices hold it together
4. Use the scene name as a memory hook via the **Method of Loci** (Memory Palace technique)
5. Associate each scene's narrative or textual idea with a location in your memory palace
6. Practice sequential recall through your memory palace, verifying boundaries at text markers

### For Study
1. Open a book's `*-base.json` file to see all story and scene boundaries with text justifications
2. Use chapter:verse references to locate text in your own Bible translation
3. Verify scene boundaries by identifying the text markers cited in the `why_start_end_and_devices` field
4. Study the literary devices (repetition, parallelism, inclusio, etc.) that hold each unit together

### For Development
1. Generate annotated Scripture documents by combining base structure with Bible text
2. Create Bible reading apps with scene/story-based navigation (not arbitrary chapter breaks)
3. Build memorization tools (flashcards, spaced repetition) keyed to scene names
4. Generate custom Bible study formats organized by narrative arc, not chapter divisions
5. Convert JSON to First-Letter Pericope memory aids (see CONVERSION_GUIDE.md Part 8)

## Known Issues & Revisions Required

### Priority Revisions
See the **Master Specification Audit Report** (generated 2025-11-17) for detailed analysis.

**Critical (Must Fix):**
1. **1 Kings 7:13-47** (35 verses) - Split into 3 scenes
2. **1 Kings 6:14-38** (25 verses) - Split into 2 scenes
3. **2 Kings 3:1-27** (27 verses) - Split into 3 scenes
4. **1 Kings 2:26-46** (21 verses) - Split into 3 scenes
5. **2 Samuel 18:6-17** (12 verses) - Split into 2 scenes

**Should Fix:**
6. **1 Kings 13:11-32** (22 verses) - Split into 2 scenes
7. **1 Samuel 18:17-30** (14 verses) - Split into 2 scenes
8. **1 Samuel 25:1-12** (12 verses) - Samuel's death deserves separate scene

## Core Principles

The Memory Method Bible is built on several key principles:

1. **Text-Driven Structure**: All boundaries derive from what the text itself shows (oracle formulas, speaker changes, narrative turns, location/time shifts)—not from theology, chapter breaks, or arbitrary verse counts
2. **Complete Thoughts**: Each scene is a single, coherent unit with a clear beginning and natural ending
3. **Zero Imposed Frameworks**: No verse-count targets, no theological themes projected onto the text, no arbitrary divisions
4. **Memorability as Outcome**: When scenes are correctly identified, they naturally become small enough to memorize; this emerges from proper analysis, not pre-set constraints
5. **Literary Precision**: All literary devices are named with exactness (repetition, parallelism, chiasm, inclusio, etc.) and tied to specific text passages
6. **Translation Agnostic**: The structure works across all English Bible translations (KJV, ESV, NIV, NASB, etc.) because it's based on verse numbers and narrative structure, not translation-specific wording
7. **Comprehensive Justification**: Every scene boundary is explicitly justified in the JSON with text citations and device identification

## Contributing

To contribute literary analyses or revised scene boundaries:

1. **Read the Master Specification** in `CONVERSION_GUIDE.md` before beginning
2. **Analyze the text yourself** - Identify scenes by text boundaries, not by imposing a framework
3. **Justify every boundary** - Cite the text marker (oracle formula, speaker change, location shift, etc.) that justifies each scene's beginning and end
4. **Name literary devices precisely** - Use exact names (repetition, parallelism, inclusio, chiasm, irony, etc.), not vague descriptions
5. **Follow the JSON schema** exactly as specified in `CONVERSION_GUIDE.md` Part 1-2
6. **Test JSON validity** before submission
7. **Flag problematic scenes** using the validation checklist in `CONVERSION_GUIDE.md`

## References

- **Hebrew Literary Structure**: Leland Ryken, *How to Read the Bible as Literature*
- **Discourse Analysis**: Stephen Levinsohn, *Discourse Features of Biblical Hebrew*
- **Textual Boundaries**: Gordon Wenham, *Numbers* (Introduction on narrative structure)
- **Literary Devices**: Adele Berlin, *Poetics and Interpretation of Biblical Narrative*
- **Cognitive Science of Memorization**: Cognitive Psychology research on chunking and recall limits
- **Translation Comparison**: Bible Hub (for cross-translation boundary verification)

## Questions?

This framework is designed to be self-documenting through its JSON structure. Each file is human-readable and machine-parseable.

For questions about the specification, methodology, or contributing, consult `CONVERSION_GUIDE.md` first. For implementation questions, refer to the JSON schema documentation.

---

**The Memory Method Bible**: Transforming Scripture from sequential text into a text-driven, structurally justified, memorizable framework.