//Under:
			Set(HEADER_GC_HS_REQUEST, CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketHSCheck), STATIC_SIZE_PACKET));
//Add:
			Set(HEADER_GC_MINIGAME_BNW, CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCMinigameBnw), STATIC_SIZE_PACKET));