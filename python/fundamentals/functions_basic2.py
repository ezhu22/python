def countdown(num):
    for x in range(num, -1, -1):
        print(x)
countdown(10)

def print_and_return(list):
    print(list[0])
    return list[1]
print(print_and_return([1,2]))

def first_plus_length(list):
    sum = list[0] + len(list)
    return sum
print(first_plus_length([1,2,3,4,5]))

def values_greater_then_second(list):
    newlist = []
    if len(list) < 2:
        return False
    else:
        for x in range (0, len(list)):
            if list[x] > list[1]:
                newlist.append(list[x])
    return newlist
print(values_greater_then_second([5,2,3,2,1,4]))
print(values_greater_then_second([3]))

def length_and_value(num1,num2):
    newlist = []
    count = 0
    while count < num1:
        newlist.append(num2)
        count += 1
    return newlist
print(length_and_value(4,7))
print(length_and_value(6,2))
