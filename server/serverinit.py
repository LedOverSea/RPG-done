# -*- coding: utf-8 -*-
import os
import clientsocket
import timecontrol
import threading
import pubdefines
import commandctrl
import mutexlock
import dbctrl
import objmanager
import mapobj
import pubglobalmanager

def InitModule():
	InitLogDir()
	objmanager.Init()
	clientsocket.Init()
	timecontrol.Init()
	commandctrl.Init()
	mutexlock.Init()
	dbctrl.Init()
	mapobj.Init()
	
def StartGame():
	pubdefines.FormatPrint("启动服务器")
	LoadServerConsole()
	clientsocket.Start()
	
def Main():
	InitModule()
	StartGame()
	

def LoadServerConsole():
	oThread = threading.Thread(target=ServerConsoleStart)
	oThread.start()

def ServerConsoleStart():
	while True:
		try:
			sCommand = input()
			ExecCommand(sCommand)
		except Exception as e:
			print(e)
			
def ExecCommand(sCommand):
	if sCommand == "shutdown":
		ShutDown()
	elif sCommand == "test":
		Test()
	elif sCommand.startswith("reload"):
		sModule = sCommand[7:]
	
def ShutDown():
	#1 断开连接
	oSocketMgr = pubglobalmanager.GetGlobalManager("socketmgr")
	oSocketMgr.Stop()
	#2 存盘
	oSaveMgr = pubglobalmanager.GetGlobalManager("saveobjmanager")
	oSaveMgr.SaveAll()
	print("-------------------服务器退出完毕-------------------")
	
	
	
def Test():
	oSaveMgr = pubglobalmanager.GetGlobalManager("saveobjmanager")
	oSave = oSaveMgr.GetItem(0)
	print(oSave.Save())
	oSave.SaveSql()
	
def InitLogDir():
	try:
		os.mkdir("log")
	except:
		pubdefines.FormatPrint("log目录已经存在")

if __name__ == "__main__":
	Main()
