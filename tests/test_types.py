# -*- coding: utf-8 -*-
import unittest

from dewloosh.core import Library
from dewloosh.core.types.defaultdict import DefaultDict, NestedDict, OrderedDictCollection
from dewloosh.core.types.numberedentity import UniqueNumbered


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
        assert data.locked
        try:
            data['a', 'b', 'd'] = 2
        except:
            has_error = True
        finally:
            assert has_error
        data.unlock()
        assert not data.locked
        data.locked = False
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
        
        # other stuff
        data['a', 'b'].root()
        data.__repr__()

    def test_lib_compliance(self):
        """
        Tests to assure that a `Library` works the same way as a `dict`.
        """
        data1 = Library(a=1, b=dict(c=2, d=3))
        data2 = dict(a=1, b=dict(c=2, d=3))
        assert data1 == data2
        assert list(data1.keys()) == list(data1.keys())
        assert list(data1.values()) == list(data1.values())
        

class TestDicts(unittest.TestCase):
    
    def test_dicts(self):
        factory = lambda *_: 'none'

        dd = DefaultDict(factory)
        print(dd['key'])

        ndd = NestedDict(ordered=False)
        ndd['a']['b']['c']['e'] = 1
        ndd['a']['b']['d'] = 2
        print(ndd['a']['b']['c'])
        print(ndd['a']['b']['d'])

        for k, v in ndd.items():
            print((k, v))

        for v in ndd.values():
            print(v)

        for k in ndd.keys():
            print(k)

        for k in ndd.keys(deep=True):
            print(k)

        for k, v in ndd.items(deep=True):
            print((k, v))

        for a, v in ndd.items(deep=True, return_address=True):
            print((a, v))

        def foo(*a):
            print(type(a))

        dc = OrderedDictCollection()
        dc['a']['b']['c']['e'] = 1
        dc['a']['b']['d'] = 2

        for v in dc.values():
            print(v)

        for k in dc.keys():
            print(k)

        for k in dc.keys(deep=True):
            print(k)


class TestNumbered(unittest.TestCase):
    
    def test_numbered(self):
        u1 = UniqueNumbered(key='somekey')
        with u1 as un:
            un.num
        u1.to_hex
        u1.to_int
        u1.GUID
        u1.GID
        u1.ID
        u1.LID
        u1.UUID
        u1.UID
        u1.key
        assert str(u1) == u1.key
        #hash(u1)
        u1.GUID = 1
        u1.GID = 1
        u1.ID = 1
        u1.LID = 1
        u1.key = 'a'
        
        has_error = False
        try:
            u1.UUID = 1
        except AttributeError:
            has_error = True
        assert has_error
        
        has_error = False
        try:
            u1.UID = 1
        except AttributeError:
            has_error = True
        assert has_error
        
        u1 = UniqueNumbered(ID=1, GID=1, key='somekey')
        u2 = UniqueNumbered(LID=1, GID=1, key='somekey')
        assert not u1 == u2
        hash(u1)    
        
        
if __name__ == "__main__":
    unittest.main()
