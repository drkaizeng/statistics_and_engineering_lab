# vim
## Installing plug-ins
### [vim-plug](https://github.com/junegunn/vim-plug)
For nvim:
```bash
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```
```
:PlugInstall to install the plugins
:PlugUpdate to install or update the plugins
:PlugDiff to review the changes from the last update
:PlugClean to remove plugins no longer in the list
```


## Registers
### Controls which register `vim` is pasting from.
Sometimes when using `p`/`P` to paste, instead of pasting from the default `"` register, it pastes the contents in the unnamed `*` register. `set clipboard?` shows the current setting. A solution is prepend (using `^=`) both the unnamed `*` and unnameplus `+` register to `clipboard`, so that operations in `vim` (yanking, deletion, etc), as well as the system clipboard, all use them:
```
set clipboard^=unnamed,unnamedplus
```
This setting will allow (1) normal yanking and pasting within vim, (2) yanking things in vim and pasting the text in other apps, and (3) copying text from other apps and pasting it into vim.


## Useful examples
### Reindent the a section of the file
We can quickly reindent a selected section of the file. The number of spaces to use for each step of (auto)indent is controlled by `shiftwidth` or `sw`.
- To reindent the entire file, do the following in normal mode: `gg` (go to the top of the file), `=` (indent), `G` (go to the end of the file)
- To indend a selected section, select the lines and then hit `=`.