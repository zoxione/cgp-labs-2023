from src.classes.SingletonMetaclass import SingletonMetaclass


class Container(metaclass=SingletonMetaclass):
	def __init__(self, current_bmp_file, current_bmp_file_prepared, database):
		self.current_bmp_file = current_bmp_file
		self.current_bmp_file_prepared = current_bmp_file_prepared
		self.database = database

	def clear_data(self):
		self.current_bmp_file = None
		self.current_bmp_file_prepared = None
		# self.database.clear()

