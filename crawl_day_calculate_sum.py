import pandas as pd
from datetime import datetime

day1 = '2024-06-01'
day2 = '2024-08-13'
day = pd.read_csv(f'output/day_data-{day1}-{day2}.csv')
day['投注金額（元）'] = day['投注金額（元）'].str.replace(',', '').astype(int)

start_date = datetime.strptime(day1, '%Y-%m-%d')
end_date = datetime.strptime(day2, '%Y-%m-%d')
df_day = pd.DataFrame(day)

# 过滤正的投注金额
positive_amount = df_day['投注金額（元）'] > 0

# 转换日期列并提取月份信息
df_day['日期'] = pd.to_datetime(df_day['日期'])
df_day['月份'] = df_day['日期'].dt.to_period('M')

# 过滤日期范围内的数据
df_day = df_day[(df_day['日期'] >= start_date) & (df_day['日期'] <= end_date)]

# 打印投注金额为负的记录
for index, row in df_day.iterrows():
    if row['投注金額（元）'] < 0:
        print(row['會員代號'], row['投注金額（元）'], row['日期'])

# 计算每个月份的会员总投注金额
df_day['投注金額'] = df_day.groupby(['會員代號', '月份'])['投注金額（元）'].transform('sum')

# 找出每个会员在每个月份的非零投注金额的日
non_zero_days = df_day[positive_amount].groupby(['會員代號', '月份'])['日期'].apply(lambda x: ','.join(x.dt.day.astype(str))).reset_index()
non_zero_days.rename(columns={'日期': '非零投注日'}, inplace=True)

# 合并非零投注日到原始数据
df_day = df_day.merge(non_zero_days, on=['會員代號', '月份'], how='left')

# 删除不再需要的列
df_day.drop('投注金額（元）', axis=1, inplace=True)

# 保留会员代号、月份、投注金额和非零投注日列
df_day = df_day[['會員代號', '月份', '投注金額', '非零投注日']]

# 去重以确保每个会员在每个月只保留一条记录
df_day.drop_duplicates(subset=['會員代號', '月份'], keep='first', inplace=True)

# 按月份和投注金额排序
df_day.sort_values(by=['月份', '投注金額'], ascending=[True, False], inplace=True)

# 计算抽奖机会和中奖机会
df_day['抽獎機會'] = df_day['投注金額'] // 200 + 1
sum_lottery = sum(df_day['抽獎機會'])
df_day['中獎機會'] = df_day['抽獎機會'] / sum_lottery

# 保存结果
df_day.to_excel(f'output/投注金額_每日-{day1}-{day2}.xls', index=False)
df_day.to_csv(f'output/投注金額_每日-{day1}-{day2}.csv', index=False)
