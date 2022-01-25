from typing import Union

from tache.batch import Batch
from tache.cached import Cached


class MagicCachedObject:
    def __init__(self, cached_func: Union[Batch, Cached], original_args, original_kwargs, cached_object = None):
        self._cached_func = cached_func
        self.args = original_args
        self.kwargs = original_kwargs
        self._obj = cached_object
        self._is_cached_obj = True
        if not cached_object:
            self.fetch_original()

    def fetch_original(self):
        if not self._is_cached_obj:
            return
        self._cached_func.invalidate(*self.args, **self.kwargs)
        self._obj = self._cached_func(*self.args, **self.kwargs)
        if isinstance(self._cached_func, Batch):
            self._obj = self._obj[0]
        self._is_cached_obj = False

    def __str__(self):
        return str(self._obj)

    def __repr__(self):
        return self._obj.__repr__()

    def __getitem__(self, item):
        try:
            return self._obj[item]
        except (TypeError, KeyError, IndexError):
            self.fetch_original()
        return self._obj[item]

    def __get__(self, item):
        try:
            return getattr(self._obj, item)
        except AttributeError:
            self.fetch_original()
        return getattr(self._obj, item)

    def __dir__(self):
        return self._obj.__dir__()

    def __eq__(self, a):
        return self._obj == a


