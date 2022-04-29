# imaksus Serializer


## Run as library
```python
from my_serializer.serializator import TomlSerializator

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

toml_ser = TomlSerializator()
_str = toml_ser.dumps(simple_func)
_obj = toml_ser.loads(_str)
```

## Run as package
 ```bash
python3 -m my_serializer -src "./data.json" -dst "./data.yaml"
```

or
 ```bash
python3 -m my_serializer -conf "./conf.ini"
```
config.ini:
```ini
[DEFAULT]
src_path = "./data.json"
dst_path = "./data.yaml"
```