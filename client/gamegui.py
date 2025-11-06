from pgu import gui

import report

class SimpleDialog(gui.Dialog):
	def __init__(self, obj = None):
		self.m_GameObj = obj
		self.m_Title = gui.Label("About RPG Fighting")
		self.m_Title.set_font(font=self.m_GameObj.font)
		self.m_Width = 400
		self.m_Height = 200
		self.m_Doc = gui.Document(x=0, y=0, width=self.m_Width, height=self.m_Height)
		self.m_Space = self.m_Title.style.font.size(" ")
		self.m_Doc.block(align=-1)       #左对齐 (-1, 0, 1)

		for word in "GAME FIGHT REPORT":
			oWord = gui.Label(word)
			oWord.set_font(font=self.m_GameObj.font)

			self.m_Doc.add(oWord)
			self.m_Doc.space(self.m_Space)
		self.m_Doc.br(self.m_Space[1])

		gui.Dialog.__init__(self, self.m_Title, gui.ScrollArea(self.m_Doc, self.m_Width, self.m_Height))

	def SetDialogData(self, lstArg):
		lstText = lstArg[3]
		for lstLine in lstText:
			iNo, lstArg = lstLine[0], lstLine[1:]
			sMsg = report.TransText(iNo, lstArg)
			self.DealMsg(sMsg)
				# print(sMsg)

	def DealMsg(self, sMsg):
		for word in sMsg.strip():
			oWord = gui.Label(word)
			oWord.set_font(font=self.m_GameObj.font)
			self.m_Doc.add(oWord)
			self.m_Doc.space(self.m_Space)
		self.m_Doc.br(self.m_Space[1])

	def close(self, *args, **kwargs):
		self.m_GameObj.AppGuiInit()
		self.m_GameObj.update()

		return super(SimpleDialog, self).close(*args, **kwargs)





