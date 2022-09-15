//At the end of file, before:
};
//Add:
	public:
		bool SendMinigameBnwStart();
		bool SendMinigameBnwCardSelected(BYTE bCard);
		bool SendMinigameBnwFinished();

	protected:
		bool RecvMinigameBnw();