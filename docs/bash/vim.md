# vim


## Tips and examples
### Reindent the a section of the file
We can quickly reindent a selected section of the file. The number of spaces to use for each step of (auto)indent is controlled by `shiftwidth` or `sw`.
- To reindent the entire file, do the following in normal mode: `gg` (go to the top of the file), `=` (indent), `G` (go to the end of the file)
- To indend a selected section, select the lines and then hit `=`.


## Packages and plug-ins
### Installing plug-ins using `packload`
Find out the `runtimepath` using command, so as to locate where the plug-ins should be stored.
```bash
echo join(split(&runtimepath, ','), "\n")
```
For `nvim`, a possible location is `~/.config/nvim/pack/*/start/*` (e.g., the ale linter is installed in `.config/nvim/pack/bundle/start/ale` using `git clone --depth 1 https://github.com/dense-analysis/ale.git`). Once the files have been copied, use the following to load it. 
```bash
packloadall | silent! helptags ALL
```
One way to check whether the plug-in has been installed (e.g., `h ale`).


## Registers
### Controls which register `vim` is pasting from.
Sometimes when using `p`/`P` to paste, instead of pasting from the default `"` register, it pastes the contents in the unnamed `*` register. `set clipboard?` shows the current setting. A solution is prepend (using `^=`) both the unnamed `*` and unnameplus `+` register to `clipboard`, so that operations in `vim` (yanking, deletion, etc), as well as the system clipboard, all use them:
```
set clipboard^=unnamed,unnamedplus
```
This setting will allow (1) normal yanking and pasting within vim, (2) yanking things in vim and pasting the text in other apps, and (3) copying text from other apps and pasting it into vim.


