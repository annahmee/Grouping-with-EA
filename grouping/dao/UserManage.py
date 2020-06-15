
from grouping.dao.SqlTool import MysqlManager
from grouping.dao.Item import User


class UserManage():


    def __init__(self, db, user, passwd, host='localhost', port=3306, charset='utf8'):
        self.sqlManage = MysqlManager(db, user, passwd, host='localhost', port=3306, charset='utf8')


    def register(self,user):
        '''
        注册用户
        user：用户对象
        :return 0:数据库有该用户名 创建失败
                1：成功
        '''
        try:
            count = len(self.findUserByUserInfo(User(userName=user.getUsername())))
            if count != 0:
                return 0
            else:
                list = []
                list.append(user.toDic())
                return self.sqlManage.insert("user", list)

        except Exception as e:
            return 0



    def findUserByUserInfo(self,user):
        '''
        根据user里的信息查询Uid
        :param user
        :return: user tuple
        '''
        try:
            return self.sqlManage.get('user', ['*'], user.toDic())
        except Exception as e:
            return 0


    def findUserByUid(self,uid):
        '''
        根据uid来查找用户
        :param uid
        :return: User
        '''
        try:
            temp = self.sqlManage.get("user", ["*"], {"uid": uid}, get_one=True)

            if temp:
                user = User(temp[0],temp[1], temp[2], temp[3])
                return user
            else:
                return 0
        except Exception as e:
            return  0

    def updateUserByUserInfo(self,user):
        '''
        根据user里面的uid以及里面的属性值来进行更新操作
        :param user:
        :return: 0:失败
                1：成功
        '''
        try:
            return self.sqlManage.update("user",user.toDic(),condition={'uid':user.getUid()})
        except Exception as e:
            return 0
        return 1

    def deleteUserByUid(self,uid):
        '''
        根据uid注销用户
        :param uid:
        :return:
        '''
        try:
            return self.sqlManage.delete("user",{'uid':uid})
        except Exception as e:
            return 0
        return 1

if __name__ == '__main__':
    um = UserManage("rdpg","root",'123456')
    # print(um.findUidByUser(User(username="czh5")))
    user = User('123',"czh6","12345","123@qq.com")

    # um.findUserByUid(2).print()
    # user = User(4,"cccccc","1111",'dsaf')
    # print(um.updateUserByUserInfo(user))
    print(um.register(user))

