from validate import validate_request

from unittest import TestCase


class Pa(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, *args, **kwargs):
        print self.__class__
        return self.x

    def __add__(self, other):
        return self.x + other

    def __str__(self):
        return '{}, {}'.format(self.x, self.y)

@validate_request(('x', Pa), ('y', int), side_effect=TypeError)
def v1(x, y):
    print 'x: ', x
    return x + y

b = 4

res = v1((3, 4), b)
assert 7 == res
