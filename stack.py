# using list as a stack

stack = [1, 2, 3]
stack.pop()  # pops the last element of the list
stack.append(3)  # pushes on to the stack

# but for queues it's more efficient to use deque

from collections import deque

queue = deque()

queue.append(1)
queue.append(2)
queue.append(3)

print(queue[0])   # first element in the queue
print(queue[-1])  # last element in the queue

queue.popleft()   # remove (first) element from the queue

print(queue)

