#Under:
	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)
#Add:
	def BINARY_MinigameBnwStart(self):
		self.interface.MinigameBnwStart()

	def BINARY_MinigameBnwDrawResult(self, result, playerPoints, enemyPoints):
		self.interface.MinigameBnwSetResult(result, playerPoints, enemyPoints)
