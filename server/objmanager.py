# -*-  coding:utf-8 -*-

import pubglobalmanager

'''
管理所有玩家对象，通过调用CManager.GetItem(ID),传入玩家ID获取到玩家对象
'''

class CManager(object):
	
	def __init__(self):
		self.m_ID = 0x7ffffff
		self.m_Item = {}
		
	def NewID(self):
		self.m_ID += 1
		return self.m_ID
		
	def AddItem(self, iID, oItem):
		self.m_Item[iID] = oItem
		
	def RemoveItem(self, iID):
		self.m_Item.pop(iID, None)
		
	def GetItem(self, iID):
		return self.m_Item.get(iID, None)
	
	def SaveAll(self):
		for oItem in self.m_Item.values():
			oItem.SaveSql()

def Init():
	oManager = CManager()
	pubglobalmanager.SetGlobalManager("saveobjmanager", oManager)