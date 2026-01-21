from typing import List, Optional, Tuple

def binary_search_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    left, right = 0, len(arr) - 1
    iterations = 0
    ub_index = -1

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        val = arr[mid]

        if val >= target:
            ub_index = mid
            right = mid - 1
        else:
            left = mid + 1

    return iterations, (None if ub_index == -1 else arr[ub_index])


if __name__ == "__main__":
    arr = [0.1, 1.2, 1.2, 2.5, 3.14, 10.01]
    print(binary_search_upper_bound(arr, 1.2))
    print(binary_search_upper_bound(arr, 1.21))
    print(binary_search_upper_bound(arr, -5))
    print(binary_search_upper_bound(arr, 999))
