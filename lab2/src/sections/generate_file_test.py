import unittest
from src.sections.generate_file import convert_to_bytes


class TestConvertToBytes(unittest.TestCase):
	def test_lower(self):
		# Test case: Single pixel, 1 bit per pixel
		pixels_values = [1]
		bits_per_pixel = 1
		expected_result = b'\x80'
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_lower_bits_overflow(self):
		# Test case: Single pixel, 1 bit per pixel
		pixels_values = [1]
		bits_per_pixel = 10
		expected_result = b'\x00\x40'
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_upper(self):
		# Test case: Single pixel, 255 bits per pixel
		pixels_values_count = (1 * 1)
		pixels_values = [65535 - 1] * pixels_values_count
		bits_per_pixel = 255
		expected_result = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xfc'
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_empty(self):
		# Test case: Empty pixel values
		pixels_values = []
		bits_per_pixel = 8
		expected_result = b''
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_valid_1(self):
		# Test case: Valid pixel values with 8 bits per pixel
		pixels_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		bits_per_pixel = 8
		expected_result = b'\x01' * 16
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_valid_2(self):
		# Test case: Valid pixel values with 2 bits per pixel
		pixels_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		bits_per_pixel = 2
		expected_result = b'\x55\x55\x55\x55'
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_valid_3(self):
		# Test case: Valid pixel values with 12 bits per pixel
		pixels_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		bits_per_pixel = 12
		expected_result = b'\x00\x10\x01' * 8
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_valid_4(self):
		# Test case: Valid pixel values with 1 bit per pixel
		pixels_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		bits_per_pixel = 1
		expected_result = b'\xFF\xFF'
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)

	def test_valid_5(self):
		# Test case: Valid pixel values with 16 bits per pixel
		pixels_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		bits_per_pixel = 16
		expected_result = b'\x00\x01' * 16
		self.assertEqual(convert_to_bytes(pixels_values, bits_per_pixel), expected_result)


if __name__ == '__main__':
	unittest.main()
