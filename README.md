# Simple Wave Function Collapse for island generation

## TODO
- remove holes in island
- backtracking
- parallelize the generation
- other overall shapes?

## Observation from looking at this [island](https://i.redd.it/uw9w6jiwjx231.png)

- lines of tiles don't end in corners
- when closing the shape towards the edge, go at a steep angle
- a tile can also be inverted, not just rotated/flipped
- turning is happening when going from one edge to an adjecent one

Holes in the island would be nonexistent if using a NxN pattern:
- downside is it requires an already built island
- upside is you could generate more than circular shapes