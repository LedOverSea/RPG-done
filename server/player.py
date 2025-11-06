# -*- coding: utf-8 -*-

import dbctrl.saveobject
import pubglobalmanager
import warreport.report

class CPlayer(dbctrl.saveobject.CSaveData):
	
	m_BirthPos = (1, 1)
	
	def __init__(self, iPlayer):
		super(CPlayer, self).__init__(iPlayer)
		self.m_SocketID = -1		#连接的编号
		self.m_MapUnitIdx = -1		#地图上小人编号
		self.m_ReportMgr = warreport.report.CReportMgr(iPlayer)
		self.m_CacheUnitData = {}	#地图上小人的数据
		
	def GetKey(self):
		return "player_%s" % self.m_ID
	
	def Load(self, dData):
		if not dData:
			return
		super(CPlayer, self).Load(dData)
		self.m_ReportMgr.Load(dData["Report"])
		self.m_CacheUnitData = dData["Unit"]
		
	def Save(self):
		dData = super(CPlayer, self).Save()
		dData["Report"] = self.m_ReportMgr.Save()
		
		oMap = pubglobalmanager.GetGlobalManager("map")
		oUnit = oMap.GetUnit(self.m_MapUnitIdx)
		dData["Unit"] = oUnit.Save() if oUnit else {}
		return dData

	def SetSocketID(self, iID):
		self.m_SocketID = iID
		
	def SetMapUnitIdx(self, iIdx):
		self.m_MapUnitIdx = iIdx
		
	def New(self):
		super(CPlayer, self).New()
		self.Set("NewFlag", 1)
		
	def IsNew(self):
		return self.Query("NewFlag", 0)
		
	def NewCreate(self, sPwd):
		self.Set("Pwd", sPwd)
		self.Set("Name", "玩家%s"%self.m_ID)
		
	def Name(self):
		return self.Query("Name", "")

	def RealLogin(self):
		oMap = pubglobalmanager.GetGlobalManager("map")
		oMap.PlayerEnter(self)
		self.Delete("NewFlag")
		
		oCommand = pubglobalmanager.GetGlobalManager("commandctrl")
		oCommand.S2CLoginSuc(self.m_SocketID)
		
		#self.m_ReportMgr.RefreshAll()

#登录成功前的协议，内存无玩家对象
def LoginCommand(oLink):
	iSubProtocol = oLink.UnpackHead()
	if iSubProtocol == 1:
		LoginCheck(oLink)

#登录成功后的协议，内存有玩家对象
def GameCommand(oLink):
	iPlayerID = oLink.GetPlayerID()
	oObjManager = pubglobalmanager.GetGlobalManager("saveobjmanager")
	oPlayer = oObjManager.GetItem(iPlayerID)
	if not oPlayer:
		return
	iSubProtocol = oLink.UnpackHead()
	if iSubProtocol == 1:
		PlayerMove(oPlayer, oLink)
	elif iSubProtocol == 2:
		EnterFight(oPlayer, oLink)

def LoginCheck(oLink):
	oCommand = pubglobalmanager.GetGlobalManager("commandctrl")
	oObjManager = pubglobalmanager.GetGlobalManager("saveobjmanager")
	sPlayerID = oLink.UnpackHead()
	sClientPwd = oLink.UnpackHead()
	
	if not sPlayerID.isdigit():
		oCommand.S2CNotify(oLink, "账号错误")
		return
	iReEnter = 1
	iPlayerID = int(sPlayerID)
	oPlayer = oObjManager.GetItem(iPlayerID)
	if not oPlayer:						#获取不到oPlayer，即玩家对象实体不在内存中
		iReEnter = 0					#无旧对象
		oPlayer = CPlayer(iPlayerID)	#创建玩家对象
		oPlayer.Init()					#尝试从数据库读取该账号历史数据
	
	if oPlayer.IsNew():					#该账号无历史数据，即第一次创建账号。设置sClientPwd为该账号初始密码
		oPlayer.NewCreate(sClientPwd)
		oPlayer.SetSocketID(oLink.m_ID)
		oLink.SetPlayerID(iPlayerID)
		oPlayer.RealLogin()				#执行登录后续流程比如 刷新数据等
		return
	
	sPwd = oPlayer.Query("Pwd")			#该账号有历史数据，即旧账号，需要校验密码
	if sPwd != sClientPwd:
		oCommand.S2CNotify(oLink, "密码错误")
		oCommand.S2CLoginFail(oLink.m_ID)
		if not iReEnter:
			oPlayer.Remove()			#无旧对象且密码错误,删除多创建的临时对象
		return
	oPlayer.SetSocketID(oLink.m_ID)
	oLink.SetPlayerID(iPlayerID)
	oPlayer.RealLogin()					#执行登录后续流程比如 刷新数据等
	
def PlayerMove(oPlayer, oLink):
	x = oLink.UnpackHead()
	y = oLink.UnpackHead()
	oMap = pubglobalmanager.GetGlobalManager("map")
	oMap.UnitMove(oPlayer.m_MapUnitIdx, (x,y))
	
def EnterFight(oPlayer, oLink):
	iFightUnitIdx = oLink.UnpackHead()
	oMap = pubglobalmanager.GetGlobalManager("map")
	oMap.EnterFight(oPlayer, iFightUnitIdx)
	
	