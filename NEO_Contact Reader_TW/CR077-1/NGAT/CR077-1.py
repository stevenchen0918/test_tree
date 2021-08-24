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

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")	

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")
		
# Burst mode OFF & Auto Poll		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Auto poll')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	

if (Result):
	DL.ShowMessageBox('Notice','cmd 03-40 will be sent all the time (100 cycles), insert card (EMV Test Card, T=0) in ANY time. Note: this is stress test, you should repeat above action until the case was stopped', 0)
		
	for i in range(99):	
		RetOfStep = DL.SendCommand('03-40')
		if (RetOfStep):
			Result = DL.Check_RXResponse("03 00 ** E0")
			if (Result):
				RetOfStep = DL.SendCommand('Activate Transaction_60-10')
				if (RetOfStep):
					Result = Result and DL.Check_RXResponse("60 63 00 00")
					alldata = DL.Get_RXResponse(1)
					CTresultcode = DL.GetTLV(alldata,"DFEE25")
					if (Result):
						Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
						if (Result):
							ksn = DL.GetTLV(alldata,"DFEE12")	
							mask57 = DL.GetTLV(alldata,"57", 0)
							enc57 = DL.GetTLV(alldata,"57", 1)
							dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
					
							mask5A = DL.GetTLV(alldata,"5A", 0)
							enc5A = DL.GetTLV(alldata,"5A", 1)
							dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
					
							# Tag 57
							Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
							if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 A1 11'):
								DL.SetWindowText("blue", "Tag 57_Mask: PASS")
							else:
								DL.SetWindowText("red", "Tag 57_Mask: FAIL")
						
							Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
							if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 C1 18'):
								DL.SetWindowText("blue", "Tag 57_Enc: PASS")
							else:
								DL.SetWindowText("red", "Tag 57_Enc: FAIL")

							# Tag 5A
							Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
							if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A A1 08'):
								DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
							else:
								DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
						
							Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
							if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A C1 10'):
								DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
							else:
								DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
						else:
							break

					# cmd 60-11					
					if  CTresultcode == "0010":
						Result = True
						RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction')
						if (RetOfStep):
							Result = Result and DL.Check_RXResponse("60 63 00 00")
							alldata = DL.Get_RXResponse(1)
							CTresultcode = DL.GetTLV(alldata,"DFEE25")	
							if (Result):
								Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
							
							# cmd 60-12
							if  CTresultcode == "0004":
								Result = True
								RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response')
								if (RetOfStep):
									Result = Result and DL.Check_RXResponse("60 63 00 00")
									alldata = DL.Get_RXResponse(1)
									CTresultcode = DL.GetTLV(alldata,"DFEE25")
									if (Result):
										Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
						
				DL.ShowMessageBox('Notice','Please remove card then click OK', 0)			