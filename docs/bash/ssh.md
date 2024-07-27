# Setting up multiple key pairs for multiple GitHub accounts
- Run the following comment to generate a new SSH key. When prompted, save the id file with an informative name to `~/.ssh`. 
```bash
ssh-keygen -t ed25519 -C "$an_informative_comment_for_identifying the key"
```
!!! note
    An id file refers to the file without the `.pub` extension.

- Start `ssh-agent`
```bash
eval "$(ssh-agent -s)"
```

- **Mac**: Add key to `ssh-agent`. If prompts for passphrase keep appearing, try to add the command to `~/.zshrc` or `~/.bashrc`.
```bash
ssh-add --apple-use-keychain $path_to_saved_id_file
```

- **Linux**: Add key to `ssh-agent`.
```bash   
ssh-add $path_to_saved_id_file
```
Install `keychain`, which could be done using either `sudo apt-get install keychain`, or downloading a binary from https://github.com/funtoo/keychain/releases. Then add the following to `~/.bash_profile` or `~/.profile`, so that each time we log into the system (including starting a new tmux server) the passphrase is loaded by `ssh-add` (see https://fingers-in-the-pi.readthedocs.io/en/latest/initial_setup/ssh_setup/).
```bash
# Use only the file name not the full path
eval `keychain --eval --agents ssh $name_of_saved_id_file`  
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