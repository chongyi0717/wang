from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from tqdm import tqdm
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
# browser.find_element(By.ID,'loginView_A4').click()
browser.get('https://retailer.sportslottery.com.tw/MemberDailyBettingByMonth')



select = Select(browser.find_element(By.ID,'Month'))
months=[i.get_attribute('innerHTML') for i in select.options]
data=[]

table = browser.find_element(By.ID,'monthlyDetailTable')

try:
    for month in tqdm(months):
        
        
        select.select_by_visible_text(month)
        time.sleep(1)
        
        try:
            while True:
                
                rows = table.find_elements(By.TAG_NAME,"tr")

                table_data = []
                for row in rows[2:]:
                    # 找到所有的表格列
                    columns = row.find_elements(By.TAG_NAME,"td")
                    # 提取每列的文本並加入列表
                    
                    row_data = [month]+[column.text for column in columns]
                    table_data.append(row_data)
                next_page=browser.find_element(By.ID,'monthlyDetailTable_next')
                
                is_disabled=next_page.get_attribute('disabled')
                
                data+=table_data
                if is_disabled :
                    
                    break
                else:
                    next_page_link = next_page.find_element(By.TAG_NAME,'a')
                    next_page_link.click()
                    time.sleep(1)
        except Exception as e:
            print(f'{e},{month} failed')
except:
    print('Pause')
        
    



browser.quit()  # 关闭浏览器
import pandas as pd
df=pd.DataFrame(data,columns=['日期','序號','會員代號','投注金額（元）'])
df.to_csv('output/month_data.csv',encoding='utf-8-sig',index=False)