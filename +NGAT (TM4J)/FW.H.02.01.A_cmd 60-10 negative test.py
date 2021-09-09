#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
Result= True
strKey = '0123456789ABCDEFFEDCBA9876543210'

# 60-10 length/ data/ crc error
#if (Result):
#	DL.SetWindowText("black", "*** 60-10 length error")
if (Result):
	DL.SetWindowText("black", "*** 60-10 data error")
	DL.SendIOCommand("IDG", "60 10 03 00 78 00 78 9C 01 00 5F 57 01 00 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 5F 2A 02 08 40", 3000, 1) 
	Result = DL.Check_RXResponse("60 05 00 00")	
#if (Result):
#	DL.SetWindowText("black", "*** 60-10 crc error")
	
# No CT terminal data
if (Result):
	DL.SetWindowText("black", "*** 60-05 Contact Remove Terminal Data")
	DL.SendIOCommand("IDG", "60 05", 32000, 1) 
	Result = DL.Check_RXResponse("60 00")
if (Result):
	DL.SetWindowText("black", "*** 60-10 Contact Start Transaction")
	DL.SendIOCommand("IDG", "60 10 01 00 78 00 78 9C 01 00 5F 57 01 00 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 5F 2A 02 08 40", 32000, 1) 
	Result = DL.Check_RXResponse("60 60")    
    
# During CT transaction, send unrelated cmd
if (Result):
	DL.SetWindowText("black", "*** 04-09")
	DL.SendIOCommand("IDG", "04 09", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** DFED59 =  00 (Send First Response 0x63)")
	DL.SendIOCommand("IDG", "04 00 DF ED 59 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")
if (Result):
	DL.SetWindowText("black", "*** 60-06 Contact Set Terminal Data")
	DL.SendIOCommand("IDG", "60 06 18 00 5F 36 01 02 9F 1A 02 08 40 9F 35 01 25 9F 33 03 60 08 C8 9F 40 05 60 00 F0 50 01 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF 26 01 01 DF 10 08 65 6E 66 72 65 73 7A 68 DF 11 01 01 DF 27 01 00 DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1E 08 D0 9C 20 F0 C2 0E 14 00 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 30 35 30 30 DF EE 20 01 3C DF EE 21 01 0A DF EE 22 03 32 3C 3C", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")
if (Result):
	DL.SetWindowText("black", "*** 60-03 Contact Set Application Data (VISA)")
	DL.SendIOCommand("IDG", "60 03 07 00 A0 00 00 00 03 10 10 0F 00 9F 01 06 56 49 53 41 30 30 5F 57 01 00 5F 2A 02 08 40 9F 09 02 00 96 5F 36 01 02 9F 1B 04 00 00 3A 98 DF 25 03 9F 37 04 DF 28 03 9F 08 02 DF EE 15 01 01 DF 13 05 00 00 00 00 00 DF 14 05 00 00 00 00 00 DF 15 05 00 00 00 00 00 DF 18 01 00 DF 17 04 00 00 27 10 DF 19 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")
if (Result):
	DL.SetWindowText("black", "*** 60-0A Contact Set CA Public Key")
	DL.SendIOCommand("IDG", "60 0A A0 00 00 99 99 E1 01 01 F8 70 7B 9B ED F0 31 E5 8A 9F 84 36 31 B9 0C 90 D8 0E D6 95 00 00 00 03 70 00 99 C5 B7 0A A6 1B 4F 4C 51 B6 F9 0B 0E 3B FB 7A 3E E0 E7 DB 41 BC 46 68 88 B3 EC 8E 99 77 C7 62 40 7E F1 D7 9E 0A FB 28 23 10 0A 02 0C 3E 80 20 59 3D B5 0E 90 DB EA C1 8B 78 D1 3F 96 BB 2F 57 EE DD C3 0F 25 65 92 41 7C DF 73 9C A6 80 4A 10 A2 9D 28 06 E7 74 BF A7 51 F2 2C F3 B6 5B 38 F3 7F 91 B4 DA F8 AE C9 B8 03 F7 61 0E 06 AC 9E 6B", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")
    
if (Result):
	DL.SetWindowText("black", "*** 60-10 Contact Start Transaction, Please insert  EMV Test Card (T=0)..........")
	DL.SendIOCommand("IDG", "60 10 01 00 78 00 78 9C 01 00 5F 57 01 00 9F 02 06 00 00 00 00 02 00 9F 03 06 00 00 00 00 00 00 5F 2A 02 08 40", 32000, 1) 
	Result = DL.Check_RXResponse("DF EE 25 02 00 10")	
if (Result):
	DL.SetWindowText("black", "*** 18-01 Ping")
	DL.SendIOCommand("IDG", "18 01", 3000, 1) 
	Result = DL.Check_RXResponse("18 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** 12-01 Get serial number")
	DL.SendIOCommand("IDG", "12 01", 3000, 1) 
	Result = DL.Check_RXResponse("12 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** 60-07 Contact Retrieve AID List")
	DL.SendIOCommand("IDG", "60 07", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
if (Result):
	DL.SetWindowText("black", "*** 60-12 Contact Apply Host Response")
	DL.SendIOCommand("IDG", "60 12 01 8A 02 30 30 91 0A 11 22 33 44 55 66 77 88 30 30", 3000, 1) 
	Result = DL.Check_RXResponse("60 0C")	