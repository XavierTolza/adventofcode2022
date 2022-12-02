import numpy as np


def compute_score(opponent, me):
    is_draw = opponent == me
    is_winning = (opponent + 1) % 3 == me

    shape_score = me + 1
    winning_score = is_draw * 3 + is_winning * 6

    score = shape_score + winning_score
    total_score = score.sum()
    return total_score


def main(data_str):
#     data_str = """A Y
# B X
# C Z"""
    # Convert data to numpy array of ints
    data = np.reshape(list(bytes(data_str.replace("\n", "").encode("utf-8"))), (-1, 3))[
        :, [0, -1]
    ]

    symbols = np.reshape(list(bytes("ABCXYZ".encode("utf-8"))), (2, -1))

    symbol_index = (
        np.arange(symbols.shape[1])[None, None, :]
        * (data[:, :, None] == symbols[None, :, :])
    ).sum(-1)

    # PART ONE
    score1 = compute_score(*symbol_index.T)

    # PART TWO
    correct_choice = np.array(
        [
            (symbol_index[:, 0] - 1) % 3,  # to loose
            symbol_index[:, 0],  # for a draw
            (symbol_index[:, 0] + 1) % 3,  # to win
        ]
    )[symbol_index[:, 1], np.arange(symbol_index.shape[0])]

    score2 = compute_score(symbol_index[:, 0], correct_choice)
    return score1, score2
