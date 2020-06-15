from grouping.dao.SqlTool import MysqlManager
from grouping.dao.Item import  Scheme
import datetime

class SchemeManage():
    def __init__(self, db, user, passwd, host='localhost', port=3306, charset='utf8'):
        self.sqlManage = MysqlManager(db, user, passwd, host=host, port=port, charset=charset)


    def uploadScheme(self,scheme):
        '''
        根据scheme对象内的信息创建一条记录
        主键id可不指定，自动增长
        :param scheme:
        :return:
        '''
        try:
            list = []
            list.append(scheme.toDic())
            return self.sqlManage.insert("scheme",list)

        except Exception as e:
            return 0

    def deleteScheme(self,scheme):
        '''
        根据scheme对象内信息删除项目 一般为sid
        :param scheme:
        :return:为删除记录数
        '''
        try:

            return self.sqlManage.delete("scheme", scheme.toDic())
        except Exception as e:
            return 0


    def findProjectFile(self, scheme):
        '''
        根据scheme内的属性查找符合要求的file
        :param scheme:
        :return: scheme_list 列表
        '''



        try:
            scheme_list = []
            res = self.sqlManage.get('scheme', ["*"], scheme.toDic())

            for i in res:
                sid , createTime,  pid, data,filePath = i
                temp = Scheme(sid=sid,createTime=createTime,pid=pid,data=data,filePath=filePath)
                scheme_list.append(temp)
            return scheme_list
        except Exception as e:
            return 0



if __name__ == '__main__':
    m = SchemeManage("rdpg","root",'12345')
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # print(m.uploadScheme(Scheme(createTime=dt,pid=666,data="[xdfxx]")))
    # print(m.deleteScheme(Scheme(pid=666,data="[xxx]")))
    res = m.findProjectFile(Scheme(pid=666))
    for i in res:
        print(i.toDic())