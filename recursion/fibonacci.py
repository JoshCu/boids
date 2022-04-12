import time

def fib(n):
    """Print the Fibonacci series up to n."""
    a, b = 0, 1
    for x in range(n):
        a, b = b, a + b
    #print(b)
    print()

start = time.time()
fib(1000000)
end = time.time()
print(end - start)

