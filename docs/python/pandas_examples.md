# pandas examples

## Joining

### Outer-joining indices and stacking columns
```python
df1 = pd.DataFrame({'A': [1, 2]}, index=['a', 'b'])
df2 = pd.DataFrame({'A': [5, 6]}, index=["a", "c"])
df3 = pd.DataFrame({'A': [7, 8], 'B': [10, 11]}, index=["a", "c"])

# List of DataFrames
dfs = [df1, df2, df3]

# Concatenate DataFrames
df = pd.concat(dfs, join="outer", axis=1)

print(df)

#      A    A    A     B
# a  1.0  5.0  7.0  10.0
# b  2.0  NaN  NaN   NaN
# c  NaN  6.0  8.0  11.0
```


## Behaviours of `|` and `&` operators
These operators have the same behaviours as those in `numpy` iff the index and columns of the two data frames are identical. Otherwise, `pandas` perform an outer join of the index and columns first.
```python
df1 = pd.DataFrame({'A': [True, False]}, index=['a', 'b'])
df2 = pd.DataFrame({'A': [False, False]}, index=['a', 'b'])
df3 = pd.DataFrame({'B': [True, False]}, index=['a', 'b'])
df4 = pd.DataFrame({'B': [True, False]}, index=['b', 'c'])

print(df1 & df2)
print(df1 | df2)
print(df1 & df3)
print(df1 | df3)
print(df1 & df4)
print(df1 | df4)

#        A
# a  False
# b  False
#        A
# a   True
# b  False
#        A      B
# a  False  False
# b  False  False
#        A      B
# a   True  False
# b  False  False
#        A      B
# a  False  False
# b  False  False
# c  False  False
#        A      B
# a   True  False
# b  False  False
# c  False  False
```