# Miscellaneous tips and examples

## `multiprocessing` relies on `pickle` and cannot handle object such as lambda functions
To send data, including functions and the objects they rely on, to different processes, Python's `multiprocessing` module needs to "pickle" them. The standard pickle library struggles to handle certain types of objects, most notably functions that are defined inside other functions (closures), lambda functions, and functions defined in the `__main__` scope of a script. When `multiprocessing` tries to pickle one of these "un-picklable" objects, it throws `AttributeError`.
```python
import multiprocessing as mp
from dataclasses import dataclass
from typing import Callable


@dataclass
class Test:
    func: Callable[[float], float]


def test1(x):
    return x * x


def test2(x):
    return 2 * x


def func(t: Test, x: float):
    return t.func(x)


if __name__ == "__main__":
    # Implementation causing problems
    t1 = Test(lambda x: x * x)
    t2 = Test(lambda x: 2 * x)

    with mp.Pool(1) as pool:
        print(pool.starmap(func, ([t1, 3], [t2, 4])))
    # _pickle.PicklingError: Can't pickle <function <lambda> at 0x102befd00>: attribute lookup <lambda> on __main__ failed

    # Avoiding the problem
    t1 = Test(test1)
    t2 = Test(test2)

    with mp.Pool(1) as pool:
        print(pool.starmap(func, ([t1, 3], [t2, 4])))
```


## Load a module using its absolute path
```python
import importlib.util
import sys

from importlib.abc import Loader

# Define the absolute path to the module
module_path = '/absolute/path/to/your/module.py'

# Load the module
spec = importlib.util.spec_from_file_location("module_name", module_path)
if spec is None:
    raise RuntimeError()
assert isinstance(spec.loader, Loader)  # To keep mypy and pytype happy   
module = importlib.util.module_from_spec(spec)
sys.modules["module_name"] = module
spec.loader.exec_module(module)

# Now you can use the module
module.some_function()
```