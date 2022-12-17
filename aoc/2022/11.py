from math import prod

demo_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

demo_result = 10605, 2713310158


def parse(data):
    monkeys = []
    for bag in data.split("\n\n"):
        items, op, test, iftrue, iffalse = [
            i.split(":")[1] for i in bag.split("\n")[1:]
        ]
        modulo = int(test.split("by ")[1])
        monkeys.append(
            dict(
                items=[int(i) for i in items.split(",")],
                operation=op.split("=")[1],
                modulo=modulo,
                dst=[int(i.split("monkey ")[1]) for i in (iftrue, iffalse)],
            )
        )
    return monkeys


def run(data, n_rounds=20, division=3):
    monkeys = parse(data)
    bigmodulo = prod([i["modulo"] for i in monkeys])

    inspect_count = [0 for _ in monkeys]
    for round in range(1, n_rounds + 1):
        for monkey_index, monkey in enumerate(monkeys):
            item_index = 0
            while monkey["items"]:
                item_index += 1
                inspect_count[monkey_index] += 1
                old = int(monkey["items"].pop(0))
                item = (eval(monkey["operation"]) // division) % bigmodulo

                modulo = monkey["modulo"]
                mod_result = item % modulo
                test = mod_result == 0
                dst = monkey["dst"][1 - test]
                monkeys[dst]["items"].append(item)
        # print(round, [i["items"] for i in monkeys])
        if (round % 1000) == 0 or round in [1, 20]:
            print(round, inspect_count)

    return prod(sorted(inspect_count)[-2:]), inspect_count


def main(data):
    res1, inspect_count1 = run(data, 20, 3)
    print("-------------")
    res2, inspect_count2 = run(data, 10_000, 1)
    return res1, res2
