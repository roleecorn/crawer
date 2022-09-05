
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
    #找load more
    try:
        nextpage=driver1.find_element("css selector","div[style=\"text-align: center;\"]")
    except:
        print("nopage")
    time.sleep(5)
    while(True):
        try :
            location=nextpage.location
            js=f"var action=document.documentElement.scrollTop={location['y']-200}" 
            driver1.execute_script(js)   
            print(location)
            time.sleep(3)    
            nextpage.click()
            time.sleep(15)
            try :
                nextpage=driver1.find_element("css selector","div[style=\"text-align: center;\"]")
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
        ###!!!
        imgpath = myhome / "eddiebauer"
        if not imgpath.exists():
            Path(imgpath).mkdir(parents=True, exist_ok=True)
        for afilename in imgfile:
            imgpath= imgpath / afilename
            if not imgpath.exists():
                Path(imgpath).mkdir(parents=True, exist_ok=True)

        # imgpath = myhome / imgfile
        if not imgpath.exists():
            Path(imgpath).mkdir(parents=True, exist_ok=True)
        ###!!!
        urllib.request.urlretrieve(
            src, f"{imgpath.resolve()}/{c}.jpg")
        tmp = cloth(datas)

        tmp.write(datapath)

    driver1.close()

#用來找一個網頁的子分頁
def getcates(url: str):
    dpath = myhome / 'chromedriver'
    # 開啟瀏覽器視窗(Chrome)
    # 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
    s = Service(dpath.resolve())
    driver1 = webdriver.Chrome(service=s)
    driver1.get(url)
    time.sleep(20)
    soup = BeautifulSoup(driver1.page_source, 'html.parser')
    lefts = soup.find_all("div", {"aria-labelledby": "category-head"})
    # 標籤群
    cates = {}
    for left in lefts:
        words = left.text.split(' ')
        if "Category" in words:
            reso = left.find_all("li", {'class': "facet"})
            for res in reso:
                cates[str(res.text)] = {}
    driver1.close()
    return (cates)

def splitword(tmp:list) -> list:
    tmp=tmp[0] 
    tmp=tmp.replace("[","").replace("\'","").replace(" ","").replace("\"","")
    tmp=tmp.split("]")
    tmp=tmp[:-1]
    return tmp
listsite = []
def siteandtag(sites: dict):
    keys = sites.keys()
    for akey in keys:
        if isinstance(sites[akey], dict):
            siteandtag(sites[akey])
        if isinstance(sites[akey], str):
            listsite.append(sites[akey])

datapath = myhome / 'test.csv'
with open(datapath.resolve(), mode='w', encoding='big5') as f:
    f.write("標題,圖片編號,價格低點,價格高點,顏色數,部位,性別,製造商\n")
#廢代碼
def ignore():
# allpage = {
#     'women': 'https://www.eddiebauer.com/c/20094/women?cm_sp=topnav_w_featured_viewall',
#     'men': 'https://www.eddiebauer.com/c/20001/men?cm_sp=topnav_m_featured_viewall',
#     'kids': 'https://www.eddiebauer.com/c/20082/kids?cm_sp=topnav_k_featured_viewall',
#     'other': 'https://www.eddiebauer.com/s/outerwear?keyword=outerwear&cm_sp=topnav_o_featured_viewall',
#     'gear': 'https://www.eddiebauer.com/c/20070/gear?cm_sp=topnav_g_featured_viewall',
# }
# allpage=[women,men,kids,other,gear]
# toppage={}
# for apage in allpage.keys():
#     toppage[apage]=getcates(url=allpage[apage])
#     if toppage[apage]=={}:
#         toppage[apage]=allpage[apage]
    pass

site = myhome / 'site.json'

with open(site.resolve(), newline='', encoding='UTF-8') as jsonfile:
    sites = json.load(jsonfile)
    jsonfile.close()

siteandtag(sites=sites)
a = find_path(sites)
for asite in listsite:
    imgp = a.the_value_path(asite)
    imgp=splitword(imgp)
    craw(
        url=asite,gender="women",
        imgfile=imgp,
        feature="test",
        datapath=datapath
        )

    
