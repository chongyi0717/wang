from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

from datetime import datetime

USERNAME = '93281049'
PASSWORD = '93281049'

chrome_options = Options()
# chrome_options.add_argument("--mute-audio")  # 将浏览器静音
chrome_options.add_experimental_option("detach", True)  # 当程序结束时，浏览器不会关闭

# -----如果咋们的linux系统没有安装桌面，下面两句一定要有哦，必须开启无界面浏览器-------
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# ------------------------------------------------------------------------
service = Service(executable_path='./chromedriver.exe')
browser = webdriver.Chrome(options=chrome_options,service=service)
browser.get('https://retailer.sportslottery.com.tw/Account/Login?ReturnUrl=%2F')
id=browser.find_element(By.CSS_SELECTOR,'input#LoginInput_UserNameOrEmailAddress.form-control')
password=browser.find_element(By.CSS_SELECTOR,'input#LoginInput_Password.form-control')
id.send_keys(USERNAME)
password.send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'button.btn-lg.mt-3.btn.btn-primary').click()
browser.get('https://retailer.sportslottery.com.tw/Reward')
table= browser.find_element(By.ID,'rewardDaily')
time.sleep(2)
button = table.find_element(By.TAG_NAME,'a')
button.click()


select = Select(browser.find_element(By.ID,'Day'))
days=[i.get_attribute('innerHTML') for i in select.options][1:]
day1 = '2024-06-01'
day2 = '2024-08-13'
start_date = datetime.strptime(day1, '%Y-%m-%d')
end_date = datetime.strptime(day2, '%Y-%m-%d')

# 保留在日期范围内的日期
days = [day for day in days if start_date <= datetime.strptime(day, '%Y-%m-%d') <= end_date]
data=[]

select_length = Select(browser.find_element(By.NAME,'memberDailyBettingTable_length'))
select_length.select_by_value('800')
table = browser.find_element(By.ID,'memberDailyBettingTable')

try:
    for day in days:    
        page = 0    
        select.select_by_visible_text(day)
        time.sleep(1)
        while True:
            try:
                while True:
                    rows = table.find_elements(By.TAG_NAME,"tr")
                    time.sleep(1)
                    table_data = []
                    for row in rows[2:]:
                        # 找到所有的表格列
                        columns = row.find_elements(By.TAG_NAME,"td")
                        # 提取每列的文本並加入列表
                        # if columns[2].text=='0':
                        #     zero=True
                        #     break
                        row_data = [day]+[column.text for column in columns]
                        table_data.append(row_data)
                    if page == 0 and len(table_data)<800:
                        print(f'{day} has no data')
                        continue
                    next_page=browser.find_element(By.ID,'memberDailyBettingTable_next')
                    
                    is_disabled=next_page.get_attribute('class').find('disabled')!=-1
                    next_page_link = next_page.find_element(By.TAG_NAME,'a')
                    data+=table_data
                    print(f'{day} page {page+1} done')
                    if is_disabled:
                        break
                    else:
                        next_page_link.click()
                        page+=1
                        time.sleep(1)
                    
                break
            except Exception as e:
                print(f'{day} failed, retrying')
except:
    print('Pause')
        
browser.quit()  # 关闭浏览器
import pandas as pd
df=pd.DataFrame(data,columns=['日期','序號','會員代號','投注金額（元）','本店所屬起算日','保障本店所屬到期日'])
df.to_csv(f'output/day_data-{day1}-{day2}.csv',encoding='utf-8-sig',index=False)