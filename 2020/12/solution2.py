import enum
import math
import sys
import time


class Operator(enum.Enum):

    MOVE_NORTH = 'N'
    MOVE_SOUTH = 'S'
    MOVE_EAST = 'E'
    MOVE_WEST = 'W'
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'
    MOVE_FORWARD = 'F'


class Positionable:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_east(self, operand):
        self.move(operand, 0)

    def move_west(self, operand):
        self.move(-operand, 0)

    def move_north(self, operand):
        self.move(0, operand)

    def move_south(self, operand):
        self.move(0, -operand)

    def bearing_from(self, other):
        return math.degrees(math.atan2(self.x - other.x, self.y - other.y))

    def _rotate_around(self, other, amount):
        r = math.radians(amount)
        s = math.sin(r)
        c = math.cos(r)
        x_r = self.x - other.x
        y_r = self.y - other.y
        new_x = round(
                c * x_r
                - s * y_r
            ) + other.x
        new_y = round(
                s * x_r
                + c * y_r
            ) + other.y
        d_x = new_x - self.x
        d_y = new_y - self.y
        self.move(d_x, d_y)

    def rotate_clockwise_around(self, other, amount):
        self._rotate_around(other, -amount)

    def rotate_counter_clockwise_around(self, other, amount):
        self._rotate_around(other, amount)

    def move_to(self, other, times):
        self.move(
            (other.x - self.x) * times,
            (other.y - self.y) * times,
        )

    def manhatten_distance(self):
        return abs(self.x) + abs(self.y)

    def __str__(self):
        return repr((self.x, self.y))


class Ship(Positionable):

    def __init__(self, x, y, waypoint):
        super().__init__(x, y)
        self.waypoint = waypoint

    def move(self, x, y):
        super().move(x, y)
        self.waypoint.move(x, y)


def main(instructions):
    waypoint = Positionable(10, 1)
    ship = Ship(0, 0, waypoint)
    
    for operator, operand in instructions:
        if operator == Operator.MOVE_EAST:
            waypoint.move_east(operand)
        elif operator == Operator.MOVE_WEST:
            waypoint.move_west(operand)
        elif operator == Operator.MOVE_NORTH:
            waypoint.move_north(operand)
        elif operator == Operator.MOVE_SOUTH:
            waypoint.move_south(operand)
        elif operator == Operator.TURN_LEFT:
            waypoint.rotate_counter_clockwise_around(ship, operand)
        elif operator == Operator.TURN_RIGHT:
            waypoint.rotate_clockwise_around(ship, operand)
        elif operator == Operator.MOVE_FORWARD:
            ship.move_to(waypoint, operand)
    
    return ship.manhatten_distance()


def reader(fh):
    for l in fh:
        yield Operator(l[0]), int(l[1:])


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)