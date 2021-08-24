#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import clr
import binascii

DataKey="0123456789abcdeffedcba9876543210"
PinKey="0123456789abcdeffedcba9876543210"
strDecryptPIN=''
Pan='371449635398431'


Result = DL.SendCommand("Activate Transaction(MSR)")
sResult = DL.Get_RXResponse(0)


Result = DL.SendCommand("Get Online Enciphered PIN(Format4 AES)")
sResult = DL.Get_RXResponse(0)
#sResult ='56 69 56 4F 70 61 79 56 33 00 02 05 00 01 A1 00 00 00 82 02 5C 00 9F 36 02 00 01 9F 07 02 FF C0 9F 26 08 78 5A D2 22 B6 63 68 B8 9F 27 01 40 8E 0C 00 00 00 00 00 00 00 00 5F 03 00 00 81 04 00 00 00 63 9F 34 03 5F 03 02 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 0D 05 00 00 00 00 00 9F 0E 05 00 00 00 00 00 9F 0F 05 00 00 00 00 00 9F 10 07 06 01 1A 03 90 00 00 9F 24 00 9F 33 03 60 F8 C8 9F 35 01 22 95 05 42 80 00 00 00 9F 37 04 8A F3 E8 6D 9F 01 06 56 49 53 41 30 30 9F 02 06 00 00 00 00 00 99 9F 03 06 00 00 00 00 00 00 5F 25 03 95 07 01 5F 24 03 20 12 31 5A 08 47 61 73 90 01 01 00 10 5F 34 01 01 5F 28 02 08 40 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1A 02 08 40 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E 57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89 5F 2A 02 08 40 9A 03 20 03 08 9F 21 03 06 07 05 9C 01 00 9F 06 07 A0 00 00 00 03 10 10 9F 09 02 00 96 5F 20 0F 46 55 4C 4C 20 46 55 4E 43 54 49 4F 4E 41 4C 9F 20 00 5F 2D 08 65 73 65 6E 66 72 64 65 50 0A 56 49 53 41 43 52 45 44 49 54 4F 07 A0 00 00 00 03 10 10 84 07 A0 00 00 00 03 10 10 9F 39 01 05 9F 4D 00 9F 13 00 9B 02 C8 00 99 00 DF EE 23 00 DF EE 0B 00 FF EE 01 05 DF EE 30 01 01 DF EE 26 01 00 D8 70'

if sResult!=None and sResult!="":
    sResult=sResult.replace(" ","")
    sResultData=sResult[30:len(sResult)-4]
    DL.SetWindowText("BLUE", sResult)
    DL.SetWindowText("GREEN", sResultData)
    EncOlPIN_Hex=sResultData[0:64]
    PINKSN_Hex=sResultData[64:112]
    EncOlPIN=binascii.a2b_hex(EncOlPIN_Hex)
    PINKSN=binascii.a2b_hex(PINKSN_Hex)
    DL.SetWindowText("BLUE", "Enciphered PIN Block:"+EncOlPIN)
    DL.SetWindowText("GREEN", "PEK KSN:"+PINKSN)
    strDecryptPIN=DL.FormatX_PIN_Block_Decipher(1,2,PINKSN, PinKey, Pan, EncOlPIN)
    #strDecryptPIN=DL.Format4_PIN_Block_Decipher(PINKSN, PinKey, Pan, EncOlPIN)

