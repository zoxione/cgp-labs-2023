class Entry:
	def __init__(self, bmp_file, path, p_hash, contrast_factor, maximum_filter_size, binarization_threshold, morphology_dilation_size, description):
		self.id = 0
		self.bmp_file = bmp_file
		self.path = path
		self.p_hash = p_hash
		self.contrast_factor = contrast_factor
		self.maximum_filter_size = maximum_filter_size
		self.binarization_threshold = binarization_threshold
		self.morphology_dilation_size = morphology_dilation_size
		self.description = description

	def to_json(self):
		return {
			"id": self.id,
			"path": self.path,
			"p_hash": self.p_hash,
			"contrast_factor": self.contrast_factor,
			"maximum_filter_size": self.maximum_filter_size,
			"binarization_threshold": self.binarization_threshold,
			"morphology_dilation_size": self.morphology_dilation_size,
			"description": self.description
		}
