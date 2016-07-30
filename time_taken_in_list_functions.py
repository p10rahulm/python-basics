import time
timestart = time.time()
for i in range(1000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	map(lambda x:x if x!= 4 else 'sss',a)
print("time taken for map",time.time()-timestart)

timestart = time.time()
for i in range(1000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	a = [4 if x==1 else x for x in a]
print("time taken for new list",time.time()-timestart)

timestart = time.time()
for i in range(1000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	for n,i in enumerate(a):
		if i==1:
			a[n]=10
print("time taken for enumerate",time.time()-timestart)

timestart = time.time()
for i in range(1000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	a.append(10)
	a.remove(6)
print("time taken for append and remove: ",time.time()-timestart)

timestart = time.time()
for i in range(1000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	a.remove(6)
	a.append(10)
print("time taken for append and remove: ",time.time()-timestart)

timestart = time.time()
for i in range(100000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	a.pop(-4)

print("time taken for pop: ",time.time()-timestart)

timestart = time.time()
for i in range(100000):
	a = [1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1]
	del a[-4]
print("time taken for del by index: ",time.time()-timestart)
import numpy as np
timestart = time.time()
for i in range(100000):
    a = np.array([1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1])
    b = np.array([1,2,3,2,3,4,3,15,6,6,5,4,5,4,31,41,31,2,1])
    g = np.equal(a,b)
print("time taken for np.equal : ",time.time()-timestart)

timestart = time.time()
for i in range(100000):
    a = np.array([1,2,3,2,3,4,3,5,6,6,5,4,5,4,3,4,3,2,1])
    b = np.array([1,2,3,2,3,4,3,15,6,6,5,4,5,4,31,41,31,2,1])
    g = (a==b)
print("time taken for equality : ",time.time()-timestart)