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

# Enable encryption (02)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")		
		
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
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 63")
		alldata = DL.Get_RXResponse(0)
		
		mask57 = DL.GetTLV(alldata,"57", 0)
		
		mask5A = DL.GetTLV(alldata,"5A", 0)
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
	# Tag 57
		Result = DL.Check_StringAB(mask57, '47 61 73 90 01 01 00 10 D2 01 21 20 00 12 33 99 00 03 1F')
		if Result == False:
			DL.SetWindowText("red", "Tag 57: FAIL")
		else:
			DL.SetWindowText("blue", "Tag 57: PASS")

	# Tag 5A
		Result = DL.Check_StringAB(mask5A, '47 61 73 90 01 01 00 10')
		if Result == False:
			DL.SetWindowText("red", "Tag 5A: FAIL")
		else:
			DL.SetWindowText("blue", "Tag 5A: PASS")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if Tag9F39 == "07": 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if TagDFEE26 == "6301": 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")