from Quicksort import Quicksort


class Rekenmachine:
    def median(self, lst):
        """ Retourneer de mediaan (float) van de lijst lst. """
        self.sorteer_data(lst)
        if len(lst) % 2 == 1:
            middelste = len(lst) / 2
            mediaan = float(lst[int(middelste)])
        else:
            pos1 = int((len(lst) - 1) // 2)
            pos2 = pos1 + 1
            middelste1 = lst[pos1]
            middelste2 = lst[pos2]
            mediaan = float(self.mean([middelste1, middelste2]))

        return mediaan

    def mean(self, lst):
        """ Retourneer het gemiddelde (float) van de lijst lst. """
        totaal = 0
        aantal = 0
        for getal in lst:
            totaal += getal
            aantal += 1
        return totaal / aantal

    def q1(self, lst):
        """
        Retourneer het eerste kwartiel Q1 (float) van de lijst lst.
        Tip: maak gebruik van median()
        """
        self.sorteer_data(lst)
        med = self.median(lst)
        sublijst = []
        for x in range(0, len(lst)):
            if lst[x] < med:
                sublijst.append(lst[x])
            if lst[x] == med and lst[x + 1] == lst[x]:
                sublijst.append(lst[x])
        return self.median(sublijst)

    def q3(self, lst):
        """ Retourneer het derde kwartiel Q3 (float) van de lijst lst. """
        self.sorteer_data(lst)
        med = self.median(lst)
        sublijst = []
        for x in range(len(lst) - 1, 0, -1):
            if lst[x] > med:
                sublijst.append(lst[x])
            if lst[x] == med and lst[x - 1] == lst[x]:
                sublijst.append(lst[x])
        return self.median(sublijst)

    def sorteer_data(self, data):
        quicksort = Quicksort(data)
        quicksort.quickSortIterative(data, 0, len(data) - 1)
        """ Deze funtie sorteert de ingevoerde data."""
