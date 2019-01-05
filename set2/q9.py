
def padding(output_len,s):
	tmp = len(s)
	padding_len = output_len - tmp
	for i in range(padding_len):
		s = s + chr(padding_len)

	return s

print (padding(20,"YELLOW SUBMARINE"))