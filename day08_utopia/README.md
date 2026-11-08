# Day 08 — Utopia
**A Metro Manila that does not flood**

**Output:** `day08_utopia/day08_utopia.png`
**Run:** `uv run python -m day08_utopia.map`

## The story

The map was made on 8 November 2026, the thirteenth anniversary of Super Typhoon
Yolanda (Haiyan), in the same week that Typhoon Tino cut through Cebu and
Negros. In the Philippines, the gap between the flood-control system that exists
and the one that was promised is no longer an abstraction; it is a political
crisis with a body count.

"Utopia" is a map of something that could be. Every river, creek, canal and
drain that OpenStreetMap knows in Metro Manila is drawn as a single luminous
network — the spine of a city that treats water as infrastructure instead of an
emergency. The map is not a proposal with a budget or an alignment. It is a
visual argument: the city already has a water network. The utopia is deciding to
build it properly.

## Data

- **Waterways:** OSM `waterway=*` features (river, stream, canal, drain, ditch)
  inside the Metro Manila box (120.90–121.10°E, 14.55–14.78°N), fetched once
  from Overpass and cached as `data/mm_waterways.gpkg`.
- **Context:** no roads are drawn. An early attempt to add the major-road layer
  failed because the Overpass mirrors were at capacity; the water-only
  composition turned out stronger, so it stayed.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Query the Overpass API for every waterway in the Metro Manila bounding box.
2. Keep only river, stream, canal, drain and ditch; drop pipelines and
   intermittent features that would add noise.
3. Cache the result as a GeoPackage and project it to UTM 51N.
4. Draw the network in two passes per waterway class: a wide, very transparent
   stroke for glow, then a narrow bright stroke. Line width depends on class
   (rivers 3.2 pt, streams 1.1 pt, canals 1.6 pt, drains and ditches under 1 pt).
5. Place city labels at known centroids (Manila, Quezon City, Caloocan, Pasig,
   Marikina, Taguig, Pasay, Makati) with dark halos, plus two italic river
   labels.
6. Compose on near-black paper with a single blue accent, a red theme label, a
   bold headline and a three-line subtitle placing the map on Yolanda's
   anniversary and in the week of Tino.
7. Save at 200 dpi.

## Numbers on the map

- Eight city labels.
- The network is drawn from every mapped waterway class, not a selected
  "major" subset.
- No count is printed because the raw feature count includes thousands of short
  drains and would imply a precision the map does not need.

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)

## What this map does not say

- This is not a flood-control plan. There are no dikes, pumping stations,
  retention basins, costs or alignments.
- OSM waterway coverage is uneven; some drains are mapped in detail, others not
  at all. The luminous network is a map of what is known, not of what exists.
- The map deliberately omits roads and buildings, so it cannot show who lives
  next to the water or which communities flooded.
- "Utopia" is a rhetorical frame. The map does not claim that a single network
  would prevent flooding in a city exposed to monsoon rain, typhoons, sea-level
  rise and subsidence.
