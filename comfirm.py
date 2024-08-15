import pandas as pd
df=pd.read_csv('output/投注金額.csv')
df_reply=pd.read_csv('data/活動報名.csv')
# df=df[['會員代號','本店所屬起算日']]
date_format1 = '%Y/%m/%d'
date_format2 = '%Y-%m-%d'
last_char=[i[0] for i in df['會員代號']]
date_website=[pd.to_datetime(i, format=date_format1) for i in df['本店所屬起算日']]
df['本店所屬起算日']=date_website

li=[]
for index,row in df_reply.iterrows():
    buff=0
    if not pd.isna(row['姓名']) and not pd.isna(row['时间戳记']):
        for jndex,jow in df.iterrows():
            if row['姓名'][-1] == jow['會員代號'][0]\
            and pd.to_datetime(row['时间戳记'].split(' ')[0],format=date_format2)==jow['本店所屬起算日']:

                buff=1
                row['網站中代號']=jow['會員代號']
                row['投注金額']=jow['投注金額']
                print(row)
                li.append(row)
                break
            else:
                pass
    else:
        pass
print(li)
df=pd.concat(li,axis=1).T
# print(df)
df.to_csv('output/checked.csv',encoding='utf-8-sig')

