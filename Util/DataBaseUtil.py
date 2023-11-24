import pymysql
'''
数据库操作工具类
'''


class DataBaseUtil:
    '''获取连接对象'''

    def getConnObj(self, host_param, unix_socket_param, user_param,
                   passwd_param, db_param):
        conn = pymysql.connect(host=host_param,
                               unix_socket=unix_socket_param,
                               user=user_param,
                               passwd=passwd_param,
                               db=db_param,
                               charset='utf8')
        return conn

    '''
    获取光标对象
    参数：连接对象conn
    '''

    def getCurObj(self, conn):
        return conn.cursor()
