
from test1 import t
from selenium.webdriver.common.action_chains import ActionChains
from classes.findpath import find_path
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from classes.cloth import cloth
import urllib.request
import json
myhome = Path.cwd()


def craw(url: str, gender: str, imgfile: list, feature: str, datapath: Path):
    print('執行開始')
    dpath = myhome / 'chromedriver'
    # 開啟瀏覽器視窗(Chrome)
    # 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
    s = Service(dpath.resolve())
    driver1 = webdriver.Chrome(service=s)
    driver1.get(url)
    time.sleep(10)

    c = 0
    # 找load more
    try:
        nextpage = driver1.find_element(
            "css selector", "div[style=\"text-align: center;\"]")
    except:
        print("nopage")
    time.sleep(5)
    while (True):
        try:
            location = nextpage.location
            js = f"var action=document.documentElement.scrollTop={location['y']-200}"
            driver1.execute_script(js)
            print(location)
            time.sleep(3)
            nextpage.click()
            time.sleep(15)
            try:
                nextpage = driver1.find_element(
                    "css selector", "div[style=\"text-align: center;\"]")
            except:
                print("nomore")
                break

            time.sleep(3)
        except:
            print("nomore")
            break

    buttons = driver1.find_elements("class name", "tile_wrapper_outer")
    for botton in buttons:
        c = c+1
        src = botton.find_element("tag name", "img").get_attribute("src")
        title = botton.find_element("class name", "title").text
        colors = botton.find_element("class name", "color_label").text
        price = botton.find_element(
            "class name", "visually_hidden").find_element("xpath", "..").text
        price = price.split("$")
        colors = colors.split(" ")[0]
        if price[-1] != price[1]:
            price[1] = price[1][:-1]
        datas = {
            "name": str(title),
            'color': colors,
            "sex": gender,
            'feature': feature,
            "price": price[-1],
            "oriprice": price[1],
            'imgcode': c}
        # !!!
        imgpath = myhome / "eddiebauer"
        if not imgpath.exists():
            Path(imgpath).mkdir(parents=True, exist_ok=True)
        for afilename in imgfile:
            imgpath = imgpath / afilename
            if not imgpath.exists():
                Path(imgpath).mkdir(parents=True, exist_ok=True)

        # imgpath = myhome / imgfile
        if not imgpath.exists():
            Path(imgpath).mkdir(parents=True, exist_ok=True)
        # !!!
        urllib.request.urlretrieve(
            src, f"{imgpath.resolve()}/{c}.jpg")
        tmp = cloth(datas)

        tmp.write(datapath)

    driver1.close()


url = "https://www.tom-tailor.eu/men/clothing/shirts"
print('執行開始')
dpath = myhome / 'chromedriver'
# 開啟瀏覽器視窗(Chrome)
# 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
s = Service(dpath.resolve())
driver1 = webdriver.Chrome(service=s)
driver1.get(url)
# driver1.delete_all_cookies()
# for i in t:

#     driver1.add_cookie(cookie_dict=i)
# time.sleep(10)
# driver1.refresh()
time.sleep(10)

buttons = driver1.find_elements("class name", "sc-gsDKAQ bDvhlO")
print(len(buttons))
for button in buttons:
    print(button.text)
print(driver1.get_cookies())
# button.click()
time.sleep(10)
driver1.close()
