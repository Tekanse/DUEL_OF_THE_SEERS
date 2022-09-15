#############################
#############################
#Made by Tekanse https://metin2.dev/profile/35360-tekanse/
#############################
import ui
import event
import random
import localeInfo
import player
import net
import uicommon

BNW_REQUIRED_VNUM = 19
BNW_REQUIRED_YANG = 30000

RESULTS_DICT = {
	0: [localeInfo.MINI_GAME_BNW_RESULT_DRAW1, localeInfo.MINI_GAME_BNW_RESULT_DRAW2],
	1: [localeInfo.MINI_GAME_BNW_RESULT_LOSE1, localeInfo.MINI_GAME_BNW_RESULT_LOSE2],
	2: [localeInfo.MINI_GAME_BNW_RESULT_WIN1, localeInfo.MINI_GAME_BNW_RESULT_WIN2],
}

SHOW_LINE_COUNT_MAX = 14
def LoadScript(self, fileName):
	pyScrLoader = ui.PythonScriptLoader()
	pyScrLoader.LoadScriptFile(self, fileName)

class CardOver(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.mainImage = None
		self.isAnimating = False
		self.animatingUp = True
		self.alphaValue = 0.0
		self.loopCount = 0
		self.loopCountRequired = 0
		self.eventFunc = None
		self.eventArgs = None
		self.Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.mainImage = None
		self.isAnimating = False
		self.animatingUp = True
		self.alphaValue = 0.0
		self.eventFunc = None
		self.eventArgs = None

	def SetImage(self, image):
		self.mainImage = image

	def OnUpdate(self):
		if self.isAnimating == True:
			if self.animatingUp == True:
				self.alphaValue += 0.05
				if self.alphaValue >= 1.0:
					self.animatingUp = False
			else:
				self.alphaValue -= 0.05
				if self.alphaValue <= 0.0:
					self.animatingUp = True
					self.loopCount += 1
					if self.loopCount >= self.loopCountRequired and self.loopCountRequired != -1:
						self.isAnimating = False
						self.CallEventOnAnimationEnd()
			self.mainImage.SetAlpha(self.alphaValue) 

	def StartAnimation(self, loopCountRequired):
		self.isAnimating = True
		self.alphaValue = 0.0
		self.animatingUp = True
		self.loopCount = 0
		self.loopCountRequired = loopCountRequired

	def StopAnimation(self):
		self.isAnimating = False

	def SetEventOnAnimationEnd(self, func, *args):
		self.eventFunc = func
		self.eventArgs = args

	def CallEventOnAnimationEnd(self):
		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def Close(self):
		self.mainImage.Hide()
		self.Hide()

	def Open(self):
		self.mainImage.Show()
		self.Show()

class BlackNWhiteGamePage(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.player1Cards = []
		self.player1CardsOver = []
		self.player1CardsOverClass = []
		self.player1CardsCross = []
		self.player2CardsOver = []
		self.player2CardsOverClass = []
		self.player2CardsCross = []
		self.alarmTexts = []
		self.player1CurCardOver = None
		self.player1CurCardOverClass = None
		self.player2CurCardOver = None
		self.player1MovingCard = None
		self.player2MovingCard = None
		self.player1_cur_card = None
		self.player2_cur_card = None
		self.canSelectCard = False
		self.curCardIDAnimating = 0
		self.isAnimatingText = False
		self.textPos = 0
		self.player1_score_text = None
		self.player2_score_text = None
		self.p1Points = None
		self.p2Points = None
		self.popWindow = None
		self.wPage = None
		self.questionDialog = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)


	def Destroy(self):
		self.ClearDictionary()
		self.isLoaded = 0
		self.player1Cards = []
		self.player1CardsOver = []
		self.player1CardsOverClass = []
		self.player1CardsCross = []
		self.player2CardsOver = []
		self.player2CardsOverClass = []
		self.player2CardsCross = []
		self.alarmTexts = []
		self.player1CurCardOver = None
		self.player1CurCardOverClass = None
		self.player2CurCardOver = None
		self.player1MovingCard = None
		self.player2MovingCard = None
		self.player1_cur_card = None
		self.player2_cur_card = None
		self.canSelectCard = False
		self.curCardIDAnimating = 0
		self.isAnimatingText = False
		self.textPos = 0
		self.player1_score_text = None
		self.player2_score_text = None
		self.p1Points = None
		self.p2Points = None
		self.popWindow = None
		self.wPage = None
		self.questionDialog = None

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			LoadScript(self, "UIScript/minigamebnwgamepage.py")
		except:
			import exception
			exception.Abort("BlackNWhiteGamePage.LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			for i in xrange(9):
				card = self.GetChild("player1_card%d_over" % (i))
				cardClass = CardOver()
				self.player1CardsOver.append(card)
				self.player1CardsOverClass.append(cardClass)
				cardClass.SetImage(card)

				card = self.GetChild("player2_card%d_over" % (i))
				card.SetAlpha(0.0)
				cardClass = CardOver()
				self.player2CardsOver.append(card)
				self.player2CardsOverClass.append(cardClass)
				cardClass.SetImage(card)
	
				cardCross = self.GetChild("player1_card%d_cross" % (i))
				self.player1CardsCross.append(cardCross)

				cardCross = self.GetChild("player2_card%d_cross" % (i))
				self.player2CardsCross.append(cardCross)

				card = self.GetChild("player1_card%d" % (i))
				card.SetEvent(ui.__mem_func__(self.__OnPlayerCardClick), i)
				self.player1Cards.append(card)

				self.player1CardsOverClass[0].SetEventOnAnimationEnd(ui.__mem_func__(self.Player1CardsAnimationOver), 0)
				self.player2CardsOverClass[0].SetEventOnAnimationEnd(ui.__mem_func__(self.Player2CardsAnimationOver), 0)

			card = self.GetChild("player1_cur_card_over")
			card.Hide()
			self.player1CurCardOver = card
			cardClass = CardOver()
			self.player1CurCardOverClass = cardClass
			cardClass.SetImage(card)
			card = self.GetChild("player2_cur_card_over")
			self.player2CurCardOver = card
			self.player2CurCardOver.Hide()

			self.player1_cur_card = self.GetChild("player1_cur_card")
			self.player1_cur_card.Hide()
			self.player2_cur_card = self.GetChild("player2_cur_card")
			self.player2_cur_card.Hide()

			for i in range(1, 3):
				alarm = self.GetChild("alarm_text_top%d" % (i))
				(x, y) = alarm.GetLocalPosition()
				alarm.SetPosition(x, y + 46)
				self.alarmTexts.append([alarm, y+46])
			for i in range(1, 3):
				alarm = self.GetChild("alarm_text_center%d" % (i))
				(x, y) = alarm.GetLocalPosition()
				alarm.SetPosition(x, y + 46)
				self.alarmTexts.append([alarm, y+46])

			player1_name_text = self.GetChild("player1_name_text")
			player1_name_text.SetText(player.GetName())

			self.player1_score_text = self.GetChild("player1_score_text")
			self.player2_score_text = self.GetChild("player2_score_text")
		except:
			import exception
			exception.Abort("BlackNWhiteGamePage.LoadWindow.BindObject")

		self.player1MovingCard = ui.MoveImageBox()
		self.player1MovingCard.SetParent(self.board)
		self.player1MovingCard.SetMoveSpeed(15)
		self.player1MovingCard.SetEndMoveEvent(ui.__mem_func__(self.OnP1CardMoveAnimationEnd))
		self.player1MovingCard.Hide()

		self.player2MovingCard = ui.MoveImageBox()
		self.player2MovingCard.SetParent(self.board)
		self.player2MovingCard.SetMoveSpeed(20)
		self.player2MovingCard.SetEndMoveEvent(ui.__mem_func__(self.OnP2CardMoveAnimationEnd))
		self.player2MovingCard.Hide()

		self.board.SetCloseEvent(ui.__mem_func__(self.OnPressCloseButton))

		self.popWindow = PopupWindow()

	def OnPressCloseButton(self):
		questionDialog = uicommon.QuestionDialog()
		questionDialog.SetText(localeInfo.MINI_GAME_GIVEUP_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.Close))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		questionDialog.SetWidth(450)
		questionDialog.Open()
		self.questionDialog = questionDialog

	def __OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None
	
	def Close(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def Open(self):
		if self.wPage is None:
			self.wPage = WaitingPage()
		self.wPage.Open()

	def Start(self):
		self.__LoadWindow()
		for text, baseY in self.alarmTexts:
			text.SetText("")
		self.player1_score_text.SetText("0")
		self.player2_score_text.SetText("0")
		self.HideAllCrossCards()
		self.StartPlayerTurnAnimation()
		self.Show()

	def HideAllCrossCards(self):
		for card in self.player1CardsCross:
			card.Hide()
		for card in self.player2CardsCross:
			card.Hide()

	def StartPlayerTurnAnimation(self):
		for card in self.player1CardsOverClass:
			card.StartAnimation(2)

	def Player1CardsAnimationOver(self):
		self.canSelectCard = True
		self.player1CurCardOver.Show()
		self.player1CurCardOverClass.StartAnimation(-1)

	def DrawEnemyCard(self):
		tab = []
		i = 0
		for card in self.player2CardsCross:
			if card.IsShow() == False:
				tab.append(i)
			i += 1
		id = random.choice(tab)
		self.curCardIDAnimating = id
		cardImg = 'back_white' if id % 2 == 1 else 'back_black'
		self.player2MovingCard.LoadImage("d:/ymir work/ui/minigame/bnw/%s.sub" % (cardImg))
		self.player2CardsCross[id].Show()

		(x, y) = self.player2CardsOver[id].GetLocalPosition()
		self.player2MovingCard.SetPosition(x, y)
		(x, y) = self.player2_cur_card.GetGlobalPosition()
		self.player2MovingCard.SetMovePosition(x, y)
		self.player2MovingCard.MoveStart()
		self.player2MovingCard.Show()

	def Player2CardsAnimationOver(self):
		self.DrawEnemyCard()

	def __OnPlayerCardClick(self, id):
		if self.canSelectCard == False:
			return
		self.canSelectCard = False
		self.player1CurCardOverClass.StopAnimation()
		self.player1CurCardOver.Hide()

		self.curCardIDAnimating = id
		self.player1MovingCard.LoadImage("d:/ymir work/ui/minigame/bnw/number%d.sub" % (id))
		(x, y) = self.player1CardsOver[id].GetLocalPosition()
		self.player1MovingCard.SetPosition(x, y)
		(x, y) = self.player1_cur_card.GetGlobalPosition()
		self.player1MovingCard.SetMovePosition(x, y)
		self.player1MovingCard.MoveStart()
		self.player1MovingCard.Show()

	def OnP1CardMoveAnimationEnd(self):
		self.player1MovingCard.Hide()
		self.player1CardsCross[self.curCardIDAnimating].Show()
		self.player1_cur_card.LoadImage("d:/ymir work/ui/minigame/bnw/number%d.sub" % (self.curCardIDAnimating))
		self.player1_cur_card.Show()
		net.MinigameBnwCardSelected(self.curCardIDAnimating)

	def OnP2CardMoveAnimationEnd(self):
		self.player2MovingCard.Hide()
		cardImg = 'back_white' if self.curCardIDAnimating % 2 == 1 else 'back_black'
		self.player2_cur_card.LoadImage("d:/ymir work/ui/minigame/bnw/%s.sub" % (cardImg))
		self.player2_cur_card.Show()
		self.StartTextAnimation()

	def StartPlayerTurn(self):
		if self.CountCardsLeft() <= 0:
			net.MinigameBnwFinished()
			self.Close()
			p1points = int(self.player1_score_text.GetText())
			p2points = int(self.player2_score_text.GetText())
			if p1points < p2points:
				self.popWindow.SetText(localeInfo.MINI_GAME_BNW_GAME_RESULT_LOSE % p1points, (localeInfo.MINI_GAME_BNW_GAME_RESULT_SCORE % p1points))
			elif p1points > p2points:
				self.popWindow.SetText(localeInfo.MINI_GAME_BNW_GAME_RESULT_WIN % (p1points + (p1points - p2points)), (localeInfo.MINI_GAME_BNW_GAME_RESULT_SCORE % p1points))
			else:
				self.popWindow.SetText(localeInfo.MINI_GAME_BNW_GAME_RESULT_DRAW % p1points, (localeInfo.MINI_GAME_BNW_GAME_RESULT_SCORE % p1points))
			self.popWindow.Open()

		self.StartPlayerTurnAnimation()

	def CountCardsLeft(self):
		count = 0
		for card in self.player1CardsCross:
			if card.IsShow() == False:
				count += 1
		return count

	def StartEnemyTurnAnimation(self):
		for card in self.player2CardsOverClass:
			card.StartAnimation(2)

	def StartEnemyTurn(self):
		self.StartEnemyTurnAnimation()

	def OnUpdate(self):
		if self.isAnimatingText == True:
			self.textPos += 2
			for text, baseY in self.alarmTexts:
				(x, y) = text.GetLocalPosition()
				text.SetPosition(x, baseY - self.textPos)
			if self.textPos >= 46:
				self.isAnimatingText = False
				self.ReverseTexts()
				self.SetTextsToDefaultPosition()
				self.ClearCards()
				self.SetPoints()
				self.StartPlayerTurn()

	def StartTextAnimation(self):
		self.isAnimatingText = True
		self.textPos = 0

	def SetResultText(self, result):
		i = 0
		for text, baseY in self.alarmTexts[2:4]:
			text.SetText(RESULTS_DICT[result][i])
			i += 1

	def ReverseTexts(self):
		i = 0
		for text, baseY in self.alarmTexts[0:2]:
			text.SetText(self.alarmTexts[i+2][0].GetText())
			i += 1

	def SetTextsToDefaultPosition(self):
		for text, baseY in self.alarmTexts:
			(x, y) = text.GetLocalPosition()
			text.SetPosition(x, baseY)

	def SetResult(self, result, p1Points, p2Points):
		self.SetResultText(result)
		self.p1Points = p1Points
		self.p2Points = p2Points
		self.StartEnemyTurn()

	def ClearCards(self):
		self.player1_cur_card.Hide()
		self.player2_cur_card.Hide()

	def SetPoints(self):
		self.player1_score_text.SetText(str(self.p1Points))
		self.player2_score_text.SetText(str(self.p2Points))

class PopupWindow(ui.Board):
	def __init__(self):
		ui.Board.__init__(self)
		self.SetSize(260, 110)
		self.line1 = ui.TextLine()
		self.line1.SetParent(self)
		self.line1.SetHorizontalAlignCenter()
		self.line1.SetPosition(130, 20)
		self.line1.Show()

		self.line2 = ui.TextLine()
		self.line2.SetParent(self)
		self.line2.SetHorizontalAlignCenter()
		self.line2.SetPosition(130, 50)
		self.line2.Show()

		self.OKButton = ui.Button()
		self.OKButton.SetParent(self)
		self.OKButton.SetUpVisual("d:/ymir work/ui/public/acceptbutton00.sub")
		self.OKButton.SetOverVisual("d:/ymir work/ui/public/acceptbutton01.sub")
		self.OKButton.SetDownVisual("d:/ymir work/ui/public/acceptbutton02.sub")
		self.OKButton.SetWindowHorizontalAlignCenter()
		self.OKButton.SetEvent(ui.__mem_func__(self.Close))
		self.OKButton.SetPosition(0, 75)
		self.OKButton.Show()

	def __del__(self):
		ui.Board.__del__(self)

	def SetText(self, l1, l2):
		self.line1.SetText(l1)
		self.line2.SetText(l2)

	def Open(self):
		self.SetCenterPosition()
		self.Show()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE


class WaitingPage(ui.ScriptWindow):
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet( self.descIndex )

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.descIndex		= 0
		self.desc_y			= 7
		self.board = None
		self.desc_board = None
		self.descriptionBox = None
		self.desc_prev_button = None
		self.desc_next_button = None
		self.game_start_button = None
		self.game_page = None
		self.questionDialog = None
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			LoadScript(self, "UIScript/minigamebnwwaitingpage.py")
		except:
			import exception
			exception.Abort("WaitingPage.LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.desc_board = self.GetChild("desc_board")
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.SetParent(self.desc_board)
			self.descriptionBox.Show()
			self.desc_prev_button = self.GetChild("prev_button")
			self.desc_prev_button.SAFE_SetEvent(self.__OnClickDescPrevButton)
			self.desc_next_button = self.GetChild("next_button")
			self.desc_next_button.SAFE_SetEvent(self.__OnClickDescNextButton)

			self.game_start_button = self.GetChild("game_start_button")
			self.game_start_button.SAFE_SetEvent(self.__OnClickStartButton)
		except:
			import exception
			exception.Abort("WaitingPage.LoadWindow.BindObject")

		self.board.SetCloseEvent(self.Close)


	def Close(self):
		event.ClearEventSet(self.descIndex)
		self.Hide()

	def Open(self):
		self.__LoadWindow()
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet("locale/en/black_and_white_desc.txt")

		event.SetVisibleLineCount(self.descIndex, 14)

		event.SetRestrictedCount(self.descIndex, 80)
		event.Skip(self.descIndex)
		
		if self.descriptionBox:
			self.descriptionBox.Show()

		self.Show()

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.desc_board.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)

	def __OnClickDescPrevButton(self):
	
		line_height			= 16

		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = SHOW_LINE_COUNT_MAX
		
		if cur_start_line - decrease_count < 0:
			return

		event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
		self.desc_y += ( line_height * decrease_count )
		
	def __OnClickDescNextButton(self):
	
		line_height			= 16

		total_line_count	= event.GetLineCount(self.descIndex)
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		increase_count = SHOW_LINE_COUNT_MAX
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )

	def __OnClickStartButton(self):
		questionDialog = uicommon.QuestionDialog()
		questionDialog.SetText(localeInfo.MINI_GAME_BNW_START_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__OnGameStart))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		questionDialog.SetWidth(550)
		questionDialog.Open()
		self.questionDialog = questionDialog

	def __OnGameStart(self):
		self.questionDialog.Close()
		self.Close()
		if player.GetItemCountByVnum(BNW_REQUIRED_VNUM) <= 0:
			self.questionDialog = uicommon.PopupDialog()
			self.questionDialog.SetText(localeInfo.MINI_GAME_BNW_NOT_ENOUGH_ITEM)
			self.questionDialog.Open()
			return
		if player.GetMoney() < BNW_REQUIRED_YANG:
			self.questionDialog = uicommon.PopupDialog()
			self.questionDialog.SetText(localeInfo.MINI_GAME_BNW_NOT_ENOUGH_YANG)
			self.questionDialog.Open()
			return
		net.MinigameBnwStart()

	def __OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE
