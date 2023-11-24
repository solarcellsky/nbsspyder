'''
国家统计局行政区划实体类
'''


class NbsRegionDTO:

    # 统计用区划代码
    nbs_code = ''

    #'国家统计局父级统计用区划code',
    nbs_parent_code = ''

    # '国家统计局区域层级', 1 - 5
    nbs_level = 0

    # '国家统计局名称',
    nbs_name = ''

    # 城乡分类代码  五级才有数据
    nbs_town_country_code = ''

    #定义构造方法
    def __init__(self, nbs_code, nbs_parent_code, nbs_level, nbs_name,
                 nbs_town_country_code):
        self.nbs_code = nbs_code
        self.nbs_parent_code = nbs_parent_code
        self.nbs_level = nbs_level
        self.nbs_name = nbs_name
        self.nbs_town_country_code = nbs_town_country_code
