'''
解析暂时出现异常的数据实体类
'''


class ParseErrorClass:

    # 当前 父节点code
    parent_code = ''

    # 当前  父节点区划等级
    parent_level = 0

    # 当前待解析url
    to_parse_url = ''

    # 定义构造方法
    def __init__(self, parent_code, parent_level, to_parse_url):
        self.parent_code = parent_code
        self.parent_level = parent_level
        self.to_parse_url = to_parse_url
