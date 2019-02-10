#!/usr/bin/env python
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def simpleLabel(text):
	''' Create a simple label object
	'''
	l = QLabel()
	l.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
	l.setText(text)
	return l

def hex2dec(h):
	''' Function : hex2dec
	    Enter a string input, and return an integer output
	    Valid input can be the following:
	    0x000
	    0x0000_0000
	    'h0000_0000
	    0000_0000
	    000
	    0x
	    11
	    0x11
	'''
	REPLACE = ["0x","0X", "h","H", "_", "'"]
	m_str = h 
	for item in REPLACE:
		m_str = m_str.replace(item,"")

	if len(m_str) == 0:
		m_str = "0"	
	i = int(m_str,16)
	return i

def dec2bin(d):
	''' Create a binary string with an '_' every 4 spaces.
	'''
	i      = int(d)
	binary = f"{i:032b}"
	l_binary = []
	for item in binary:		
		l_binary.append(item)
	for i in range(len(l_binary))[::-4][1:]:
		l_binary.insert(i+1,"_")
	result = "".join(l_binary)
	return result

def hexByteSwap(h):
	''' Byte Swap a hex value
	'''
	i    = hex2dec(h)
	val  = f"{i:08x}"
	swap = val[2:4] + val[0:2] + val[6:8] + val[4:6]
	return swap





