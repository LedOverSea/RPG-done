# -*- coding: utf-8 -*-
#所有socket管理类

import traceback
import socket
import pubdefines
import clientsocket.clientobject
import pubglobalmanager

class CSocketManger(object):
	
	def __init__(self):
		self.m_UID = 0		  #socket编号
		self.m_oSocket = None
		self.m_bClose = False
		self.m_dItem = {}
		self.InitManger()

	def InitManger(self):
		try:
			pubdefines.FormatPrint("服务器监听开始")
			self.m_oSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.m_oSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.m_oSocket.bind(("127.0.0.1", 6666))
			self.m_oSocket.listen(5)
		except:
			self.m_oSocket = None
			pubdefines.PythonError()

	#产生新的客户端索引
	def NewUID(self):
		self.m_UID += 1
		return self.m_UID

	def Stop(self):
		self.m_bClose = True
		for iUid in list(self.m_dItem.keys()):
			oItem = self.GetItem(iUid)
			if oItem:
				oItem.Release()
		self.m_oSocket.close()

	def Start(self):
		if not self.m_oSocket:
			return
		pubdefines.FormatPrint("等待客户端链接")
		while not self.m_bClose:
			try:
				sockobj, address = self.m_oSocket.accept()
			except:
				continue
			pubdefines.FormatPrint("客户端链接成功\n")
			iUID = self.NewUID()
			ip, port = address
			self.NewItem(iUID, sockobj, ip, port)
			
	def PrintError(self):
		oMap = pubglobalmanager.GetGlobalManager("map")
		if oMap.ExceptStr:
			print(oMap.ExceptStr)
			oMap.ExceptStr = ""
	
	def NewItem(self, iUID, sockobj, ip, port):
		oClient = clientsocket.clientobject.CLink(iUID, sockobj, ip, port)
		self.m_dItem[iUID] = oClient

	def GetItem(self, iUID):
		return self.m_dItem.get(iUID, None)

	def DelItem(self, iUID):
		if iUID in self.m_dItem:
			del self.m_dItem[iUID]
			
	def GetAllSocket(self):
		return list(self.m_dItem.keys())

	def Disconnected(self, iUID, sReason=""):
		pubdefines.LogFile("clientsocket", "%d disconnected reason is %s" % (iUID, sReason))
		oClient = self.GetItem(iUID)
		oClient.Release()
		self.DelItem(iUID)
		print("客户端断线 %s" % sReason)

