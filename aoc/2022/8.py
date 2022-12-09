import numpy as np

from tools.decorators import string2numpy

demo_data = """30373
25512
65332
33549
35390"""

demo_result = 21, 8


@string2numpy()
def main(data, bag_index):
    shape = n_rows, n_cols = bag_index.max() + 1, np.nonzero(bag_index)[0][0]
    assert n_cols == n_rows

    ri, ci = np.arange(n_rows), np.arange(n_cols)
    data = data.reshape(shape) - ord("0")

    indexes = np.array(np.meshgrid(ri, ci, indexing="ij"))

    rowscol = np.reshape(
        [
            data.repeat(n_rows, axis=0),
            np.tile(data.T, (n_cols, 1)),
        ],
        (2, n_rows, n_cols, -1),
    )
    diff = np.flip(
        np.array([ri, ci])[:, None, None, :] - indexes[:, :, :, None], axis=0
    )

    is_blocking = np.logical_and(
        data[None, :, :, None] <= rowscol,
        (indexes[::-1, :, :, None] != ri[None, None, None, :]),
    )
    is_blocking_sides = np.array([is_blocking * (diff < 0), is_blocking * (diff > 0)])
    n_blocking_sides = is_blocking_sides.sum(-1)

    is_visible = (n_blocking_sides == 0).any((0, 1))
    res1 = is_visible.sum()

    # Part 2
    los = (
        np.array(
            [
                (
                    np.cumsum(is_blocking_sides[0, :, :, :, ::-1], axis=-1)[
                        :, :, :, ::-1
                    ]
                    + (diff >= 0)
                ),
                np.cumsum(
                    is_blocking_sides[
                        1,
                    ],
                    axis=-1,
                )
                + (diff <= 0),
            ]
        )
        == 0
    )
    n_views = los.sum(-1)
    n_view_max = np.array([indexes, n_rows - indexes - 1])[:, ::-1]
    is_viewing_max = n_views == n_view_max
    n_views[~is_viewing_max] += 1
    scenic_score = np.product(n_views, axis=(0, 1))
    res2 = scenic_score.max()

    return res1, res2
