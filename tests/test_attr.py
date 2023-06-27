# -*- coding: utf-8 -*-
import unittest

from dewloosh.core import attributor


class TestAttributor(unittest.TestCase):
    def test_attributor(self):
        axiom = attributor("__isaxiom__")
        abstractaxiom = attributor("__isaxiom__", "__isabstractmethod__")

        @axiom
        def foo(a, b):
            return "an axiom"

        self.assertTrue(foo.__isaxiom__)

        @abstractaxiom
        def foo(a, b):
            return "an abstract axiom"

        self.assertTrue(foo.__isaxiom__)
        self.assertTrue(foo.__isabstractmethod__)


if __name__ == "__main__":
    unittest.main()
