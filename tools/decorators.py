import inspect
from functools import wraps
from typing import Callable

import numpy as np


class decorator:
    def wrapper(self, f:Callable, *args, **kwargs)->dict:
        pass
    
    def __call__(self, f:Callable) -> Callable:
        signature:inspect.Signature = inspect.signature(f)
        params = signature.parameters
        params_names = list(params)
        has_kwargs = any(i.kind==inspect._ParameterKind.VAR_KEYWORD for i in params.values())
        
        def wrapper(*args, **kwargs):
            res = self.wrapper(*args, **kwargs)
            if not has_kwargs:
                res = {k:v for k,v in res.items() if k in params_names}
            res = f(**res)
            return res
        return wrapper

class string2numpy(decorator):
    def __init__(self,encoding="utf-8",shape:tuple=None, sep:str="\n") -> None:
        self.encoding = encoding
        self.shape=shape
        self.sep = sep
        
    def wrapper(self, data_str):
        data = np.frombuffer(data_str.encode(self.encoding),dtype=np.uint8)
        if self.sep is not None:
            sep = ord(self.sep)
            is_sep = data==sep
            data = data[~is_sep]

        if self.shape:
            data = data.reshape(self.shape)


        n_elements_by_bag = np.diff(np.nonzero(np.concatenate([[1],is_sep,[1]]))[0])-1

        # Compute item index in bag
        n_elements_by_bag_max = n_elements_by_bag.max()

        mask = np.arange(n_elements_by_bag_max)[None,:]< n_elements_by_bag[:,None]
        bag_index, item_bag_index = np.unravel_index(np.arange(mask.size)[mask.ravel()],mask.shape)
        
        
        res = dict(
            bag_index=bag_index,
            data=data,
            data_str=data_str,
            n_elements_by_bag=n_elements_by_bag,
            item_bag_index=item_bag_index
            )
        return res
        