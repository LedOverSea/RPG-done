# -*- coding: utf-8 -*-

import time
import war
'''
地图上的物件
'''
from pubdefines import TupleTime
from . import astar
from pubcore import Functor
from .defines import UNIT_PLAYER, UNIT_THIEF

import pubglobalmanager
import timecontrol
import random

class CMapUnit(object):
	
	m_Type = UNIT_PLAYER
	m_MoveTime = 0.4			#移动一格所需的时间
	
	def __init__(self, oMap, iUnitIdx):
		self.m_Map = oMap
		self.m_UnitIdx = iUnitIdx
		self.m_Pos = (0, 0)			#坐标
		self.m_Owner = 0
		
		self.m_Moving = 0			#是否在移动中
		self.m_MovePath = []		#移动坐标路径  如[(1,1), (2,1), (3,1)]
		self.m_MovePathIdx = 0		#走到了路径第X序号的坐标
		self.m_StepStart = (0, 0)	#从坐标出发的时间
		self.m_NewMovePos = None	#移动过程中，改变目的地
		
	def Config(self, iUnitIdx, tPos):
		self.m_UnitIdx = iUnitIdx
		self.m_Pos = tPos
		
	def Save(self):
		data = {}
		data["Pos"] = self.m_Pos
		return data
	
	def Load(self, data):
		if not data:
			return
		self.m_Pos = data["Pos"]
		
	def Name(self):
		return ""
		
	def Refresh(self):
		oSocketManager = pubglobalmanager.GetGlobalManager("socketmgr")
		oCommand = pubglobalmanager.GetGlobalManager("commandctrl")
		lstPackInfo = self.GetPackInfo()
		for iSocket in oSocketManager.GetAllSocket():
			oCommand.S2CRefreshMapUnit(iSocket, lstPackInfo)
	
	def GetPackInfo(self):
		return []
	
	def Move(self, tMovePos):
		oAStar = astar.AStar(self.m_Map.m_Block, self.m_Pos, tMovePos)
		lstPath = oAStar.start()
		if not lstPath:
			return
		if not self.m_Moving:
			self.m_Moving = 1
			self.m_StepStart = TupleTime()
			self.m_MovePathIdx = 0
			self.m_MovePath = lstPath
			oCB = Functor(UnitMoveStep, self.m_UnitIdx)
			timecontrol.Call_Out(oCB, self.m_MoveTime, "Move%s" % self.m_UnitIdx)
			self.Refresh()
		else:
			self.m_NewMovePos = tMovePos
			
	def MoveStepDone(self):
		self.m_MovePathIdx += 1
		self.m_Pos = self.m_MovePath[self.m_MovePathIdx]
		
		# 检查是否与其他单位十字相遇
		self.CheckCrossEncounter()
		
		if not self.m_NewMovePos:
			if self.m_MovePathIdx >= len(self.m_MovePath)-1:
				self.ClearMove()
				self.Refresh()
				return
			tNextPos = self.m_MovePath[self.m_MovePathIdx+1]
			if self.m_Map.IsBlock(tNextPos):
				self.ClearMove()
				self.Refresh()
				return
			self.m_StepStart = TupleTime()
			oCB = Functor(UnitMoveStep, self.m_UnitIdx)
			timecontrol.Call_Out(oCB, self.m_MoveTime, "Move%s" % self.m_UnitIdx)
			self.Refresh()
		else:
			self.m_Moving = 1
			oAStar = astar.AStar(self.m_Map.m_Block, self.m_Pos, self.m_NewMovePos)
			lstPath = oAStar.start()
			if not lstPath:
				self.ClearMove()
				self.Refresh()
				return
			self.m_StepStart = TupleTime()
			self.m_MovePathIdx = 0
			self.m_MovePath = lstPath
			self.m_NewMovePos = None
			oCB = Functor(UnitMoveStep, self.m_UnitIdx)
			timecontrol.Call_Out(oCB, self.m_MoveTime, "Move%s" % self.m_UnitIdx)
			self.Refresh()
			
	def CheckCrossEncounter(self):
		"""检查是否与其他单位十字相遇（上下左右相邻）"""
		# 获取所有其他单位
		for oOtherUnit in self.m_Map.m_MapUnit.values():
			# 跳过自己
			if oOtherUnit.m_UnitIdx == self.m_UnitIdx:
				continue
			
			# 计算位置差
			dx = abs(self.m_Pos[0] - oOtherUnit.m_Pos[0])
			dy = abs(self.m_Pos[1] - oOtherUnit.m_Pos[1])
			
			# 检查是否十字相遇（dx+dy=1，即相邻）
			if dx + dy == 1:
				# 判断是否是玩家和蒙面大盗相遇
				if (self.m_Type == UNIT_PLAYER and oOtherUnit.m_Type == UNIT_THIEF) or \
				   (self.m_Type == UNIT_THIEF and oOtherUnit.m_Type == UNIT_PLAYER):
					# 确定哪个是玩家单位，哪个是大盗单位
					oPlayerUnit = self if self.m_Type == UNIT_PLAYER else oOtherUnit
					oThiefUnit = oOtherUnit if self.m_Type == UNIT_PLAYER else self
					
					# 获取玩家对象
					oSaveMgr = pubglobalmanager.GetGlobalManager("saveobjmanager")
					oPlayer = oSaveMgr.GetItem(oPlayerUnit.m_Owner)
					if oPlayer:
						# 进入战斗
						try:
							oWar = war.NewWar()
							oWar.Config(oPlayerUnit, oThiefUnit)
							oWar.WarStart()
						except Exception as e:
							print(e)
					
	def ClearMove(self):
		self.m_Moving = 0
		self.m_StepStart = (0, 0)
		self.m_MovePathIdx = 0
		self.m_MovePath = []
		self.m_NewMovePos = None
		
	def Release(self):
		self.m_Map = None
	
		
class CPlayerUnit(CMapUnit):
	
	m_Type = UNIT_PLAYER
	
	def Config(self, iPlayer, tPos):
		self.m_Owner = iPlayer
		self.m_Pos = tPos
		
	def Name(self):
		return "玩家%s" % self.m_Owner
		
	def GetPackInfo(self):
		return [self.m_UnitIdx, self.m_Type, self.m_Pos, self.m_Owner, self.m_Moving, 
			self.m_StepStart, self.m_MovePathIdx, self.m_MovePath]
		
		
class CThiefUnit(CMapUnit):
	
	m_Type = UNIT_THIEF
	
	def __init__(self, oMap, iUnitIdx):
		super(CThiefUnit, self).__init__(oMap, iUnitIdx)
		self.m_Name = "蒙面大盗"
		self.m_SpawnTime = time.time()
		# 启动随机移动
		self.StartRandomMove()
	
	def Config(self, tPos):
		self.m_Pos = tPos
	
	def Name(self):
		return self.m_Name
	
	def GetPackInfo(self):
		return [self.m_UnitIdx, self.m_Type, self.m_Pos, self.m_UnitIdx, self.m_Moving, 
			self.m_StepStart, self.m_MovePathIdx, self.m_MovePath]
	
	def StartRandomMove(self):
		# 随机延迟后移动到随机位置
		delay = random.uniform(2, 5)
		oCB = Functor(self.RandomMove, self.m_UnitIdx)
		timecontrol.Call_Out(oCB, delay, "ThiefMove%s" % self.m_UnitIdx)
	
	def RandomMove(self, iUnitIdx):
		# 生成随机目标位置
		max_x = len(self.m_Map.m_Block[0]) - 1
		max_y = len(self.m_Map.m_Block) - 1
		target_x = random.randint(1, max_x - 1)
		target_y = random.randint(1, max_y - 1)
		target_pos = (target_x, target_y)
		
		# 检查目标位置是否可通行
		if not self.m_Map.IsBlock(target_pos):
			self.Move(target_pos)
		
		# 继续随机移动
		self.StartRandomMove()


def UnitMoveStep(iUnitIdx):
	oMap = pubglobalmanager.GetGlobalManager("map")
	oUnit = oMap.GetUnit(iUnitIdx)
	if not oUnit:
		return
	oUnit.MoveStepDone()
	