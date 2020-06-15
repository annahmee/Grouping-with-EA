class User():
    def __init__(self,uid=None,userName=None,password=None,email=None):
        if uid is not None:
            self.uid = uid
        else:
            self.uid = None
        self.userName = userName
        self.password = password
        self.email = email
    def toDic(self):
        dic = {}
        for key,value in vars(self).items():
            if value:
                dic[key] = value
        return dic
    def print(self):
        print("uid:{}---userName:{}---passWord:{}---email:{}".format(self.uid,self.userName,self.password,self.email))
    def getUsername(self):
        return self.userName
    def getUid(self):
        return self.uid
    def getPassword(self):
        return self.password
    def getEmail(self):
        return  self.email


class Project():

    def __init__(self,pid=None,uid=None,projectName=None,createTime=None,fid=None,school=None,college=None,year=None,major=None,algorithm=None,groupNum=None,teacherNum=None,together=None,notTogether=None):
        self.pid = pid
        self.uid = uid
        self.projectName = projectName
        self.createTime = createTime
        self.fid = fid
        self.school = school
        self.college = college
        self.year = year
        self.major = major
        self.algorithm = algorithm
        self.groupNum = groupNum
        self.teacherNum=teacherNum
        self.together = together
        self.notTogether = notTogether

    def toDic(self):
        dic = {}
        for key,value in vars(self).items():
            if value:
                dic[key] = value
        return dic

class ProjectFile():
    def __init__(self,fid=None,createTime=None,filePath=None,fileName=None,uid=None):
        self.fid = fid
        self.createTime = createTime
        self.filePath = filePath
        self.fileName = fileName
        self.uid = uid

    def toDic(self):
        dic = {}
        for key, value in vars(self).items():
            if value:
                dic[key] = value
        return dic

class Scheme():

    def __init__(self,sid=None, createTime=None,  pid=None, data=None,filePath=None):
        self.sid=sid
        self.createTime=createTime
        self.pid = pid
        self.data = data
        self.filePath=filePath

    def toDic(self):
        dic = {}
        for key, value in vars(self).items():
            if value:
                dic[key] = value
        return dic