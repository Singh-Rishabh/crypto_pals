import base64


def set1_6(filename):
	file_op = open(filename)
	s = file_op.read()
	# print(s)
	s = s.decode('base64')
	# print(s)
	len_key = 0
	min_indexOFcoincidence = []
	index = []
	for i in range(1,40):
		freq = {}
		for j in range(0,len(s),i):
			if s[j] in freq:
				freq[s[j]] = freq[s[j]] + 1
			else :
				freq[s[j]] = 1
		N = 0
		sum_ = 0
		for key, value in freq.iteritems():			
			sum_ = sum_ + value*(value-1)
			N = N + value
		ic = float(sum_)*len(freq)/(N*(N-1))
		# print(i, ic)
		if (abs(ic-1.73) < 0.01):
			min_indexOFcoincidence.append(ic)
			index.append(i)

	# print("\n\n")
	print(index,min_indexOFcoincidence)

	
	key_val = ""
	for k in range(index[0]):
		max_space_count = -1
		tmp_key = '1'
		for i in range(256):
			key = chr(i)

			count = 0
			for j in range(k,len(s),index[0]):

				if (ord(s[j]) ^ ord(key) == 32 ):
					count += 1
			
			if (count > max_space_count):
				max_space_count = count
				tmp_key = key

		key_val = key_val + tmp_key

	print(key_val)


set1_6("set1_6.txt")