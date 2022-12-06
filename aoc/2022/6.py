import numpy as np

from tools.decorators import string2numpy

demo_data = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
demo_result = 7, 19


@string2numpy(sep=None)
def detect_start_index(data, header_size: int = 4):
    start_index = np.arange(data.size - header_size)
    index = start_index[:, None] + np.arange(header_size)[None, :]
    packets = data[index]

    comp = packets[:, :, None] == packets[:, None, :]
    comp[:, np.arange(header_size), np.arange(header_size)] = False
    is_valid = ~comp.any((1, 2))
    res = np.nonzero(is_valid)[0][0] + header_size
    return res


def main(data_str):
    res1 = detect_start_index(data_str, header_size=4)
    res2 = detect_start_index(data_str, header_size=14)
    return res1, res2
