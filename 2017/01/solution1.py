sum([int(j[i]) for i in range(len(j)) if j[i]==j[i-1]])

# Didn't quite get this one to work, but would be O(n) rather than O(2n)
#
# from functools import reduce
# reduce(lambda i,s:(j[i]==j[i-1])*int(j[i])+s,range(len(j)))