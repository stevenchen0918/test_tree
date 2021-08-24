﻿#!/usr/bin/env python
import sys
import time
Result = True
RetOfStep = True
strKey = '0123456789ABCDEFFEDCBA9876543210'

if (Result):
	RetOfStep = DL.SendCommand('DFEE1D-00002A0B30')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 00 00 00 ")

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('Master NO3 card')
	if (RetOfStep):
		DL.Check_RXResponse(1, "56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? D3 ** DF EF 18 A1 25 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 3D 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 18 C1 30 ** 9F 6B A1 13 BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BF 9F 6B C1 20")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"DFEF18", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result1 = DL.Check_StringAB(str4, 'DFEF1825353235363833323033303030303030303D31323132353032')
		str5 = DL.GetTLV(str1,"FFEE04")
		str6 = DL.GetTLV(str5,"FFEE05",1)
		str7 = DL.GetTLV(str6,"FF8105")
		str8 = DL.GetTLV(str7,"9F6B",1)
		str9 = DL.DecryptDLL(0,2, strKey, str3, str8)
		Result2 = DL.Check_StringAB(str9, '9F6B135256832030000000D121250')
		Result = Result1 and Result2

if (Result):
	RetOfStep = DL.SendCommand('Online decline')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 03 03 00 00 00 ")

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00 ")
