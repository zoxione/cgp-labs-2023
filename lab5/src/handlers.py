import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from src.algorithms.general import p_hash_to_html
from src.classes import Window
from src.classes.BmpFile import BmpFile
from src.modules.analyze_image import recursive_connected_areas
from src.modules.analyze_image.hamming_distance import hamming_distance
from src.modules.database import Entry
from src.modules.preparation_image import maximum_filter, grayscale, binarization, morphology_dilation


def clear_all(win):
	win.container.clear_data()
	win.clear_ui()


def change_label_text(win, label, text):
	label.setText(f'{text}')


def load_image(win):
	files = QFileDialog.getOpenFileName(win, "Open File", "variant1/", "BMP Files (*.bmp)")
	if files[0] != '':
		clear_all(win)
		with open(files[0], 'rb') as file:
			bmp_file = BmpFile(files[0])
		bmp_file.show()
		win.container.current_bmp_file = bmp_file
		win.loadImageLabel.setText(f'Загруженное изображение: {bmp_file.name}, {bmp_file.biWidth}x{bmp_file.biHeight}, {bmp_file.biBitCount}')


def apply(win):
	if win.container.current_bmp_file is None:
		win.error_dialog.setText('Выберите изображение')
		win.error_dialog.exec()
		return

	win.image0Label.clear()
	win.image1Label.clear()
	win.image2Label.clear()
	win.image3Label.clear()
	win.image4Label.clear()

	contrast_factor = win.contrastDoubleSpinBox.value()
	maximum_filter_size = win.maxFilterSlider.value()
	binarization_threshold = win.binarizationSlider.value()
	morphology_dilation_size = win.morphologyDilationSlider.value()

	win.container.current_bmp_file.save_file(f'src/modules/preparation_image/images/0_original.bmp')
	image = win.container.current_bmp_file.to_image()
	win.image0Label.setPixmap(QPixmap.fromImage(image))

	# 1. Приведение исходного полноцветного изображения к полутоновому: уровень контрастности, 24-бит RGB в 8-бит GRAYSCALE
	bmp_file1 = grayscale(win.container.current_bmp_file, contrast_factor=contrast_factor)
	bmp_file1.save_file(f'src/modules/preparation_image/images/1_grayscale.bmp')
	image1 = bmp_file1.to_image()
	win.image1Label.setPixmap(QPixmap.fromImage(image1))

	# 2. Дополнительные преобразования полутонового изображения: фильтр «максимум»
	bmp_file2 = maximum_filter(bmp_file1, size=maximum_filter_size)
	bmp_file2.save_file(f'src/modules/preparation_image/images/2_maximum_filter.bmp')
	image2 = bmp_file2.to_image()
	win.image2Label.setPixmap(QPixmap.fromImage(image2))

	# 3. Приведение полутонового изображения к монохромному изображению (бинаризация): 8-бит GRAYSCALE в 1-бит MONOCHROME
	bmp_file3 = binarization(bmp_file2, threshold=binarization_threshold)
	bmp_file3.save_file(f'src/modules/preparation_image/images/3_binarization.bmp')
	image3 = bmp_file3.to_image()
	win.image3Label.setPixmap(QPixmap.fromImage(image3))

	# 4. Морфологическое преобразование монохромного изображения: морфологическая дилатация
	bmp_file4 = morphology_dilation(bmp_file3, size=morphology_dilation_size)
	bmp_file4.save_file(f'src/modules/preparation_image/images/4_morphology.bmp')
	image4 = bmp_file4.to_image()
	win.image4Label.setPixmap(QPixmap.fromImage(image4))

	win.container.current_bmp_file_prepared = bmp_file4


def search_areas(win):
	win.findedAreasListWidget.clear()
	win.databaseAreasListWidget.clear()

	result_areas = []
	target_images = []
	count_repeat = win.repeatSpinBox.value()
	count_spent_repeat = 0

	for repeat_index in range(0, count_repeat + 1):
		count_spent_repeat += 1

		bmp_file = win.container.current_bmp_file_prepared
		result_areas = recursive_connected_areas(bmp_file)

		for area_index, (area_bmp_file, p_hash) in enumerate(result_areas):
			# Отображение найденного образа
			area_image = area_bmp_file.to_image()
			item = QListWidgetItem()
			item.setText(f'{area_index}')
			item.setToolTip(p_hash_to_html(p_hash))
			item.setIcon(QIcon(QPixmap.fromImage(area_image)))
			win.findedAreasListWidget.addItem(item)

			# Отображение образов из базы данных
			entries = win.container.database.find_all()
			for entry in entries:
				percent = hamming_distance(entry.p_hash, p_hash)
				value = win.percentSlider.value() / 100
				if percent >= value:
					# Проверка, нет ли уже такого элемента в databaseAreasListWidget
					found_item = None
					for index in range(win.databaseAreasListWidget.count()):
						item = win.databaseAreasListWidget.item(index)
						if item.data(Qt.UserRole) == entry.id:
							item_percent = item.data(Qt.UserRole + 1)
							if item_percent >= percent:
								found_item = item
								break

					if found_item is None:
						image = entry.bmp_file.to_image()
						item = QListWidgetItem()
						item.setText(f'{area_index}: {percent:.2f}%')
						item.setToolTip(p_hash_to_html(p_hash))
						item.setData(Qt.UserRole, entry.id)
						item.setData(Qt.UserRole + 1, percent)
						item.setIcon(QIcon(QPixmap.fromImage(image)))
						win.databaseAreasListWidget.addItem(item)
						target_images.append((entry.id, image, percent))

		if len(target_images) > 0:
			break
		else:
			if repeat_index != count_repeat:
				# Еще есть попытки
				contrast_factor = random.uniform(0.0, 2.0)
				maximum_filter_size = random.randint(0, 10)
				binarization_threshold = random.randint(0, 255)
				morphology_dilation_size = random.randint(0, 10)

				msg_box = QMessageBox()
				msg_box.setIcon(QMessageBox.Question)
				msg_box.setText(f"Ничего не найдено, вот новые параметры:\n"
				                f"Contrast Factor: {contrast_factor}\n"
				                f"Maximum Filter Size: {maximum_filter_size}\n"
				                f"Binarization Threshold: {binarization_threshold}\n"
				                f"Morphology Dilation Size: {morphology_dilation_size}\n"
				                f"Продолжить поиск?")
				msg_box.setWindowTitle("Ой, ничего не найдено!")
				msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

				reply = msg_box.exec()
				if reply == QMessageBox.Ok:
					win.contrastDoubleSpinBox.setValue(contrast_factor)
					win.maxFilterSlider.setValue(maximum_filter_size)
					win.binarizationSlider.setValue(binarization_threshold)
					win.morphologyDilationSlider.setValue(morphology_dilation_size)
					win.run_function_safely(apply, win)
				else:
					break

	win.databaseAreasListWidget.sortItems(Qt.DescendingOrder)
	win.findAreasLabel.setText(f'Всего найдено: {len(result_areas)}')
	win.databaseAreasLabel.setText(f'Взято из базы данных: {len(target_images)}')
	win.countRepeatLabel.setText(f'Попыток потрачено: {count_spent_repeat}')

	most_similar_area = win.databaseAreasListWidget.item(0)
	if most_similar_area is not None:
		_id = most_similar_area.data(Qt.UserRole)
		entry = win.container.database.find_one_by_id(_id)
		win.thisIsLabel.setText(f'Скорее всего это... {entry.description}')


def clear_areas(win):
	win.findedAreasListWidget.clear()
	win.databaseAreasListWidget.clear()


def save_image(win):
	if win.container.current_bmp_file_prepared is None:
		win.error_dialog.setText('Не выполнена обработка изображения')
		win.error_dialog.exec()
		return

	contrast_factor = win.contrastDoubleSpinBox.value()
	maximum_filter_size = win.maxFilterSlider.value()
	binarization_threshold = win.binarizationSlider.value()
	morphology_dilation_size = win.morphologyDilationSlider.value()

	p_hash = win.container.current_bmp_file_prepared.calculate_hash()

	rand = random.randint(0, 100000)
	file_name = win.container.current_bmp_file_prepared.name.split(".")[0]
	path = f'src/modules/database/images/{file_name}_{contrast_factor}_{maximum_filter_size}_{binarization_threshold}_{morphology_dilation_size}_{rand}.bmp'
	entry = Entry(
		win.container.current_bmp_file_prepared,
		path,
		p_hash,
		contrast_factor,
		maximum_filter_size,
		binarization_threshold,
		morphology_dilation_size,
		win.descriptionLineEdit.text()
	)

	win.container.database.insert_one(entry)
	win.container.database.layoutChanged.emit()


def find_image(win):
	search_value = win.searchLineEdit.text()

	if search_value.isdigit() is False:
		win.error_dialog.setText('Некорректное значение')
		win.error_dialog.exec()
		return

	entry_index = win.container.database.binary_search_by_id(int(search_value))
	if entry_index is not None:
		win.imagesListView.setCurrentIndex(entry_index)


def remove_image(win):
	selected_index = win.imagesListView.currentIndex()
	selected_entry = win.container.database.find_one_by_index(selected_index)
	if selected_entry is not None:
		win.container.database.delete_one_by_index(selected_index)
		win.container.database.layoutChanged.emit()


def sort_images(win, criterion):
	if criterion == "id":
		win.container.database.bubble_sort_by_field("id")
	elif criterion == "hash":
		win.container.database.bubble_sort_by_field("p_hash")
