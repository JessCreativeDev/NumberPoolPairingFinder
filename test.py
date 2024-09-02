def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)

def flatten_list(lst):
    for p in lst:
        if hasattr(p, '__iter__'):
            yield from flatten_list(p)
        else:
            yield p
            
def subset_sum_range(min, max, *num_pools):
    nums = list(flatten_list(num_pools))
    
    num_sum_list = dict()
    for num in range(min, max + 1):
        sub_sum = []
        [sub_sum.append(n) for n in subset_sum(nums, num) if n not in sub_sum]
        if len(sub_sum) != 0:
            num_sum_list[num] = sub_sum
    return num_sum_list

def get_new_nums(nums_to_remove, num_pools):
    num_pools_copy = [[n for n in p] for p in num_pools]
    nums_to_remove_copy = [n for n in nums_to_remove]
    for p in num_pools_copy:
        if len(nums_to_remove_copy) != 0:
            for r in nums_to_remove:
                if len(p) != 0 and r in p:
                    p.remove(r)
                    nums_to_remove_copy.remove(r)
                    
    return num_pools_copy

def find_pairs(num_sum_list, num_of_results, min, max, *num_pools):
    result_list = []
    
    if len(num_sum_list) != 0:
        for num in num_sum_list:
            sum_list = num_sum_list[num]
            sum_result_list = []
            for sum in sum_list:
                new_num_pools = get_new_nums(sum, num_pools)
                new_num_sumlist = subset_sum_range(min, max, *new_num_pools)
                result = find_pairs(new_num_sumlist, num_of_results, min, max, *new_num_pools)
                if result == []:
                    return num
                else:
                    sum_result_list.append(result)
            result_list.append(list(flatten_list(sum_result_list)))    
    return result_list

min = 12
max = 20
num_of_results = 6

four_pool = [4 for _ in range(7)]
five_pool = [5 for _ in range(5)]
six_pool = [6 for _ in range(6)]

nums_available = four_pool + five_pool + six_pool

num_list = find_pairs(subset_sum_range(min, max, four_pool, five_pool, six_pool), num_of_results, min, max, four_pool, five_pool, six_pool)

print(num_list)


            
        
        
        