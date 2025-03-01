import heapq

# Min-heap is used by a list initatialized to 0
# For a max-heap, negate each number before and after getting out from the heap
# Elements start at position 0, left child is at position 2k + 1, and right at 2k + 2


heap = []

heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappush(heap, -1)
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)

# # The smallest element in a heap is always heap[0]
# print(heap[0])
#
# while len(heap) > 0:
#     top = heapq.heappop(heap)
#     print(top)


# To transform any list to a min-heap use heap.heapify()

def top_k(nums: list, k: int) -> list:
    import heapq

    heap = []
    for num in nums:
        if len(heap) < k:
            heapq.heappush(heap, num)
        else:
            if heap[0] < num:
                heapq.heappop(heap)
                heapq.heappush(heap, num)

    return sorted(heap, reverse=True)


print(top_k([3, 5, 2, 7, 5, 4], k=3))


x = [2, 2, 3, 3, 5, 6]

heapq.heapify(x)

print(x)