from validate import coerce_to


class Pa(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return self.x + self.y + other

    def __str__(self):
        return '{}, {}'.format(self.x, self.y)

@coerce_to(('x', Pa), ('y', int), side_effect=TypeError)
def v1(x, y):
    return x + y


res = v1((3, 4), 34)
assert 41 == res



@coerce_to(("arg1", {"some_key1": int, "some_key2": str},))
def foo(arg1):
    assert isinstance(arg1['some_key1'], int)
    assert isinstance(arg1['some_key2'], str)
    return arg1

d = {"some_key1": '5', "some_key2": 10}
result = foo(d)
assert result['some_key1'] + 10 == 15
assert result['some_key2'] + '10' == '1010'