# vim

## Registers
### Controls which register `vim` is pasting from.
Sometimes when using `p`/`P` to paste, instead of pasting from the default `"` register, it pastes the contents in the unnamed `*` register. `set clipboard?` shows the current setting. A solution is prepend (using `^=`) both the unnamed `*` and unnameplus `+` register to `clipboard`, so that operations in `vim` (yanking, deletion, etc), as well as the system clipboard, all use them:
```
set clipboard^=unnamed,unnamedplus
```
This setting will allow (1) normal yanking and pasting within vim, (2) yanking things in vim and pasting the text in other apps, and (3) copying text from other apps and pasting it into vim.