# -*- coding: utf-8 -*-
import copy
import time
import pubglobalmanager

class CReportMgr(object):
	
	m_MaxSize = 10
	
	def __init__(self, iOwner):
		self.m_Owner = iOwner
		self.m_Idx = 0
		self.m_Item = {}
		
	def Save(self):
		data = {}
		data["Idx"] = self.m_Idx
		
		dItem = {}
		for iIdx, oReport in self.m_Item.items():
			dItem[iIdx] = oReport.Save()
		data["Item"] = dItem
		return data
	
	def Load(self, data):
		if not data:
			return
		self.m_Idx = data["Idx"]
		for iIdx, dReport in data["Item"].items():
			oReport = CReport()
			oReport.Load(dReport)
			self.m_Item[iIdx] = oReport
		
	def AddReport(self, oReport):
		self.m_Idx += 1
		oReport.Config(self.m_Idx, int(time.time()))
		self.m_Item[self.m_Idx] = oReport
		
		if len(self.m_Item) > self.m_MaxSize:
			iMinIdx = min(self.m_Item.keys())
			self.m_Item.pop(iMinIdx)
		return self.m_Idx
	
	def GetReport(self, iIdx):
		return self.m_Item.get(iIdx, None)
	
	def RefreshReport(self, iIdx):
		oReport = self.GetReport(iIdx)
		if not oReport:
			return
		oMgr = pubglobalmanager.GetGlobalManager("saveobjmanager")
		oPlayer = oMgr.GetItem(self.m_Owner)
		lstPack = oReport.GetPackInfo()
		oCommand = pubglobalmanager.GetGlobalManager("commandctrl")
		oCommand.S2CSendReport(oPlayer.m_SocketID, lstPack)
		
	def RefreshAll(self):
		for iIdx in self.m_Item:
			self.RefreshReport(iIdx)


class CReport(object):
	
	def __init__(self):
		self.m_Idx = 0
		self.m_Time = 0
		self.m_Msg = []
		self.m_WinName = ""
		
	def Config(self, iIdx, iTime):
		self.m_Idx = iIdx
		self.m_Time = iTime
		
	def Save(self):
		data = {}
		data["Idx"] = self.m_Idx
		data["Time"] = self.m_Time
		data["Msg"] = self.m_Msg
		data["WN"] = self.m_WinName
		return data
	
	def Load(self, data):
		self.m_Idx = data["Idx"]
		self.m_Time = data["Time"]
		self.m_Msg = data["Msg"]
		self.m_WinName = data.get("WN", "")
		
	def AddMsg(self, iMsgID, *args):
		self.m_Msg.append((iMsgID, *args))
		
	def CopyReport(self):
		oCopy = CReport()
		oCopy.m_Msg = copy.deepcopy(self.m_Msg)
		return oCopy
	
	def GetPackInfo(self):
		return [self.m_Idx, self.m_Time, self.m_WinName, self.m_Msg]
	