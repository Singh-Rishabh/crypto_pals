import base64

def set1_3(s):
	space_count_arr  = [0 for i in range(256)]

	for i in range(256):
		for j in range(0,len(s),2):
			if ( int(s[j]+s[j+1],16)^ord(chr(i)) == 32):
				space_count_arr[i] += 1
	# print(space_count_arr)
	max_index = space_count_arr[0]
	for i in range(len(space_count_arr)):
		if (space_count_arr[i] > space_count_arr[max_index]):
			max_index = i

	out = ""
	for j in range(0,len(s),2):
		out = out +  chr(int(s[j]+s[j+1],16)^max_index)
	# print(out)
	return out


# set1_3("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

