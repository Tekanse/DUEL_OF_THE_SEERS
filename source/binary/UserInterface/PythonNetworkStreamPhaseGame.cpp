//Under:
			case HEADER_GC_HS_REQUEST:
				ret = RecvHSCheckRequest();
				break;
//Add:
			case HEADER_GC_MINIGAME_BNW:
				ret = RecvMinigameBnw();
				break;


//At the end of file add:
bool CPythonNetworkStream::SendMinigameBnwStart()
{
	TPacketCGMinigameBnw packet;
	packet.header = HEADER_CG_MINIGAME_BNW;
	packet.subheader = MINIGAME_BNW_SUBHEADER_CG_START;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("SendMinigameBnwStart Error");
		return false;
	}
	return SendSequence();
}

bool CPythonNetworkStream::SendMinigameBnwCardSelected(BYTE bCard)
{
	TPacketCGMinigameBnw packet;
	packet.header = HEADER_CG_MINIGAME_BNW;
	packet.subheader = MINIGAME_BNW_SUBHEADER_CG_SELECTED_CARD;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("SendMinigameBnwCardSelected Error");
		return false;
	}

	if (!Send(sizeof(BYTE), &bCard))
	{
		Tracen("SendMinigameBnwCardSelected Error2");
		return false;
	}

	Tracenf("SendMinigameBnwCardSelected");
	return SendSequence();
}

bool CPythonNetworkStream::SendMinigameBnwFinished()
{
	TPacketCGMinigameBnw packet;
	packet.header = HEADER_CG_MINIGAME_BNW;
	packet.subheader = MINIGAME_BNW_SUBHEADER_CG_FINISHED;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("SendMinigameBnwFinished Error");
		return false;
	}
	return SendSequence();
}

bool CPythonNetworkStream::RecvMinigameBnw()
{
	TPacketCGMinigameBnw p;
	Tracef("RecvMinigameBnw\n");
	if (!Recv(sizeof(p), &p))
		return false;

	switch (p.subheader)
	{
		case MINIGAME_BNW_SUBHEADER_GC_START:
		{
			Tracef("RecvMinigameBnw MINIGAME_BNW_SUBHEADER_GC_START\n");
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_MinigameBnwStart", Py_BuildValue("()"));
			break;
		}
		case MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT:
		{
			Tracef("RecvMinigameBnw MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT\n");
			TPacketGCMinigameBnwDrawResult result;
			if (!Recv(sizeof(TPacketGCMinigameBnwDrawResult), &result))
				return false;
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_MinigameBnwDrawResult", Py_BuildValue("(iii)", result.result, result.playerPoints, result.enemyPoints));
			break;
		}
	}
	return true;
}

