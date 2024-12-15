import operator
import sys
import time


def main(plan):
    # Walk and allocate area IDs as we go
    plant_positions = {}
    for y, row in enumerate(plan):
        for x, plant in enumerate(row):
            plant_positions.setdefault(plant, []).append((x, y))

    seen = set()
    coords_to_area_id = {}
    area_to_plant = {}
    area_coords = {}
    area_sides = {}
    next_area_id = 0
    for y, row in enumerate(plan):
        for x, plant in enumerate(row):
            if (x, y) in coords_to_area_id:
                continue

            area_id, area = find_area(plant_positions, coords_to_area_id, seen, plant, x, y)
    
            if area_id is None:
                area_id = next_area_id
                next_area_id += 1
                area_coords[area_id] = area
                area_to_plant[area_id] = plant

            for coords in area:
                coords_to_area_id[coords] = area_id

            #sides = find_sides(area, x, y)
            sides = find_sides_2(area)

            area_sides.setdefault(area_id, 0)
            area_sides[area_id] = sides

    total_cost = 0
    for area_id, area_points in area_coords.items():
        sides = area_sides[area_id]
        cost = sides * len(area_points)
        if len(area_coords) < 100:
            print(f'- A region of `{area_to_plant[area_id]}` plants with price `{len(area_points)} * {sides} = {cost}`')
        total_cost += cost

    return total_cost


def find_area(plant_positions, coords_to_area_id, seen, plant, x, y, area_id=None, area=None):
    if (x, y) in seen:
        return area_id, area
    if area is None:
        area = set()
    seen.add((x, y)) # don't go over the same area twice
    area.add((x, y))
    north_neighbour = (x, y - 1)
    west_neighbour = (x - 1, y)
    south_neighbour = (x, y + 1)
    east_neighbour = (x + 1, y)
    for neighbour_x, neighbour_y in (north_neighbour, west_neighbour, south_neighbour, east_neighbour):
        if (neighbour_x, neighbour_y) not in plant_positions[plant]:
            continue
        
        area_id = coords_to_area_id.get((neighbour_x, neighbour_y), area_id)

    if area_id is None:
        for neighbour_x, neighbour_y in (north_neighbour, west_neighbour, south_neighbour, east_neighbour):
            if (neighbour_x, neighbour_y) in plant_positions[plant] and (neighbour_x, neighbour_y) not in seen:
                area_id, area = find_area(plant_positions, coords_to_area_id, seen, plant, neighbour_x, neighbour_y, area_id, area)

    return area_id, area


DIRECTIONS = (
    (0, 1, 'SOUTH'),
    (1, 0, 'EAST'),
    (0, -1, 'NORTH'),
    (-1, 0, 'WEST'),
)


def find_sides_2(area):
    # define edges as sides of cells
    edge_points = []
    for x, y in area:
        for direction in DIRECTIONS:
            try_x, try_y = (x + direction[0]), (y + direction[1])
            if (try_x, try_y) not in area:
                edge_points.append((x, y, DIRECTIONS.index(direction)))

    edge_points.sort()
    # find contiguous edges and count them
    edges = {}
    next_edge_id = 0
    edge_point_to_edge = {}
    for edge_point in edge_points:
        if edge_point in edge_point_to_edge:
            # already allocated an edge ID
            continue
        edge_id = next_edge_id
        next_edge_id += 1
        edges[edge_id] = set([edge_point])
        # check em to the "right"
        right_direction = DIRECTIONS[(edge_point[2] + 1) % 4]
        next_x, next_y = edge_point[0] + right_direction[0], edge_point[1] + right_direction[1]
        right_edge = (next_x, next_y, edge_point[2])
        # merge edges if we've bumped into another one
        if right_edge in edge_point_to_edge:
            old_edge_id = edge_point_to_edge[right_edge]
            edges[edge_id] |= edges[old_edge_id]
            del edges[old_edge_id]
        if right_edge in edge_points:
            edges[edge_id].add((next_x, next_y, edge_point[2]))
            edge_point_to_edge[edge_point] = edge_id
        # check em to the "left"
        left_direction = DIRECTIONS[(edge_point[2] + 3) % 4]
        next_x, next_y = edge_point[0] + left_direction[0], edge_point[1] + left_direction[1]
        left_edge = (next_x, next_y, edge_point[2])
        # merge edges if we've bumped into another one
        if left_edge in edge_point_to_edge:
            old_edge_id = edge_point_to_edge[left_edge]
            edges[edge_id] |= edges[old_edge_id]
            del edges[old_edge_id]
        if left_edge in edge_points:
            edges[edge_id].add((next_x, next_y, edge_point[2]))
            edge_point_to_edge[edge_point] = edge_id

    return len(edges)


def has_left_edge(area, direction, x, y):
    left_direction = (direction + 1) % 4
    left_coords = (x + DIRECTIONS[left_direction][0], y + DIRECTIONS[left_direction][1])
    return left_coords not in area


def find_sides(area, x, y, direction=1, start=None):
    # This works fine for isolated areas, but doesn't account for enclaves
    # Walk the perimeter of an area keeping the edge on your left, counting the changes in direction
    if start is None:
        start = (x, y, direction)
    turns = 0

    next_x, next_y = x + DIRECTIONS[direction][0], y + DIRECTIONS[direction][1]
    next_direction = direction
    if (next_x, next_y) not in area:
        for next_direction in ((direction + 1) % 4, (direction + 3) % 4):
            # turn right
            next_x, next_y = x + DIRECTIONS[next_direction][0], y + DIRECTIONS[next_direction][1]
            if (next_x, next_y) in area:
                break
            if (x, y, next_direction) == start:
                return turns + 1
    else:
        # try to proactively turn left
        left_direction = (direction + 1) % 4
        left_x, left_y = next_x + DIRECTIONS[next_direction][0], next_y + DIRECTIONS[next_direction][1]
        if (left_x, left_y) in area and has_left_edge(area, left_direction, left_x, left_y):
            next_x, next_y, next_direction = left_x, left_y, left_direction

    if (next_x, next_y) not in area:
        # no choice but to 180
        next_direction = (direction + 2) % 4
        turns = 2
    else:
        turns = 1

    if direction != next_direction:
        next_x, next_y = x, y
    else:
        turns = 0

    if (next_x, next_y, next_direction) == start:
        return turns

    turns += find_sides(area, next_x, next_y, next_direction, start)
    return turns


def reader(fh):
    plan = []
    for row in fh:
        plan.append(row.strip())
    
    return plan
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        plan = reader(fh)
        start = time.monotonic_ns()
        result = main(plan)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)