import sys
import PyQt5.QtWidgets as qt

def window():
   app = qt.QApplication([])
   label = qt.QLabel('jimbo')
   start_dt = qt.QDateEdit()
   label.show()
   start_dt.show()
   app.exec()
 
	
if __name__ == '__main__':
   window()