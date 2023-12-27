from PyQt5 import QtWidgets, uic, QtGui
from src.classes import Container
from src.handlers import clear_all, save_image, load_image, apply, change_label_text, search_areas, remove_image, find_image, clear_areas, sort_images
from src.modules.database.DataBase import DataBase


class Window(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		uic.loadUi("src/assets/window.ui", self)
		self.setWindowIcon(QtGui.QIcon("src/assets/logo.ico"))

		# Инициализация данных
		self.container = Container(None, None, DataBase())
		self.container.database.load("src/modules/database/data.json")

		# Инициализация текста
		self.loadImageLabel.setText(f'Загруженное изображение: ')
		self.findAreasLabel.setText(f'Всего найдено: 0')
		self.databaseAreasLabel.setText(f'Взято из базы данных: 0')
		self.countRepeatLabel.setText(f'Попыток потрачено: 0')
		self.thisIsLabel.setText(f'Скорее всего это...')

		# Настройка виджетов
		self.tabWidget.setTabIcon(0, QtGui.QIcon("src/assets/logo.ico"))
		self.tabWidget.setTabIcon(1, QtGui.QIcon("src/assets/analyze.ico"))
		self.tabWidget.setTabIcon(2, QtGui.QIcon("src/assets/database.ico"))
		self.error_dialog = QtWidgets.QMessageBox()
		self.error_dialog.setWindowTitle("Внимание!")
		self.error_dialog.setWindowIcon(QtGui.QIcon("src/assets/logo.ico"))
		self.imagesListView.setModel(self.container.database)
		self.imagesListView.setSpacing(16)

		# Обработчики нажатий
		self.loadImagePushButton.clicked.connect(lambda: self.run_function_safely(load_image, self))
		self.clearPushButton.clicked.connect(lambda: self.run_function_safely(clear_all, self))
		self.applyAllPushButton.clicked.connect(lambda: self.run_function_safely(apply, self))
		self.searchAreasPushButton.clicked.connect(lambda: self.run_function_safely(search_areas, self))
		self.clearAreasPushButton.clicked.connect(lambda: self.run_function_safely(clear_areas, self))
		self.saveImagePushButton.clicked.connect(lambda: self.run_function_safely(save_image, self))
		self.findImagePushButton.clicked.connect(lambda: self.run_function_safely(find_image, self))
		self.removeImagePushButton.clicked.connect(lambda: self.run_function_safely(remove_image, self))
		self.maxFilterSlider.valueChanged.connect(lambda value: change_label_text(self, self.maxFilterLabel, value))
		self.binarizationSlider.valueChanged.connect(lambda value: change_label_text(self, self.binarizationLabel, value))
		self.morphologyDilationSlider.valueChanged.connect(lambda value: change_label_text(self, self.morphologyDilationLabel, value))
		self.percentSlider.valueChanged.connect(lambda value: change_label_text(self, self.percentLabel, value / 100))
		self.sortImagesByHashPushButton.clicked.connect(lambda: sort_images(self, "hash"))
		self.sortImagesByIdPushButton.clicked.connect(lambda: sort_images(self, "id"))

	def closeEvent(self, event):
		self.container.database.save("src/modules/database/data.json")
		event.accept()

	def clear_ui(self):
		self.loadImageLabel.setText(f'Загруженное изображение: ')
		self.image0Label.clear()
		self.image1Label.clear()
		self.image2Label.clear()
		self.image3Label.clear()
		self.image4Label.clear()
		self.contrastDoubleSpinBox.setValue(1)
		self.maxFilterSlider.setValue(3)
		self.binarizationSlider.setValue(128)
		self.morphologyDilationSlider.setValue(3)

	def run_function_safely(self, func, *args):
		try:
			func(*args)
		except Exception as e:
			error_dialog = QtWidgets.QMessageBox()
			error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
			error_dialog.setWindowTitle("Ошибка!")
			error_dialog.setText(f"Произошла ошибка {str(e)}")
			error_dialog.setWindowIcon(QtGui.QIcon("src/assets/logo.ico"))
			error_dialog.exec_()

