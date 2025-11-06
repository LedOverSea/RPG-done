# -*- coding: utf-8 -*-

from . import clientobject
from . import command

if not "g_ClientSocket" in globals():
	g_ClientSocket = clientobject.CClientSocket()
	g_ClientCommand = command.CCommand(g_ClientSocket)
	
def GetClientSocket():
	return g_ClientSocket

def GetClientCommand():
	return g_ClientCommand

def RegisterCommand(iProtocol, oCommand):
	oMgr = GetClientCommand()
	oMgr.Register(iProtocol, oCommand)



'''
调用样例
oClient = GetClientSocket()
oClient.Connect()
oClient.start()
'''

#弹窗消息
def OnNotify(lstArg):
	sMsg, = lstArg
	print("Notify", sMsg)

#登录成功
# def OnLoginSuc(lstArg):
# 	print("login success?", lstArg)
# 	return True

#登录失败
# def OnLoginFail(lstArg):
# 	print("login Fail", lstArg)

#刷新人物状态，可能包含有别人的人物
# def OnPlayerRefresh(*args):
# 	print('**OnPlayerRefresh**\n服务器回传数据：%s\n'%args)
# 	print(args)
# 	return args[-1]

	# iUnitIdx, tPos, iPlayerID, iMovingState, tStepStart, iMovePathIdx, lstMovePath = lstArg
	#
	# iUnitIdx 小人在地图的编号 NPC
	# tPos (1,1)小人当前坐标
	# iPlayerID 小人所属玩家编号
	# iMovingState 0或者1代表是否移动中
	# tStepStart (12345,67)假设在移动中，那么这个格子开始移动的时间 即12345.67时刻
	# iMovePathIdx 当前在路径的第几个，从0开始数
	# lstMovePath [(0,0), (0,1), (0,2)]移动路径


RegisterCommand(1, OnNotify)
# RegisterCommand(2, OnLoginSuc)
# RegisterCommand(3, OnLoginFail)
# RegisterCommand(4, OnPlayerRefresh)
# RegisterCommand(5, OnRefreshReport)

'''
发送协议给服务器
oCommand = GetClientCommand()
oCommand.C2SLogin("#123123", "sfdsfdd")


'''