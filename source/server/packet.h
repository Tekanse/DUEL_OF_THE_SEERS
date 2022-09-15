//To GC packets add (you may need to change number if its already taken, but it need to match clientside):
	HEADER_GC_MINIGAME_BNW			= 171,


//To CG packets add (you may need to change number if its already taken, but it need to match clientside):
	HEADER_CG_MINIGAME_BNW			= 85,

//ABOVE:
#pragma pack()
//Add:
typedef struct SPacketCGMinigameBnw
{
	BYTE header;
	BYTE subheader;
} TPacketCGMinigameBnw;

enum 
{
	MINIGAME_BNW_SUBHEADER_CG_START,
	MINIGAME_BNW_SUBHEADER_CG_SELECTED_CARD,
	MINIGAME_BNW_SUBHEADER_CG_FINISHED,
};

typedef struct SPacketGCMinigameBnw
{
	BYTE header;
	BYTE subheader;
} TPacketGCMinigameBnw;

enum 
{
	MINIGAME_BNW_SUBHEADER_GC_START,
	MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT,
};

typedef struct SPacketGCMinigameBnwDrawResult
{
	BYTE result;
	BYTE playerPoints;
	BYTE enemyPoints;
} TPacketGCMinigameBnwDrawResult;

