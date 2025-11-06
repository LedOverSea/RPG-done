# -*- coding: utf-8 -*-
from . import mapdata
from . import mapunit
from .defines import UNIT_THIEF

import war
import pubglobalmanager
import timecontrol
from pubcore import Functor
import random

class CMap(object):
	
	def __init__(self):
		self.m_UnitIdx = 0	
		self.m_MapUnit = {}
		self.m_Block = []	#二维数组
		self.m_ThiefCount = 0	#当前蒙面大盗数量
		self.m_MaxThiefCount = 5	#最大蒙面大盗数量
		self.m_SpawnInterval = 10	#生成间隔（秒）
		self.ExceptStr = ""
	def Init(self):
		self.m_Block = mapdata.BLOCK
		# 启动定时生成蒙面大盗
		self.StartThiefSpawnTimer()
		
	def NewUnitIdx(self):
		self.m_UnitIdx += 1
		return self.m_UnitIdx
	
	def GetUnit(self, iUnitIdx):
		return self.m_MapUnit.get(iUnitIdx, None)
	
	def NewPlayerUnit(self, iPlayer):
		iUnitIdx = self.NewUnitIdx()
		oUnit = mapunit.CPlayerUnit(self, iUnitIdx)
		self.m_MapUnit[iUnitIdx] = oUnit
		return oUnit
	
	def PlayerEnter(self, oPlayer):
		oUnit = self.GetUnit(oPlayer.m_MapUnitIdx)
		if not oUnit:
			oUnit = self.NewPlayerUnit(oPlayer.m_ID)
			oUnit.Config(oPlayer.m_ID, oPlayer.m_BirthPos)
			oUnit.Load(oPlayer.m_CacheUnitData)
			oPlayer.SetMapUnitIdx(oUnit.m_UnitIdx)
		for oUnit in self.m_MapUnit.values():
			oUnit.Refresh()
		
	def IsBlock(self, tPos):
		iWidth, iHight = tPos
		return self.m_Block[iHight][iWidth]
		
	def UnitMove(self, iUnitIdx, tMovePos):
		oUnit = self.GetUnit(iUnitIdx)
		if not oUnit:
			return
		if self.IsBlock(tMovePos) or tMovePos == oUnit.m_Pos:
			return
		oUnit.Move(tMovePos)
		
	def NewThiefUnit(self):
		iUnitIdx = self.NewUnitIdx()
		oUnit = mapunit.CThiefUnit(self, iUnitIdx)
		self.m_MapUnit[iUnitIdx] = oUnit
		self.m_ThiefCount += 1
		return oUnit
	
	def RemoveThiefUnit(self, iUnitIdx):
		if iUnitIdx in self.m_MapUnit and self.m_MapUnit[iUnitIdx].m_Type == UNIT_THIEF:
			# 取消该大盗的定时器
			timecontrol.Remove_Call_Out("ThiefMove%s" % iUnitIdx)
			# 移除大盗对象
			del self.m_MapUnit[iUnitIdx]
			self.m_ThiefCount -= 1
	
	def SpawnThief(self):
		# 检查是否达到最大数量
		if self.m_ThiefCount >= self.m_MaxThiefCount:
			return
		
		try:
			# 寻找一个随机的可通行位置
			max_x = len(self.m_Block[0]) - 1
			max_y = len(self.m_Block) - 1
			
			# 尝试最多10次找到可通行位置
			for _ in range(10):
				target_x = random.randint(1, max_x - 1)
				target_y = random.randint(1, max_y - 1)
				target_pos = (target_x, target_y)
				
				if not self.IsBlock(target_pos):
					# 创建并配置蒙面大盗
					oThief = self.NewThiefUnit()
					oThief.Config(target_pos)
					oThief.Refresh()
					break
		except Exception as e:
			self.ExceptStr = str(e)
		
		# 继续定时生成
		self.StartThiefSpawnTimer()
	
	def EnterFight(self, oPlayer, iFightUnitIdx):
		oTarget = self.GetUnit(iFightUnitIdx)
		oPlayerUnit = self.GetUnit(oPlayer.m_MapUnitIdx)
		if not oTarget or not oPlayerUnit:
			return
		if not isinstance(oTarget,mapunit.CPlayerUnit):
			return
		#if abs(oTarget.m_Pos[0]-oPlayerUnit.m_Pos[0]) + abs(oTarget.m_Pos[1]-oPlayerUnit.m_Pos[1]) != 1:
		#	return
		try:
			oWar = war.NewWar()
			oWar.Config(oPlayerUnit, oTarget)
			oWar.WarStart()
		except Exception as e:
			print(e)
	
	def StartThiefSpawnTimer(self):
		# 设置定时器，每隔10秒生成一个蒙面大盗
		oCB = Functor(self.SpawnThief)
		timecontrol.Call_Out(oCB, self.m_SpawnInterval, "ThiefSpawnTimer")
