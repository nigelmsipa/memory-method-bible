
## Narrative-arc pre-roll / "you are here" orientation (2026-06-24)

The base-structure `stories[]` ARE the book's grand narrative arcs (e.g. Joshua:
Conquest 1-12, Division 13-21, Farewell 22-24). They already carry a title +
chapter range — we just don't surface them in the video yet.

Idea (presentation layer, not new data): before a chapter plays, show a short
**orientation card** that maps the whole book into its 2-4 grand arcs and marks
"you are here" (e.g. "THE CONQUEST · chapters 1-12"). Then during playback the
overlay Story (top) + Scene (bottom) continue as now, with the arc list visible
on the side. One cohesive system: arc → story → scene, using every layer we built.

- Source for the arc map = the base-structure story_letter / story_title /
  reference (already exists for every finished book).
- Where it shows: thumbnail-adjacent pre-roll / intro card; optional persistent
  side rail. "Fine that it only shows up" briefly at the start.
- Build this in the video renderer (make_youtube.py / snail player), NOT in the
  pericope data — the data is already there.
