from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QFileDialog
from src.classes.DrawThread import DrawThread
from src.data.constants import Mode, GRID_COLOR, BACKGROUND_COLOR


@pyqtSlot()
def start_draw(win, mode: str):
	win.change_buttons_state(False)

	win.draw_thread = DrawThread(win, mode)
	win.draw_thread.resultAvailable.connect(lambda result: draw_ready(win, result))
	win.draw_thread.start()


@pyqtSlot(float)
def draw_ready(win, result):
	win.change_buttons_state(True)
	win.draw_thread = None
	win.draw_timer.start()

	if win.overlapCheckBox.isChecked():
		win.timeSpentOverlapsLabel.setText(f'Затраченное время на растеризацию слоёв с отсечениями: {result:.4f}')
	else:
		win.timeSpentLabel.setText(f'Затраченное время на растеризацию слоёв без отсечений: {result:.4f}')


def change_layer(win, mode: str):
	"""
	Обработчик нажатия на кнопку для изменения номера полигона
	"""
	if mode == "back":
		win.container.current_layer_index = (win.container.current_layer_index - 1) % win.container.count_layers
	if mode == "forward":
		win.container.current_layer_index = (win.container.current_layer_index + 1) % win.container.count_layers
	win.currentLayerLabel.setText(f'Текущий слой: {win.container.current_layer_index}/{win.container.count_layers - 1}')


def clear_all(win):
	"""
	Обработчик нажатия на кнопку для очистки изображений
	"""
	win.mainImage.fill(QColor(*BACKGROUND_COLOR))
	win.update_scenes()


def upscale(win):
	"""
	Обработчик нажатия на кнопку для увеличения изображений
	"""
	resize_factor = win.resizeDoubleSpinBox.value()
	win.resize_images(resize_factor)


def toggle_show_grid(win):
	"""
	Обработчик нажатия на кнопку для отображения/скрытия сетки
	"""
	state = win.gridCheckBox.isChecked()
	if state:
		grid_color = QColor(*GRID_COLOR)
	else:
		grid_color = QColor(*BACKGROUND_COLOR)

	win.draw_grid(grid_color)


def toggle_mode(win, clicked_button):
	if win.modeAlphaRadioButton == clicked_button:
		win.current_mode = Mode.ALPHA
	elif win.modeBravoRadioButton == clicked_button:
		win.current_mode = Mode.BRAVO
	elif win.modeCharlieRadioButton == clicked_button:
		win.current_mode = Mode.CHARLIE


def change_frame_sizes(win, value):
	win.container.frame_sizes = (value, value)
	win.container.crop_layer.polygons[0].points = [
		(-(win.container.frame_sizes[0] // 2), -(win.container.frame_sizes[1] // 2)),
		(-(win.container.frame_sizes[0] // 2), (win.container.frame_sizes[1] // 2)),
		((win.container.frame_sizes[0] // 2), (win.container.frame_sizes[1] // 2)),
		((win.container.frame_sizes[0] // 2), -(win.container.frame_sizes[1] // 2))
	]
	win.frameSizeLabel.setText(f'{win.container.frame_sizes[0]}')


def add_texture(win):
	"""
	Обработчик нажатия на кнопку для добавления текстуры
	"""
	file = QFileDialog.getOpenFileName(win, "Open File", "textures/", "All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)")
	pixmap = QPixmap(file[0])
	win.texture = pixmap.toImage()
