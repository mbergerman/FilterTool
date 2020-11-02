class DesignConfig:
    def __init__(self):
        self.filter_types = ['Pasa Bajos', 'Pasa Altos', 'Pasa Banda', 'Rechaza Banda', 'Retardo de Grupo']
        self.aprox_types = ['Butterworth', 'Chebyshev I', 'Chebyshev II', 'Bessel', 'Cauer', 'Legendre', 'Gauss']

        self.type = 0
        self.aprox = 0
        self.denorm = 0
        self.minord = 0
        self.maxord = 0
        self.qmax = 0
        self.Ap = 0
        self.Aa = 0
        self.wp = 0
        self.wa = 0
        self.wp2 = 0
        self.wa2 = 0

    def setType(self, type):
        self.type = self.type if type not in self.filter_types else self.filter_types.index(type)

    def setAprox(self, aprox):
        self.aprox = self.aprox if aprox not in self.aprox_types else self.aprox_types.index(aprox)

    def getType(self):
        return self.filter_types[self.type]

    def getAprox(self):
        return self.filter_types[self.aprox]

    def setParameters(self, type, aprox, denorm, minord, maxord, qmax, Ap, Aa, wp, wa, wp2, wa2):
        self.setType(type)
        self.setAprox(aprox)
        self.denorm = denorm
        self.minord = minord
        self.maxord = maxord
        self.qmax = qmax
        self.Ap = Ap
        self.Aa = Aa
        self.wp = wp
        self.wa = wa
        self.wp2 = wp2
        self.wa2 = wa2
