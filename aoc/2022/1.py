import numpy as np

def main(data):
    data = data.split("\n")
    is_sep = np.array([len(i)==0 for i in data])
    elf_index = np.cumsum(is_sep)[~is_sep]
    data = np.array([int(i) for i in data if len(i)])

    selector = data[None,:]*(np.arange(elf_index.max()+1)[:,None]==elf_index[None,:])
    elf_total = selector.sum(1)
    res1 = elf_total.max()
    res2 = np.sort(elf_total)[-3:].sum()
    return res1,res2