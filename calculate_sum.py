import pandas as pd

df=pd.read_csv('data/投注金額.csv')
scratch_sum={}
li=[]
for i,row in df.iterrows():
    if row['會員代號'] not in scratch_sum:
        scratch_sum[row['會員代號']]=int(row['投注金額（元）'].replace(',',''))
        li.append(row['本店所屬起算日'])
    else:
        scratch_sum[row['會員代號']]+=int(row['投注金額（元）'].replace(',',''))
    

df=pd.DataFrame(scratch_sum.items(), columns=['會員代號', '投注金額'])
df['本店所屬起算日']=li
df.to_csv('output/投注金額.csv',encoding='utf-8-sig')
