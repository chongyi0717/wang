import pandas as pd

# 示例数据框
data1 = {'A': [1, 2, 3, 4],
         'B': [5, 6, 7, 8]}
data2 = {'A': [1, 2, 3],
         'B': [5, 6, 7]}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# 比较两个数据框的值，找出哪些行的值在第一个数据框中比第二个数据框少
less_values = df1.lt(df2)

# 筛选出第一个数据框中的相应行
less_values_in_df1 = df1[less_values.any(axis=1)]
print("df1中比df2少的行：")
print(less_values_in_df1)
