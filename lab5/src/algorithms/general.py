def greater_multiple_of_4(number: int) -> int:
	remainder = number % 4
	if remainder == 0:
		return number
	else:
		return number + (4 - remainder)


def p_hash_to_html(p_hash: str) -> str:
	n = 30
	formatted_text = '<br>'.join(p_hash[i:i+n] for i in range(0, len(p_hash), n))
	return f'<html><body>{formatted_text}</body></html>'

