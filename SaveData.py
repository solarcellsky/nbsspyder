'''
国家统计局 数据入库存储
'''
from Util.DataBaseUtil import DataBaseUtil


#批量插入
def nbsDataToSaveBatch(tar_obj_set):
    #参数处理成列表套元组的形式
    tar_list = list()  #或  tar_list = []
    for tar_obj in tar_obj_set:
        tar_tuple = (tar_obj.nbs_code, tar_obj.nbs_parent_code,
                     tar_obj.nbs_level, tar_obj.nbs_name,
                     tar_obj.nbs_town_country_code)
        tar_list.append(tar_tuple)
    # 数据库信息
    dataBaseUtilObj = DataBaseUtil()
    host_param = 'xxxx.xx.xx.xx'
    unix_socket_param = ''
    user_param = 'root'
    passwd_param = 'xxxxx'
    db_param = 'qqq'
    conn = dataBaseUtilObj.getConnObj(host_param, unix_socket_param,
                                      user_param, passwd_param, db_param)
    cur = dataBaseUtilObj.getCurObj(conn)

    #执行sql
    cur.execute("use qqq")
    # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
    '''
    另外，针对executemany
    execute(sql) : 接受一条语句从而执行
    executemany(templet,args)：能同时执行多条语句，执行同样多的语句可比execute()快很多，强烈建议执行多条语句时使用executemany
        templet : sql模板字符串,　 例如 ‘insert into table(id,name,age) values(%s,%s,%s)’
        args: 模板字符串中的参数，是一个list，在list中的每一个元素必须是元组！！！ 　例如： [(1,‘mike’),(2,‘jordan’),(3,‘james’),(4,‘rose’)]
    '''
    cur.executemany(
        'insert into nbs_region(nbs_code,nbs_parent_code,nbs_level,nbs_name,nbs_town_country_code) values (%s,%s,%s,%s,%s)',
        tar_list)
    conn.commit()
    cur.close()
    conn.close()
