﻿#!/usr/bin/env python
import sys
import time
RetOfStep = True
Result=True
strKey = '0123456789ABCDEFFEDCBA9876543210'

if (Result):
	RetOfStep = DL.SendCommand('DFEE1D-06042A0C31')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 00 00 00 00")

if (Result):
	RetOfStep = DL.SendCommand('Select data DUKPT Slot0')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 81 09 00 00 00 90 6C")

if (Result):
	RetOfStep = DL.SendCommand('Discover')
	if (RetOfStep):
		DL.Check_RXResponse(1, "56 69 56 4F 70 61 79 56 33 00 02 05 23 ?? ?? D3 DF EF 17 A1 41 2A 36 30 31 31 30 30 2A 2A 2A 2A 2A 2A 34 32 37 31 5E 44 49 53 43 4F 56 45 52 2F 4E 45 54 57 4F 52 4B 20 20 20 20 20 20 20 20 20 20 5E 31 31 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 17 C1 50 ** DF EF 18 A1 25 36 30 31 31 30 30 2A 2A 2A 2A 2A 2A 34 32 37 31 3D 31 31 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A DF EF 18 C1 30 ** 56 A1 41 2A 36 30 31 31 30 30 2A 2A 2A 2A 2A 2A 34 32 37 31 5E 44 49 53 43 4F 56 45 52 2F 4E 45 54 57 4F 52 4B 20 20 20 20 20 20 20 20 20 20 5E 31 31 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 56 C1 50 ** 57 A1 13 60 11 00 CC CC CC 42 71 D1 11 21 01 CC CC CC CC CC CC CC 57 C1 20")
		str1 = DL.Get_RXResponse(1)
		str2 = DL.GetTLV(str1,"DFEF17", 1)
		str3 = DL.GetTLV(str1,"DFEE12")
		str4 = DL.DecryptDLL(0,2, strKey, str3, str2)
		Result = DL.Check_StringAB(str4, 'DFEF174142363031313030303939313930343237315E444953434F5645522F4E4554574F524B202020202020202020205E3131313231303131303030313635353935353031')
		str5 = DL.GetTLV(str1,"DFEF18", 1)
		str6 = DL.DecryptDLL(0,2, strKey, str3, str5)
		Result = DL.Check_StringAB(str6, 'DFEF1825363031313030303939313930343237313D3131313231303131303030313635353935353031')
		str7 = DL.GetTLV(str1,"FFEE04")
		str8 = DL.GetTLV(str7,"FFEE05")
		str9 = DL.GetTLV(str8,"FF8105")
		str10 = DL.GetTLV(str9,"56", 1)
		str11 = DL.DecryptDLL(0,2, strKey, str3, str10)
		Result = DL.Check_StringAB(str11, '564142363031313030303939313930343237315E444953434F5645522F4E4554574F524B202020202020202020205E3131313231303131303030313635353935353031')
		str12 = DL.GetTLV(str9,"57", 1)
		str13 = DL.DecryptDLL(0,2, strKey, str3, str12)
		Result = DL.Check_StringAB(str13, '57136011000991904271D11121011000165595501F')

if (Result):
	RetOfStep = DL.SendCommand('Set parameter defaults')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("56 69 56 4F 70 61 79 56 33 00 04 09 00 00 00")