import unittest
import my_serializer

import data

ser = my_serializer.TomlSerializator()

class TomlTest(unittest.TestCase):
    def test_func(self):
        arg = 2
        real_func = data.test_func(arg)
        parse_func = ser.loads(ser.dumps(data.test_func))(arg)
        self.assertEqual(real_func, parse_func)

    def test_class(self):
        arg = 5
        real_class = data.TestClass(arg)
        parse_class = ser.loads(ser.dumps(data.TestClass))(arg)
        self.assertEqual(real_class.count(), parse_class.count())


    def test_obj(self):
        real_obj = data.test_obj
        parse_obj = ser.loads(ser.dumps(real_obj))
        self.assertEqual(real_obj.count(), parse_obj.count())

        
    def test_module(self):
        real_module = data.func_test_module
        parse_module = ser.loads(ser.dumps(data.func_test_module))
        self.assertEqual(real_module(), parse_module())


if __name__ == '__main__':
    unittest.main()