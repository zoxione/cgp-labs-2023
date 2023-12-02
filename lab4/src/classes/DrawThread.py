import time
from PyQt5.QtCore import QThread, pyqtSignal
from src.algorithms.general import draw_one_layer


class DrawThread(QThread):
	resultAvailable = pyqtSignal(float)

	def __init__(self, win, mode):
		QThread.__init__(self)
		self.win = win
		self.mode = mode
		self.alive = True

	def run(self):
		start_time = time.perf_counter()

		if self.mode == "one":
			draw_one_layer(self.win, self.win.container.current_layer, self.win.container.current_layer_index)
		elif self.mode == "all":
			for i in range(len(self.win.container.layers) - 1, -1, -1):
				draw_one_layer(self.win, self.win.container.layers[i], i)

		end_time = time.perf_counter()
		execution_time = (end_time - start_time) * 1000
		self.resultAvailable.emit(execution_time)

	def stop(self):
		self.alive = False
		self.wait()
