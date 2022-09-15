//Under:
		DWORD GetLogOffInterval() const { return m_dwLogOffInterval; }
//Add:
	public:
		DWORD m_dwFishingBarTimer;	

	public:
		bool IsMinigameBnwStarted() { return m_bMinigameBnwIsStarted; }
		void SetMinigameBnwStarted(bool bIsStarted) { m_bMinigameBnwIsStarted = bIsStarted; }
		std::vector<BYTE> m_vMinigameBnwMyCards;
		std::vector<BYTE> m_vMinigameBnwEnemyCards;
		void MinigameBnwSetPlayerPoints(BYTE bPoints) { m_bMinigameBnwPlayerPoints = bPoints; }
		BYTE MinigameBnwGetPlayerPoints() { return m_bMinigameBnwPlayerPoints; }
		void MinigameBnwSetEnemyPoints(BYTE bPoints) { m_bMinigameBnwEnemyPoints = bPoints; }
		BYTE MinigameBnwGetEnemyPoints() { return m_bMinigameBnwEnemyPoints; }

	private:
		bool m_bMinigameBnwIsStarted;
		BYTE m_bMinigameBnwPlayerPoints;
		BYTE m_bMinigameBnwEnemyPoints;