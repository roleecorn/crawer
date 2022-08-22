from pathlib import Path
class cloth:
    #打包每件衣服的資料
    def __init__(self,datas:dict) -> None:
        keys=datas.keys()
        for akey in keys:
            if "," in str(datas[akey]):
                print(akey)
                val=datas[akey]
                newval=val.replace(",","")
                datas[akey]=newval
        self.name     = datas["name"]     if ("name" in keys)     else "nodata"
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
        with open(str(path),mode='a+',encoding='Big5') as f:
            f.write(f"\
{self.name},\
{self.oriprice},\
{self.price},\
{self.star},\
{self.color },\
{self.feature},\
{self.sex},\
{self.facturer}\n")
#測試
if __name__=="__main__":
    cdata={"name":"op","price":123,"color":'gr,een',"sex":'woman',"star":4.5,"oriprice":145}
    cloth1=cloth(cdata)
    print(cloth1.discount())
    p = Path('/Users/sunifu/Documents/python/crawer/class/test.csv')
    cloth1.write(p)