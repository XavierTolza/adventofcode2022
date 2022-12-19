import numpy as np

demo_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
demo_result = 13


def compare(a, b):
    ta, tb = type(a), type(b)

    if ta == tb:
        if ta == list:
            for i, j in zip(a, b):
                res = compare(i, j)
                if res is not None:
                    return res
            else:
                if len(a) < len(b):
                    return True
                if len(a) > len(b):
                    return False
                return None
        elif ta == int:
            if a < b:
                return True
            elif a > b:
                return False
            else:
                return None
        else:
            raise NotImplementedError
    elif ta == int:
        return compare([a], b)
    elif tb == int:
        return compare(a, [b])
    else:
        raise NotImplementedError


def main(data_str):
    data = eval(data_str.replace("\n\n", ",").replace("\n", ","))
    compare(data[0 + 4 * 2], data[0 + 4 * 2 + 1])
    res = [compare(data[i], data[i + 1]) for i in range(0, len(data), 2)]
    res1 = (np.arange(len(res))+1)[np.array(res)].sum()
    raise NotImplementedError
