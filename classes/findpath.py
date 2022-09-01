class find_path(object):
    def __init__(self, target):
        self.target = target  # 查詢的字典/列表

    def find_the_key(self, target, key, path_list=None):
        '''
        輸入：只是用來查詢目的key所在的dict；輸出：然後以dict作爲value 調用find_dict 查詢
        '''
        if isinstance(target, dict):  # 判斷了它是字典
            dict1 = target.copy()
            for k, v in dict1.items():
                if str(key) == str(k):
                    path = str([k])
                    self.find_dict_path(self.target, dict1, path, path_list)
                else:
                    # 此key不是所查找的，那麼調用自身遍歷這個v，看所找的key是否在裏面
                    self.find_the_key(v, key, path_list)

        elif isinstance(target, (list, tuple)):  # 判斷了它是列表
            list1 = target.copy()
            for i in list1:
                self.find_the_key(i, key, path_list)  # 調用自身遍歷這個I，看所找的key是否在裏面

    def find_in_value(self, target, value, path='', path_list=None):
        '''查詢的value只能是str/int，遍歷字典跟列表，
        如果裏面的元素是str，那麼就判斷該元素是否包含value(包含匹配)，
                           如果是是的話，那麼就把當前的元素所在的dict/list當作關鍵字用find_dict查詢
        如果元素不是str，那麼繼續循環自身'''
        if isinstance(target, dict):  # 判斷了它是字典
            dict1 = target.copy()
            for k, v in dict1.items():
                if isinstance(v, (str, int)):  # 當字典的v是str時才進一步判斷
                    if str(value) in str(v):  # 如果某個value就是要找的，就把k放進path，
                        path1 = path
                        # 把此v所在的dict作爲所查找的value，調用find_dict得到路徑path
                        path1 = str([k]) + path1
                        self.find_dict_path(
                            self.target, dict1, path1, path_list)
                else:
                    # 此v可能是dict/list，調用自身確認裏面是否有所查詢的value
                    self.find_in_value(v, value, path, path_list)

        elif isinstance(target, (list, tuple)):  # 判斷了它是列表
            list1 = target.copy()
            for i in list1:
                if isinstance(i, (str, int)):  # 當列表的i是str時才進一步判斷
                    if str(value) in str(i):
                        path1 = path
                        posi = list1.index(i)
                        # 把此i所在的list作爲所查找的value，調用find_dict得到路徑path
                        path1 = '[%s]' % posi + path1
                        self.find_dict_path(
                            self.target, list1, path1, path_list)
                else:
                    # 此i可能是dict/list，調用自身確認裏面是否有所查詢的value
                    self.find_in_value(i, value, path, path_list)

    def find_the_value(self, target, value, path='', path_list=None):
        '''上同，差別在於 這個是”完全匹配“'''
        if isinstance(target, dict):
            dict1 = target.copy()
            for k, v in dict1.items():
                if isinstance(v, (str, int)):
                    if str(value) == str(v):  # 必須完全相同
                        path1 = path
                        path1 = str([k]) + path1
                        self.find_dict_path(
                            self.target, dict1, path1, path_list)
                else:
                    self.find_the_value(v, value, path, path_list)

        elif isinstance(target, (list, tuple)):
            list1 = target.copy()
            for i in list1:  # 遍歷列表
                if isinstance(i, (str, int)):
                    if str(value) == str(i):  # 必須完全相同
                        path1 = path
                        posi = list1.index(i)
                        path1 = '[%s]' % posi + path1
                        self.find_dict_path(
                            self.target, list1, path1, path_list)
                else:
                    self.find_the_value(i, value, path, path_list)

    def find_dict_path(self, target, value, path='', path_list=None):
        '''查詢的value只能是dict/list整體，str類型不能再這裏驗證，這是最後步驟'''

        if self.target == value:
            path_list.append(path) if path not in path_list else None

        elif isinstance(target, dict):  # 判斷了它是字典
            dict1 = target.copy()
            for k, v in dict1.items():
                if isinstance(v, (list, tuple, dict)):  # 只有當v是dict/list時才判斷
                    if value == v:  # 如果某個value就是要找的，就把k放進path，然後把這個字典作爲新的value循環
                        path1 = path
                        path1 = str([k])+path1
                        self.find_dict_path(
                            self.target, dict1, path1, path_list)
                    else:
                        # 此值v不是要找的，那麼遍歷這個v，看所找的value是否在裏面
                        self.find_dict_path(v, value, path, path_list)

        elif isinstance(target, (list, tuple)):  # 判斷了它是列表
            list1 = target.copy()
            for i in list1:  # 遍歷列表
                if isinstance(i, (list, tuple, dict)):  # 只有當v是dict/list時才判斷
                    if i == value:  # 如果某個元素就是要找的，就把posi放進path，然後把這個列表作爲新的value循環
                        path1 = path
                        posi = list1.index(i)
                        path1 = '[%s]' % posi + path1
                        self.find_dict_path(
                            self.target, list1, path1, path_list)
                    else:
                        # 此元素不是要找的，那麼遍歷這個i，看所找的value是否在裏面
                        self.find_dict_path(i, value, path, path_list)

    def in_value_path(self, value):
        '''包含匹配value'''
        path_list = []
        self.find_in_value(self.target, value, path_list=path_list)
        return path_list

    def the_value_path(self, value):
        '''完全匹配value'''
        path_list = []
        self.find_the_value(self.target, value, path_list=path_list)
        return path_list

    def the_key_path(self, value):
        '''只查找key'''
        path_list = []
        self.find_the_key(self.target, value, path_list=path_list)
        return path_list

# a=find_path(dict1)
# in_value_path=a.in_value_path('基礎傷害') #包含匹配，只要dict/list的元素中包含這個str，就能得到對應的path
# the_value_path=a.the_value_path('40')   #完全匹配，只要dict/list的元素中就是這個 str，就能得到對應的path
# the_key_path=a.the_key_path('description')#只搜索dict的key，相同的就會得到對應的path
# print(in_value_path)
# print(the_key_path)
# print(the_value_path)
