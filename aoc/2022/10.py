demo_data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

demo_result = 13140

import numpy as np


def process_data(data_str):
    data_str = data_str.replace("noop", "1, 0").replace("addx", "2,").replace("\n", ",")
    data = np.fromstring(data_str, dtype=np.int32, sep=",").reshape((-1, 2))

    res = np.cumsum(data, axis=0)
    res[:, 1] += 1
    res[:, 0] += 1
    res = np.concatenate([[[1, 1]], res], axis=0)

    cycle = np.arange(res[:, 0].max()) + 1
    selector = np.cumsum(cycle[:, None] < res[None, :, 0], axis=1) == 1
    indexes = (
        np.broadcast_to(np.arange(res.shape[0])[None, :], selector.shape)[selector] - 1
    )
    indexes = np.concatenate([indexes, [-1]])
    return np.transpose([cycle, res[indexes, 1]])


def main(data_str):
    data = process_data(data_str)

    cycles_to_fetch = np.array([20, 60, 100, 140, 180, 220])
    values = data[cycles_to_fetch - 1, 1]
    res1 = (values * cycles_to_fetch).sum()

    screen = np.zeros((6, 40), dtype=np.bool)
    cycle, X = data.T
    crt_pos = data[:, 0] - 1
    sprite_pos = X[:, None] + np.arange(3) - 1

    draws = ((crt_pos[:, None] % 40) == sprite_pos).any(1)
    screen.ravel()[: draws.size] = draws[: screen.size]

    screen_txt = np.zeros_like(screen, dtype=np.uint8) + 32
    screen_txt[screen] += 3
    print("\n".join([i.tobytes().decode("utf-8") for i in screen_txt]))
    return res1
