from itertools import permutations, combinations, batched
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count, Manager
from collections.abc import Iterable
from collections import OrderedDict, defaultdict, Counter

def find_combinations_for_each_input(perm_input: tuple, min_limit: int, num_dict: OrderedDict, num_of_results: int):
    sum_list, input_mask, possible_sum_list = [], [], []
    input_sum = sum(perm_input)

    def update_lists_and_removed_count(number: int, possible_sum: tuple):
        possible_sum_len = len(possible_sum)
        possible_sum_list_len = len(possible_sum_list)

        times_to_add_number = 0
        for i in range(possible_sum_list_len, len(perm_input), possible_sum_len):
            if Counter(perm_input[i : i + possible_sum_len]) == Counter(possible_sum):
                times_to_add_number += 1
            else:
                break

        sum_list.extend([number] * times_to_add_number)
        input_mask.extend(possible_sum * times_to_add_number)
        possible_sum_list.extend(possible_sum * times_to_add_number)

        possible_sum_total = sum(possible_sum)
        return possible_sum_total * times_to_add_number

    while len(sum_list) != num_of_results:
        for number, possible_sums in num_dict.items():
            for possible_sum in possible_sums:
                input_sum -= update_lists_and_removed_count(number, possible_sum)

                if perm_input and input_sum < min_limit * (num_of_results - len(sum_list)):
                    return perm_input[:len(input_mask)]
    return sum_list

def generate_num_dict_and_permutations(pools: tuple, min_limit: int, max_limit: int):
    pool_values = [value for value, count in pools for _ in range(count)]

    def subset_sum_range():
        sum_to_combos = defaultdict(set)

        for r in range(len(pool_values) + 1):
            for combo in combinations(pool_values, r):
                combo_sum = sum(combo)
                if min_limit <= combo_sum <= max_limit:
                    sum_to_combos[combo_sum].add(combo)

        return {num: sum_to_combos[num] for num in range(min_limit, max_limit + 1)}

    nums_available = [value for value, count in pools for _ in range(count)]
    num_dict = OrderedDict(sorted(subset_sum_range().items(), reverse=True))
    perm_gen = permutations(nums_available)

    return num_dict, perm_gen, len(pool_values)

def find_combinations(num_dict: OrderedDict, perm_gen: Iterable, num_count: int, num_of_results: int, min_limit: int):
    def filter_permutations(perm_batch: list, min_limit: int, num_dict: OrderedDict, num_of_results: int, results, failed_masks):
        def is_valid_permutation(perm_input: tuple):
            return all(mask != perm_input[:len(mask)] for mask in failed_masks if len(mask) <= len(perm_input))
        
        for perm in perm_batch:
            if is_valid_permutation(tuple(perm)):
                result = find_combinations_for_each_input(perm, min_limit, num_dict, num_of_results)
                sorted_result = sorted(result, reverse=True)
                if len(result) == num_of_results and sorted_result not in results:
                    print(sorted_result, flush=True)
                    results.append(sorted_result)
                elif len(result) != num_of_results:
                    failed_masks.append(result)
        return 

    with Manager() as manager:
        results = manager.list()
        failed_masks = manager.list()
        iterations = 0

        # for perm_batch in batched(perm_gen, 1024):
        #     filter_permutations(perm_batch,
        #             min_limit,
        #             num_dict,
        #             num_of_results,
        #             results,
        #             failed_masks)
        #     iterations += 1
        #     print(iterations)
        # return results
        
        with ProcessPoolExecutor() as pool:
            futures = [pool.submit(
                    filter_permutations,
                    perm_batch,
                    min_limit,
                    num_dict,
                    num_of_results,
                    results,
                    failed_masks
                )
                for perm_batch in batched(perm_gen, 128)]

            for future in as_completed(futures):
                perm_result = future.result()
                iterations += 1
                print(iterations)
        return list(results)

if __name__ == '__main__':
    num_dict, perm_gen, num_count = generate_num_dict_and_permutations(((4, 7), (5, 5), (6, 6)), 12, 20)
    print(find_combinations(num_dict, perm_gen, num_count, 6, 12))