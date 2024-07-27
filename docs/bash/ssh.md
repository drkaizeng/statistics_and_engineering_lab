# Setting up multiple key pairs for multiple GitHub accounts
- Run the following comment to generate a new SSH key. When prompted, save the id file with an informative name to `~/.ssh`. 
```bash
ssh-keygen -t ed25519 -C "$an_informative_comment_for_identifying the key"
```
!!! note
    An id file refers to the file without the `.pub` extension.

!!! important
    Leave the passphrase blank or use `ssh-keygen -p` to remove the existing passphrase. The problem with having passphrase is that `ssh-agent` does not seem to be able to remember the passphrases for different accounts correctly between different log in sessions. This breaks the association between SSH key and the correct GitHub account (i.e., `ssh -T git@$host` does not return the correct account name). Even in the simpler case where there is only one account, having passphrase often results in being prompted to enter it, even though it has been added via `ssh-agent` before.

- Start `ssh-agent`
```bash
eval "$(ssh-agent -s)"
```

- Add key to `ssh-agent`. 
```bash
ssh-add $path_to_saved_id_file
# Mac: Add `--apple-use-keychain` if passphrase is set. 
# Mac: If prompts for passphrase keep appearing, try to add the command to `~/.zshrc` or `~/.bashrc`.
```

- **Mac**: Update `~/.ssh/config`. One entry for each id file. ***NB***: `~/.ssh/config` must have permisson `644`.
```bash
Host github.com  # this should be unique for each id file 
    HostName github.com  # the true web address; leave as is
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519  # path to id file
```

- **Linux**: Update `~/.ssh/config`. One entry for each id file. ***NB***: `~/.ssh/config` must have permisson `644`.
```bash
Host github.com
    HostName github.com
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

- Test
```bash
ssh -T git@$host  # $host is the name set the Host field in ~/.ssh/config
```