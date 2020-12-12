import collections
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


Location = collections.namedtuple('Location', ['x', 'y'])


class Ship:

    def __init__(self, x, y, bearing):
        self.x = x
        self.y = y
        self.bearing = bearing

    def obey(self, operator, operand):
        if operator == Operator.TURN_LEFT:
            self.bearing = (self.bearing - operand) % 360
        elif operator == Operator.TURN_RIGHT:
            self.bearing = (self.bearing + operand) % 360
        elif operator == Operator.MOVE_FORWARD:
            r = math.radians(self.bearing)
            self.x += round(math.sin(r) * operand)
            self.y += round(math.cos(r) * operand)
        elif operator == Operator.MOVE_NORTH:
            self.y += operand
        elif operator == Operator.MOVE_SOUTH:
            self.y -= operand
        elif operator == Operator.MOVE_EAST:
            self.x += operand
        elif operator == Operator.MOVE_WEST:
            self.x -= operand

    def manhatten_distance(self):
        return abs(self.x) + abs(self.y)

    def __str__(self):
        return repr((self.x, self.y, self.bearing))


def main(instructions):
    ship = Ship(0, 0, 90)
    for operator, operand in instructions:
        ship.obey(operator, operand)
    
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