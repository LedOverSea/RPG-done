# -*- coding: utf-8 -*-
import threading
import clientnet

class CCommand(object):
	
	def __init__(self, oSocket):
		self.m_Socket = oSocket
		self.m_Command = {}		#客户端收到服务器
		self.m_Lock = threading.Lock()
		
	def OnCommand(self, lstPackInfo):
		if not lstPackInfo:
			return
		iProtocol = lstPackInfo[0]
		lstArgs = lstPackInfo[1:]
		oCommand = self.m_Command.get(iProtocol, None)
		if not oCommand:
			print("未支持的协议%s" % iProtocol)
			return
		self.m_Lock.acquire()
		try:
			oCommand(lstArgs)
		except Exception as e:
			print("协议发生异常 %s" % iProtocol, e)
			
		self.m_Lock.release()
		
	def Register(self, iProtocol, oCommand):
		if iProtocol in self.m_Command:
			print("重复注册的协议 %s" % iProtocol)
			return
		self.m_Command[iProtocol] = oCommand
	
	#1. 登录
	def C2SLogin(self, sAccount, sPwd):
		lstPackInfo = [1, 1, sAccount, sPwd]
		self.m_Socket.Send(lstPackInfo)
		
	#2. 玩家人物移动
	def C2SPlayerMove(self, tPos):
		lstPackInfo = [2, 1, *tPos]
		self.m_Socket.Send(lstPackInfo)
		
	#3. 与npc进入战斗
	def C2SFight(self, iNpcIdx):
		lstPackInfo = [2, 2, iNpcIdx]
		self.m_Socket.Send(lstPackInfo)
		
	#4. 查看战报
	def C2SReadReport(self, iReportIdx):
		lstPackInfo = [2, 3, iReportIdx]
		self.m_Socket.Send(lstPackInfo)
		
	