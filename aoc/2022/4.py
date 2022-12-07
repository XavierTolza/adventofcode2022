import numpy as np

demo_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

demo_result = 2, 4


def main(data_str):
    data = np.fromstring(
        data_str.replace("-", ",").replace("\n", ",").encode("utf-8"),
        sep=",",
        dtype=np.uint16,
    ).reshape((-1, 2, 2))

    start, stop = data.T
    a_includes_b = (start[0] <= start[1]) * (stop[0] >= stop[1])
    b_includes_a = (start[1] <= start[0]) * (stop[1] >= stop[0])

    inclusion = np.logical_or(a_includes_b, b_includes_a)
    res1 = inclusion.sum()

    # Part two
    overlap = (
        ((start[0] <= start[1]) * (start[1] <= stop[0]))
        + ((start[0] <= stop[1]) * (stop[1] <= stop[0]))
        + ((start[1] <= start[0]) * (start[0] <= stop[1]))
        + ((start[1] <= stop[0]) * (stop[0] <= stop[1]))
    )
    res2 = overlap.sum()
    return res1, res2
