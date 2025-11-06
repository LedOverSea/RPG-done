# -*- coding: utf-8 -*-
from .warrior import CWarrior, CThiefWarrior
from .defines import *

import warreport
import pubglobalmanager

class CWar(object):
	
	def __init__(self):
		self.m_Turn = 0
		self.m_Warrior = []
		self.m_Report = None
	
	def Config(self, oAttUnit, oDefUnit):
		self.m_AttUnit = oAttUnit
		self.m_DefUnit = oDefUnit
		self.m_Unit = [self.m_AttUnit, self.m_DefUnit]
		
		# 配置攻击方
		sAttName = oAttUnit.Name()
		# 检查是否是大盗单位（根据名称判断）
		is_thief_att = "蒙面大盗" in sAttName
		if is_thief_att:
			# 大盗只有1个战士
			iSide = SIDE_ATTACK
			iPos = 1
			oWarrior = CThiefWarrior(iSide, iPos)
			oWarrior.Config(self, sAttName)
			self.m_Warrior.append(oWarrior)
		else:
			# 普通单位创建3个战士
			for iPos in range(1, 4):
				iSide = SIDE_ATTACK
				oWarrior = CWarrior(iSide, iPos)
				oWarrior.Config(self, sAttName)
				self.m_Warrior.append(oWarrior)
		
		# 配置防御方
		sDefName = oDefUnit.Name()
		# 检查是否是大盗单位
		is_thief_def = "蒙面大盗" in sDefName
		if is_thief_def:
			# 大盗只有1个战士
			iSide = SIDE_DEFEND
			iPos = 4
			oWarrior = CThiefWarrior(iSide, iPos)
			oWarrior.Config(self, sDefName)
			self.m_Warrior.append(oWarrior)
		else:
			# 普通单位创建3个战士
			for iPos in range(4, 7):
				iSide = SIDE_DEFEND
				oWarrior = CWarrior(iSide, iPos)
				oWarrior.Config(self, sDefName)
				self.m_Warrior.append(oWarrior)
			
		self.m_Report = warreport.NewReport()
			
	def WarStart(self):
		while True:
			self.m_Turn += 1
			print("回合开始了",self.m_Turn)
			self.m_Report.AddMsg(MSG_NEWTURN, self.m_Turn)
			for oWarrior in self.SortOrder():
				oWarrior.Action()
				if self.CheckEnd():
					break
			
			if self.CheckEnd():
				break
		
		self.WarEnd()
			
	def CheckEnd(self):
		if self.m_Turn >= 10:
			return 1
		
		lstAtt = []
		lstDef = []
		for oWor in self.m_Warrior:
			if not oWor.IsAlive():
				continue
			if oWor.m_Side == SIDE_ATTACK:
				lstAtt.append(oWor)
			else:
				lstDef.append(oWor)
				
		if lstAtt and lstDef:
			return 0
		return 1
	
	def CalWinUnit(self):
		lstAtt = []
		lstDef = []
		for oWor in self.m_Warrior:
			if not oWor.IsAlive():
				continue
			if oWor.m_Side == SIDE_ATTACK:
				lstAtt.append(oWor)
			else:
				lstDef.append(oWor)
		if not lstDef:
			return self.m_AttUnit
		else:
			return self.m_DefUnit
	
	def FindWarriorBySide(self, iSide):
		return [oWor for oWor in self.m_Warrior if oWor.m_Side==iSide]
			
	def SortOrder(self):
		lstLive = [oWarrior for oWarrior in self.m_Warrior if oWarrior.IsAlive()]
		return sorted(lstLive, key=lambda x:x.m_Speed)
		
	def WarEnd(self):
		oWinUnit = self.CalWinUnit()
		self.m_Report.m_WinName = oWinUnit.Name()
		self.SendReport(self.m_AttUnit.m_Owner)
		self.SendReport(self.m_DefUnit.m_Owner)
		self.Release()
	
	def SendReport(self, iPlayer):
		oMgr = pubglobalmanager.GetGlobalManager("saveobjmanager")
		oPlayer = oMgr.GetItem(iPlayer)
		if not oPlayer:
			return
		oReport = self.m_Report.CopyReport()
		iIdx = oPlayer.m_ReportMgr.AddReport(oReport)
		oPlayer.m_ReportMgr.RefreshReport(iIdx)
		
	def Release(self):
		for oWarrior in self.m_Warrior:
			oWarrior.Release()
		self.m_Warrior = []
		