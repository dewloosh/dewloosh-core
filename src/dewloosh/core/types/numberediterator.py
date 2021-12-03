from pyoneer.core.types.numberedentity import UniqueNumbered
import numpy as np


class NumberedList(list):
    """
    Makes it possible to loop over a list of items with discontinous numbering.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.Sequence = None
        self.SortedLoop = False
        self.counter = None
        return

    def build_sequence(self):
        state = self.SortedLoop
        self.SortedLoop = False
        self.Sequence = np.zeros(len(self), dtype=np.int32)
        numbers = np.array([item.Num for item in self], dtype=np.int32)
        self.Sequence = np.argsort(numbers)
        self.SortedLoop = state
        return

    def __iter__(self):
        if (self.SortedLoop == True) and (self.Sequence is None):
            self.build_sequence()
        self.counter = -1
        return self

    def __next__(self):
        if self.counter < len(self)-1:
            self.counter += 1
            if self.SortedLoop:
                return self[self.Sequence[self.counter]]
            else:
                return self[self.counter]
        else:
            self.counter = -1
            raise StopIteration

    def append(self, item):
        if not hasattr(item, 'Num'):
            raise TypeError("Item doesn't have attribute 'Num'.")
        super().append(item)
        return


if __name__ == '__main__':

    item1 = UniqueNumbered(num=2)
    item2 = UniqueNumbered(num=1)
    item3 = UniqueNumbered(num=-5)
    item4 = UniqueNumbered(num=100)
    item5 = UniqueNumbered(num=-1)

    l = NumberedList()
    l.append(item1)
    l.append(item2)
    l.append(item3)
    l.append(item4)
    l.append(item5)

    print('first print')
    l.SortedLoop = True
    for item in l:
        print(item.Num)

    print('second print')
    l.SortedLoop = False
    for item in l:
        print(item.Num)
