# Miscellaneous tips and examples

## Running a bash script
A bash script is run in a sub-shell, which is an independent, and non-interactive shell. The following table from [here](https://shreevatsa.wordpress.com/2008/03/30/zshbash-startup-files-loading-order-bashrc-zshrc-etc/) shows that `.bashrc` is not loaded.
```
+----------------+-----------+-----------+------+
|                |Interactive|Interactive|Script|
|                |login      |non-login  |      |
+----------------+-----------+-----------+------+
|/etc/profile    |   A       |           |      |
+----------------+-----------+-----------+------+
|/etc/bash.bashrc|           |    A      |      |
+----------------+-----------+-----------+------+
|~/.bashrc       |           |    B      |      |
+----------------+-----------+-----------+------+
|~/.bash_profile |   B1      |           |      |
+----------------+-----------+-----------+------+
|~/.bash_login   |   B2      |           |      |
+----------------+-----------+-----------+------+
|~/.profile      |   B3      |           |      |
+----------------+-----------+-----------+------+
|BASH_ENV        |           |           |  A   |
+----------------+-----------+-----------+------+
|                |           |           |      |
+----------------+-----------+-----------+------+
|                |           |           |      |
+----------------+-----------+-----------+------+
|~/.bash_logout  |    C      |           |      |
+----------------+-----------+-----------+------+
```
Thus, in some cases, `.bashrc` needs to be explicitly sourced in the script.
!!! important
    Ubuntu's default `.bashrc` contains the following that stops `.bashrc` from being sourced from non-interactive shells.

    ```
    case $- in
        *i*) ;;
        *) return;;
    esac
    ```

## Skip the first N lines when printing a file
```
tail -n +<N+1> <filename>  # N is the number of lines
tail -n +11 <filename>  # Skip the first 10 lines
```