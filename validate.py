# coding: utf-8
from __future__ import unicode_literals

import collections
import inspect


def validate_request(*fields, **kwargs):
    side_effect = kwargs.pop('side_effect', Exception)

    field_map = collections.OrderedDict()
    for field, type_t in fields:
        field_map[field] = type_t

    def validate(kwargs):
        f, val = kwargs[0], isinstance(kwargs[1], tuple) and kwargs[1] or (kwargs[1], )
        try:
            mapped = field_map[f](*val)
        except (ValueError, TypeError) as e:
            raise side_effect(e)
        return (f, mapped)

    def wrap(func):
        def wrap1(*args, **kwargs):
            allar = inspect.getcallargs(func, *args, **kwargs)
            map_kwargs = dict(tuple(map(validate, allar.items())))
            return func(**map_kwargs)
        return wrap1
    return wrap

