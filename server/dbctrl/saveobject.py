# -*- coding: utf-8 -*-

import marshal
import pubglobalmanager
import timecontrol

from . import defines

class CSaveData(object):
	def __init__(self, iID):
		self.m_ID = iID
		self.m_Data = {}
		self.m_Loaded = True

	def Query(self, sAttr, default = 0):
		return self.m_Data.get(sAttr, default)
	
	def Set(self, sAttr, val):
		self.m_Data[sAttr] = val

	def Add(self, sAttr, iVal):
		self.m_Data.setdefault(sAttr, 0)
		self.m_Data[sAttr] += iVal

	def Delete(self, sAttr):
		if sAttr in self.m_Data:
			del self.m_Data[sAttr]

	def GetKey(self):
		raise Exception("未实现Key")

	def GetUpdateSql(self):
		sData = marshal.dumps(self.m_Data)
		sSql = "update tbl_global set rl_sData='%s',rl_dmSaveTime=now() where rl_sName='%s'" % (sData, self.GetKey())
		return sSql

	def GetQuerySql(self):
		sSql = "select rl_sData from tbl_global where rl_sName ='%s'" % self.GetKey()
		return sSql

	def Init(self):
		oObjManager = pubglobalmanager.GetGlobalManager("saveobjmanager")
		oObjManager.AddItem(self.m_ID, self)	#添加到管理器中
		if self.LoadSql():
			self.AutoSave()
			return
		self.New()
		self.AutoSave()

	def LoadSql(self):
		sSql = self.GetQuerySql()
		resultList = pubglobalmanager.CallManagerFunc(defines.DBCTRL_MANAGER_NAME, "Query", sSql)
		if resultList:
			sData = resultList[0][0]
			sData = sData.decode()
			sData = bytes.fromhex(sData)
			dData = marshal.loads(sData)
			self.Load(dData)
			return True
		return False
	
	def Load(self, dData):
		if not dData:
			return
		self.m_Data = dData["Data"]

	def New(self):
		sData = marshal.dumps(None)
		sData = sData.hex()
		sSql = "insert into tbl_global(rl_sName, rl_dmSaveTime, rl_sData) values('%s', now(), '%s')" % (self.GetKey(), sData)
		pubglobalmanager.CallManagerFunc(defines.DBCTRL_MANAGER_NAME, "ExecSql", sSql)

	def SaveSql(self):
		sData = marshal.dumps(self.Save())
		sData = sData.hex()
		sSql = "update tbl_global set rl_sData='%s',rl_dmSaveTime=now() where rl_sName='%s'" % (sData, self.GetKey())
		pubglobalmanager.CallManagerFunc(defines.DBCTRL_MANAGER_NAME, "ExecSql", sSql)
		
	def Save(self):
		data = {}
		data["Data"] = self.m_Data
		return data
		
	def AutoSave(self):
		oObjManager = pubglobalmanager.GetGlobalManager("saveobjmanager")
		if not oObjManager.GetItem(self.m_ID):
			return
		timecontrol.Call_Out(self.AutoSave, 5*60, self.GetKey())
		self.SaveSql()
		
	def Remove(self):
		oObjManager = pubglobalmanager.GetGlobalManager("saveobjmanager")
		oObjManager.RemoveItem(self.m_ID)
