from pathlib import Path
from classes.big5 import formatbig5
class cloth:
    #打包每件衣服的資料
    def __init__(self,datas:dict) -> None:
        keys=datas.keys()
        # tmp1=datas["name"].encode(encoding="big5",errors='ignore')
        # datas["name"]=tmp1.decode(encoding="big5")
        datas["name"]=formatbig5(datas["name"])
        for akey in keys:
            if "," in str(datas[akey]):
                print(akey)
                val=datas[akey]
                newval=val.replace(",","")
                datas[akey]=newval
        self.name     = datas["name"]     if ("name" in keys)     else "nodata"
        self.imgcode  = datas["imgcode"]  if ("imgcode" in keys)  else -1
        self.price    = datas["price"]    if ("price" in keys)    else -1
        self.star     = datas["star"]     if ("star" in keys)     else -1
        self.oriprice = datas["oriprice"] if ("oriprice" in keys) else self.price
        self.color    = datas["color"]    if ("color" in keys)    else "nodata"
        self.feature  = datas["feature"]  if ("feature" in keys)  else "nodata"
        self.sex      = datas["sex"]      if ("sex" in keys)      else "nodata"
        self.facturer = datas["facturer"] if ("facturer" in keys) else "nodata"
    #計算打折
    def discount(self) -> int:
        return (self.oriprice-self.price)
    #寫入檔案
    def write(self,path:Path) -> None:
        
        with open(str(path),mode='a+',encoding='big5') as f:
            f.write(f"\
{self.name},\
{self.imgcode},\
{self.oriprice},\
{self.price},\
{self.color },\
{self.feature},\
{self.sex},\
{self.facturer}\n")
#測試
if __name__=="__main__":
    cdata={"name":"op","price":123,"color":'gr,een',"sex":'woman',"star":4.5,"oriprice":145}
    cloth1=cloth(cdata)
    print(cloth1.discount())
    p = Path('.')
    cloth1.write(p)