# -*- coding: utf-8 -*-

SIDE_ATTACK = 0		#进攻方
SIDE_DEFEND = 1		#防守方

MSG_NEWTURN = 1		#第a轮开始 （轮数，）
MSG_ATTACK = 2		#a对b发动攻击，造成c点伤害 (进攻者名字，进攻者位置，防守者名字，防守方位置，伤害数量)
MSG_SKILL_BLOODY_RAIN = 3		#暴雨梨花针技能 (使用者名字，目标名字，伤害数量)
MSG_EVADE = 4		#闪避技能 (闪避者名字，攻击者名字)
MSG_STAMINA_DEFEND = 5	#耐力防御 (战士名字，抵消伤害值)

