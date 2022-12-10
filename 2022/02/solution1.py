import enum
import sys
import time


class OpponentShape(enum.Enum):

    ROCK     = "A"
    PAPER    = "B"
    SCISSORS = "C"


class PlayerShape(enum.Enum):

    ROCK     = "X"
    PAPER    = "Y"
    SCISSORS = "Z"



SHAPE_SCORE = {
    PlayerShape.ROCK: 1,
    PlayerShape.PAPER: 2,
    PlayerShape.SCISSORS: 3,
}


LOSS_SCORE, DRAW_SCORE, WIN_SCORE = 0, 3, 6


# Yes, you could generate these. But why?
RESULT_SCORE = {
    (OpponentShape.ROCK, PlayerShape.ROCK):         DRAW_SCORE,
    (OpponentShape.PAPER, PlayerShape.PAPER):       DRAW_SCORE,
    (OpponentShape.SCISSORS, PlayerShape.SCISSORS): DRAW_SCORE,
    (OpponentShape.ROCK, PlayerShape.PAPER):        WIN_SCORE,
    (OpponentShape.ROCK, PlayerShape.SCISSORS):     LOSS_SCORE,
    (OpponentShape.PAPER, PlayerShape.SCISSORS):    WIN_SCORE,
    (OpponentShape.PAPER, PlayerShape.ROCK):        LOSS_SCORE,
    (OpponentShape.SCISSORS, PlayerShape.ROCK):     WIN_SCORE,
    (OpponentShape.SCISSORS, PlayerShape.PAPER):    LOSS_SCORE,
}


def main(shapes):
    total_score = 0
    for opponent_shape, player_shape in shapes:
        total_score += SHAPE_SCORE[player_shape] + RESULT_SCORE[(opponent_shape, player_shape)]

    return total_score


def reader(fh):
    for l in fh:
        o, p = l.strip().split(' ', 1)
        yield (OpponentShape(o), PlayerShape(p))


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)