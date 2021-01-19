class Quicksort:
    def __init__(self, data):
        """ Init functie van de class"""
        self.data = data

    def start_recursive(self):
        """ Deze functie wordt aangeroepen om het recursive quicksort algoritme te gebruiken"""
        self.quicksortRecusrive(self.data, 0, len(self.data) - 1)

    def start_iterative(self):
        """ Deze functie wordt aangeroepen om het iteratieve quicksort algoritme te gebruiken (grote data)"""
        self.quickSortIterative(self.data, 0, len(self.data) - 1)

    def quicksortRecusrive(self, lst, min, max):
        """ deze functie bepaalt het middenpunt, en als het element kleiner is dan het middelpunt wordt
         het naar links verplaatst"""
        if min < max:
            middelpunt = self.verplaatsRecusive(lst, min, max)
            self.quicksortRecusrive(lst, min, middelpunt - 1)
            self.quicksortRecusrive(lst, middelpunt + 1, max)

    def verplaatsRecusive(self, data, min, max):
        """ Deze functie verplaatst het element en bepaalt een nieuw middenpunt"""
        kleinste = (min - 1)
        middelpunt = data[max]

        for j in range(min, max):

            if data[j] < middelpunt:
                kleinste = kleinste + 1
                data[kleinste], data[j] = data[j], data[kleinste]

        data[kleinste + 1], data[max] = data[max], data[kleinste + 1]
        return kleinste + 1

    def verplaatsIterative(self, arr, l, h):
        """ Deze functie verplaatst het element en bepaalt een nieuw middenpunt"""
        i = (l - 1)
        x = arr[h]

        for j in range(l, h):
            if arr[j] <= x:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[h] = arr[h], arr[i + 1]
        return i + 1

    def quickSortIterative(self, arr, l, h):
        """ deze functie bepaalt het middenpunt, en als het element kleiner is dan het middelpunt wordt
                 het naar links verplaatst, anders naar rechts."""

        # Create an auxiliary stack
        size = h - l + 1
        stack = [0] * size

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
            p = self.verplaatsIterative(arr, l, h)

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
