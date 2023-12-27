import json
import os
import shutil
from PyQt5.QtCore import Qt, QAbstractListModel
from PyQt5.QtGui import QPixmap
from src.classes import BmpFile
from src.modules.database.Entry import Entry


class EntryEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Entry):
			return obj.to_json()
		return json.JSONEncoder.default(self, obj)


class DataBase(QAbstractListModel):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.__entries = []

	def data(self, index, role):
		if not index.isValid():
			return None

		entry = self.__entries[index.row()]

		if role == Qt.DecorationRole:
			image = entry.bmp_file.to_image()
			pixmap = QPixmap.fromImage(image)
			return pixmap
		elif role == Qt.DisplayRole:
			if index.column() == 0:
				return f'{entry.id}. {entry.path.split("/")[-1]}'
		elif role == Qt.ToolTipRole:
			return (f'ID: {entry.id}\n'
			        f'Hash: {entry.p_hash[:10]}...\n'
			        f'Path: {entry.path}\n'
			        f'Contrast: {entry.contrast_factor}\n'
			        f'Max filter size: {entry.maximum_filter_size}\n'
			        f'Binarization threshold: {entry.binarization_threshold}\n'
			        f'Morphology dilation size: {entry.morphology_dilation_size}\n'
			        f'Description: {entry.description}')
		return None

	def rowCount(self, index):
		return len(self.__entries)

	def get_index_by_id(self, _id: int):
		for entry in self.__entries:
			if entry.id == _id:
				index = self.createIndex(self.__entries.index(entry), 0)
				return index
		return None

	def insert_one(self, entry):
		entry.id = len(self.__entries)
		self.__entries.append(entry)
		self.bubble_sort_by_field("id")

	def find_one_by_index(self, index):
		row = index.row()
		if index.isValid() and 0 <= row < self.rowCount(index):
			return self.__entries[row]

	def find_one_by_id(self, _id):
		for entry in self.__entries:
			if entry.id == _id:
				return entry
		return None

	def find_all(self):
		return self.__entries

	def delete_one_by_index(self, index):
		row = index.row()
		if index.isValid() and 0 <= row < self.rowCount(index):
			del self.__entries[row]
			self.bubble_sort_by_field("id")

	def load(self, path):
		try:
			with open(path, 'r') as f:
				json_data = json.load(f)
				for item in json_data:
					bmp_file = BmpFile(item['path'])
					entry = Entry(
						bmp_file,
						item['path'],
						item['p_hash'],
						item['contrast_factor'],
						item['maximum_filter_size'],
						item['binarization_threshold'],
						item['morphology_dilation_size'],
						item['description']
					)
					entry.id = item['id']
					self.__entries.append(entry)
		except FileNotFoundError:
			print(f'Не удалось загрузить данные из файла {path}')

	def save(self, path):
		with open(path, 'w') as f:
			json.dump(self.__entries, f, cls=EntryEncoder, indent=4)

		# Сохранить bmp файлы
		shutil.rmtree('./src/modules/database/images')
		os.mkdir('src/modules/database/images')
		for entry in self.__entries:
			entry.bmp_file.save_file(f'{entry.path}')

	def binary_search_by_id(self, _id):
		self.bubble_sort_by_field("id")

		left, right = 0, len(self.__entries) - 1

		while left <= right:
			mid = left + (right - left) // 2
			mid_entry = self.__entries[mid]

			if mid_entry.id == _id:
				index = self.createIndex(self.__entries.index(mid_entry), 0)
				return index

			if mid_entry.id < _id:
				left = mid + 1
			else:
				right = mid - 1

		return None

	def bubble_sort_by_field(self, field_name):
		if len(self.__entries) == 0:
			return

		# Проверка существования поля
		if not hasattr(self.__entries[0], field_name):
			return

		# Сортировка пузырьком по полю
		for i in range(0, len(self.__entries)):
			for j in range(0, len(self.__entries) - i - 1):
				if getattr(self.__entries[j], field_name) > getattr(self.__entries[j + 1], field_name):
					self.__entries[j], self.__entries[j + 1] = self.__entries[j + 1], self.__entries[j]

		# Обновление модели данных после сортировки
		self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), 0))
