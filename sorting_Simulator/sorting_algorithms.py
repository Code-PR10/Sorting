import time
from typing import List, Callable, Any

class SortingAlgorithms:
    def __init__(self, update_callback: Callable[[List[int], dict, dict], None]):
        self.update_callback = update_callback
        
    def bubble_sort(self, arr: List[int], stats: dict) -> None:
        n = len(arr)
        swapped = True
        
        while swapped:
            swapped = False
            for j in range(n - 1):
                # Update state for comparison
                state = {'comparing': [j, j + 1]}
                stats["comparisons"] += 1
                self.update_callback(arr, stats, state)
                
                if arr[j] > arr[j + 1]:
                    # Update state for swap
                    state = {'swapping': [j, j + 1]}
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    stats["swaps"] += 1
                    self.update_callback(arr, stats, state)
                    swapped = True
                    
            # Mark the last element as sorted
            n -= 1
            state = {'sorted': list(range(n, len(arr)))}
            self.update_callback(arr, stats, state)
            
        # Mark all elements as sorted at the end
        state = {'sorted': list(range(len(arr)))}
        self.update_callback(arr, stats, state)
        
    def selection_sort(self, arr: List[int], stats: dict) -> None:
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                stats["comparisons"] += 1
                self.update_callback(arr, stats)
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                stats["swaps"] += 1
                self.update_callback(arr, stats)
                
    def insertion_sort(self, arr: List[int], stats: dict) -> None:
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            
            stats["comparisons"] += 1
            self.update_callback(arr, stats)
            
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                stats["swaps"] += 1
                stats["comparisons"] += 1
                self.update_callback(arr, stats)
                
            arr[j + 1] = key
            self.update_callback(arr, stats)
            
    def merge_sort(self, arr: List[int], stats: dict) -> None:
        def merge(left: List[int], right: List[int], start_idx: int) -> List[int]:
            result = []
            left_idx = right_idx = 0
            
            while left_idx < len(left) and right_idx < len(right):
                stats["comparisons"] += 1
                self.update_callback(arr, stats)
                
                if left[left_idx] < right[right_idx]:
                    result.append(left[left_idx])
                    left_idx += 1
                else:
                    result.append(right[right_idx])
                    right_idx += 1
                    
            result.extend(left[left_idx:])
            result.extend(right[right_idx:])
            return result
            
        def sort(arr: List[int], start_idx: int = 0) -> List[int]:
            if len(arr) <= 1:
                return arr
                
            mid = len(arr) // 2
            left = sort(arr[:mid], start_idx)
            right = sort(arr[mid:], start_idx + mid)
            
            result = merge(left, right, start_idx)
            
            # Update the original array
            for i, val in enumerate(result):
                arr[i] = val
                self.update_callback(arr, stats)
                
            return result
            
        sort(arr)
        
    def quick_sort(self, arr: List[int], stats: dict) -> None:
        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                stats["comparisons"] += 1
                self.update_callback(arr, stats)
                
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    stats["swaps"] += 1
                    self.update_callback(arr, stats)
                    
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            stats["swaps"] += 1
            self.update_callback(arr, stats)
            return i + 1
            
        def sort(low: int, high: int) -> None:
            if low < high:
                pi = partition(low, high)
                sort(low, pi - 1)
                sort(pi + 1, high)
                
        sort(0, len(arr) - 1)
        
    def heap_sort(self, arr: List[int], stats: dict) -> None:
        def heapify(n: int, i: int) -> None:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n:
                stats["comparisons"] += 1
                self.update_callback(arr, stats)
                if arr[left] > arr[largest]:
                    largest = left
                    
            if right < n:
                stats["comparisons"] += 1
                self.update_callback(arr, stats)
                if arr[right] > arr[largest]:
                    largest = right
                    
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                stats["swaps"] += 1
                self.update_callback(arr, stats)
                heapify(n, largest)
                
        n = len(arr)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)
            
        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            stats["swaps"] += 1
            self.update_callback(arr, stats)
            heapify(i, 0)
            
    def counting_sort(self, arr: List[int], stats: dict) -> None:
        max_val = max(arr)
        min_val = min(arr)
        range_of_elements = max_val - min_val + 1
        
        count = [0] * range_of_elements
        output = [0] * len(arr)
        
        # Store count of each element
        for i in range(len(arr)):
            count[arr[i] - min_val] += 1
            self.update_callback(arr, stats)
            
        # Change count[i] so that it contains actual position
        for i in range(1, len(count)):
            count[i] += count[i - 1]
            
        # Build the output array
        for i in range(len(arr) - 1, -1, -1):
            output[count[arr[i] - min_val] - 1] = arr[i]
            count[arr[i] - min_val] -= 1
            stats["swaps"] += 1
            self.update_callback(arr, stats)
            
        # Copy the output array to arr
        for i in range(len(arr)):
            arr[i] = output[i]
            self.update_callback(arr, stats)
            
    def radix_sort(self, arr: List[int], stats: dict) -> None:
        def counting_sort_for_radix(exp: int) -> None:
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            # Store count of occurrences
            for i in range(n):
                index = (arr[i] // exp) % 10
                count[index] += 1
                self.update_callback(arr, stats)
                
            # Change count[i] so that it contains actual position
            for i in range(1, 10):
                count[i] += count[i - 1]
                
            # Build the output array
            for i in range(n - 1, -1, -1):
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                stats["swaps"] += 1
                self.update_callback(arr, stats)
                
            # Copy the output array to arr
            for i in range(n):
                arr[i] = output[i]
                self.update_callback(arr, stats)
                
        max_val = max(arr)
        exp = 1
        
        while max_val // exp > 0:
            counting_sort_for_radix(exp)
            exp *= 10
            
    def bucket_sort(self, arr: List[int], stats: dict) -> None:
        if not arr:
            return
            
        # Find maximum and minimum values
        max_val = max(arr)
        min_val = min(arr)
        range_of_elements = max_val - min_val
        
        # Create buckets
        bucket_size = range_of_elements / len(arr)
        buckets = [[] for _ in range(len(arr))]
        
        # Distribute elements into buckets
        for i in range(len(arr)):
            index = min(int((arr[i] - min_val) / bucket_size), len(arr) - 1)
            buckets[index].append(arr[i])
            self.update_callback(arr, stats)
            
        # Sort individual buckets
        for i in range(len(buckets)):
            if buckets[i]:
                # Use insertion sort for each bucket
                for j in range(1, len(buckets[i])):
                    key = buckets[i][j]
                    k = j - 1
                    while k >= 0 and buckets[i][k] > key:
                        buckets[i][k + 1] = buckets[i][k]
                        k -= 1
                        stats["comparisons"] += 1
                        stats["swaps"] += 1
                        self.update_callback(arr, stats)
                    buckets[i][k + 1] = key
                    
        # Concatenate all buckets
        index = 0
        for bucket in buckets:
            for item in bucket:
                arr[index] = item
                index += 1
                self.update_callback(arr, stats) 