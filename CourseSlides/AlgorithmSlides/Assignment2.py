
# Give the best upper bound that you can on the solution to the following recurrence:
# T(1)=1 and
# T(n)≤T([sqrt(n)])+1 for n>1.
# (Here [x] denotes the "floor" function, which rounds down to the nearest integer.)
'''
Solution: T(1) = 1
T(1.01) <=2
T(4) <=3
T(16) <= 4
T(256) <= 5
...

So upper bounded by 2+ log(n)/log(4)
'''