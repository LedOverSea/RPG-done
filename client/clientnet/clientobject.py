# -*- coding: utf-8 -*-

import threading
import socket
import marshal
import struct
import clientnet

class CClientSocket(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.m_Socket = None
		self.setDaemon(True)
		self.m_Connected = False
		self.m_Data = b""
		self.m_iMaxSize = 1024
		
	def Connect(self):
		if self.m_Connected:
			return
		tIP = ("127.0.0.1", 6666)
		self.m_Socket = socket.socket()
		self.m_Socket.connect(tIP)
		self.m_Connected = True
		
	def run(self):
		while self.m_Connected:
			try:
				sData = self.m_Socket.recv(self.m_iMaxSize)
			except Exception as e:
				self.Disconnect(str(e))
				return
			try:
				self.ParseData(sData)
			except Exception as e:
				print("数据有误  %s %s" % (sData, e))
				
	def Send(self, dData):
		sData = marshal.dumps(dData)
		iSize = len(sData)
		iTotalSize = iSize + 4
		sSize = struct.pack("i", iTotalSize)
		sTotalStr = sSize + sData

		iCount = (iTotalSize - 1)//self.m_iMaxSize +1 
		for i in range(iCount):
			iBegin = self.m_iMaxSize * i
			iEnd = iBegin + self.m_iMaxSize
			sSubSend = sTotalStr[iBegin:iEnd]
			try:
				self.m_Socket.sendall(sSubSend)
			except:
				self.Disconnect("sendfail")
				return
				
	def ParseData(self, sData):
		self.m_Data += sData
		while True:
			iLen = len(self.m_Data)
			if iLen < 4:		#前4字节是长度
				return
			sSize = self.m_Data[:4]
			iSize = struct.unpack("i", sSize)[0]
			if iSize > iLen:	#未发完，继续等待
				return
			sPack = self.m_Data[4:iSize]
			self.m_Data = self.m_Data[iSize:]
			lstPackData = marshal.loads(sPack)
			self.OnCommand(lstPackData)

	def OnCommand(self, lstPackData):
		oCommand = clientnet.GetClientCommand()
		oCommand.OnCommand(lstPackData)
				
	def Disconnect(self, sReason):
		self.m_Connected = False
		self.m_Socket.close()
		self.m_Socket = None
		self.m_Data = ""
		print("断线了 %s" % sReason)

