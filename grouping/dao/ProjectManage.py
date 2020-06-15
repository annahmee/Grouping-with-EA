import datetime
from grouping.dao.SchemeManage import SchemeManage
from grouping.dao.SqlTool import MysqlManager
from grouping.dao.Item import Project,Scheme
# from grouping.dao.


class ProjectManage():


    def __init__(self, db, user, passwd, host='localhost', port=3306, charset='utf8'):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.charset = charset
        self.sqlManage = MysqlManager(db, user, passwd, host='localhost', port=3306, charset='utf8')

    def createPro(self,project):
        '''
        根据project对象内的信息创建一条记录
        主键pid可不指定，自动增长
        :param project:
        :return:
        '''
        try:
            list = []
            list.append(project.toDic())
            return self.sqlManage.insert("project",list)

        except Exception as e:
            return 0

    def deletePro(self,project):
        '''
        根据project对象内信息删除项目 一般为pid
        :param project:
        :return:为删除记录数
        '''
        try:
            return self.sqlManage.delete("project",project.toDic())
        except Exception as e:
            return 0

    def findPro(self,project):
        '''
        根据project内的属性查找符合要求的pro

        :param project:
        :return: pro_list 列表
        '''



        try:
            pro_list = []
            res = self.sqlManage.get('project',["*"],project.toDic())
            for pro in res:
                pid , uid , projectName , createTime , fid , school , college , year , major , algorithm , groupNum ,teacherNum, together , notTogether = pro
                temp = Project(pid,uid,projectName,createTime,fid,school,college,year,major,algorithm,groupNum ,teacherNum, together , notTogether)
                pro_list.append(temp)
            return pro_list
        except Exception as e:
            return 0

    def updatePro(self,project,change):
        '''
        根据pro对应的pid进行修改
        if：
            原来的project中的所选分组、所选算法、相同答辩教师组与不同答辩教师组改变、则将scheme表对应的记录删除,change=1
        eles:
            不涉及scheme表改变，change=0
        :param project:
        :return:(a,b) a为改记录是否修改成功，b为对应scheme删除条数
        '''
        try:

            a = self.sqlManage.update("project", project, {"pid": project.get('pid')})
            b = 0


            if change:
                man = SchemeManage(self.db,self.user,self.passwd)
                man.deleteScheme(Scheme(pid=project.get('pid')))


            return (a,b)
        except Exception as e:
            return 0;



if __name__ == '__main__':
    pm = ProjectManage("rdpg","root",'123456')
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #pro = Project(uid=5,createTime=dt,fid=1,pid=1,school="fzuuuuu",algorithm="de",group_num=4,pname='测试1',major='计算机',year='2020',college='sj')
    #print(pm.createPro(pro))
    # print(pm.deletePro(Project(uid = 3)))
    #a = pm.findPro(Project(uid=5))
    #print(a[0].toDic())
    # a[0].createTime = None
    print(pm.deletePro(Project(pid='10')))
    # res = pm.findPro(Project(uid=4))
    # for i in res:
    #     print(i.toDic())

    # print(res[0].toDic())

    # pm.updatePro(Project(pid=9,pname="613"),0)
    #pm.updatePro(Project(pid=9,algorithm="ga"),1)