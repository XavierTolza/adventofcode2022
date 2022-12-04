import numpy as np

demo_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

demo_result = (24000, 45000)


def main(data_str):
    data = np.fromstring(data_str.replace("\n\n", "\n-1\n"), dtype=np.int32, sep="\n")
    is_sep = data < 0
    elf_index = np.cumsum(is_sep)[~is_sep]
    data = data[~is_sep]

    selector = data[None, :] * (
        np.arange(elf_index.max() + 1)[:, None] == elf_index[None, :]
    )
    elf_total = selector.sum(1)
    res1 = elf_total.max()
    res2 = np.sort(elf_total)[-3:].sum()
    return res1, res2
