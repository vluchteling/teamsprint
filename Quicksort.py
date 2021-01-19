class Quicksort:
    def __init__(self, data):
        self.data = data

    def start_recursive(self):
        self.quicksortRecusrive(self.data, 0, len(self.data) - 1)

    def start_iterative(self):
        self.quickSortIterative(self.data, 0, len(self.data) - 1)

    def quicksortRecusrive(self, lst, min, max):
        if min < max:
            pi = self.verplaatsRecusive(lst, min, max)
            self.quicksortRecusrive(lst, min, pi - 1)
            self.quicksortRecusrive(lst, pi + 1, max)

    def verplaatsRecusive(self, data, min, max):
        kleinste = (min - 1)
        middelpunt = data[max]

        for j in range(min, max):

            if data[j] < middelpunt:
                kleinste = kleinste + 1
                data[kleinste], data[j] = data[j], data[kleinste]

        data[kleinste + 1], data[max] = data[max], data[kleinste + 1]
        return kleinste + 1

    def partitionIterative(self, arr, l, h):
        i = (l - 1)
        x = arr[h]

        for j in range(l, h):
            if arr[j] <= x:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[h] = arr[h], arr[i + 1]
        return (i + 1)

    def quickSortIterative(self, arr, l, h):

        # Create an auxiliary stack
        size = h - l + 1
        stack = [0] * (size)

        # initialize top of stack
        top = -1

        # push initial values of l and h to stack
        top = top + 1
        stack[top] = l
        top = top + 1
        stack[top] = h

        # Keep popping from stack while is not empty
        while top >= 0:

            # Pop h and l
            h = stack[top]
            top = top - 1
            l = stack[top]
            top = top - 1

            # Set pivot element at its correct position in
            # sorted array
            p = self.partitionIterative(arr, l, h)

            # If there are elements on left side of pivot,
            # then push left side to stack
            if p - 1 > l:
                top = top + 1
                stack[top] = l
                top = top + 1
                stack[top] = p - 1

            # If there are elements on right side of pivot,
            # then push right side to stack
            if p + 1 < h:
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = h
