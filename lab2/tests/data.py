import module_test

def test_func(a : int) -> int:
    return 228*a


class TestClass():
    some_bool_value = True
    class_value = 18
    c = 10.2

    def __init__(self, a: int, b: int = 2):
        self.c += (a+b)

    def count(self) -> int:
        return self.c/18

test_obj = TestClass(2)


def func_test_module():
    return module_test.printing()