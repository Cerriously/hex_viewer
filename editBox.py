from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import common 

#######################################################
class editHexBox(QGroupBox):
	left_clicked    = pyqtSignal()
	right_clicked   = pyqtSignal()
	reset_clicked   = pyqtSignal()
	reverse_clicked = pyqtSignal()
	swap_clicked    = pyqtSignal()
	def __init__(self, *args, **kwargs):
		super(editHexBox, self).__init__(*args, **kwargs)
		self.resetValue = "0x00000000"
		self.setTitle("Edit")
		hb_btns = QHBoxLayout()
		vb_r = QVBoxLayout()
		hb = QVBoxLayout()

		btn_shift_left  = QPushButton("Shift <<")
		btn_shift_right = QPushButton("Shift >>")
		btn_reset       = QPushButton("Reset")
		btn_reverse     = QPushButton("Reverse")
		btn_swap        = QPushButton("Byte Swap")
		
		hb_btns.addWidget(btn_shift_left )
		hb_btns.addWidget(btn_shift_right)
		hb_btns.addWidget(btn_reset      )
		hb_btns.addWidget(btn_reverse    )
		hb_btns.addWidget(btn_swap       )

		form = QFormLayout()
		self.line_hex = QLineEdit()
		self.line_dec = QLineEdit()
		self.line_bin = QLineEdit()
		self.line_hex.setReadOnly(True)
		self.line_dec.setReadOnly(True)
		self.line_bin.setReadOnly(True)		

		l_hex = QLabel()
		l_hex.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		l_hex.setText("Hex Value")

		l_dec = QLabel()
		l_dec.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		l_dec.setText("Dec Value")

		l_bin = QLabel()
		l_bin.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		l_bin.setText("Binary Value")


		form.addRow(l_hex, self.line_hex)
		form.addRow(l_dec, self.line_dec)
		form.addRow(l_bin, self.line_bin)	

		vb_r.addLayout(form)
		hb.addLayout(hb_btns)
		hb.addLayout(vb_r)

		btn_shift_left.pressed.connect(self.left_click)
		btn_shift_right.pressed.connect(self.right_click)
		btn_reset.pressed.connect(self.reset_click)
		btn_reverse.pressed.connect(self.reverse_click)
		btn_swap.pressed.connect(self.swap_click)
		
		self.setLayout(hb)

	def left_click(self):
		i = common.hex2dec(self.line_hex.text())
		i = (i << 1) & 0xFFFFFFFF
		value = f"'h{i:08X}"
		self.line_hex.setText(value)
		self.line_bin.setText(common.dec2bin(i))
		self.left_clicked.emit()

	def right_click(self):		
		i = common.hex2dec(self.line_hex.text())
		value = f"'h{i >> 1:08X}"
		self.line_hex.setText(value)
		self.line_bin.setText(common.dec2bin(i))
		self.right_clicked.emit()

	def reverse_click(self):
		i = common.hex2dec(self.line_hex.text())
		value = f"{i:032b}"[::-1]
		i = int(value,2)
		self.line_hex.setText(f"'h{i:08X}")
		self.line_bin.setText(common.dec2bin(i))
		self.reverse_clicked.emit()

	def swap_click(self):		
		h = self.line_hex.text()
		s = common.hexByteSwap(h)
		self.line_hex.setText("'h"+s)
		self.swap_clicked.emit()

	def reset_click(self):
		self.line_hex.setText(self.resetValue)
		self.reset_clicked.emit()

	def getHexValue(self):
		return self.line_hex.text()

	def setResetValue(self, value):
		self.resetValue = value
		self.line_hex.setText(self.resetValue)
		i = common.hex2dec(value)
		self.line_bin.setText(common.dec2bin(i))

#######################################################

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		w = editHexBox()
		w.left_clicked.connect(self.click_left)
		w.right_clicked.connect(self.click_right)
		w.reset_clicked.connect(self.click_rst)
		self.setCentralWidget(w)

		self.show()

	def click_rst(self):
		print("RESET!")

	def click_right(self):
		print("RIGHT!")

	def click_left(self):
		print("LEFT!")

#######################################################
if __name__ == '__main__':
	 app = QApplication([])
	 window = MainWindow()
	 app.exec_()

