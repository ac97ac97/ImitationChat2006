"""服务端启动"""
import socket
import logging
import sys
import json
from com.liyang.qq.server.dao.user_dao import UserDao
import traceback as tb

logger = logging.getLogger(__name__)
# 服务端ip
SERVER_IP='127.0.0.1'
# 服务器端口号
SERVER_POST=8888
#操作命令代码
COMMAND_LOGIN=1 #登录名令
COMMAND_LOGOUT=2 #下线命令
COMMAND_SENDMSG=3#发消息命令
COMMAND_REFRESH=4#刷新好友列表
#所有已登录的客户端消息
clientlist=[]

server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP,SERVER_POST))
logger.info('服务端启动，监听自己的端口{0}...'.format(SERVER_POST))

#创建字节序列对象列表，作为接收数据的缓冲区
buffer=[]
#主循环
while True:
    #服务器端处理
    try:
        #接收数据包
        data,client_address=server_socket.recvfrom(1024)
        json_obj=json.loads(data.decode())
        logger.info('服务端接收客户端，消息：{0}...'.format(json_obj))
        #取出客户端传递过来的操作命令
        command=json_obj['command']

        if command == COMMAND_LOGIN:   #用户登录过程
            #通过id查询用户信息
            userid=json_obj['userid']
            userpwd=json_obj['user_pwd']
            logger.debug('userid:{0} user_pwd:{1}'.format(userid,userpwd))
            dao = UserDao()
            user=dao.findbyid(userid)
            logger.info(user)
            #判断客户端发送过来的密码与数据库的密码是否一致
            if user is not None and user['user_pwd'] == userpwd: #登录成功
                #登录成功
                #创创建保存用户登录信息的二元数组
                clientinfo=(userid,client_address)
                #用户信息添加到clientlist
                clientlist.append(clientinfo)

                json_obj=user
                json_obj['result']='0'
                # 取出好友用户列表
                dao=UserDao()
                friends=dao.findfriends(userid)
                # 返回clientinfo中的userid列表
                cinfo_userids=map(lambda it:it[0],clientlist)
                for friend in friends:
                    fid=friend['user_id']
                    # 添加好友状态 '1' 在线 '0' 离线
                    friend['online']='0'
                    if fid in cinfo_userids: #用户登录
                        friend['online']='1'
                json_obj['friends'] = friends
                logger.info('服务端发送用户成功，消息：{0}...'.format(json_obj))

                #json编码
                json_str=json.dumps(json_obj)
                #给客户端发送数据
                server_socket.sendto(json_str.encode(),client_address)
            else: #登录失败
                json_obj={}
                json_obj['result']='-1'
                #json编码
                json_str=json.dumps(json_obj)
                #给客户端发数据
                server_socket.sendto(json_str.encode(),client_address)
        elif command == COMMAND_SENDMSG: #用户发送消息
            #用户发送消息
            pass
        elif command == COMMAND_LOGOUT: #用户发送下线命令
            #用户发送下线命令
            pass
        #刷新用户列表
        #如果clientlist中没有元素则跳到下一次循环
        if len(clientlist)==0:
            continue
        json_obj={}
        json_obj['command']=COMMAND_REFRESH
        userid_map=map(lambda it :it[0],clientlist)
        useridlist=list(userid_map)
        json_obj['OnlineUserList']=useridlist
        for clientinfo in clientlist:
            _,address=clientinfo
            #Json编码
            json_str=json.dumps(json_obj)
            # 给客户端发送数据
            server_socket.sendto(json_str.encode(),address)

    except Exception:
        tb.print_exc()
        logger.info('timed out')






