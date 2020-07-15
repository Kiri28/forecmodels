# minimization class

class minimize:


    def __init__(self, funk, bounds = [-1, 1], method = 'dihotomy'):
        self.funk = funk
        self.data = data
        self.valid_space = bounds
        self.method = method

    def fit(self):
        # Here you can upload new methods!
        varians_mass = {'dihotomy': minimize.dihotomy(self)}
        return varians_mass[self.method]

    # Dihotomy minimization method
    def dihotomy(self):
        foo = self.funk
        ranger = self.valid_space

        delta = (ranger[1] - ranger[0])/4
        point = (ranger[1] + ranger[0])/2

        lenn = int(round((abs(ranger[1] - ranger[0])+100)/100.0)*100)
        for _ in range(100):
            if foo([point + delta]) < foo([point - delta]):
                point += delta
            else:
                point -= delta
            delta /= 2

        return [point, foo([point])]
