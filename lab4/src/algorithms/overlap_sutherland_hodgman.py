from typing import List, Tuple, Any


def is_inside(p1, p2, q):
	R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
	if R <= 0:
		return True
	else:
		return False


def compute_intersection(p1, p2, p3, p4):
	# Eсли первая линия вертикальная
	if p2[0] - p1[0] == 0:
		x = p1[0]
		m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
		b2 = p3[1] - m2 * p3[0]
		y = m2 * x + b2

	# Если вторая линия вертикальная
	elif p4[0] - p3[0] == 0:
		x = p3[0]
		m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
		b1 = p1[1] - m1 * p1[0]
		y = m1 * x + b1

	# Если ни одна линия не вертикальна
	else:
		m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
		b1 = p1[1] - m1 * p1[0]
		m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
		b2 = p3[1] - m2 * p3[0]
		x = (b2 - b1) / (m1 - m2)
		y = m1 * x + b1

	return round(x), round(y)


def overlap_sutherland_hodgman(subject_points: List[Tuple[int, int]], clip_points: List[Tuple[int, int]]) -> list[Any] | Any:
	"""
	Алгоритм определения видимости и отсечения для перекрытия: алгоритм Сазерленда-Ходжмана
	"""
	overlap_points = subject_points.copy()

	for i in range(0, len(clip_points)):
		next_points = overlap_points.copy()
		overlap_points = []

		# Вершины отсечения многоугольника
		c_edge_start = clip_points[i]
		c_edge_end = clip_points[(i + 1) % len(clip_points)]

		for j in range(0, len(next_points)):
			# Вершины многоугольника
			s_edge_start = next_points[j]
			s_edge_end = next_points[(j + 1) % len(next_points)]

			if is_inside(c_edge_start, c_edge_end, s_edge_end):
				if not is_inside(c_edge_start, c_edge_end, s_edge_start):
					intersection = compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
					overlap_points.append(intersection)
				overlap_points.append(s_edge_end)
			elif is_inside(c_edge_start, c_edge_end, s_edge_start):
				intersection = compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
				overlap_points.append(intersection)

	return overlap_points

