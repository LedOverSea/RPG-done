# -*- coding: utf-8 -*-

TEXT = {
	1: "第{0}回合:",
	2: "{0}战士攻击{2}战士,造成伤害{4}",
	3: "{0}发动暴雨梨花针，对{1}战士造成{2}点伤害",
	4: "{0}发动飞檐走壁，躲闪了来自{1}战士的攻击",
	5: "{0}战士由于耐力充沛，减少了{1}点伤害",
}

def TransText(iNo, lstArg):
	if not iNo in TEXT:
		return ""
	sText = TEXT[iNo]
	return sText.format(*lstArg)
