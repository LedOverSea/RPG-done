# -*- coding: utf-8 -*-
from . import defines

import pubdefines
import threading
import pubglobalmanager
import struct
import marshal
import commandctrl


class CLink(threading.Thread):
	def __init__(self, uid, oSocket, ip, port):
		threading.Thread.__init__(self)
		self.m_ID = uid		#用于区分不同socket连接
		self.m_oSocket = oSocket
		self.m_IP = ip
		self.m_Port = port
		self.m_bConnected = True
		self.m_MaxSize = 1024
		self.m_sData = b""
		self.m_PlayerID = 0
		self.m_SendPackInfo = []	#[1, 5, "哈哈"] 当前要发的数据
		self.m_RecvPackInfo = []	#[1, 5, "哈哈"] 当前收到的数据
		self.InitObj()

	def InitObj(self):
		self.start()
		
	def GetPlayerID(self):
		return self.m_PlayerID
	
	def SetPlayerID(self, iPlayerID):
		self.m_PlayerID = iPlayerID
	
	def run(self):
		while self.m_bConnected:
			try:
				sData = b""
				sData = self.m_oSocket.recv(self.m_MaxSize)
			except Exception as e:
				self.Disconnected(str(e))
				return
			if not sData:
				self.Disconnected("clientclose")
				return
			
			try:
				self.Recv(sData)
			except Exception as e:
				pubdefines.PythonError("RecvFail")

	def Recv(self, sData):
		self.m_sData += sData
		while True:
			iLen = len(self.m_sData)
			if iLen < 4:	#包基本格式不齐
				return
			sSize = self.m_sData[:4]
			iSize = struct.unpack("i", sSize)[0]
			if iSize > iLen:	#未发完，继续等待
				return
			sPack = self.m_sData[4:iSize]
			self.m_sData = self.m_sData[iSize:]
			lstPackData = marshal.loads(sPack)
			self.OnCommand(lstPackData) 

	def PacketSend(self):
		sData = marshal.dumps(self.m_SendPackInfo)
		self.m_SendPackInfo = []
		iSize = len(sData)
		iTotalSize = iSize + 4
		sSize = struct.pack("i", iTotalSize)
		sTotalStr = sSize + sData

		iCount = (iTotalSize - 1)//self.m_MaxSize +1 
		for i in range(iCount):
			iBegin = self.m_MaxSize * i
			iEnd = iBegin + self.m_MaxSize
			sSubSend = sTotalStr[iBegin:iEnd]
			try:
				self.m_oSocket.sendall(sSubSend)
			except:
				self.Disconnected("sendfail")
				return
			
	#压包进数据
	def PacketAdd(self, val):
		self.m_SendPackInfo.append(val)
		
	#多重压包
	def DataExpand(self, lstVal):
		self.m_SendPackInfo.extend(lstVal)
		
	#截取数据的第一个元素,留下剩余部分  例[1,"Hello"] -> ["Hello"]
	def UnpackHead(self):
		if not self.m_RecvPackInfo:
			return None
		return self.m_RecvPackInfo.pop(0)
			
	def Release(self):
		try:
			self.m_bConnected = False
			self.m_oSocket.close()
		except:
			pubdefines.PythonError()

	def Disconnected(self, sReason):
		pubglobalmanager.CallManagerFunc(defines.SOCKET_MANAGER, "Disconnected", self.m_ID, sReason)

	def OnCommand(self, lstPackData):
		self.m_RecvPackInfo = lstPackData
		commandctrl.OnCommand(self)