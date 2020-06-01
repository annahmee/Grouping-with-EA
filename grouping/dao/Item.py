class User():
    def __init__(self,uid=None,userName=None,password=None,email=None):
        if uid is not None:
            self.uid = uid
        else:
            self.uid = None
        self.userName = userName
        self.passWord = password
        self.email = email
    def toDic(self):
        dic = {}
        if self.uid:
            dic['uid']=self.uid
        if self.userName:
            dic['userName']=self.userName
        if self.passWord:
            dic['password']=self.passWord
        if self.email:
            dic['email']=self.email
        return dic
    def print(self):
        print("uid:{}---userName:{}---passWord:{}---email:{}".format(self.uid,self.userName,self.passWord,self.email))
    def getUsername(self):
        return self.userName
    def getUid(self):
        return self.uid
    def getPassword(self):
        return self.passWord
    def getEmail(self):
        return  self.email
