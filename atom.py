class Atom:
    def __init__(self, atomic_number, atomic_weight, symbol):
        self.atomic_number = atomic_number
        self.atomic_weight = atomic_weight
        self.symbol = symbol
        self.group = self.get_group()
        self.period = self.get_period()

    def get_period(self):
        if self.atomic_number < 3:
            return 1
        elif self.atomic_number < 11:
            return 2
        elif self.atomic_number < 19:
            return 3
        elif self.atomic_number < 37:
            return 4
        elif self.atomic_number < 55:
            return 5
        elif self.atomic_number < 87:
            return 6
        else:
            return 7

    def get_group(self):
        # k, l, m, n = 0
        k = 0
        l = 0
        m = 0
        n = 0
        electrons = []
        for i in range(2):
            if self.atomic_number > i:
                k += 1
        if k > 0:
            electrons.append(k)

        for i in range(8):
            if self.atomic_number - k > i:
                l += 1

        for i in range(8):
            if self.atomic_number - k - l > i:
                m += 1

        if m > 0:
            electrons.append(m)

        for i in range(8):
            if self.atomic_number - k - l - m > i + 1:
                n += 1

        if n > 0:
            electrons.append(n)

        return electrons[-1]