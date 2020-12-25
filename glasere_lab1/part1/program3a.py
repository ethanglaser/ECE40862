num = int(input("How many Fibonacci numbers would you like to generate? "))
fib = [1, 1]
while len(fib) < num:
    fib.append(fib[-1] + fib[-2])
fibs = [str(val) for val in fib[:num]]
print("The Fibonacci Sequence is: " + ", ".join(fibs))