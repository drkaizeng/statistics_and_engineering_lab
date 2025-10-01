# pandas examples

## Miscellaneous

### The `FutureWarning: Downcasting object dtype arrays on` problem in `pandas 2`
When using `.replace`, `.fillna`, `.ffill`, `.bfill` on an object dtype array, it would cause it to downcast it to a different type (e.g., `bool` or `float`). This behaviour is not supported in future `pandas` versions. The solution is to use `with pd.option_context('future.no_silent_downcasting', True):` so that the code in the context will behave like in a future `pandas` release, and avoid doing silent downcasting, or globally, by setting `pd.set_option(‘future.no_silent_downcasting’, True)`. If the most appropriate type of the array is important, use `infer_objects()` to get it.
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'c1': [True, False, np.nan],
    'c2': [pd.NA, 2, 1]
  })
print(df)
#       c1    c2
# 0   True  <NA>
# 1  False     2
# 2    NaN     1

df.dtypes
# c1    object
# c2    object
# dtype: object

df.fillna(0)
# <ipython-input-7-0979152f11c1>:1: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
#       c1  c2
# 0   True   0
# 1  False   2
# 2      0   1

df.fillna(0).dtypes
# c1    object
# c2     int64  (downcasting)
# dtype: object

with pd.option_context('future.no_silent_downcasting', True):
    print(df.fillna(0).dtypes)
# c1    object
# c2    object (no downcasting)

with pd.option_context('future.no_silent_downcasting', True):
    print(df.fillna(0).infer_objects().dtypes)
# c1    object
# c2     int64
```

### `to_datetime()`
For safety and clarity, a format should ***always*** be explicitly specified
```python
df = pd.DataFrame({"date": ["2020-01-02", "2020-01-23", np.nan]})
# NA values does not cause error
print(pd.to_datetime(df["date"], errors="raise", format="%Y-%m-%d"))
# 0   2020-01-02
# 1   2020-01-23
# 2          NaT
```


## Joining

### Outer-joining indices and stacking columns with identical names
```python
df1 = pd.DataFrame({'A': [1, 2]}, index=['a', 'b'])
df2 = pd.DataFrame({'A': [5, 6]}, index=["a", "c"])
df3 = pd.DataFrame({'A': [7, 8], 'B': [10, 11]}, index=["a", "c"])
dfs = [df1, df2, df3]
df = pd.concat(dfs, join="outer", axis=1)
print(df)
#      A    A    A     B
# a  1.0  5.0  7.0  10.0
# b  2.0  NaN  NaN   NaN
# c  NaN  6.0  8.0  11.0

print(df["A"])
#      A    A    A
# a  1.0  5.0  7.0
# b  2.0  NaN  NaN
# c  NaN  6.0  8.0
print(df[["A"]])
#      A    A    A
# a  1.0  5.0  7.0
# b  2.0  NaN  NaN
# c  NaN  6.0  8.0
print(df.drop(columns=["A"]))
#       B
# a  10.0
# b   NaN
# c  11.0
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


## Fancy indexing
### Selecting elements from a data frame using a data frame of `bool`s
```python
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
sel = pd.DataFrame({"A": [False, False, True], "B": [False, True, False], "C": [True, False, True]})
sel1 = pd.DataFrame(
    {"A": [False, False, True], "B": [False, True, False], "C": [True, False, True]}, index=["a", "b", "c"]
)
# Only works as expected when the index and columns labels match
print(df[sel])
#      A    B    C
# 0  NaN  NaN  7.0
# 1  NaN  5.0  NaN
# 2  3.0  NaN  9.0
print(df[sel1])
#     A   B   C
# 0 NaN NaN NaN
# 1 NaN NaN NaN
# 2 NaN NaN NaN

# Unclear how/why this works
print(df[sel.values])
#    A  B  C
# 0  1  4  7
# 1  2  5  8
# 2  3  6  9
# 2  3  6  9

```