import numpy as np
from tools.decorators import *

demo_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

demo_result = 157, 70


@string2numpy()
def main(data, bag_index, item_bag_index, n_elements_by_bag, **kwargs):
    data = data.astype(np.int32)
    data[data >= ord("a")] -= ord("a") - 1
    data[data >= ord("A")] -= ord("A") - 27
    n_elements_in_bag = n_elements_by_bag[bag_index]
    in_first_half = item_bag_index < (n_elements_in_bag / 2)

    fhalf = np.array([data, bag_index])[:, in_first_half]
    shalf = np.array([data, bag_index])[:, ~in_first_half]

    comp = (fhalf[:, :, None] == shalf[:, None, :]).all(0)
    indexes = np.unravel_index(np.arange(comp.size)[comp.ravel()], comp.shape)

    res1 = np.unique(fhalf[:, indexes[0]].T, axis=0)[:, 0].sum()

    # PART 2
    group_id = np.floor(bag_index / 3)
    n_groups = group_id.max() + 1
    n_bags = bag_index.max() + 1
    n_symbols = data.max() + 1

    n_times_an_item_is_in_a_bag = (
        (data[None, None, :] == np.arange(n_symbols)[:, None, None])
        * (bag_index[None, None, :] == np.arange(n_bags)[None, :, None])
    ).sum(-1)
    item_is_in_a_bag = n_times_an_item_is_in_a_bag > 0
    items_is_in_group = item_is_in_a_bag.reshape((n_symbols, -1, 3)).all(-1)
    assert (items_is_in_group.sum(0) == 1).all()

    res2 = (
        np.arange(n_symbols)[:, None]
        .repeat(n_bags // 3, axis=1)[items_is_in_group]
        .sum()
    )

    return res1, res2
