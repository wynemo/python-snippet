# -*- coding: utf-8 -*-
from lib6 import unicode, _PY3


class _LazyString(object):
    """Class for strings created by a function call.
    The proxy implementation attempts to be as complete as possible, so that
    the lazy objects should mostly work as expected, for example for sorting.
    """
    __slots__ = ('_func', '_args', '_kwargs', '_value')

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._value = None

    @property
    def value(self):
        if not self._value:
            try:
                self._value = self._func(*self._args, **self._kwargs)
            except AttributeError as e:
                raise RuntimeError("Suppressed AttributeError: " + str(e))
        return self._value

    # value = property(lambda self: self._func(*self._args, **self._kwargs))

    def __contains__(self, key):
        return key in self.value

    def __nonzero__(self):
        return bool(self.value)

    def __dir__(self):
        return dir(unicode)

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return str(self.value)

    def __unicode__(self):
        return unicode(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __mod__(self, other):
        return self.value % other

    def __rmod__(self, other):
        return other % self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __getattr__(self, name):
        if name == '__members__':
            return self.__dir__()
        return getattr(self.value, name)

    def __getstate__(self):
        return self._func, self._args, self._kwargs

    def __setstate__(self, tup):
        self._func, self._args, self._kwargs = tup

    def __getitem__(self, key):
        return self.value[key]

    def __copy__(self):
        return self

    def __repr__(self):
        try:
            return 'l' + repr(self.value)
        except Exception:
            return '<%s broken>' % self.__class__.__name__

    def format(self, **params):
        if _PY3:
            translated = str(self)
        else:
            translated = unicode(self)
        return translated.format(**params)

