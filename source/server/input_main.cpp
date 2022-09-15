//Under:
#include "HackShield.h"
//Add:
#include "minigame_bnw.h"



//ABOVE:
int CInputMain::Analyze(LPDESC d, BYTE bHeader, const char * c_pData)
//Add:
int CInputMain::MinigameBnw(LPCHARACTER ch, const char* c_pData, size_t uiBytes)
{
	TPacketCGMinigameBnw* p = (TPacketCGMinigameBnw*) c_pData;
	
	if (uiBytes < sizeof(TPacketCGMinigameBnw))
		return -1;

	c_pData += sizeof(TPacketCGMinigameBnw);
	uiBytes -= sizeof(TPacketCGMinigameBnw);

	switch (p->subheader)
	{
		case MINIGAME_BNW_SUBHEADER_CG_START:
			{
				MinigameBnwStart(ch);
			}
			return 0;
		case MINIGAME_BNW_SUBHEADER_CG_SELECTED_CARD:
			{
				if (uiBytes < sizeof(BYTE))
					return -1;

				const BYTE card = *reinterpret_cast<const BYTE*>(c_pData);
				MinigameBnwSelectedCard(ch, card);
			}
			return sizeof(BYTE);

		case MINIGAME_BNW_SUBHEADER_CG_FINISHED:
			{
				MinigameBnwFinished(ch);
			}
			return 0;
	}
	return 0;
}



//Under:
		case HEADER_CG_CLIENT_VERSION:
			Version(ch, c_pData);
			break;
//Add:
		case HEADER_CG_MINIGAME_BNW:
			if ((iExtraLen = MinigameBnw(ch, c_pData, m_iBufferLeft))<0)
				return -1;
			break;