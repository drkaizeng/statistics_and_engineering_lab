# conda

## Using `conda activate` in bash scripts
Some of the required bash environment variables/functions are not exported to sub-shells. Therefore, even if `conda` has been set up in `.bashrc`, we cannot using `conda activate` in a bash script because the script is executed in a sub-shell. A possible solution is to `source` the following file in `conda`'s folder: `etc/profile.d/conda.sh`. This is sub-optimal because it ties it to the specific location of `conda`'s folder. A better solution is the following, assuming `conda` is in the `PATH`:
```bash
__conda_setup="$('conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    echo "Failed to initialise conda"
    exit 1
fi
```