import pygame,sys, time
from pgu import gui
from gamegui import SimpleDialog
from defines import UNIT_PLAYER

import clientnet
from core import CGameMap, CharWalk, CPlayer, CNpc, CThief

g_Game = None	   # 全局单例


def GetGame(name='0', pswd='0'):
	global g_Game
	if g_Game is None:
		g_Game = CGame("MMORPG World", 640, 480, name=name, pswd=pswd)
	return g_Game


class CGame:
	def __init__(self, title, width, height, fps=60, name="9", pswd="9"):
		"""
		:param title: 游戏窗口的标题
		:param width: 游戏窗口的宽度
		:param height: 游戏窗口的高度
		:param fps: 游戏每秒刷新次数
		"""
		self.m_Title = title
		self.m_Width = width
		self.m_Height = height

		self.m_Fps = fps
		self.m_ListenerList = []
		self.m_GameReport = []
		self.m_IsLogin = 0  # 0未登录 1已登录

		self.m_DireList = [[0, 1], [0, -1], [1, 0], [-1, 0]]

		self.m_OtherPlayerList = []
		self.m_CtrlBornList = []
		self.m_OtherPlayerDict = {}
		self.m_OtherMapUnit = {}

		self.m_sName = name
		self.m_sPwd = pswd
		self.m_HasReport = 0

		self.InitPyGame()
		self.AppGuiInit()
		self.InitGame()

	def InitPyGame(self):
		"""pygame相关的初始化操作"""
		pygame.init()
		pygame.font.init()
		self.font = pygame.font.Font('.\sources\Font\simhei.ttf', 10)

		pygame.display.set_caption(self.m_Title)
		self.m_Screen = pygame.display.set_mode([self.m_Width, self.m_Height])
		self.m_Clock = pygame.time.Clock()
		self.RegisteCmd()

	def InitGame(self):
		"""我们游戏的一些初始化操作"""
		self.m_Hero = pygame.image.load('./sources/img/character/hero.png').convert_alpha()
		self.m_MapBottom = pygame.image.load('./sources/img/map/0.png').convert_alpha()
		self.m_MapTop = pygame.image.load('./sources/img/map/0_top.png').convert_alpha()
		self.m_GameMapObj = CGameMap(self.m_MapBottom, self.m_MapTop, self.m_Width, self.m_Height)
		# self.m_GameMapObj.load_walk_file('./sources/img/map/0.map')

		self.connect()
		self.m_CliCmdObj = clientnet.GetClientCommand()
		self.m_iPlayerID = 0
		self.login()
		self.role = CPlayer(self.m_Hero, self.m_iPlayerID, CharWalk.DIR_DOWN, 1, 1, obj=self)

	def RegisteCmd(self):
		clientnet.RegisterCommand(2, self.OnLoginSuc)
		clientnet.RegisterCommand(3, self.OnLoginFail)
		clientnet.RegisterCommand(4, self.OnPlayerRefresh)
		clientnet.RegisterCommand(5, self.OnRefreshReport)

	def OnLoginSuc(self, lstArg):
		print("登录成功  Welcome")
		self.m_IsLogin = 1

	def OnLoginFail(self, lstArg):
		print("登录失败  ComeOn BB")
		self.login()

	def OnRefreshReport(self, lstArg):
		self.m_HasReport = 1
		self.m_DialogObj.SetDialogData(lstArg)
		
	def AppGuiInit(self):
		self.m_App = gui.App()
		self.m_App.rect = pygame.Rect(0, 0, 50, 50)
		self.m_App.connect(gui.QUIT, self.m_App.quit, None)
		self.m_App.screen = self.m_Screen

		self.m_DialogObj = SimpleDialog(obj=self)
		oTemp = gui.Container(width=self.m_Width, height=self.m_Height)
		self.m_App.init(oTemp)     #

		self.m_CatObj = gui.Table(width=self.m_Width, height=self.m_Height)
		self.m_CatObj.tr()
		self.m_CatObj.td(self.m_DialogObj)                                    #

	def ShowDialog(self):
		try:
			# self.m_App.paint(self.m_Screen)
			self.m_App.run(self.m_CatObj, self.m_Screen, delay=20)

		except Exception as e:
			print(e, "等待战报数据，请重试...")
			# import traceback
			# traceback.print_exc()

	def connect(self):
		# 与服务端建立连接
		oClient = clientnet.GetClientSocket()
		oClient.Connect()
		oClient.start()

	def login(self):
		"""登录"""
		print("欢迎进入MMORPG世界~")
		print(self.m_sName, self.m_sPwd)

		username = self.m_sName
		password = self.m_sPwd
		#  username = input("请输入账号：")
		# password = input("请输入密码：")
		self.m_iPlayerID = int(username)

		self.m_CliCmdObj.C2SLogin(username, password)

	def OnPlayerRefresh(self, data):
		iType = data[1]
		if iType == UNIT_PLAYER:
			self.DealPlayer(data)
		else:
			self.DealNpc(data)
		
	def DealPlayer(self, data):
		if self.m_iPlayerID == data[3]:
			self.role.mx, self.role.my = data[2][0], data[2][1]
			self.role.x, self.role.y = data[2][0]*48, data[2][1]*48
			if not bool(data[7]):
				return
			self.role.SetPathData(data)
			self.role.m_PosX, self.role.m_PosY = data[7][-1][0], data[7][-1][1]
			self.role.m_iNpcIdx = data[0]
		else:
			self.dealotherdata(data)
			
	def DealNpc(self, data):
		iMapID = data[0]
		iType = data[1]
		tMPos = data[2]
		if not iMapID in self.m_OtherMapUnit:
			if iType == 2:
				oUnit = CNpc(iType, iMapID, tMPos[0], tMPos[1], self)
			else:
				oUnit = CThief(self.m_Hero, data[3], CharWalk.DIR_DOWN, data[2][0], data[2][1], name=str(data[3]) + "号玩家", uuid=data[3], obj=self)
			self.m_OtherMapUnit[iMapID] = oUnit
			
		oUnit = self.m_OtherMapUnit[iMapID]
		oUnit.mx, oUnit.my = data[2][0], data[2][1]
		oUnit.x, oUnit.y = data[2][0]*48, data[2][1]*48
		oUnit.SetPathData(data)

	def dealotherdata(self, data):
		if self.m_CtrlBornList is None or data[3] not in self.m_CtrlBornList:
			self.m_CtrlBornList.append(data[3])

		for iplayer in self.m_CtrlBornList:
			if iplayer == data[3]:
				if self.m_OtherPlayerDict.get(iplayer) is None:
					oplayer = CPlayer(self.m_Hero, data[3], CharWalk.DIR_DOWN, data[2][0], data[2][1], name=str(data[3]) + "号玩家", uuid=data[3], obj=self)
					oplayer.m_iNpcIdx = data[0]
					self.m_OtherPlayerList.append(oplayer)
					self.m_OtherPlayerDict.setdefault(iplayer, oplayer)

				if iplayer in self.m_OtherPlayerDict.keys():
					oplayer = self.m_OtherPlayerDict[iplayer]
					oplayer.mx, oplayer.my = data[2][0], data[2][1]
					oplayer.x, oplayer.y = data[2][0]*48, data[2][1]*48
					if not bool(data[7]):
						return
					oplayer.SetPathData(data)
					oplayer.m_iNpcIdx = data[0]
					oplayer.m_PosX, oplayer.m_PosY = data[7][-1][0], data[7][-1][1]
					

	def update(self):
		while not self.m_App._quit:
			self.m_Clock.tick(self.m_Fps)
			if self.m_IsLogin == 0:	# 还未登录的时候，没必要执行这些逻辑
				continue
			# 逻辑更新
			self.role.logic()
			self.event_handler()

			# 其他玩家逻辑（移动逻辑）
			for oplayer in self.m_OtherPlayerDict.values():
				oplayer.logic()

			self.m_GameMapObj.roll(self.role.x, self.role.y)
			# 画面更新
			self.m_GameMapObj.draw_bottom(self.m_Screen)
			self.role.draw(self.m_Screen, self.m_GameMapObj.x, self.m_GameMapObj.y)

			# 绘制其他玩家
			for player in self.m_OtherPlayerDict.values():
				player.draw(self.m_Screen, self.m_GameMapObj.x, self.m_GameMapObj.y)
				
			for oNpc in self.m_OtherMapUnit.values():
				oNpc.logic()
				oNpc.draw(self.m_Screen, self.m_GameMapObj.x, self.m_GameMapObj.y)
				
			self.m_GameMapObj.draw_top(self.m_Screen)
			pygame.display.update()
			
			if self.m_HasReport:
				self.m_HasReport = 0
				self.ShowDialog()

	def event_handler(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 3:     #鼠标右键
					mouse_x, mouse_y = pygame.mouse.get_pos()
					mx = int((mouse_x - self.m_GameMapObj.x) / 48)
					my = int((mouse_y - self.m_GameMapObj.y) / 48)

					if not self.m_GameMapObj.IsAllowWalk((mx, my)):
						continue
					
					if not self.role.m_IsWalking:
						self.m_CliCmdObj.C2SPlayerMove((mx, my))		 #上传数据
					else:
						self.role.m_NextDest = (mx, my)
			else:
				self.m_App.event(event)
