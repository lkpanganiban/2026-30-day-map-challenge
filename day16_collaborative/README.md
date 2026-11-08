# Day 16 — Collaborative map
**The crowd maps the storm**

**Output:** `day16_collaborative/day16_collaborative.png`
**Run:** `uv run python -m day16_collaborative.map`

## The story

The brief for Day 16 asks for a map made with another person. This map is made
with thousands of them. OpenStreetMap is a collaborative artefact: every road,
building and evacuation route is someone's edit. When Typhoon Tino crossed Cebu
and Negros on 4 November 2026, mappers kept editing through the week — adding
buildings, correcting roads, fixing names.

The map shows the **changesets** (edit sessions) in the Cebu–Negros box returned
by the OSM API, coloured by mapper. Thirty changesets dated after Tino's
landfall are highlighted; seventy earlier ones are left as faint context. It is
a portrait of a community doing maintenance in the middle of a disaster.

## Data

- **Changesets:** OpenStreetMap changeset API,
  `GET /api/0.6/changesets?bbox=123.3,9.6,124.6,11.4`, requested without
  authentication. The API returns the 100 most recent changesets; they span
  23 October to 8 November 2026.
- **Attributes:** changeset id, user, `created_at`, and bounding box
  (`min_lat`, `min_lon`, `max_lat`, `max_lon`). Cached as
  `data/cebu_changesets.xml`.
- **Roads:** OSM trunk/primary/secondary/tertiary ways in the same box
  (`data/cebu_roads.gpkg`), used as context.
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Request the changeset feed for the Cebu–Negros bounding box and cache the
   XML.
2. Parse each `<changeset>` element with `xml.etree.ElementTree`, keeping user,
   timestamp and bounding box.
3. Convert each bounding box to a Shapely polygon and build a GeoDataFrame in
   EPSG:4326, then project to Web Mercator.
4. Split the data into "after Tino" (created on or after 4 November) and
   "before Tino".
5. Draw land and roads in dark tones. Draw pre-Tino changesets as very faint
   grey rectangles so the week's activity has context without competing.
6. Draw post-Tino changesets as translucent rectangles with thin edges, and a
   point at each centroid, coloured by mapper. The five most active mappers get
   fixed colours; everyone else is slate.
7. Draw a dashed red 120 km circle around the Tino crossing area.
8. Label Cebu City, Toledo, Tagbilaran and Dumaguete for orientation.
9. Add a mapper legend with counts and a note about the API's 100-changeset
   limit.

## Numbers on the map

- 100 changesets returned by the API, 23 October–8 November 2026.
- 30 changesets after 4 November 2026.
- 15 distinct mappers in the post-Tino set.
- Most active: Totor (6), junyeah (4), imiraldz (4), DodaBettaMountain (3),
  RusumoFalls (2).

## Data links

External sources used for this map (the local caches live in `data/`):

- [OSM API v0.6 changesets](https://wiki.openstreetmap.org/wiki/API_v0.6#Changesets_2)
- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)

## What this map does not say

- The API returns at most 100 changesets, so this is a sample of the most recent
  activity, not a complete count of edits since Tino. A busier week would push
  older changesets out of the response.
- A changeset is an edit session, not a feature. One changeset can touch a
  single node or thousands of objects; the rectangles show where the session's
  bounding box lies, not the amount or quality of work.
- Mapper colours are assigned to the top five only; "others" is a aggregate.
- The map does not measure whether edits were repairs, imports, armchair
  mapping or unrelated maintenance.
- Bounding boxes overlap heavily in Cebu City, so the visual density is not a
  count of features.
