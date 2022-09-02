def formatbig5(name:str) -> str :
    name=name.encode(encoding="big5",errors='ignore')
    name=name.decode(encoding="big5")
    return name