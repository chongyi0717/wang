import pandas as pd
import json
df=pd.read_csv('data/活動報名.csv',encoding='utf-8')
duplicate_names = df[df.duplicated(subset=['姓名'], keep='first')]
if not duplicate_names.empty:
    print(f"以下姓名有重複，共有{len(duplicate_names)}筆重複：")
    print(duplicate_names)
else:
    print("所有姓名都是獨一無二的。")

print('處理後:')
filter_column=['身份證統一編號','行動電話號碼']
for i in filter_column:
    df = df[~df.duplicated(subset=[i], keep='first')]
filtered_df=df
duplicate_names = filtered_df[filtered_df.duplicated(subset=['姓名'], keep='first')]
# 如果有重複的姓名，它們將顯示在 duplicate_names 中
if not duplicate_names.empty:
    print("以下姓名有重複：")
    print(duplicate_names.sort_values(by='姓名'))
else:
    print("所有姓名都是獨一無二的。")
filtered_df.to_excel('output/member.xls')
filtered_df.to_csv('output/member.csv',encoding='utf-8-sig')
print(filtered_df['加入的經銷商證號 '].value_counts())
duplicate_names = filtered_df[filtered_df.duplicated(subset=['姓名'], keep=False)]
duplicate_names.sort_values(by='姓名').to_excel('output/duplicate_names.xls')
# # 將資料轉換成 JSON 格式的列表
# member_list = []
# count=0
# for idx, row in filtered_df.iterrows():
#     count+=1
#     member_info = {
#         "id": count,
#         "name": row["姓名"]
#     }
#     member_list.append(member_info)

# # 將 JSON 寫入 JavaScript 檔案
# with open('output/member.js', 'w', encoding='utf-8') as js_file:
#     js_file.write('window.members = ')
#     js_file.write(json.dumps(member_list, ensure_ascii=False, indent=2))



# print(f"已生成 member.js 和member.csv檔案({len(member_list)})")