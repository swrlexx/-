# sort_functions.py
def bubble_sort(input_list):
    n = len(input_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if input_list[j]['index'] > input_list[j+1]['index']:
                input_list[j], input_list[j+1] = input_list[j+1], input_list[j]
    return input_list

def selection_sort(input_list):
    n = len(input_list)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if input_list[j]['index'] < input_list[min_index]['index']:
                min_index = j
        input_list[i], input_list[min_index] = input_list[min_index], input_list[i]
    return input_list