import sys
from PyQt5 import QtWidgets
from src.classes.Window import Window
import qdarktheme


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	qdarktheme.setup_theme("light")
	window = Window()
	window.show()
	sys.exit(app.exec_())
