import copy

import scipy.sparse

from pytensor.compile import SharedVariable, shared_constructor
from pytensor.sparse.basic import SparseTensorType, _sparse_py_operators


class SparseTensorSharedVariable(_sparse_py_operators, SharedVariable):
    dtype = property(lambda self: self.type.dtype)
    format = property(lambda self: self.type.format)


@shared_constructor.register(scipy.sparse.spmatrix)
def sparse_constructor(
    value, name=None, strict=False, allow_downcast=None, borrow=False, format=None
):
    if format is None:
        format = value.format

    type = SparseTensorType(format=format, dtype=value.dtype)

    if not borrow:
        value = copy.deepcopy(value)

    return SparseTensorSharedVariable(
        type=type, value=value, name=name, strict=strict, allow_downcast=allow_downcast
    )