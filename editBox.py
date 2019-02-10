from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import common 

#######################################################
class editHexBox(QGroupBox):
	''' editHexBox is meant to create a small QGroupBox
	    for simple testing/manipulation of hex value assigned
	    to this QGroupBox
	'''
	# Series of pyqtSignals to emit when buttons are pressed
	left_clicked    = pyqtSignal()
	right_clicked   = pyqtSignal()
	reset_clicked   = pyqtSignal()
	reverse_clicked = pyqtSignal()
	swap_clicked    = pyqtSignal()
	def __init__(self, *args, **kwargs):
		super(editHexBox, self).__init__(*args, **kwargs)
		self.resetValue = "0x00000000"
		self.setTitle("Manipulate")
		# Create all the Forms this widget will need
		hb_btns = QHBoxLayout()
		vb_r    = QVBoxLayout()
		hb      = QVBoxLayout()
		form    = QFormLayout()

		# Create all the buttons with their text
		btn_shift_left  = QPushButton("Shift <<")
		btn_shift_right = QPushButton("Shift >>")
		btn_reset       = QPushButton("Reset")
		btn_reverse     = QPushButton("Reverse")
		btn_swap        = QPushButton("Byte Swap")
		
		# Add all the buttons to a horizontal layout
		hb_btns.addWidget(btn_shift_left )
		hb_btns.addWidget(btn_shift_right)
		hb_btns.addWidget(btn_reset      )
		hb_btns.addWidget(btn_reverse    )
		hb_btns.addWidget(btn_swap       )
		
		# Create some line edit's w/ properties		
		self.line_hex = QLineEdit()
		self.line_dec = QLineEdit()
		self.line_bin = QLineEdit()
		self.line_hex.setReadOnly(True)
		self.line_dec.setReadOnly(True)
		self.line_bin.setReadOnly(True)		
		
		# Add some labels to the widget
		l_hex = common.simpleLabel("Hex Value")
		l_dec = common.simpleLabel("Dec Value")
		l_bin = common.simpleLabel("Binary Value")

		form.addRow(l_hex, self.line_hex)
		form.addRow(l_dec, self.line_dec)
		form.addRow(l_bin, self.line_bin)	

		# Set all the layouts 
		vb_r.addLayout(form)
		hb.addLayout(hb_btns)
		hb.addLayout(vb_r)

		# Add functionality so this does something by itself
		btn_shift_left.pressed.connect(self.left_click)
		btn_shift_right.pressed.connect(self.right_click)
		btn_reset.pressed.connect(self.reset_click)
		btn_reverse.pressed.connect(self.reverse_click)
		btn_swap.pressed.connect(self.swap_click)

		# Set the main layout
		self.setLayout(hb)

	def left_click(self):
		''' When left clicked, shift the hex value left 1  '''
		i = common.hex2dec(self.line_hex.text())
		i = (i << 1) & 0xFFFFFFFF
		value = f"'h{i:08X}"
		self.line_hex.setText(value)
		self.line_bin.setText(common.dec2bin(i))
		self.left_clicked.emit()

	def right_click(self):	
		''' When right clicked, shift the hex values right 1 '''	
		i = common.hex2dec(self.line_hex.text())
		value = f"'h{i >> 1:08X}"
		self.line_hex.setText(value)
		self.line_bin.setText(common.dec2bin(i))
		self.right_clicked.emit()

	def reverse_click(self):
		''' When reverse clicked, reverse the hex value '''
		i = common.hex2dec(self.line_hex.text())
		value = f"{i:032b}"[::-1]
		i = int(value,2)
		self.line_hex.setText(f"'h{i:08X}")
		self.line_bin.setText(common.dec2bin(i))
		self.reverse_clicked.emit()

	def swap_click(self):
		''' When swap clicked, byte swap the hex value'''
		h = self.line_hex.text()
		s = common.hexByteSwap(h)
		self.line_hex.setText("'h"+s)
		self.swap_clicked.emit()

	def reset_click(self):
		''' When reset clicked, re-apply the initial value'''
		self.line_hex.setText(self.resetValue)
		self.reset_clicked.emit()

	def getHexValue(self):
		''' Helper function to easily return the hex value 
		in its current state''' 
		return self.line_hex.text()

	def setResetValue(self, value):
		''' Set the reset value, and then apply that to all the 
		    line edit widgets. 
		'''
		self.resetValue = value
		self.line_hex.setText(self.resetValue)
		i = common.hex2dec(value)
		self.line_bin.setText(common.dec2bin(i))


class MainWindow(QMainWindow):
	''' Main application for debugging the 
	    editBox widget
	'''	
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		w = editHexBox()
		w.left_clicked.connect(self.click_left)
		w.right_clicked.connect(self.click_right)
		w.reset_clicked.connect(self.click_rst)
		w.swap_clicked.connect(self.click_swap)
		w.reverse_clicked.connect(self.click_reset)
		
		self.setCentralWidget(w)

		self.show()

	def click_rst(self):
		''' Debugging - print statement '''
		print("RESET!")

	def click_right(self):
		''' Debugging - print statement '''
		print("RIGHT!")

	def click_left(self):
		''' Debugging - print statement '''
		print("LEFT!")

	def click_swap(self):
		''' Debugging - print statement '''
		print("SWAP!")

	def click_reset(self):
		''' Debugging - print statement '''
		print("RESET!")


if __name__ == '__main__':
	 app = QApplication([])
	 window = MainWindow()
	 app.exec_()

