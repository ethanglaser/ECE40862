nums = [10,20,10,40,50,60,70]
target = int(input("What is your target number? "))
status = 0
for index, value in enumerate(nums):
    for index2, value2 in enumerate(nums[index + 1:]):
        if value + value2 == target and status == 0:
            print("index1=" + str(index) + ", index2=" + str(index2))
            status = 1
if status == 0:
    print("No values add to " + str(target))