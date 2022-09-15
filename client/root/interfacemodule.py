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