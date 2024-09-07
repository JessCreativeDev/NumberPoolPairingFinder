from itertools import permutations
from collections import Counter
from line_profiler import LineProfiler
import numpy as np
import threading

def subset_sum(numbers, target, partial = [], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)
            
def boolean_indexing(v, fillval=np.nan):
    lens = np.array([len(item) for item in v], np.int_)
    mask = lens[:,None] > np.arange(lens.max())
    out = np.full(mask.shape,fillval,np.int_)
    out[mask] = np.concatenate(v)
    return out
       
def subset_sum_range(min_limit, max_limit, num_pools):
    num_sum_list = dict()
    
    for num in range(min_limit, max_limit + 1):
        num_sum_list[num] = []
        sub_sum = []
        [sub_sum.append(n) for n in subset_sum(num_pools, num) if n not in sub_sum]
        if len(sub_sum) != 0:
            for possible_sum in sub_sum:
                if num not in num_sum_list.keys() or not np.array_equal(possible_sum, num_sum_list[num]):
                    num_sum_list[num].append(possible_sum)
    
    return num_sum_list

def does_list_contain_list(input_list, checked_list, type):
    if type == 0:
        for e in input_list:
            if e == checked_list[:len(e)]:
                return True
    elif type == 1:
        for n in input_list:
            for r in input_list[n]:
                if any(np.isin(checked_list, r)):
                    return True
    elif type == 2:
        for r in input_list:
            if r[0] == checked_list:
                return True
    elif type == 3:
        for i in input_list:
            for p in permutations(i[1]):
                checked_list_copy = np.copy(checked_list)
                for r in p:
                    if np.array_equal(r, checked_list_copy[:len(r)]):
                        checked_list_copy = checked_list_copy[len(r):]
                if len(checked_list_copy) == 0:
                    return True
    return False

def add_sum_from_input(possible_sum, number, min_limit, input, input_mask, sum_list, possible_sum_list):
    input_copy = input
    old_input_copy = np.copy(input_copy)
    
    while np.array_equal(np.sort(possible_sum), np.sort(input_copy[:len(possible_sum)])):
        [input_mask.append(element) for element in input_copy[:len(possible_sum)]]
        input_copy = input_copy[len(possible_sum):]
        sum_list.append(number)
        
        if len(input_copy) != len(old_input_copy):
            possible_sum_list.append(possible_sum)
        
        if len(input_copy) != 0 and np.sum(input_copy) < min_limit * (num_of_results - len(sum_list)):
            return True, input_copy
    return False, input_copy

def find_combinations_for_each_input(failed_masks, perm_input, result, min_limit, smallest_set, num_dict, num_of_results):
    stop_looping = False
    if not does_list_contain_list(result, perm_input, 3):
        if not does_list_contain_list(failed_masks, perm_input, 0):
            sum_list = []
            input_mask = []
            possible_sum_list = []
            input_copy = np.copy(perm_input)
        
            while len(input_copy) != 0 and does_list_contain_list(num_dict, input_copy, 1):
                for number in reversed(num_dict):
                    for possible_sum in num_dict[number]:
                        stop_looping, input_copy = add_sum_from_input(possible_sum, number, min_limit, input_copy, input_mask, sum_list, possible_sum_list)

                        if not stop_looping and input_copy.size != 0 and input_copy.size < smallest_set:
                            stop_looping = True
                        if stop_looping:
                            break
                    if stop_looping:
                        break
                if stop_looping:
                    failed_masks.append(perm_input[:len(input_mask)])
                    break
            sorted_sum_list = sorted(sum_list, reverse=True)
            
            if len(sorted_sum_list) == num_of_results and (len(result) == 0 or not does_list_contain_list(result, sorted_sum_list, 2)):
                result.append([sorted_sum_list, possible_sum_list])
                                         
def find_combinations(permutations, num_dict, num_of_results, min_limit, smallest_set):
    result = []
    failed_masks = []
    iterations = 0
    lp = LineProfiler()
    for perm_input in permutations:
        
        #lp_wrapper = lp(does_list_contain_list)
        #lp_wrapper(result, perm_input, 3)
        #lp.print_stats()
                    
        find_combinations_for_each_input(failed_masks, perm_input, result, min_limit, smallest_set, num_dict, num_of_results)
        
        iterations += 1
        print(iterations)
    return result

min_limit = 12
max_limit = 20
num_of_results = 6

four_pool = [4 for _ in range(7)]
five_pool = [5 for _ in range(5)]
six_pool = [6 for _ in range(6)]

nums_available = np.array(four_pool + five_pool + six_pool)
sum_of_pools = sum(nums_available)

perm = permutations(nums_available)
num_dict = subset_sum_range(min_limit, max_limit, nums_available)

smallest_set = len(next(iter(num_dict.values())))

for n in num_dict:
    for s in num_dict[n]:
        if len(s) < smallest_set:
            smallest_set = len(s)
     
print(find_combinations(perm, num_dict, num_of_results, min_limit, smallest_set))
#print(num_list)