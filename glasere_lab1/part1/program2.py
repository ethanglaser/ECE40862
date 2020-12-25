a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print("a = " + str(a))
number = int(input("Enter number: "))
b = []
for val in a:
    if val < number:
        b.append(val)
print("The new list is " + str(b))
