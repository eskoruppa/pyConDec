# pyConDec

**pyConDec** is a lightweight Python library that provides conditional decorators — decorators that apply an acceleration or transformation only when the required dependency is available, and fall back to a no-op otherwise.

The primary use case is [Numba](https://numba.readthedocs.io/) JIT compilation: code decorated with `cond_jit` will be compiled with `numba.jit` when Numba is installed, and will run as plain Python when it is not. This lets you write performance-optimised code that remains portable and installable without making Numba a hard dependency.

---

## Installation

### From PyPI (once published)

```bash
pip install pyConDec
```

### From source

```bash
git clone https://github.com/eskoruppa/pyConDec.git
cd pyConDec
pip install .
```

To also install the optional Numba dependency:

```bash
pip install numba
```

---

## Usage

### `cond_jit` — conditional `numba.jit`

`cond_jit` wraps `numba.jit`. When Numba is installed the function is JIT-compiled; when it is not, the original Python function is returned unchanged.

```python
from pycondec import cond_jit

@cond_jit(nopython=True, cache=True)
def dot_product(a, b):
    result = 0.0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result

print(dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]))  # 32.0
```

If Numba is **not** installed, `dot_product` behaves as a regular Python function — no import errors, no code changes needed.

### `cond_jitclass` — conditional `numba.experimental.jitclass`

```python
import numpy as np
from pycondec import cond_jitclass

spec = [('value', float)]

@cond_jitclass(spec)
class Counter:
    def __init__(self, value):
        self.value = value

    def increment(self):
        self.value += 1.0
```

Again, if Numba is absent the class is returned as a plain Python class.

### `cond_dec` — conditional arbitrary decorator

`cond_dec` is the general-purpose variant. It applies **any** decorator conditionally based on a boolean flag. Two calling styles are supported:

**Style 1 — pre-configured decorator** (decorator already holds its own arguments):

```python
from functools import lru_cache
from pycondec import cond_dec

USE_CACHE = True

@cond_dec(lru_cache(maxsize=128), USE_CACHE)
def expensive(n):
    return sum(range(n))
```

**Style 2 — decorator factory with arguments** (pass the factory and its arguments separately):

```python
from functools import lru_cache
from pycondec import cond_dec

USE_CACHE = True

@cond_dec(lru_cache, USE_CACHE, maxsize=128)
def expensive(n):
    return sum(range(n))
```

Both styles are equivalent. The second style mirrors the `cond_jit` experience and is convenient when you want to keep the decorator factory and its arguments readable inline.

When `condition` is `False` the original, undecorated function is returned — no branching needed at the call site and no hard dependency on the library providing the decorator.

---

## License

GNU General Public License v2.0 — see [LICENSE](LICENSE) for details.
