# pandas examples

## Joining

### Outer-joining indices and stacking columns
```
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
