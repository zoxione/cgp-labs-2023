import sys


def search(pixels, max_cols: int, max_rows: int, label: int, row: int, col: int, area):
	pixels[col][row] = label
	area.points.append((col, row))
	sys.setrecursionlimit(max_rows * max_cols)

	for row_delta, col_delta in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
		row_t, col_t = row + row_delta, col + col_delta
		if 0 <= row_t < max_rows and 0 <= col_t < max_cols:
			if pixels[col_t][row_t] == -1:
				search(pixels, max_cols, max_rows, label, row_t, col_t, area)
