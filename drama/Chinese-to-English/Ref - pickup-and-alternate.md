# Masters, Pickups, and Alternate Versions

| Version | Responsibility | Default relationship |
|---|---|---|
| Master | All source requirements for the current shot | Current primary version |
| Pickup | Adds an action, reaction, composition, or effect | Coexists with the master; does not replace it |
| Alternate | A different implementation of the same requirement | May replace the master only after explicit comparison |

Narrowing a prompt's scope is often the correct repair. The danger is not that the prompt becomes shorter, but that a version covering only part of the shot silently becomes the master, leaving dialogue, reactions, reveals, or endpoints outside its scope with no responsible version.

## Account for Every Requirement in a Pickup

In `视频提示词.md`, give each pickup or alternate a stable `MOTION-...` ID and state clearly:

1. Which master it corresponds to.
2. Whether each source requirement is carried by this version, the master, another pickup, or must return to storyboarding.
3. The version's exact starting point, endpoint, and elements that must remain unchanged.
4. Whether it supplements the master or requests replacement.

For example, suppose the master requires “A slaps down the ledger page, B looks away, and C stands.” If the pickup films only a close-up of the hand, the pickup carries A's action, B's reaction remains in the master, and C's action must return to storyboarding if neither version includes it. Renaming a version cannot make an omission disappear.

A pickup does not replace the master by default. Later review determines replacement by considering all story obligations; a motion prompt cannot approve its own replacement.
