# Simple Wave Function Collapse for island generation

## TODO
- parallelize the generation

## Observation from looking at this [island](https://i.redd.it/uw9w6jiwjx231.png)

- lines of tiles don't end in corners
- when closing the shape towards the edge, go at a steep angle
- a tile can also be inverted, not just rotated/flipped
- turning is happening when going from one edge to an adjecent one

Holes in the island would be nonexistent if using a NxN pattern:
- downside is it requires an already built island
- upside is you could generate more than circular shapes

## Backtracking
- using a stack
- when a random choice needs to be made, save all other tile options to the stack
- when a dead end is reached, pop the stack and try the next option
- an item in the stack contains: the grid, the tile to be collapsed, the possible tiles for that Option

## Parallelization
- the backtracking stack is populated only after the workers have made their choices
- workers are split into 2 stages: tile selection and tile collapsing
- a minimum distance between tiles chosen by different workers is enforced
- backtracking still works because workers can't go into unrecoverable states thanks to the distance constrain
- optional: worker can be killed when choosing a tile that's too close indicating the size of not collapsed tiles is low

## Other possible tiles
- tiles with 3 corners (Y shape) + 2 corners same side to connect these