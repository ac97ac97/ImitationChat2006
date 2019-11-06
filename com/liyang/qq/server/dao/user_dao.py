#用户管理DAO
from com.liyang.qq.server.dao.base_dao import BaseDao

class UserDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findbyid(self, userid):
        #根据用户的id查询用户的相关信息
        try:
            #创建游标对象
            with self.conn.cursor() as cursor:
                sql = 'select  user_id,user_pwd,user_name,user_icon from  users  where  user_id=%s'
                cursor.execute(sql, userid)
                row = cursor.fetchone()
                if row is not None:
                    user = {}
                    user['user_id'] = row[0]
                    user['user_pwd'] = row[1]
                    user['user_name'] = row[2]
                    user['user_icon'] = row[3]
                    return user
        finally:
            self.close()


    def findfriends(self, userid):
        #根据用户的id查询用户好友信息
        users=[]
        try:
            #创建游标对象
            with self.conn.cursor() as cursor:
                sql = 'select  user_id,user_pwd,user_name,user_icon from  users  where  user_id IN (select user_id2 as user_id from friends where user_id1 = %s) or user_id IN (select user_id1 as user_id from friends where user_id2=%s)'
                cursor.execute(sql, (userid,userid))
                result_set=cursor.fetchall()
                for row in result_set:
                    user = {}
                    user['user_id'] = row[0]
                    user['user_pwd'] = row[1]
                    user['user_name'] = row[2]
                    user['user_icon'] = row[3]
                    users.append(user)
        finally:
            self.close()

        return users
