import numpy as np


def flatten_and_remove_duplicates(iterables_list):
    result = []
    unique_elements = set()
    for iterable in iterables_list:
        if hasattr(iterable, '__iter__') and not isinstance(iterable, (str, bytes)):
            for element in iterable:
                if element not in unique_elements:
                    result.append(element)
                    unique_elements.add(element)
        else:
            if iterable not in unique_elements:
                result.append(iterable)
                unique_elements.add(iterable)
    return result


data = {
    "saph": {"sil": 1, "nick": 1},
    "jiv": {"alu": 1, "zinc": 1},
    "stir": {"silv": 1},
    "crot": {"alu": 1},
    "rub": {"nick": 1, "alu": 1, "sil": 1},
    "bob": {"sil": 1, "silv": 1, "zinc": 1}
}
inputs = data.keys()
outputs = [list(data[inp].keys()) for inp in inputs]
outputs = flatten_and_remove_duplicates(outputs)


for inp in inputs:
    data[inp]["resources"] = -1 - np.sum([data[inp].get(out, 0) for out in outputs])
print(data)

outputs = [data[inp].keys() for inp in inputs]
outputs = flatten_and_remove_duplicates(outputs)
outputs = sorted(outputs, key=lambda x: len(x))

mat = np.array([[data[inp].get(out, 0) for out in outputs] for inp in inputs]).T
print(mat)
inv = np.round(np.linalg.inv(mat), 5)
print(inv)

for row, inp in zip(inv, inputs):
    print(inp, ": ", [f"{out}: {n}" for n, out in zip(row, outputs) if n != 0])
