from base64 import b64decode

import numpy as np

demo_data = b64decode(
    b"ICAgIFtEXSAgICAKW05dIFtDXSAgICAKW1pdIFtNXSBbUF0KIDEgICAyICAgMyAKCm1vdmUgMSBmcm9tIDIgdG8gMQptb3ZlIDMgZnJvbSAxIHRvIDMKbW92ZSAyIGZyb20gMiB0byAxCm1vdmUgMSBmcm9tIDEgdG8gMg=="
).decode("utf-8")

demo_result = "CMZ", "MCD"


def recursive_perform(schema, movements, new_mover: bool = False):
    if len(movements) == 1 or not isinstance(movements, np.ndarray):
        N, _from, _to = np.ravel(movements)
        if not new_mover or N == 1:
            if N > 1:
                res = recursive_perform(schema, (N - 1, _from, _to))
            remove_index = np.where(schema[:, _from] != -1)[0][0]
            dst_index = np.where(schema[:, _to] == -1)[0][-1]
            schema[dst_index, _to] = schema[remove_index, _from]
            schema[remove_index, _from] = -1
            res = schema
        else:
            remove_index = np.arange(N) + np.where(schema[:, _from] != -1)[0][0]
            dst_index = np.arange(N) - N + 1 + np.where(schema[:, _to] == -1)[0][-1]
            schema[dst_index, _to] = schema[remove_index, _from]
            schema[remove_index, _from] = -1
            res = schema
    else:
        m1, m2 = np.split(movements, [movements.shape[0] // 2], 0)
        schema = recursive_perform(schema, m1, new_mover=new_mover)
        schema = recursive_perform(schema, m2, new_mover=new_mover)
        res = schema
    return res


def main(data_str):
    schema_str, movements_str = data_str.split("\n\n")

    schema = np.frombuffer(schema_str.replace("\n", "").encode("utf-8"), dtype=np.uint8)
    n_stacks = int(np.round(schema_str.find("\n") / 4))
    schema = schema.reshape((-1, n_stacks * 4 - 1))
    schema = schema[:-1, (np.arange(schema.shape[1]) % 4) == 1]
    schema -= ord("A")
    schema = schema.astype(np.int32)
    schema[schema == 223] = -1

    # allocate som extra space for schema
    maxsize = (schema != -1).sum() + 2
    schema = np.concatenate(
        [-np.ones((maxsize - schema.shape[0], n_stacks), dtype=schema.dtype), schema],
        axis=0,
    )

    movements = np.fromstring(
        movements_str.replace("move ", "")
        .replace(" from ", ",")
        .replace(" to ", ",")
        .replace("\n", ",")
        .encode("utf-8"),
        sep=",",
        dtype=np.int,
    ).reshape((-1, 3))

    # indexing from 0 in python
    movements[:, 1:] -= 1

    new_schema = recursive_perform(schema.copy(), movements)

    stack_top = new_schema[np.argmax(new_schema > 0, axis=0), np.arange(n_stacks)]
    res1 = (stack_top + ord("A")).astype(np.uint8).tobytes().decode("utf-8")

    new_schema = recursive_perform(schema.copy(), movements, new_mover=True)

    stack_top = new_schema[np.argmax(new_schema > 0, axis=0), np.arange(n_stacks)]
    res2 = (stack_top + ord("A")).astype(np.uint8).tobytes().decode("utf-8")

    return res1, res2
