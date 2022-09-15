#Under:
import miniMap
#Add:
import uiminigameblacknwhite



#Under:
		self.dlgRefineNew.Hide()
#Add:
		self.dlgMinigameBnw = uiminigameblacknwhite.BlackNWhiteGamePage()
		self.dlgMinigameBnw.Hide()



#Under:
		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()
#Add:
		if self.dlgMinigameBnw:
			self.dlgMinigameBnw.Destroy()



#Under:
		del self.dlgRefineNew
#Add:
		del self.dlgMinigameBnw



#Under:
	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)
#Add:
	def MinigameBnwOpen(self):
		self.dlgMinigameBnw.Open()

	def MinigameBnwStart(self):
		self.dlgMinigameBnw.Start()

	def MinigameBnwSetResult(self, result, playerPoints, enemyPoints):
		self.dlgMinigameBnw.SetResult(result, playerPoints, enemyPoints)