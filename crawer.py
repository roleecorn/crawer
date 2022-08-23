
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from pathlib import Path
from classes.cloth import cloth
import urllib.request
myhome=Path.cwd()
print(myhome.resolve())
def craw(url:str,gender:str,imgfile:str,feature:str,datapath:Path):
    print('執行開始')
    dpath= myhome / 'chromedriver'
    
    
    # 開啟瀏覽器視窗(Chrome)
    # 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
    
    
    s=Service(dpath.resolve())

    driver1 = webdriver.Chrome(service=s)
    print('抓驅動')
    driver1.get(url)
    time.sleep(10)

    buttons = driver1.find_elements("class name","tile_wrapper_outer")
    
    c=0
    for botton in buttons:
        c=c+1
        src=botton.find_element("tag name","img" ).get_attribute("src")
        title=botton.find_element("class name","title" ).text
        colors=botton.find_element("class name","color_label" ).text
        price=botton.find_element("class name","visually_hidden").find_element("xpath","..").text
        price=price.split("$")
        colors=colors.split(" ")[0]
        if price[-1]!=price[1]:
            price[1]=price[1][:-1]
        datas={
        "name":str(title),
        'color':colors,
        "sex":gender,
        'feature':feature,
        "price":price[-1],
        "oriprice":price[1],
        'imgcode':c}
        imgpath= myhome / imgfile 
        if not imgpath.exists():
            print("nedug")
            Path(imgpath).mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(src,f"/Users/sunifu/Documents/python/crawer/{imgfile}/{c}.jpg")
        tmp=cloth(datas)
        
        tmp.write(datapath)
        
    print(c)
    driver1.close()
print('城市開始')
datapath= myhome / 'test.csv'
with open(datapath.resolve(),mode='w',encoding='big5') as f:
    f.write("標題,圖片編號,價格低點,價格高點,顏色數,部位,性別,製造商\n")
print('寫入開頭')
url='https://www.eddiebauer.com/c/20151/womens-shirts?cm_sp=topnav_w_tops_shirts'
print('執行前')
craw(
url=url,
gender="woman",
feature="shirt",
imgfile="shirt",
datapath=datapath
)
