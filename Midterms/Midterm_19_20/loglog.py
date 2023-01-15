import math
import hashlib

def bin_hash(x):
	hash_object = hashlib.sha1(str(x).encode('utf-8'))
	hexa=hash_object.hexdigest()
	bina=bin(int(hexa, 16))[2:].zfill(160)[:32]
	return bina
	
### CODE TO BE COMPLETED	
	
def cardinality(tab):
	final = set()
	for el in tab:
		if el not in final:
			final.add(el)
	return len(final)

	
def bucket(bina,b): # returns the integer corresponding to the leftmost b bits in bina
	sum = 0
	bina_cut = bina[:b]
	n = len(bina_cut)
	c = n-1
	for b in bina_cut:
		if b == '1':
			sum += 2**c
		c-=1
	return sum

	
def zeros(bina,b): # return the largest l, called b-length of bina, such that all entries in bina[b:b+l] are zero
	l=0
	for k in bina[b:]:
		if k == "0":
			l+=1
		else:
			break
	return l
		
def sketch(L,b): # returns the array A of length 2**b, such that A[i] is 0 if the bucket of index i is empty, and otherwise A[i] is one plus the maximum value taken by the b-length over all elements in the bucket of index i
	A = [0 for _ in range(2**b)]
	buckets = {}
	for l in L:
		bina = bin_hash(l)
		i = bucket(bina, b)
		if i in buckets:
			buckets[i].append(zeros(bina,b))
		else:
			buckets[i] = [zeros(bina,b)]
	for a in buckets:
		A[a] = 1+max(buckets[a])
	return A


def constant(b): # function to compute the constant alpha(b), given
	if b==4: return 0.673
	elif b==5: return 0.697
	elif b==6: return 0.709
	else: return 0.7213/(1+1.079/2**b)
								

def loglog(L,b):
	const = constant(b)
	m = 2**b
	s = sketch(L, b)

	sum = 0
	for i in range(m):
		sum+=2**(-s[i])
	return const*m**2/sum

def loglog_small_range_correction(L,b):
	const = constant(b)
	m = 2 ** b
	est = loglog(L,b)
	if est > 5*m//2:
		return est
	else:
		s = sketch(L,b)
		empty = 0
		for el in s:
			if el == 0:
				empty+=1
		if empty!=0:
			return m*math.log(m/empty)
		return est
