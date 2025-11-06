# -*- coding: utf-8 -*-

from .perform import CBaseAttack, CBloodyRainNeedle
import pubglobalmanager
from .defines import MSG_STAMINA_DEFEND

class CWarrior(object):
	
	def __init__(self, iSide, iPos):
		self.m_Side = iSide		# 0进攻方 1防守方
		self.m_Pos = iPos		# 1 2 3号位置
		self.m_Perform = []
		self.m_Stamina = 100	# 耐力值
		self.m_StaminaMax = 100	# 耐力上限
		self.m_StaminaTimerKey = None	# 耐力恢复计时器键名
		
	def Config(self, oWar, sOwnerName):
		self.m_War = oWar
		self.m_OwnerName = sOwnerName
		self.m_Att = 1	#攻击
		self.m_Def = 0	#防御
		self.m_Speed = 1#行动速度
		self.m_HP = 3	#生命值
		self.m_HPMax = 3
		self.m_Stamina = 100	# 初始耐力100
		
		oBaseAttack = CBaseAttack(self)
		self.m_Perform.append(oBaseAttack)
		
		# 注册耐力恢复计时器
		self.StartStaminaRecovery()
		
	def Name(self):
		return "%s的%s号位" % (self.m_OwnerName, self.m_Pos%3)
		
	def IsAlive(self):
		return self.m_HP > 0
	
	def Action(self):
		for oPerform in self.m_Perform:
			oPerform.Perform()
			
	def GetEnemy(self):
		lstEnemy = []
		for oEnemy in self.m_War.m_Warrior:
			if oEnemy.m_Side == self.m_Side:
				continue
			lstEnemy.append(oEnemy)
		return lstEnemy
	
	def Release(self):
		self.StopStaminaRecovery()
		self.m_War = None
		self.m_Perform = []
		
	def StartStaminaRecovery(self):
		"""开始耐力恢复计时器，每秒恢复1点耐力"""
		self.StopStaminaRecovery()  # 先停止可能存在的计时器
		self.m_StaminaTimerKey = f"stamina_{self.m_Side}_{self.m_Pos}"
		# 使用timecontrol模块的Call_Out函数注册计时器
		from timecontrol import Call_Out
		Call_Out(self.RecoverStamina, 1.0, self.m_StaminaTimerKey)
		
	def StopStaminaRecovery(self):
		"""停止耐力恢复计时器"""
		if self.m_StaminaTimerKey:
			# 使用timecontrol模块的Remove_Call_Out函数取消计时器
			from timecontrol import Remove_Call_Out
			Remove_Call_Out(self.m_StaminaTimerKey)
			self.m_StaminaTimerKey = None
		
	def RecoverStamina(self):
		"""恢复耐力的回调函数"""
		if self.IsAlive() and self.m_Stamina < self.m_StaminaMax:
			self.m_Stamina += 1
			if self.m_Stamina > self.m_StaminaMax:
				self.m_Stamina = self.m_StaminaMax
		# 重新注册计时器，实现每秒恢复
		self.StartStaminaRecovery()
		
	def ApplyDamage(self, iDamage):
		"""应用伤害，考虑耐力抵消"""
		iStaminaDefend = min(iDamage, self.m_Stamina)
		iRealDamage = iDamage - iStaminaDefend
		
		# 更新耐力
		if iStaminaDefend > 0:
			self.m_Stamina -= iStaminaDefend
			# 添加耐力防御战报
			if self.m_War and hasattr(self.m_War, 'm_Report'):
				self.m_War.m_Report.AddMsg(MSG_STAMINA_DEFEND, self.Name(), iStaminaDefend)
		
		return iRealDamage


class CThiefWarrior(CWarrior):
    """蒙面大盗战士类"""
    
    def Config(self, oWar, sOwnerName):
        # 先调用父类Config方法初始化基础属性和耐力恢复
        super(CThiefWarrior, self).Config(oWar, sOwnerName)
        # 大盗战斗属性（覆盖父类默认值）
        self.m_Att = 1    # 攻击1
        self.m_Def = 1    # 防御1
        self.m_Speed = 10 # 速度10
        self.m_HP = 10    # 生命值10
        self.m_HPMax = 10
        # 确保耐力初始化为100
        self.m_Stamina = 100
        
        # 移除父类添加的基础攻击
        self.m_Perform = []
        # 添加基础攻击
        oBaseAttack = CBaseAttack(self)
        self.m_Perform.append(oBaseAttack)
        
        # 添加暴雨梨花针技能
        oSkill = CBloodyRainNeedle(self)
        self.m_Perform.append(oSkill)
    
    def Name(self):
        # 大盗的名称直接返回"蒙面大盗"，不需要添加位置号
        return self.m_OwnerName
    
    def has_evasion_skill(self):
        """检查是否拥有飞檐走壁（闪避）技能"""
        return True  # 大盗默认拥有飞檐走壁技能