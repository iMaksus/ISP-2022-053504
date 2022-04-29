import math
from my_serializer.converter import Converter

opi = 2
def simple_func(arg1):
    """Aboba"""
    t = 6
    def _h(arg2):
        i = 7
        def _hahahah():
            return math.pi ** 2
        return math.sin(arg1 * arg2 * opi * t * i * _hahahah())
    return _h(6)


converter = Converter()
converter.get_args()
converter.parse_args(simple_func)