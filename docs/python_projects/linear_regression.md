# Linear regression

**Project status:** Complete

This work is part of my first Rust project (see [here](../rust_projects/linear_regression.md)). The aim is to learn how to write Python bindings for Rust code.


## Roadmap
- [x] Write Python API wrapper for the Rust library crate.
- [x] Add CI pipeline for automatic publishing to PyPI.


## Installation
=== "python -m venv"

    ```bash
    python -m venv my-venv
    source my-venv/bin/activate
    pip install drkaizeng-linear-regression
    ```

=== "uv venv"

    ```bash
    uv venv my-venv
    source my-venv/bin/activate
    uv pip install drkaizeng-linear-regression
    ```

## Usage
### As a CLI tool
Assume that an environment with the package installed has been activated.
```bash
linear-regression --help
```

### As an importable library
```python
from pathlib import Path

from linear_regression.linear_regression import linear_regression

input_tsv = Path("input.tsv")
with open(input_tsv, "w") as f:
    f.write("1\t2\n2\t3\n3\t4\n")

output_tsv = Path("output.tsv")

linear_regression.callback(input_tsv=input_tsv, output_tsv=output_tsv, overwrite=True)
```

Note that `linear_regression` is a function decorated with `@click.command()`, which turns it into a `click.core.Command` object. We need to use its `.callback` attribute to access the underlying function.
