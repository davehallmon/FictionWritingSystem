# Location / View Design

## Division of Responsibility

- **Location** stores spatial identity: navigable geography, relationships between zones, entrances, fixed anchors, and primary materials.
- **View** stores a reusable viewing direction or production state: which zone it faces, which anchors are visible together, and the stage of set dressing, time of day, weather, and lighting state.

A Location is not a scene-title string, and a View is not every camera angle. The goal is to give reference images, storyboards, and adjacent shots the same spatial logic rather than creating a “new scene” for every shot.

## Build the Mental Floor Plan Before Writing Atmosphere

When reading the script, identify first:

1. Interior or exterior space and navigable boundaries.
2. The relative relationships between zones.
3. Entrances and exits used by people and props.
4. Immovable identifying anchors.
5. Primary materials, scale, and function.
6. Script-defined time, weather, and causally relevant light sources.

“Damp,” “oppressive,” and “nostalgic” may support atmosphere, but they cannot replace geographic facts such as “the north door opens to the corridor, the window faces the river, and the electrical box is behind the counter.” Do not add an attractive door that later changes a chase route.

## Location Boundaries

### New Location

Create a new Location when a space has distinct, independently producible geography, entrances, or fixed anchors. For example, if the waiting hall and duty office within one ferry terminal each contain complete actions and have an explicit connection, use two Locations and record `connected_to`.

### Same Location

A power outage, shift from day to night, change from clear weather to rain, or temporary set-dressing change does not alter spatial identity. Creating a new location merely because the camera turns causes contradictory door and window directions and actor movement.

**`reviewed_invariant` AST-04:** Do not split fixed geography and temporary time, weather, or lighting into two Location identities.

## View Boundaries

A View is worthwhile when downstream work repeatedly references a stable direction or state that explains the space:

- From the counter toward the north door, simultaneously showing the door, river window, and electrical box.
- The same direction after the outage, with the main light off and only cold light from the river window.
- An exterior during heavy rain, preserving the relationship among the station sign, steps, and riverbank while weather and ground state change.

A simple “low angle,” “close-up of the door handle,” or “35mm” belongs to a shot or keyframe, not a View. An actor standing on the left is not a location fact. **`craft_default` AST-03:** Create a View only when a group of shots can share a direction or state and needs a reference plate.

## Light, Weather, and Set Dressing Require Sources

- If the script specifies a power outage, the View may change from `normal_night` to `blackout`, with cause pointing to the outage block.
- A creator-selected blue-hour night is visual direction and may record a creator source.
- Do not add neon, fog, backlighting, or a moved window from prompting habit.
- Temporary posters, scattered documents, or standing water enter View state or delta when they affect story or continuity. Ordinary replaceable decoration may remain set dressing.

## Synthetic Example: Old Ferry-Terminal Duty Office

`LOC-FERRY-OFFICE`: A narrow interior; the north door opens to the waiting hall; a river-facing window is on the east; an old counter spans the west wall; the electrical box is fixed to the wall behind the counter. Location does not record “night,” “heavy rain,” or “Gu He stands in the doorway.”

- `VIEW-FERRY-OFFICE-NORTH-NIGHT`: Viewed from behind the counter toward the north door, with the river window at the rear right of frame; the ceiling light operates normally at night, and only a metal box sits on the counter.
- `VIEW-FERRY-OFFICE-NORTH-BLACKOUT`: The same geography and direction; after the outage, the ceiling light is off, cold light from the river window remains, and the metal box has not moved. This is a View/state variant, not a new “dark duty office” Location.

If the script needs only one close-up of a door handle, do not create `VIEW-FERRY-OFFICE-DOOR-CLOSEUP`. The shot can reference the Location or existing View and own its framing.

## Review Questions

- Without atmospheric adjectives, can you still determine entrances, fixed anchors, and relationships between zones?
- Can the directions of doors, windows, and light across Views of the same space be reconciled?
- Does a View incorrectly own camera focal length, actor position, or shot boundary?
- Do changes in time, weather, lighting state, and set dressing have a source, cause, and validity period?
- Is the decision to split adjacent spaces into Locations or Views based on geography and production reuse rather than naming habit?
- Has the creator explicitly selected an empty-space or character-present policy? A later image prompt implements that policy precisely.

The granularity of spatial decomposition may be a **`taste_option`**. Whether coarse or fine, entrance relationships and continuity must remain explainable; style choices cannot hide contradictions.
