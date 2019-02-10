#!/usr/bin/env python
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import common 
import editBox

BYTES = [    0,  1,  2,  3,
			 8,  9, 10, 11,
			16, 17, 18, 19,
			24, 25, 26, 27  ]

#######################################################
class hexBox(QWidget):
	expandable = pyqtSignal(int, int)
	clicked = pyqtSignal()
	ohno = pyqtSignal()

	def __init__(self, x, y, *args, **kwargs):
		super(hexBox, self).__init__(*args, **kwargs)

		self.setFixedSize(QSize(25, 30))
		self.is_revealed = False
		self.x = x
		self.y = y
		
		self.l = QLabel()
		self.l.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		#self.l.setText("")

		hb = QHBoxLayout()
		hb.addWidget(self.l)
		self.setLayout(hb)

	def setText(self,val):
		self.l.setText(val)
		if val != '0':
			f = self.l.font()			
			f.setBold(True)
			self.l.setStyleSheet("color: rgb(25,25,112)")			
		else:
			f = self.l.font()
			f.setBold(False)
			self.l.setStyleSheet("color: black;")
		self.l.setFont(f)

		self.reset()

	def reset(self):
		self.update()

	def paintEvent(self, event):
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)

		r = event.rect()
		# http://www.discoveryplayground.com/computer-programming-for-kids/rgb-colors/
		# https://contrast-ratio.com
		if self.x in BYTES:
			color = self.palette().color(QPalette.Background)
			outer, inner = Qt.black, QColor(240,230,140)
		else:
			outer, inner = Qt.black, QColor(238,229,222)

		p.fillRect(r, QBrush(inner))
		pen = QPen(outer)
		pen.setWidth(1)
		p.setPen(pen)
		p.drawRect(r)

#######################################################
class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		w    = QWidget()
		form_l = QFormLayout()
		form_r = QFormLayout()
		vb     = QVBoxLayout()
		hb_top = QHBoxLayout()
		self.individual_hex = {}

		self.edit_box = editBox.editHexBox()
		
		self.line_hex = QLineEdit()
		self.line_dec = QLineEdit()
		self.line_bin = QLineEdit()
		self.line_hex.setStyleSheet("background-color: cyan; color: black ")
				
		self.line_hex.setText("")
		
		self.grid = QGridLayout()
		self.grid.setSpacing(1)

		reg_ex = QRegExp("^(0[xX]|'[hH])?[A-Fa-f0-9]{1,8}")
		hex_validator = QRegExpValidator(reg_ex, self.line_hex)
		self.line_hex.setValidator(hex_validator)

		l_hex = common.simpleLabel("Hex Value")
		l_dec = common.simpleLabel("Dec Value")
		l_bin = common.simpleLabel("Binary Value")

		form_l.addRow(l_hex, self.line_hex)
		form_l.addRow(l_dec, self.line_dec)
		form_l.addRow(l_bin, self.line_bin)	
		
		hb_top.addLayout(form_l)
		hb_top.addWidget(self.edit_box)

		vb.addLayout(hb_top)
		vb.addLayout(self.grid)

		w.setLayout(vb)

		self.add_things()

		self.setCentralWidget(w)

		self.line_hex.textChanged.connect(self.hex2dec)

		self.edit_box.left_clicked.connect(self.updatePicture)
		self.edit_box.right_clicked.connect(self.updatePicture)
		self.edit_box.reset_clicked.connect(self.updatePicture)
		self.edit_box.reverse_clicked.connect(self.updatePicture)
		self.edit_box.swap_clicked.connect(self.updatePicture)

		self.hex2dec()
		self.show()


	def hex2dec(self):
		self.edit_box.line_hex.setText(self.line_hex.text())
		self.edit_box.setResetValue(self.line_hex.text())
		h = self.edit_box.line_hex.text()
		i = common.hex2dec(h)
		self.line_dec.setText(f"{i:,}")
		self.line_bin.setText(common.dec2bin(i))		
		self.updatePicture()

	def updatePicture(self):
		h = self.edit_box.line_hex.text()
		i = common.hex2dec(h)
		self.edit_box.line_dec.setText(f"{i:,}")
		self.edit_box.line_bin.setText(common.dec2bin(i))
		self.setHex(i)

	def add_things(self):
		y = 1
		for x in range(0,32):			
			m = hexBox(x, y)
			l = QLabel()
			l.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
			l.setText(f"{x}")
			r = 31 - x
			self.individual_hex[f"{r}"] = m
			self.grid.addWidget(m, y, x)
			self.grid.addWidget(l, y+1, r)

	def setHex(self, i):
		for x in range(0,32):
			bit = i >> x
			if bit % 2 != 0:
				B = 1
			else:
				B = 0
			self.individual_hex[f"{x}"].setText(f"{B}")

#######################################################
if __name__ == '__main__':
	 app = QApplication([])
	 window = MainWindow()
	 app.exec_()

