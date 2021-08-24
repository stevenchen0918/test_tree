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
		if Result != True:
			DL.SetWindowText("red", "Please set C7-36 = 03 first!")		
		
# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		if Result != True:
			Result = DL.SendCommand('0-use TDES to encrypt (C7-32)')
			if (Result):
				Result = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TransArmor TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 02")		
		
# C7-30 Get Data Encryption Key Variant Type
if (Result):
	RetOfStep = DL.SendCommand('C7-30 Get Data Encryption Key Variant Type = Pin')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")
		
# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Burst mode OFF		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Set group B0
if (Result):
	RetOfStep = DL.SendCommand('Set group B0')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40, MSR/ CL/ CT				
if (Result):	
	for i in range (1, 6):
		if i <= 2 or i == 5:
			RetOfStep = DL.SendCommand('Poll on Demand')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")	
			if (Result):			
				if i == 1:
					RetOfStep = DL.SendCommand('02-40, MSR -- Discover')
				if i == 2:
					RetOfStep = DL.SendCommand('02-40, CL -- Discover')		
				if i == 5:
					RetOfStep = DL.SendCommand('60-10, CT -- EMV Test Card V2 T=0')	
		if i >= 3 and i <= 4:
			RetOfStep = DL.SendCommand('Auto Poll')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")		
			if (Result):
				if i == 3:
					RetOfStep = DL.SendCommand('03-40, MSR -- Discover')
					time.sleep(1)
				if i == 4:
					RetOfStep = DL.SendCommand('03-40, CL -- Discover')
					time.sleep(1)
				
		if (RetOfStep):
			# MSR transaction
			if i == 1 or i == 3:
				if i == 1:
					sResult=DL.Get_RXResponse(0)
				if i == 3:
					sResult=DL.Get_RXResponse(1)	
				if Result == True and sResult!=None and sResult!="":
					sResult=sResult.replace(" ","")
					CardData=DL.GetTLV(sResult,"DFEE23")
					bresult = False
					if CardData!=None and CardData!='':
						objectMSR = DL.ParseCardData(CardData ,bresult,Key,MacKey)
						EncryptType = DL.Get_EncryptionKeyType_CardData()
						EncryptMode = DL.Get_EncryptionMode_CardData()
						if objectMSR!=None:
							DL.SetWindowText("blue", "Track 1:")
							Track1_CardData = DL.Get_TrackN_CardData(1)
							DL.SetWindowText("blue", "Track 2:")
							Track2_CardData = DL.Get_TrackN_CardData(2)
							DL.SetWindowText("blue", "Track 3:")
							Track3_CardData = DL.Get_TrackN_CardData(3)
							DL.SetWindowText("blue", "Track 1_Enc:")
							TRK1 = DL.Get_EncryptTrackN_CardData(1)
							DL.SetWindowText("blue", "Track 2_Enc:")
							TRK2 = DL.Get_EncryptTrackN_CardData(2)
							DL.SetWindowText("blue", "Track 3_Enc:")
							TRK3 = DL.Get_EncryptTrackN_CardData(3)
							DL.SetWindowText("blue", "KSN:")
							KSN=DL.Get_KSN_CardData()
							if len(TRK1)> 0:
								DL.SetWindowText("blue", "Track 1:")
								TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK1)
								TRK1DecryptData = TRK1DecryptData[0:((objectMSR[0].msr_track1Length)*2)]
							if len(TRK2)> 0:
								DL.SetWindowText("blue", "Track 2:")
								TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
								TRK2DecryptData = TRK2DecryptData[0:((objectMSR[0].msr_track2Length)*2)]
							if len(TRK3) > 0:
								DL.SetWindowText("blue", "Track 3:")
								TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
								TRK3DecryptData = TRK3DecryptData[0:((objectMSR[0].msr_track3Length)*2)]
									
							Tag9F39 = DL.GetTLV(sResult,"9F39")
							TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
							TagDFEE26 = DL.GetTLV(sResult,"DFEE26")
										
							# Verify specific tags
							Result = DL.Check_StringAB(Tag9F39, '90')
							if Result != True:
								DL.SetWindowText("red", "Tag9F39: FAIL")							
							Result = DL.Check_StringAB(TagFFEE01, 'DFEE30010C')
							if Result != True:
								DL.SetWindowText("red", "TagFFEE01: FAIL")	
							Result = DL.Check_StringAB(TagDFEE26, 'EC06')
							if Result != True:
								DL.SetWindowText("red", "TagDFEE26: FAIL")
																								
							# Discover	
							TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?;6510********0026=1712****************?"
							TR1plaintextdata = "2542363531303030303030303030303032365E434152442F494D414745203033202020202020202020202020205E31373132323031313030303032313030303030303F3B363531303030303030303030303032363D31373132323031313030303032313030303030303F"
											
							Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
							if Result != True:
								DL.SetWindowText("red", "TR1maskdata: FAIL")
							Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
							if Result != True:
								DL.SetWindowText("red", "TR1plaintextdata: FAIL")
			# CL transaction
			if i == 2 or i == 4:
				if (RetOfStep):
					if i == 2:
						alldata=DL.Get_RXResponse(0)
					if i == 4:
						alldata=DL.Get_RXResponse(1)	
					DL.Check_StringAB(alldata, 'F5 DF EE 12')
					ksn = DL.GetTLV(alldata,"DFEE12")	
							
					maskDFEF17 = DL.GetTLV(alldata,"DFEF17", 0)
					encDFEF17 = DL.GetTLV(alldata,"DFEF17", 1)
					decDFEF17 = DL.DecryptDLL(1,1, strKey, ksn, encDFEF17)	
							
					maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
					encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
					decDFEF18 = DL.DecryptDLL(1,1, strKey, ksn, encDFEF18)	

					tagFF8105 = DL.GetTLV(alldata,"FF8105", 0)		
					mask56 = DL.GetTLV(tagFF8105,"56", 0)
					enc56 = DL.GetTLV(tagFF8105,"56", 1)
					dec56 = DL.DecryptDLL(1,1, strKey, ksn, enc56)	
							
					mask57 = DL.GetTLV(tagFF8105,"57", 0)
					enc57 = DL.GetTLV(tagFF8105,"57", 1)
					dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
							
					Tag9F39 = DL.GetTLV(alldata,"9F39")
					TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
					TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
							
					# Tag DFEF17
					r1 = DL.Check_StringAB(maskDFEF17, '2A363531302A2A2A2A2A2A2A2A')
					r2 = DL.Check_StringAB(maskDFEF17, '5E434152442F494D414745')
					r3 = DL.Check_StringAB(maskDFEF17, '5E313731322A2A2A2A2A2A2A2A2A2A2A2A2A')
					if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "DF EF 17 A1"):
						DL.SetWindowText("blue", "Tag DFEF17_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF17_Mask: FAIL")
								
					r1 = DL.Check_StringAB(decDFEF17, 'DF EF 17')
					r2 = DL.Check_StringAB(decDFEF17, '42 36 35 31 30 30 30 30 30 30 30 30 30')
					r3 = DL.Check_StringAB(decDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
					r4 = DL.Check_StringAB(decDFEF17, '5E 31 37 31 32 32 30 31')
					if r1 == True and r2 == True and r3 == True and r4 == True and DL.Check_StringAB(alldata, "DF EF 17 C1"):
						DL.SetWindowText("blue", "Tag DFEF17_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF17_Enc: FAIL")

					# Tag DFEF18
					r1 = DL.Check_StringAB(maskDFEF18, '36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
					r2 = DL.Check_StringAB(maskDFEF18, '3D 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
					if r1 == True and r2 == True and DL.Check_StringAB(alldata, "DF EF 18 A1"):
						DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
								
					r1 = DL.Check_StringAB(decDFEF18, 'DF EF 18')
					r2 = DL.Check_StringAB(decDFEF18, '36 35 31 30 30 30 30 30 30 30 30 30')
					r3 = DL.Check_StringAB(decDFEF18, '3D 31 37 31 32 32 30 31')
					if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "DF EF 18 C1"):
						DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
								
					# Tag 56
					r1 = DL.Check_StringAB(mask56, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
					r2 = DL.Check_StringAB(mask56, '5E 43 41 52 44 2F 49 4D 41 47 45')
					r3 = DL.Check_StringAB(mask56, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
					if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "56 A1"):
						DL.SetWindowText("blue", "Tag 56_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag 56_Mask: FAIL")
							
					r1 = DL.Check_StringAB(dec56, '56')
					r2 = DL.Check_StringAB(dec56, '42 36 35 31 30 30 30 30 30 30 30 30 30')
					r3 = DL.Check_StringAB(dec56, '5E 43 41 52 44 2F 49 4D 41 47 45')
					r4 = DL.Check_StringAB(dec56, '5E 31 37 31 32 32 30 31')
					if r1 == True and r2 == True and r3 == True and r4 == True and DL.Check_StringAB(alldata, "56 C1"):
						DL.SetWindowText("blue", "Tag 56_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag 56_Enc: FAIL")
								
					# Tag 57
					r1 = DL.Check_StringAB(mask57, '65 10 CC CC CC CC')
					r2 = DL.Check_StringAB(mask57, 'D1 71 2C CC CC CC CC CC')
					if r1 == True and r2 == True and DL.Check_StringAB(alldata, "57 A1"):
						DL.SetWindowText("blue", "Tag 57_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag 57_Mask: FAIL")
								
					r1 = DL.Check_StringAB(dec57, '57')
					r2 = DL.Check_StringAB(dec57, '65 10 00 00 00 00')
					r3 = DL.Check_StringAB(dec57, 'D1 71 22 01')
					if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "57 C1"):
						DL.SetWindowText("blue", "Tag 57_Enc: PASS")
					else:
						DL.SetWindowText("red", "Tag 57_Enc: FAIL")	
								
					# Tags 9F39/ FFEE01/ DFEE26
					if Tag9F39 == "91": 
						DL.SetWindowText("blue", "Tag 9F39: PASS")
					else:
						DL.SetWindowText("Red", "Tag 9F39: FAIL")
							
					if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
						DL.SetWindowText("blue", "Tag FFEE01: PASS")
					else:
						DL.SetWindowText("Red", "Tag FFEE01: FAIL")
							
					if TagDFEE26 == "F506": 
						DL.SetWindowText("blue", "Tag DFEE26: PASS")
					else:
						DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
			# CT transaction
			if i == 5:						
				Result = Result and DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(1)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")	
				
						mask57 = DL.GetTLV(alldata,"57", 0)
						enc57 = DL.GetTLV(alldata,"57", 1)
						dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
				
						mask5A = DL.GetTLV(alldata,"5A", 0)
						enc5A = DL.GetTLV(alldata,"5A", 1)
						dec5A = DL.DecryptDLL(1,1, strKey, ksn, enc5A)	
				
						Tag9F39 = DL.GetTLV(alldata,"9F39")
						TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
						TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
						# Tag 57
						Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 A1 11'):
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
						Result = DL.Check_StringAB(dec57, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '57 C1'):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")

						# Tag 5A
						Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A A1 08'):
							DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
					
						Result = DL.Check_StringAB(dec5A, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(1), '5A C1'):
							DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
					
						# Tags 9F39/ FFEE01/ DFEE26				
						if TagFFEE01 != "DFEE300101": 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if TagDFEE26 != "E406": 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
						
						DL.SendCommand('05-01')
						
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
time.sleep(2)