# Bible Book Analysis Spec Sheet
**Systematic Approach – Version 1.0**
(As finalized in development)

## Goal
Create a non-arbitrary, memorization-friendly, literary-sensitive hierarchical outline of any Bible book that serves two projects:

1. **Bible Memory Method** (deep-research tool / future app)
2. **Wolf and Words** (memorization app that will later pull simplified chunks from this system while keeping traditional chapters/verses)

## Core Principles (never break these)
1. Divisions must be justified by the text itself (flow, speaker change, resolution, literary device, chiasm hinge, inclusio, shift in topic/time/audience, etc.).
2. Nothing is arbitrary. Every cut gets a short, plain-English "why this starts/ends here + literary glue".
3. We are translation-agnostic. The scaffolding works with KJV, ESV, NIV, French Louis Segond, etc.
4. Traditional chapter-verse numbers are preserved in metadata (never hidden from the user, just not visually dominant in reading mode).

## Fixed Hierarchy (always this order)
```
Book
├─ Hebrew Name + English Name
├─ Canonical Grouping (Torah, Major Prophets, Writings, Gospel, Pauline, etc.)
├─ Big-Picture Literary Notes (overall chiasm, repeated refrains, non-chronological arrangement, etc.)
└─ Stories (self-contained arcs that advance the book's narrative)
   └─ Scenes (memorizable beats/pericopes, naturally determined by text)
      └─ Chunks (OPTIONAL rehearsal sublayer — see below; only where a scene is long)
```

**NOTE ON THEMES:** Themes are optional scaffolding that can be imposed later if desired. Stories and scenes are the core building blocks and take priority.

## Required Fields at Each Level

**Story level**
- Story letter (A, B, C, etc.)
- Story title (memorable & accurate)
- Why it starts here
- Why it ends here
- Literary glue / devices that hold it together (chiasm, parallelism, repetition, metaphor, inclusio, allusion, irony, hyperbole, wordplay, etc.)
- Traditional reference range

**Scene level**
- Scene number (1, 2, 3, etc.)
- Scene title (short, vivid when possible)
- Why it starts here
- Why it ends here (thought resolves, speaker changes, image completes, divine speech ends, etc.)
- Key literary devices at play in this exact scene
- Traditional verse range

**Chunk level (optional, `chunks` array on a scene)**
- Chunk number (1, 2, 3, … within its parent scene)
- Chunk title
- Traditional verse range

### Optional `chunks`: a rehearsal sublayer, never a replacement for scenes
Added 2026-08-14 by the Psalms Resegmentation Audit. Some books — Psalms above all —
have literary scenes that are longer than one sitting's rehearsal. A scene may
therefore carry an optional `chunks` array of smaller units.

The distinction is a hard rule, and it is the one the Psalms file originally got wrong:
- **Scenes follow poetic/literary form.** They may be any length. They may NOT be
  capped at a verse count.
- **Chunks are pedagogy.** They may be size-limited (≤6 verses) because they exist
  for rehearsal, not for structure.

Constraints:
- A scene that is already small enough carries no `chunks` at all.
- Chunks must tile their parent scene exactly — no gaps, no overlaps, nothing outside it.
- Consumers that predate this field may ignore it.

**The unit stays the scene.** A foothold is referenced as chapter + letter — Genesis 1A,
Genesis 50B, Psalm 19A — so the chapter is always the anchor and the letters run inside it.
`build_units.py` therefore emits one unit per *scene* and nests the chunks inside that unit;
it does not flatten chunks into units. Two consequences worth stating plainly:
- A psalm short enough to hold together is **one unit**: Psalm 23A, Psalm 117A, and
  Psalm 121A are each the whole poem, which is what the resegmentation was for.
- Psalm 19 is 19A / 19B / 19C — creation, Torah, prayer — not four pieces cut at a
  verse count.

Titles carry no book-and-chapter prefix. Every other book labels scenes bare ("Holy,
Holy, Holy"), the read-along header already shows the chapter, and the reference
already names it. Psalms was the lone exception and no longer is.

Validator: `tools/validate_psalms.py` (coverage, tiling, the ≤6 chunk ceiling, and
Psalm 119's 22 eight-verse stanzas).

### Critical: Scene Definition
A scene is **one complete, memorizable thought**. It is not a forced chunk of arbitrary length. The text itself determines where scenes naturally end:
- Thought completion
- Speaker change
- Resolution of a narrative arc
- Shift in time/place/action
- Natural pause in the text's flow

## Title Styles (for Bible Memory Method app)
User chooses one style globally per session:

1. **Plain** (neutral, modern, factual)
   → "Indictment of Judah"
2. **Evocative** (punchy, memorable, slightly dramatic)
   → "God Roars at His Rebellious Children"
3. **Archaic** (KJV-era poetic feel)
   → "The Lord's Controversy with His People"

Metadata explanations always stay Plain English (clarity > style when studying).

## Two Modes in the Final Product

**Reading / Orientation Mode**
Only titles are visible (Story → Scene) + text.
Acts as guardrails / mental map.
No verse numbers prominent.

**Study / Deep Mode** (toggle on)
All metadata appears:
- Why start/end
- Literary devices
- Traditional chapter-verse range
- Cross-references, allusions, wordplay notes
- Hebrew/Greek key terms when helpful

## Output Format (exact template we use for every book)

```
Book of [English Name] (Hebrew: [Name])
Grouping: [e.g., Torah]
Big-picture notes: [2–4 sentences max on overall structure/themes]

- Story A: [Title]
  → Why start/end + literary glue: [plain English]
  → Reference: [chapters:verses]
  - Scene 1: [Title]
    → Why start/end + devices: [plain English]
    → Reference: [verses]
  - Scene 2: [Title]
    → Why start/end + devices: [plain English]
    → Reference: [verses]
  - Scene 3: [Title]
    → Why start/end + devices: [plain English]
    → Reference: [verses]

- Story B: [Title]
  → Why start/end + literary glue: [plain English]
  → Reference: [chapters:verses]
  - Scene 1: [Title]
    → Why start/end + devices: [plain English]
    → Reference: [verses]
  - Scene 2: [Title]
    → Why start/end + devices: [plain English]
    → Reference: [verses]
```

## Workflow Going Forward
1. Pick the book.
2. Use AI prompt (see GENESIS-PROMPT.md for template) to generate stories and scenes.
3. Let the TEXT determine story and scene count—no arbitrary minimums or maximums.
4. Each scene must be a complete thought; don't force-fit into predetermined chunks.
5. Review/adjust if needed.
6. Approved version becomes the master scaffold for both apps.

## Key Commits & History
- **v1.0**: Initial spec finalized after Jeremiah V1 and new structure exploration
- Simplified from theme-heavy approach to story/scene-first methodology
- Focus on shipping over perfectionism
- Translation-agnostic, text-driven boundaries

---

**This spec is locked. Use it for all future Bible book outlines.**
