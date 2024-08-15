import pandas as pd
from datetime import datetime
day1 = '2024-06-01'
day2 = '2024-08-13'
day = pd.read_csv(f'output/day_data-{day1}-{day2}.csv')
day['投注金額（元）'] = day['投注金額（元）'].str.replace(',', '').astype(int)

start_date = datetime.strptime(day1, '%Y-%m-%d')
end_date = datetime.strptime(day2, '%Y-%m-%d')
df_day=pd.DataFrame(day)
positive_amount = df_day['投注金額（元）'] >= 0

df_day['日期'] = pd.to_datetime(df_day['日期'])

df_day = df_day[(df_day['日期'] >= start_date) & (df_day['日期'] <= end_date)]
for index,row in df_day.iterrows():
    if row['投注金額（元）'] < 0:
        print(row['會員代號'],row['投注金額（元）'],row['日期'])
df_day['投注金額'] = df_day[positive_amount].groupby('會員代號')['投注金額（元）'].transform('sum')

df_day.drop('投注金額（元）', axis=1, inplace=True)
df_day = df_day[['會員代號','投注金額']]
df_day.drop_duplicates(subset='會員代號', keep='first', inplace=True)
df_day.sort_values(by='投注金額', ascending=False, inplace=True)
df_day['抽獎機會']=df_day['投注金額']//200+1
sum_lottery = sum(df_day['抽獎機會'])
df_day['中獎機會'] = df_day['抽獎機會']/sum_lottery
df_day.to_excel(f'output/投注金額_每日-{day1}-{day2}.xls',index=False)
df_day.to_csv(f'output/投注金額_每日-{day1}-{day2}.csv',index=False)
