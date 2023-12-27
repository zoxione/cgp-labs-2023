def hamming_distance(hash1, hash2) -> float:
	len_hash1 = len(hash1)
	len_hash2 = len(hash2)

	if len_hash1 == 0 and len_hash2 == 0:
		return 100.0

	length = min(len_hash1, len_hash2)
	dist = 0

	for i in range(0, length):
		bit1 = hash1[i % len_hash1]
		bit2 = hash2[i % len_hash2]
		if bit1 != bit2:
			dist += 1

	similarity = (length - dist) / length
	return similarity
