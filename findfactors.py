from math import sqrt
def factors(n):
    if n==0:return [0]
    f1 = lambda x: x
    f2 = lambda x: n//x
    step = 2 if n%2 else 1
    a = [f(i) for i in range(1, int(sqrt(n))+1, step) if n % i == 0 for f in (f1,f2)]
    if a[-1]**2 == n: a.pop()
    return a




if __name__ == "__main__":
    print(factors(100))