#include "stdafx.h"
#include "utils.h"
#include "minigame_bnw.h"
#include "char.h"
#include <algorithm>
#include <random>

DWORD BNW_REWARD_VNUM = 50100;
DWORD BNW_REQUIRED_VNUM = 19;
int BNW_REQUIRED_YANG = 30000;
void MinigameBnwStart(LPCHARACTER ch)
{
	if (ch->GetGold() < BNW_REQUIRED_YANG)
		return;

	if (ch->CountSpecifyItem(BNW_REQUIRED_VNUM) <= 0)
		return;

	ch->RemoveSpecifyItem(BNW_REQUIRED_VNUM, 1);
	ch->PointChange(POINT_GOLD, -BNW_REQUIRED_YANG, true);

	ch->SetMinigameBnwStarted(true);
	ch->m_vMinigameBnwMyCards.clear();
	ch->m_vMinigameBnwEnemyCards.clear();
	ch->MinigameBnwSetPlayerPoints(0);
	ch->MinigameBnwSetEnemyPoints(0);
	for (BYTE i = 0; i < 9; i++)
	{
		ch->m_vMinigameBnwEnemyCards.push_back(i);
	}

	auto rd = std::random_device {}; 
	auto rng = std::default_random_engine { rd() };
	std::shuffle(std::begin(ch->m_vMinigameBnwEnemyCards), std::end(ch->m_vMinigameBnwEnemyCards), rng);

	//Use with c++98
	//std::srand(get_dword_time());
	//std::random_shuffle(ch->m_vMinigameBnwEnemyCards.begin(), ch->m_vMinigameBnwEnemyCards.end());

	TPacketGCMinigameBnw p;
	p.header		= HEADER_GC_MINIGAME_BNW;
	p.subheader		= MINIGAME_BNW_SUBHEADER_GC_START;

	ch->GetDesc()->Packet(&p, sizeof(TPacketGCMinigameBnw));
}

void MinigameBnwSelectedCard(LPCHARACTER ch, BYTE bCard)
{
	if (!ch->IsMinigameBnwStarted())
		return;
	if (std::find(ch->m_vMinigameBnwMyCards.begin(), ch->m_vMinigameBnwMyCards.end(), bCard) != ch->m_vMinigameBnwMyCards.end())
		return;
	ch->m_vMinigameBnwMyCards.push_back(bCard);

	BYTE enemyCard = ch->m_vMinigameBnwEnemyCards.back();
	ch->m_vMinigameBnwEnemyCards.pop_back();

	BYTE bState = 0;
	if (bCard < enemyCard)
	{
		ch->MinigameBnwSetEnemyPoints(ch->MinigameBnwGetEnemyPoints() + 1);
		bState = 1;
	}
	else if (bCard > enemyCard)
	{
		ch->MinigameBnwSetPlayerPoints(ch->MinigameBnwGetPlayerPoints() + 1);
		bState = 2;
	}

	TPacketGCMinigameBnw p;
	p.header		= HEADER_GC_MINIGAME_BNW;
	p.subheader		= MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT;

	TPacketGCMinigameBnwDrawResult p2;
	p2.result = bState;
	p2.playerPoints = ch->MinigameBnwGetPlayerPoints();
	p2.enemyPoints = ch->MinigameBnwGetEnemyPoints();

	ch->GetDesc()->BufferedPacket(&p, sizeof(TPacketGCCatchKing));
	ch->GetDesc()->Packet(&p2, sizeof(TPacketGCCatchKingSelected));
}

void MinigameBnwFinished(LPCHARACTER ch)
{
	if (!ch->IsMinigameBnwStarted())
		return;
	if (ch->m_vMinigameBnwEnemyCards.size() != 0)
		return;

	ch->SetMinigameBnwStarted(false);
	BYTE diff = 0;
	if (ch->MinigameBnwGetPlayerPoints() > ch->MinigameBnwGetEnemyPoints())
	{
		diff = ch->MinigameBnwGetPlayerPoints() - ch->MinigameBnwGetEnemyPoints();
	}
	ch->m_vMinigameBnwMyCards.clear();

	ch->AutoGiveItem(BNW_REWARD_VNUM, ch->MinigameBnwGetPlayerPoints() + diff);
}
