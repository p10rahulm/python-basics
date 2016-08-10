
def get_zeros_in_factorial(n):
    if type(n) != int:
        print("Please input integer")
        quit()
    no_of_zeros = 0
    while n != 0:
        no_of_zeros += n//5
        n = n//5
    return no_of_zeros

if __name__ == "__main__":
    import time
    starttime = time.time()
    for i in range(100000):
        get_zeros_in_factorial(100000)
    print(get_zeros_in_factorial(100000))
    print("time taken for ", i +1, " iterations = ",time.time() - starttime)