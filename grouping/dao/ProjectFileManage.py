from grouping.dao.SqlTool import MysqlManager
from grouping.dao.Item import ProjectFile
import datetime

class ProjectFileManage():

    def __init__(self, db, user, passwd, host='localhost', port=3306, charset='utf8'):
        self.sqlManage = MysqlManager(db, user, passwd, host=host, port=port, charset=charset)


    def uploadFile(self,projectFile):
        '''
        根据projectFile对象内的信息创建一条记录
        主键fid可不指定，自动增长
        :param project:
        :return:
        '''
        try:
            list = []
            list.append(projectFile.toDic())
            return self.sqlManage.insert("project_file",list)

        except Exception as e:
            return 0

    def deleteProjectFile(self,projectFile):
        '''
        根据projectFile对象内信息删除项目 一般为pid
        :param projectFile:
        :return:为删除记录数
        '''
        try:

            return self.sqlManage.delete("project_file", projectFile.toDic())
        except Exception as e:
            return 0


    def findProjectFile(self, projectFile):
        '''
        根据projectFile内的属性查找符合要求的file
        :param projectFile:
        :return: profile_list 列表
        '''



        try:
            projectFile_list = []
            res = self.sqlManage.get('project_file', ["*"], projectFile.toDic())
            for file in res:
                fid , create_time, file_src, file_name, uid = file
                temp = ProjectFile(fid=fid,createTime=create_time,filePath=file_src,fileName=file_name,uid=uid)
                projectFile_list.append(temp)
            return projectFile_list
        except Exception as e:
            return 0

    def updateProjectFile(self,projectFile):
        '''
        一般是根据fid修改名称，根据对象信息修改
        :param projectFile:
        :return: 1成功，0失败
        '''
        try:
            return self.sqlManage.update("project_file",projectFile.toDic(),{"fid":projectFile.fid})
        except Exception as e:
            return 0
        return 1


if __name__ == '__main__':
    m = ProjectFileManage("rdpg",'root','12345')
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # a = ProjectFile(create_time=dt,file_src='123',file_name="123",uid=4)
    # m.uploadFile(a)
    # print(m.deleteProjectFile(ProjectFile(fid=3)))
    res = m.findProjectFile(ProjectFile(file_name='123'))
    # print(res)
    for i in res:
        print(i.toDic())