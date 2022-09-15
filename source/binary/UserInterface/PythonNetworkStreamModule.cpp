//Under:
		{ "RecvGuildSymbol",						netRecvGuildSymbol,							METH_VARARGS },
//Add:
		{ "MinigameBnwStart",						netMinigameBnwStart,						METH_VARARGS },
		{ "MinigameBnwCardSelected",				netMinigameBnwCardSelected,					METH_VARARGS },
		{ "MinigameBnwFinished",					netMinigameBnwFinished,						METH_VARARGS },



//ABOVE:
void initnet()
//Add:
PyObject* netMinigameBnwStart(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream& rkNetStream = CPythonNetworkStream::Instance();
	rkNetStream.SendMinigameBnwStart();
	return Py_BuildNone();
}

PyObject* netMinigameBnwCardSelected(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream& rkNetStream = CPythonNetworkStream::Instance();

	BYTE bCard = 0;
	if (!PyTuple_GetByte(poArgs, 0, &bCard))
		return Py_BuildException();
	rkNetStream.SendMinigameBnwCardSelected(bCard);
	return Py_BuildNone();
}

PyObject* netMinigameBnwFinished(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream& rkNetStream = CPythonNetworkStream::Instance();

	rkNetStream.SendMinigameBnwFinished();
	return Py_BuildNone();
}