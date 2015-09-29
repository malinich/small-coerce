# coding: utf-8
from __future__ import unicode_literals

import collections
import inspect

def call_func(f, val, acc=None):
    if isinstance(f, dict):
        acc = {}
        for ff, vv in f.items():
            d = {ff: call_func(f[ff], val[ff], acc)}
            acc.update(d)

    else:
        val = val if isinstance(val, tuple) else (val,)
        return f(*val)
    return acc


def coerce_to(*fields, **kwargs):
    side_effect = kwargs.pop('side_effect', Exception)

    field_map = collections.OrderedDict()
    for field, type_t in fields:
        field_map[field] = type_t

    def validate(kwargs):

        f, val = kwargs[0], (kwargs[1], )
        try:
            mapped = call_func(field_map[f], *val)
        except (ValueError, TypeError) as e:
            raise side_effect(e)
        return f, mapped

    def wrap(func):
        def wrap1(*args, **kwargs):
            allar = inspect.getcallargs(func, *args, **kwargs)
            map_kwargs = dict(tuple(map(validate, allar.items())))
            return func(**map_kwargs)
        return wrap1
    return wrap

