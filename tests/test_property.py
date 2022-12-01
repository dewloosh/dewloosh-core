# -*- coding: utf-8 -*-
import unittest

from dewloosh.core.cp import classproperty


class TestProperty(unittest.TestCase):

    def test_class_property(self):

        class TestClasss:

            @classproperty
            def prop(cls):
                return 1

        self.assertEqual(TestClasss.prop, 1)


if __name__ == "__main__":
    unittest.main()
