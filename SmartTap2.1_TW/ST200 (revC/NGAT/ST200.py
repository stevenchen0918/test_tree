#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")	

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")			
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, tap card
if (Result):
	for i in range(1, 3):
		if i == 1:
			RetOfStep = DL.SendCommand('02-40 #9987 VAS_AND_PAY')
		if i == 2:
			RetOfStep = DL.SendCommand('02-40 #9987 VAS_OR_PAY')	
			
		if (RetOfStep):
			DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 DF EE 12 0A **")
			alldata = DL.Get_RXResponse(0)
			ksn = DL.GetTLV(alldata,"DFEE12")	
			
			mask57 = DL.GetTLV(alldata,"57", 0)
			enc57 = DL.GetTLV(alldata,"57", 1)
			dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
			
			mask5A = DL.GetTLV(alldata,"5A", 0)
			enc5A = DL.GetTLV(alldata,"5A", 1)
			dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
			
			# Tag 57
			Result1 = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC CC CC')
			Result2 = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D3 01 2C CC CC CC CC CC CC CC CC')
			if (Result1 == True or Result2 == True) and DL.Check_RXResponse("57 A1 13"):
				DL.SetWindowText("blue", "Tag 57_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Mask: FAIL")
				
			Result1 = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D2 01 21 20 00 12 33 99 00 03 1F')
			Result2 = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D3 01 21 20 00 12 33 99 00 03 1F')
			if (Result1 == True or Result2 == True) and DL.Check_RXResponse("57 C1"):
				DL.SetWindowText("blue", "Tag 57_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Enc: FAIL")

			# Tag 5A
			Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
			if Result == True and DL.Check_RXResponse("5A A1 08"):
				DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
				
			Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
			if Result == True and DL.Check_RXResponse("5A C1"):
				DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 5A_Enc: FAIL")	
				
			# Tags 9F39/ FFEE01/ DFEE26/ DFEF7B
			if (DL.Check_RXResponse("9F 39 01 07")): 
				DL.SetWindowText("blue", "Tag 9F39: PASS")
			else:
				DL.SetWindowText("Red", "Tag 9F39: FAIL")
			
			if (DL.Check_RXResponse("FF EE 01 ** DF EE 30 01 00")): 
				DL.SetWindowText("blue", "Tag FFEE01: PASS")
			else:
				DL.SetWindowText("Red", "Tag FFEE01: FAIL")
			
			if (DL.Check_RXResponse("DF EE 26 02 E3 01")): 
				DL.SetWindowText("blue", "Tag DFEE26: PASS")
			else:
				DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				
			if (DL.Check_RXResponse("DF EF 7B 01 00")): 
				DL.SetWindowText("blue", "Tag DFEF7B: PASS")
			else:
				DL.SetWindowText("Red", "Tag DFEF7B: FAIL")				