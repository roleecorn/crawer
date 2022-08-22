
from selenium import webdriver
import time
import sys
from selenium.webdriver.chrome.service import Service
# 開啟瀏覽器視窗(Chrome)
# 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
urls=["https://www.eddiebauer.com/",'https://jettylife.com']
s=Service("./chromedriver")
driver1 = webdriver.Chrome(service=s)
# driver2 = webdriver.Chrome(service=s)

driver1.get(urls[0])
time.sleep(10)


# driver2.get(urls[1])
# time.sleep(30)
# for i in len(range(urls)):
#     tit=drivers[i].execute_script('return document.title;')
#     print(tit)
#     time.sleep(3)
buttons = driver1.find_elements("xpath",'/html/body/div[3]/div/header/div[3]/div/div/div/div[2]/ul/li')
for botton in buttons:
    print(botton.accessible_name)
