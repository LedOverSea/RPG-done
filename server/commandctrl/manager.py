# -*- coding: utf-8 -*- 

import importlib
import mutexlock
import traceback
import pubdefines
import pubglobalmanager

class CCommandManager:
	def __init__(self):
		self.InitCommand()
	
	def InitCommand(self):
		self.m_CommandDict = {
			1 : ("player", "LoginCommand"),
			2 : ("player", "GameCommand"),
		}

	@mutexlock.AutoLock("oncommand")
	def OnCommand(self, oLink):
		try:
			iProtocol = oLink.UnpackHead()
			if not iProtocol in self.m_CommandDict:
				pubdefines.FormatPrint("未定义客户端的调用%s" % iProtocol)
				return 
			sImport, sFunc = self.m_CommandDict[iProtocol]
			oModule = importlib.import_module(sImport)
			oFunc = getattr(oModule, sFunc, None)
			if not oFunc:
				pubdefines.FormatPrint("客户端触发%s行为，%s模块未找到接口%s" % (iProtocol, sImport, sFunc))
				return
			oFunc(oLink)
		except Exception as e:
			print("出现报错", traceback.format_exc())
		
	def S2CNotify(self, oSocket, sMsg):
		iProtocol = 1
		oSocket.PacketAdd(iProtocol)
		oSocket.PacketAdd(sMsg)
		oSocket.PacketSend()
		
	def S2CLoginSuc(self, iSocketID):
		oSocketManager = pubglobalmanager.GetGlobalManager("socketmgr")
		oSocket = oSocketManager.GetItem(iSocketID)
		if not oSocket:
			return
		iProtocol = 2
		oSocket.PacketAdd(iProtocol)
		oSocket.PacketSend()
		
	def S2CLoginFail(self, iSocketID):
		oSocketManager = pubglobalmanager.GetGlobalManager("socketmgr")
		oSocket = oSocketManager.GetItem(iSocketID)
		if not oSocket:
			return
		iProtocol = 3
		oSocket.PacketAdd(iProtocol)
		oSocket.PacketSend()
		
	def S2CRefreshMapUnit(self, iSocketID, lstPackInfo):
		oSocketManager = pubglobalmanager.GetGlobalManager("socketmgr")
		oSocket = oSocketManager.GetItem(iSocketID)
		if not oSocket:
			return
		iProtocol = 4
		oSocket.PacketAdd(iProtocol)
		oSocket.DataExpand(lstPackInfo)
		oSocket.PacketSend()
		
	def S2CSendReport(self, iSocketID, lstPackInfo):
		oSocketManager = pubglobalmanager.GetGlobalManager("socketmgr")
		oSocket = oSocketManager.GetItem(iSocketID)
		if not oSocket:
			return
		iProtocol = 5
		oSocket.PacketAdd(iProtocol)
		oSocket.DataExpand(lstPackInfo)
		oSocket.PacketSend()




