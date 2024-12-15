import operator
import sys
import time


def main(plan):
    # Walk and allocate area IDs as we go
    y_max = len(plan)
    x_max = len(plan[0])
    plant_positions = {}
    for y, row in enumerate(plan):
        for x, plant in enumerate(row):
            plant_positions.setdefault(plant, []).append((x, y))

    seen = set()
    coords_to_area_id = {}
    area_to_plant = {}
    area_coords = {}
    area_perimeters = {}
    next_area_id = 0
    for y, row in enumerate(plan):
        for x, plant in enumerate(row):
            if (x, y) in coords_to_area_id:
                continue

            area_id, area, perimeter = find_area(plant_positions, coords_to_area_id, seen, plant, x, y)
    
            if area_id is None:
                area_id = next_area_id
                next_area_id += 1
                area_coords[area_id] = area
                area_to_plant[area_id] = plant

            area_perimeters.setdefault(area_id, 0)
            area_perimeters[area_id] = perimeter
            for coords in area:
                coords_to_area_id[coords] = area_id

    total_cost = 0
    for area_id, area_points in area_coords.items():
        perimeter = area_perimeters[area_id]
        cost = perimeter * len(area_points)
        if len(area_coords) < 100:
            print(f'- A region of `{area_to_plant[area_id]}` plants with price `{len(area_points)} * {perimeter} = {cost}`')
        total_cost += cost

    return total_cost


def find_area(plant_positions, coords_to_area_id, seen, plant, x, y, area_id=None, area=None):
    if (x, y) in seen:
        return area_id, seen, 0
    if area is None:
        area = set()
    seen.add((x, y)) # don't go over the same area twice
    area.add((x, y))
    north_neighbour = (x, y - 1)
    west_neighbour = (x - 1, y)
    south_neighbour = (x, y + 1)
    east_neighbour = (x + 1, y)
    perimeter = 0
    for neighbour_x, neighbour_y in (north_neighbour, west_neighbour, south_neighbour, east_neighbour):
        if (neighbour_x, neighbour_y) not in plant_positions[plant]:
            perimeter += 1
            continue
        
        area_id = coords_to_area_id.get((neighbour_x, neighbour_y), area_id)

    if area_id is None:
        for neighbour_x, neighbour_y in (north_neighbour, west_neighbour, south_neighbour, east_neighbour):
            if (neighbour_x, neighbour_y) in plant_positions[plant] and (neighbour_x, neighbour_y) not in seen:
                area_id, area, sub_perimeter = find_area(plant_positions, coords_to_area_id, seen, plant, neighbour_x, neighbour_y, area_id, area)
                perimeter += sub_perimeter

    return area_id, area, perimeter


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