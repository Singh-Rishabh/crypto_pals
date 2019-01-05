
def set1_5(s):
	key = "ICE"
	out = ""
	for i in range(len(s)):

		# print(ord(s[i]),ord(key[i]))
		tmp = ord(s[i])^(ord(key[i%3]))
		# print(tmp)
		tmp = hex(tmp)
		# print(tmp)
		tmp = tmp[2:]
		if (len(tmp) != 2):
			tmp = '0' + tmp
		out = out + tmp
	return out


print(set1_5("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"))


