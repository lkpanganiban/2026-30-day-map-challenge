# Day 23 — Senses: Taste
**The taste of the city**

**Output:** `day23_taste/day23_taste.png`
**Run:** `uv run python -m day23_taste.map`

## The story

Taste is the most local sense. In Metro Manila, the everyday food map is not the
mall; it is the **palengke** (wet market), the panaderia, the butcher, the
greengrocer and the fishmonger. When floods close the roads, these are the last
mile of the food supply chain.

This map plots every food shop the crowd has mapped in Metro Manila, coloured by
type. Bakeries dominate by count — 1,255 of 2,746 — which is a very Filipino
result: the neighborhood bakery is more common than the supermarket. The 385 wet
markets are drawn as stars because they anchor the everyday table.

## Data

- **Food retail:** OSM nodes and ways in the Metro Manila box
  (120.85–121.20°E, 14.45–14.80°N) tagged
  `amenity=marketplace`, `shop=supermarket|greengrocer|butcher|seafood|bakery`.
  Fetched with `out center` and cached as `data/mm_food.gpkg`.
- **Counts:** 2,746 features: 1,255 bakeries, 840 supermarkets, 385 wet markets,
  150 butchers, 91 greengrocers, 28 fishmongers (269 fresh-food shops in total).
- **Land:** Natural Earth 1:10m (`data/ph_land.gpkg`).
- **Roads:** major OSM roads in the same box (`data/mm_roads.gpkg`), drawn as
  faint context.
- **Licence:** OSM data © OpenStreetMap contributors, ODbL.

## Process

1. Query Overpass for markets, supermarkets, greengrocers, butchers, fishmongers
   and bakeries; cache the JSON and convert to a GeoDataFrame.
2. Split the layer by tag: markets (`amenity=marketplace`), supermarkets
   (`shop=supermarket`), fresh-food shops (butcher, greengrocer, seafood) and
   bakeries.
3. Project to Web Mercator.
4. Draw land and major roads as dark context.
5. Plot bakeries as tiny sand-coloured dots, fresh-food shops as small olive
   dots, supermarkets as small blue dots, and wet markets as larger red stars
   with cream edges.
6. Set a fixed extent over Metro Manila so the surrounding province does not
   dilute the city pattern.
7. Add a legend with counts for each class, place it in the lower-left over the
   bay, and compose the title, the headline counts, and the food-supply line.

## Numbers on the map

- 2,746 food shops in total.
- 1,255 bakeries.
- 840 supermarkets.
- 385 wet markets.
- 269 butchers, greengrocers and fishmongers.
- The class counts add to slightly more than 2,746 because a handful of
  features carry overlapping tags (for example a market with a shop tag).

## Data links

External sources used for this map (the local caches live in `data/`):

- [OpenStreetMap copyright](https://www.openstreetmap.org/copyright)
- [Overpass API](https://overpass-api.de/)

## What this map does not say

- OSM retail coverage is incomplete and biased toward malls, chains and
  well-mapped neighborhoods. Informal stalls, sari-sari stores and talipapa are
  largely absent.
- A point is a location, not a measure of supply, price, quality or opening
  hours.
- The map does not show population or demand, so it cannot identify food
  deserts. A dense cluster of bakeries may serve a small area; a sparse area may
  be underserved or simply under-mapped.
- The claim that wet markets are "the last mile" is a narrative frame, not a
  measured supply-chain fact.
- The map is not an evacuation or disruption analysis; it does not model which
  shops remain open after a flood.
