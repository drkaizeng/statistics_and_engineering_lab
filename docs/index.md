# Stat gen playground
Here is a collection of tips that are hopefully useful for statistical geneticists and bioinformaticians.

## Compute environments
### `mkdocs`
The environment for running `mkdocs` is specified by `docs/pyproject.toml`. This file determines `poetry.lock`, which is exported to `docs/requirements.txt` (for details see [here](misc/setting_up_mkdocs.md#setting-up-mkdocs)). 

### Other code
To run the code in `src` (mostly Python and C), first construct a docker image
```bash
./build_docker.sh
```
Then spin up a container
```bash
./enter_docker.sh
```
This binds the repo to `/workspace`. We can now attach VS Code to the container.
