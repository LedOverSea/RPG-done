import pygame
from astar import Point


class Sprite:
	"""用于绘制精灵图的工具类"""

	@staticmethod
	def draw(dest, source, x, y, cell_x, cell_y, cell_w=48, cell_h=48):
		"""
		绘制精灵图中，指定x,y的图像
		:param dest: surface类型，要绘制到的目标surface
		:param source: surface类型，来源surface
		:param x: 绘制图像在dest中的坐标
		:param y: 绘制图像在dest中的坐标
		:param cell_x: 在精灵图中的格子坐标
		:param cell_y: 在精灵图中的格子坐标
		:param cell_w: 单个精灵的宽度
		:param cell_h: 单个精灵的高度
		:return:
		"""
		dest.blit(source, (x, y), (cell_x * cell_w, cell_y * cell_h, cell_w, cell_h))


class Array2D:
	"""
		说明：
			1.构造方法需要两个参数，即二维数组的宽和高
			2.成员变量w和h是二维数组的宽和高
			3.使用：‘对象[x][y]’可以直接取到相应的值
			4.数组的默认值都是0
	"""

	def __init__(self, w, h, default=0):
		self.m_Width = w
		self.m_Height = h
		self.m_DataList = []
		self.m_DataList = [[default for y in range(h)] for x in range(w)]

	def show_array2d(self):
		for y in range(self.m_Height):
			for x in range(self.m_Width):
				print(self.m_DataList[x][y], end=' ')
			print("")

	def __getitem__(self, item):
		return self.m_DataList[item]


class CGameMap(Array2D):
	"""
	游戏地图类
	"""

	def __init__(self, bottom, top, x, y):
		# 将地图划分成w*h个小格子，每个格子48*48像素
		w = int(bottom.get_width() / 48) + 1
		h = int(top.get_height() / 48) + 1
		super().__init__(w, h)
		self.m_Bottom = bottom
		self.m_Top = top
		self.x = x
		self.y = y
		self.m_Map_data = [
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,],
				[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1,],
				[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,],
				[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
				[1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
				[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
				[1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
			]

	def draw_bottom(self, screen_surf):
		screen_surf.blit(self.m_Bottom, (self.x, self.y))

	def draw_top(self, screen_surf):
		screen_surf.blit(self.m_Top, (self.x, self.y))

	def draw_grid(self, screen_surf):
		"""
		画网格
		"""
		for x in range(self.m_Width):
			for y in range(self.m_Height):
				if self[x][y] == 0:  # 不是障碍，画空心的矩形
					pygame.draw.rect(screen_surf, (255, 255, 255), (self.x + x * 48, self.y + y * 48, 48, 48), 1)
				else:  # 是障碍，画黑色实心的矩形
					pygame.draw.rect(screen_surf, (0, 0, 0), (self.x + x * 48 + 1, self.y + y * 48 + 1, 30, 30), 0)

	def roll(self, role_x, role_y, WIN_WIDTH=640, WIN_HEIGHT=480):
		"""
		地图滚动
		:param role_x: 角色相对于地图的坐标
		:param role_y:
		"""
		if role_x < WIN_WIDTH / 2:
			self.x = 0
		elif role_x > self.m_Bottom.get_width() - WIN_WIDTH / 2:
			self.x = -(self.m_Bottom.get_width() - WIN_WIDTH)
		else:
			self.x = -(role_x - WIN_WIDTH / 2)

		if role_y < WIN_HEIGHT / 2:
			self.y = 0
		elif role_y > self.m_Bottom.get_height() - WIN_HEIGHT / 2:
			self.y = -(self.m_Bottom.get_height() - WIN_HEIGHT)
		else:
			self.y = -(role_y - WIN_HEIGHT / 2)

	def IsAllowWalk(self, tPos):
		if not self.m_Map_data[tPos[1]][tPos[0]]:
			return True
		else:
			return False

	def load_walk_file(self, path):
		"""
		读取可行走区域文件
		"""
		with open(path, 'r') as file:
			for x in range(self.m_Width):
				for y in range(self.m_Height):
					v = int(file.readline())
					self[x][y] = v


class CharWalk:
	"""
	人物行走类 char是character的缩写
	"""
	DIR_DOWN = 0
	DIR_LEFT = 1
	DIR_RIGHT = 2
	DIR_UP = 3

	def __init__(self, hero_surf, char_id, dir, mx, my, obj=None):
		"""
		:param hero_surf: 精灵图的surface
		:param char_id: 角色id
		:param dir: 角色方向
		:param mx: 角色所在的小格子坐标
		:param my: 角色所在的小格子坐标
		"""
		self.m_HeroSurf = hero_surf
		self.m_CharID = char_id
		self.m_Dir = dir
		self.mx = mx
		self.my = my
		self.m_SubGameObj = obj					 #游戏运行对象

		self.m_Frame = 1  # 角色当前帧
		self.x = mx * 48  # 角色相对于地图的坐标
		self.y = my * 48
		# 角色下一步需要去的格子
		self.m_NextPosX = 0
		self.m_NextPosY = 0
		self.step = 2       # 每帧移动的像素
		self.m_PathList = []      # 寻路路径

		# 当前路径下标
		self.m_iPathIndex = 0

		self.m_IsWalking = False  # 角色是否正在移动
		self.m_IsWalkDone = True
		self.m_IsFight = False
		self.m_NextDest = None

	def SetPathData(self, data):
		path = []
		if data[7] is None:
			return

		if self.m_IsWalking:
			self.m_PathList = []
			self.m_iPathIndex = 0
			self.m_IsWalkDone = True

		for point in data[7]:
			path.append(Point(point[0], point[1]))

		if not path:
			return
		self.m_PathList = path
		self.m_iPathIndex = data[7].index(data[2]) + 1
		
		iNextPosIdx = min(len(self.m_PathList)-1, self.m_iPathIndex)
		self.m_NextPosX, self.m_NextPosY = data[7][iNextPosIdx]
		self.m_IsWalkDone = False

	def draw(self, screen_surf, map_x, map_y):
		cell_x = self.m_CharID % 12 + int(self.m_Frame)
		cell_y = self.m_CharID // 12 + self.m_Dir
		Sprite.draw(screen_surf, self.m_HeroSurf, map_x + self.x, map_y + self.y, cell_x, cell_y)

	def goto(self, x, y):
		"""
		:param x: 目标点
		:param y: 目标点
		"""
		self.m_NextPosX = x
		self.m_NextPosY = y

		# 设置人物面向
		if self.m_NextPosX > self.mx:
			self.m_Dir = CharWalk.DIR_RIGHT
		elif self.m_NextPosX < self.mx:
			self.m_Dir = CharWalk.DIR_LEFT

		if self.m_NextPosY > self.my:
			self.m_Dir = CharWalk.DIR_DOWN
		elif self.m_NextPosY < self.my:
			self.m_Dir = CharWalk.DIR_UP

		self.m_IsWalking = True

	def move(self):
		if not self.m_IsWalking:
			return
		dest_x = self.m_NextPosX * 48
		dest_y = self.m_NextPosY * 48

		# 向目标位置靠近
		if self.x < dest_x:
			self.x += self.step
			if self.x >= dest_x:
				self.x = dest_x
		elif self.x > dest_x:
			self.x -= self.step
			if self.x <= dest_x:
				self.x = dest_x

		if self.y < dest_y:
			self.y += self.step
			if self.y >= dest_y:
				self.y = dest_y
		elif self.y > dest_y:
			self.y -= self.step
			if self.y <= dest_y:
				self.y = dest_y

		# 改变当前帧
		self.m_Frame = (self.m_Frame + 0.1) % 3
		
		# 角色当前位置
		self.mx = int(self.x / 48)
		self.my = int(self.y / 48)
		# 到达了目标点
		if self.x == dest_x and self.y == dest_y:
			self.m_Frame = 1
			self.m_IsWalking = False

	def logic(self):
		if self.m_IsWalkDone:
			return
		
		if self.x%48==0 and self.y%48==0 and self.m_NextDest:
			self.m_SubGameObj.m_CliCmdObj.C2SPlayerMove(self.m_NextDest)
			self.m_NextDest = None
			return
		self.move()

		# 如果角色正在移动，就不管它了
		if self.m_IsWalking:
			return
		if not self.m_PathList:
			return
		
		# 如果寻路走到终点了
		tEndPos = (self.m_PathList[-1].x, self.m_PathList[-1].y)
		if (self.mx, self.my) == tEndPos:
			self.m_PathList = []
			self.m_iPathIndex = 0
			self.m_IsWalkDone = True

			self.CheckFight()

		# 如果没走到终点，就往下一个格子走
		else:
			try:
				self.goto(self.m_PathList[self.m_iPathIndex].x, self.m_PathList[self.m_iPathIndex].y)
				self.m_iPathIndex += 1
			except Exception as e:
				if self.m_IsWalking:
					print(e, "频繁请求! 正在寻路中...")
					return

	def CheckFight(self):
		for oplayer in self.m_SubGameObj.m_OtherPlayerList:
			for dx, dy in self.m_SubGameObj.m_DireList:
				nx, ny = self.mx + dx, self.my + dy

				if oplayer.m_PosX == nx and oplayer.m_PosY == ny:
					self.m_IsFight = True
					self.m_SubGameObj.m_CliCmdObj.C2SFight(oplayer.m_iNpcIdx)
				else:
					self.m_IsFight = False


class CPlayer(CharWalk):
	"""玩家类"""
	def __init__(self, hero_surf, char_id, dir, mx, my, name="name", uuid = 999, obj = None, iRole=0):
		self.m_Name = name  		# 昵称
		self.m_Uuid = uuid  		# uuid 玩家的唯一标识
		self.m_PosX = mx
		self.m_PosY = my
		self.m_iPlayerID = char_id
		self.m_iNpcIdx = -1
		super().__init__(hero_surf, iRole, dir, mx, my, obj=obj)

class CNpc(CharWalk):
	
	m_Image = {
		2:"./sources/img/character/box.png",
		#3:"./sources/img/character/chicken.png",
	}
	
	def __init__(self, iType, iMapID, mx, my, oGame):
		sSourcePath = self.m_Image[iType]
		hero_surf = pygame.image.load(sSourcePath).convert_alpha()
		self.m_MapID = iMapID
		super(CNpc, self).__init__(hero_surf, 0, CharWalk.DIR_DOWN, mx, my, oGame)
		
	def draw(self, screen_surf, map_x, map_y):
		tPos = (map_x + self.x, map_y + self.y)
		screen_surf.blit(self.m_HeroSurf, tPos)
		
class CThief(CPlayer):
	
	def __init__(self, hero_surf, char_id, dir, mx, my, name="name", uuid = 999, obj = None, iRole=0):
		super().__init__(hero_surf, char_id, dir, mx, my, name=name, uuid = uuid, obj = obj, iRole=48)
