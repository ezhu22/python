def biggie_size(list):
    for x in range (len(list)):
        if list[x] > 0:
            list[x] = str("big")
    return list
print(biggie_size([-1,3,5,-5]))

def count_positives(list):
    positivecounter = 0
    for x in range (len(list)):
        if list[x] > 0:
            positivecounter += 1
    list[len(list) - 1] = positivecounter
    return list
print(count_positives([-1,1,1,3]))
print(count_positives([1,6,-4,-2,-7,-2]))

def sum_total(list):
    sum = 0
    count = 0
    while count < len(list):
        sum = sum + list[count]
        count += 1
    return sum
print(sum_total([1,2,3,4]))
print(sum_total([6,3,-2]))

def average(list):
    sum = 0
    count = 0
    while count < len(list):
        sum = sum + list[count]
        count += 1
    return sum / len(list)
print(average([1,2,3,4]))

def length(list):
    return len(list)
print(length([37,2,1,-9]))
print(length([]))

def minimum(list):
    if len(list) == 0:
        return False
    min = list[0]
    for x in range (len(list)):
        if list[x] < min:
            min = list[x]
    return min
print(minimum([37,2,1,-9]))
print(minimum([]))

def maximum(list):
    if len(list) == 0:
        return False
    max = list[0]
    for x in range (len(list)):
        if list[x] > max:
            max = list[x]
    return max
print(maximum([37,2,1,-9]))
print(maximum([]))

def ultimate_analysis(list):
    if len(list) == 0:
        return False
    sum = 0
    min = list[0]
    max = list[0]
    for x in range (len(list)):
        sum = sum + list[x]
        if list[x] < min:
            min = list[x]
        if list[x] > max:
            max = list[x]
    ultimate = {
        "SumTotal": sum,
        "Average": sum / len(list),
        "Maximum": max,
        "Minimum": min,
        "Length": len(list)
        }
    return ultimate
print(ultimate_analysis([37,2,1,-9]))

def reverse_list(list):
    for x in range (int(len(list) / 2)):
        temp = list[x]
        list[x] = list[len(list) - 1 - x]
        list[len(list) - 1 - x] = temp
    return list
print(reverse_list([1,2,3,4,5,6]))
print(reverse_list([37,2,1,-9]))
