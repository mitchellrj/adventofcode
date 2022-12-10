import enum
import sys
import time


class Shape(enum.Enum):

    ROCK     = "A"
    PAPER    = "B"
    SCISSORS = "C"


class Result(enum.Enum):

    LOSS = "X"
    DRAW = "Y"
    WIN  = "Z"



SHAPE_SCORE = {
    Shape.ROCK: 1,
    Shape.PAPER: 2,
    Shape.SCISSORS: 3,
}


RESULT_SCORE = {
    Result.LOSS: 0,
    Result.DRAW: 3,
    Result.WIN:  6,
}


# Yes, you could generate these. But why?
PLAYER_SHAPE = {
    (Shape.ROCK, Result.DRAW):         Shape.ROCK,
    (Shape.PAPER, Result.DRAW):        Shape.PAPER,
    (Shape.SCISSORS, Result.DRAW):     Shape.SCISSORS,
    (Shape.ROCK, Result.WIN):          Shape.PAPER,
    (Shape.ROCK, Result.LOSS):         Shape.SCISSORS,
    (Shape.PAPER, Result.WIN):         Shape.SCISSORS,
    (Shape.PAPER, Result.LOSS):        Shape.ROCK,
    (Shape.SCISSORS, Result.WIN):      Shape.ROCK,
    (Shape.SCISSORS, Result.LOSS):     Shape.PAPER,
}


def main(rounds):
    total_score = 0
    for opponent_shape, result_required in rounds:
        player_shape = PLAYER_SHAPE[(opponent_shape, result_required)]
        total_score += SHAPE_SCORE[player_shape] + RESULT_SCORE[result_required]

    return total_score


def reader(fh):
    for l in fh:
        o, p = l.strip().split(' ', 1)
        yield (Shape(o), Result(p))


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)