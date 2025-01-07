# ssh

## Setting up multiple key pairs for multiple GitHub accounts
- Run the following command to generate new SSH keys (one for each GitHub account and add them to the account). When prompted, save the id file with an informative name to `~/.ssh`. 
```bash
ssh-keygen -t ed25519 -C "$an_informative_comment_for_identifying_the_key"
```
!!! note
    An id file refers to the file without the `.pub` extension, and secret file is the file with the same prefix, but without the extension. The permission for the `.pub` file and the secret file should be `644` and `600`, respectively.

!!! important
    Leave the passphrase blank or use `ssh-keygen -p` to remove the existing passphrase. The problem with having passphrase is that `ssh-agent` does not seem to be able to remember the passphrases for different accounts correctly between different log in sessions. This breaks the association between SSH key and the correct GitHub account (i.e., `ssh -T git@$host` does not return the correct account name). Even in the simpler case where there is only one account, having passphrase often results in being prompted to enter it, even though it has been added via `ssh-agent` before.

- Start `ssh-agent`
```bash
eval "$(ssh-agent -s)"
```

- Add key to `ssh-agent`. 
```bash
ssh-add $path_to_saved_secret_file
# Mac: Add `--apple-use-keychain` if passphrase is set. 
# Mac: If prompts for passphrase keep appearing, try to add the command to `~/.zshrc` or `~/.bashrc`.
```

- **Mac**: Update `~/.ssh/config`. One entry for each id file. ***NB***: `~/.ssh/config` must have permisson `644`.
```bash
Host $host_name  # this should be unique for each id file 
    HostName github.com  # the true web address; leave as is
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519  # path to id file
```

- **Linux**: Update `~/.ssh/config`. One entry for each id file. ***NB***: `~/.ssh/config` must have permisson `644`.
```bash
Host $host_name  # this should be unique for each id file 
    HostName github.com  # the true web address; leave as is
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

- Test. For each `$host_name`, do the following, the output of which should include the correct account name.
```bash
ssh -T git@$host_name  # $host_name is the name set the Host field in ~/.ssh/config
```

- Use the correct `$host_name` for GitHub repos under different accounts.
```bash
# Clone new repos
git clone git@${host_name}:drkaizeng/stat_gen_playground.git

# Update existing repos
git remote set-url origin git@${host_name}:drkaizeng/stat_gen_playground.git
```



## Starting `ssh-agent` automatically on login
Based on this [ref](https://unix.stackexchange.com/questions/90853/how-can-i-run-ssh-add-automatically-without-a-password-prompt), add the following to `.bash_profile`:
```bash
if [ -n "$SSH_AUTH_SOCK" ]; then
    ids=$(pgrep ssh-agent)
    # quote to prevent word split
    if [ -n "$ids" ]; then
	      # do not quote; otherwise no word split and the loop runs once
	      for id in $ids; do
	          SSH_AGENT_PID="$id"
	          # `ssh-agent -k` relies on SSH_AGENT_PID being set
	          export SSH_AGENT_PID
	          eval "$(ssh-agent -k)" > /dev/null
	      done
    fi
fi
eval "$(ssh-agent -s)" > /dev/null
ssh-add -q ~/.ssh/$name_of_secret_file
```
and the following to `.bash_logout` to kill the agent on logout:
```bash
if [ -n "$SSH_AUTH_SOCK" ]; then
    ids=$(pgrep ssh-agent)
    # quote to prevent word split
    if [ -n "$ids" ]; then
	      # do not quote; otherwise no word split and the loop runs once
	      for id in $ids; do
	          SSH_AGENT_PID="$id"
	          # `ssh-agent -k` relies on SSH_AGENT_PID being set
	          export SSH_AGENT_PID
	          eval "$(ssh-agent -k)" > /dev/null
	      done
    fi
fi
```
