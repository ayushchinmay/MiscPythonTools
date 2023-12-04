# def del_multiples(n, nums):
# 	for i in nums:
# 		if (i > n) and (i%n == 0):
# 			nums.remove(i)
# 	return nums


# def prime_sieve(n):
# 	nums = [n for n in range(2, n+1)]
# 	for i in nums:
# 		del_multiples(i, nums)
# 	return nums
# ====================================
def prime_sieve(n):
	nums = [n for n in range(2, n+1)]
	for curr in nums:
		for multiple in nums:
			if(multiple>curr) and not(multiple%curr):
				nums.remove(multiple)
		# print(nums)
	return nums


def main():
	primes = prime_sieve(100)
	# print(primes)
	number = int(input())

	if number in prime_sieve(number):
		print("prime")
	else:
		print("composite")


if __name__ == '__main__':
	main()