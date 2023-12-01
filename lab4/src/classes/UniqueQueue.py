from collections import deque


class UniqueQueuePoints(deque):
	def __init__(self, iterable=None, maxlen=None):
		super().__init__(iterable=iterable, maxlen=maxlen)

	def __overwrite_insert(self, value):
		for index, item in enumerate(self):
			if value[0] == item[0] and value[1] == item[1]:
				self[index] = value
				break
		else:
			super().append(value)

	def append(self, value):
		self.__overwrite_insert(value)

	def appendleft(self, value):
		self.__overwrite_insert(value)

	def extend(self, iterable):
		for value in iterable:
			self.__overwrite_insert(value)

	def extendleft(self, iterable):
		for value in reversed(iterable):
			self.__overwrite_insert(value)
