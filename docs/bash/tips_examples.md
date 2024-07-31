# Miscellaneous tips and examples

## Skip the first N lines when printing a file
```
tail -n +<N+1> <filename>  # N is the number of lines
tail -n +11 <filename>  # Skip the first 10 lines
```