# -*- coding: utf-8 -*-
from pubcore import RandomList
import random
from .defines import *

class CPerform(object):
	
	def __init__(self, oWarrior):
		self.m_Warrior = oWarrior
		
	def Perform(self):
		pass
	
	
class CBaseAttack(CPerform):
	
	def Perform(self):
		lstEnemy = self.m_Warrior.GetEnemy()
		lstEnemy = [oEnemy for oEnemy in lstEnemy if oEnemy.IsAlive()]
		if not lstEnemy:
			return
		oTarget = RandomList(lstEnemy)
		
		# 检查目标是否有飞檐走壁技能，50%概率闪避
		if hasattr(oTarget, 'has_evasion_skill') and oTarget.has_evasion_skill():
			if random.random() < 0.5:  # 50%闪避概率
				oWar = self.m_Warrior.m_War
				oReport = oWar.m_Report
				oReport.AddMsg(MSG_EVADE, oTarget.Name(), self.m_Warrior.Name())
				return
			
		iDamage = self.m_Warrior.m_Att - oTarget.m_Def
		if iDamage < 0:
			iDamage = 0
		# 使用ApplyDamage方法处理伤害，考虑耐力抵消
		iRealDamage = oTarget.ApplyDamage(iDamage)
		iReadDamage = min(oTarget.m_HP, iRealDamage)
		oTarget.m_HP = oTarget.m_HP - iReadDamage
		
		oWar = self.m_Warrior.m_War
		oReport = oWar.m_Report
		oReport.AddMsg(MSG_ATTACK, self.m_Warrior.Name(), self.m_Warrior.m_Pos, oTarget.Name(), oTarget.m_Pos, iReadDamage)


class CBloodyRainNeedle(CPerform):
	"""暴雨梨花针：对敌方全体造成1倍攻击力的伤害"""
	
	def __init__(self, oWarrior):
		super(CBloodyRainNeedle, self).__init__(oWarrior)
		self.m_Name = "暴雨梨花针"
	
	def Perform(self):
		lstEnemy = self.m_Warrior.GetEnemy()
		lstEnemy = [oEnemy for oEnemy in lstEnemy if oEnemy.IsAlive()]
		if not lstEnemy:
			return
		
		# 对敌方全体造成伤害
		for oTarget in lstEnemy:
			iDamage = self.m_Warrior.m_Att  # 1倍攻击力
			if iDamage < 0:
				iDamage = 0
			# 使用ApplyDamage方法处理伤害，考虑耐力抵消
			iRealDamage = oTarget.ApplyDamage(iDamage)
			iReadDamage = min(oTarget.m_HP, iRealDamage)
			oTarget.m_HP = oTarget.m_HP - iReadDamage
			
			# 为每个目标单独添加战报
			oWar = self.m_Warrior.m_War
			oReport = oWar.m_Report
			oReport.AddMsg(MSG_SKILL_BLOODY_RAIN, self.m_Warrior.Name(), oTarget.Name(), iReadDamage)


class CFlyingWallSkill(CPerform):
	"""飞檐走壁：被动技能，提供50%概率闪避普通攻击"""
	
	def __init__(self, oWarrior):
		super(CFlyingWallSkill, self).__init__(oWarrior)
		self.m_Name = "飞檐走壁"
		
		
		