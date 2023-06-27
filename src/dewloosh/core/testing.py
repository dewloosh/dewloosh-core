import unittest
from typing import Callable


class TestCase(unittest.TestCase):
    def assertFailsProperly(self, exc: Exception, fnc: Callable, *args, **kwargs):
        failed_properly = False
        try:
            fnc(*args, **kwargs)
        except exc:
            failed_properly = True
        finally:
            self.assertTrue(failed_properly)
