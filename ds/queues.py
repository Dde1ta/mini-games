import math
import random


class Queue:

    def __init__(self, list_=None):
        if list_ is None:
            list_ = []
        self.q = list_

    def pop(self) -> int:
        return self.q.pop()

    def push(self, obj):
        p = [obj]
        p.extend(self.q)
        self.q = p

    def __str__(self):
        print(self.q)

    def __iter__(self):
        return iter(self.q)


class Heap:

    def __init__(self, size: int = 1000, dummy=math.inf):
        self.heap = []
        self.last = 0

    def insert(self, obj):
        self.heap.append(obj)

        for i in range(len(self.heap) - 1, -1, -1):
            self.heapify(i)

    def heapify(self, i: int):
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = self.heap[i]
        small = i

        if left < len(self.heap) and self.heap[left] < smallest:
            smallest = self.heap[left]
            small = left

        if right < len(self.heap) and self.heap[right] < smallest:
            smallest = self.heap[right]
            small = right

        if small != i:
            top = self.heap[i]
            self.heap[i] = self.heap[small]
            self.heap[small] = top
            self.heapify(small)

    def pop(self):
        top = self.heap[0]
        self.heap[0] = self.heap[-1]


        del self.heap[-1]

        if len(self.heap) == 0: return top

        for i in range(len(self.heap) - 1, -1, -1):
            self.heapify(i)


        return top

    def __str__(self):
        s = ""
        for i in self.heap:
            s += str(i)
            s += "->"
        return s


if __name__ == "__main__":
    heap = Heap(20)
    for i in range(20):
        heap.insert(random.randint(1,100))
        print(heap)


    while len(heap.heap) != 0:
        print(heap.pop())
