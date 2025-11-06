# -*- coding: utf-8 -*-
import pubdefines

'''
g_GlobalManager中以key-value的形式，保存了全局唯一的对象
可以通过接口GetGlobalManager(key)获取到全局唯一的对象
'''

if not "g_GlobalManager" in globals():
	global g_GlobalManager
	g_GlobalManager = {}


def SetGlobalManager(sKey, obj):
	global g_GlobalManager
	g_GlobalManager[sKey] = obj


def GetGlobalManager(sKey):
	global g_GlobalManager
	return g_GlobalManager.get(sKey, None)

def DelGlobalManager(sKey):
	global g_GlobalManager
	if sKey in g_GlobalManager:
		del g_GlobalManager[sKey]

def CallManagerFunc(sKey, sFunc, *args):
	obj = GetGlobalManager(sKey)
	oFunc = getattr(obj, sFunc, None)
	if not oFunc:
		pubdefines.LogFile("err", "%s %s is not exist" % (sKey, sFunc))
		return None
	return oFunc(*args)