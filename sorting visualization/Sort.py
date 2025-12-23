"""
Contains the sorting algos

1) bubble
2) selection
3) insertion
4) merge
5) quick

"""
import random
import tkinter as tk

class Sort:

    def __init__(self, length, canvas=None, speed=20):
        self.arr = self.create_array(length)
        self.length = length
        self.speed = speed
        self.width = 1500/length
        print(self.width)
        self.canvas = canvas
        self.draw_arr()

        self.quick_sort(0, length -1)

    def wait(self):
        pass

    def create_array(self, length=10):
        return [random.randint(1, 800) for i in range(length)]

    def __array_state__(self):
        return self.arr

    def bubble_sort(self):
        for i in range(self.length):
            for j in range(0, self.length-i-1):
                if self.arr[j] > self.arr[j+1]:
                    temp = self.arr[j]
                    self.arr[j] = self.arr[j+1]
                    self.arr[j+1] = temp
                self.empty_canvas()
                self.draw_arr(j)
                self.canvas.after(self.speed, self.wait)

    def selection_sort(self):
        min = self.arr[0]
        min_index = 0
        temp = 0
        for i in range(self.length):
            min = self.arr[i]
            min_index = i
            for j in range(i, self.length):
                if min > self.arr[j]:
                    min = self.arr[j]
                    min_index = j

                self.empty_canvas()
                self.draw_arr(min_index)
                self.canvas.after(self.speed, self.wait)
            temp = self.arr[min_index]
            self.arr[min_index] = self.arr[i]
            self.arr[i] = temp
            # print(self.arr)

    def insertion_sort(self):
        temp = 0
        for i in range(self.length):
            k = i
            j = i-1
            while(self.arr[k] < self.arr[j] and k > 0):
                temp = self.arr[k]
                self.arr[k] = self.arr[j]
                self.arr[j] = temp
                k -= 1
                j -= 1
                self.empty_canvas()
                self.draw_arr(k)
                self.canvas.after(self.speed, self.wait)

    def quick_sort(self, start, end):
        if(start >= end):
            return None

        povit = start
        lesser = start + 1
        bigger = end

        while lesser <= bigger:

            while(lesser <= bigger and self.arr[lesser] <= self.arr[povit]):
                lesser += 1

            while(self.arr[bigger] >= self.arr[povit] and lesser <= bigger):
                bigger -= 1

            if lesser <= bigger:
                temp = self.arr[lesser]
                self.arr[lesser] = self.arr[bigger]
                self.arr[bigger] = temp

            self.empty_canvas()
            self.draw_arr(povit)
            # self.canvas.after(0, self.wait)

        temp = self.arr[povit]
        self.arr[povit] = self.arr[bigger]
        self.arr[bigger] = temp
        self.quick_sort(start, bigger - 1)
        self.quick_sort(bigger + 1, end)

    def empty_canvas(self):
        self.canvas.delete("all")

    def draw_arr(self, current=-1):
        for i in range(self.length):
            if i == current:

                self.canvas.create_rectangle(i*self.width, 800, (i+1)*self.width, 800-self.arr[i],fill = "green")
            else:
                self.canvas.create_rectangle(i * self.width, 800, (i + 1) * self.width, 800 - self.arr[i], fill="white")

        self.canvas.update()


if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1500x800+0+0")

    canvas = tk.Canvas(root, bg="black", height=800, width=1500)
    canvas.pack()

    sort = Sort(900, canvas, speed=1)

    root.mainloop()

