# -*- coding: utf-8 -*-
import unittest

from dewloosh.core import Library


class TestLibrary(unittest.TestCase):

    def test_lib_basic(self):
        """
        Qualitative test on basic usage of a Library.
        """
        data = Library()
        data['a', 'b', 'c'] = 1
        f = data.containers
        assert [c.key for c in f(inclusive=True, deep=True)] == [
            None, 'a', 'b']
        assert [c.key for c in f(inclusive=True, deep=False)] == [None, 'a']
        assert [c.key for c in f(inclusive=False, deep=True)] == ['a', 'b']
        assert [c.key for c in f(inclusive=False, deep=False)] == ['a']
        assert data['a', 'b'].depth == 2
        assert data['a', 'b'].key == 'b'
        assert data.is_root() is True
        assert data['a', 'b'].is_root() is False
        assert data['a', 'b'].parent == data['a']
        assert data['a', 'b'].root() == data

        # lock test
        has_error = False
        data.lock()
        try:
            data['a', 'b', 'd'] = 2
        except:
            has_error = True
        finally:
            assert has_error
        data.unlock()
        has_error = False
        try:
            data['a', 'b', 'd'] = 2
        except:
            has_error = True
        finally:
            assert not has_error

        # try indexing
        data['a']['b']['e'] = 3
        assert data['a', 'b', 'e'] == 3

    def test_lib_compliance(self):
        """
        Tests to assure that a `Library` works the same way as a `dict`.
        """
        data1 = Library(a=1, b=dict(c=2, d=3))
        data2 = dict(a=1, b=dict(c=2, d=3))
        assert data1 == data2
        assert list(data1.keys()) == list(data1.keys())
        assert list(data1.values()) == list(data1.values())


if __name__ == "__main__":
    unittest.main()
