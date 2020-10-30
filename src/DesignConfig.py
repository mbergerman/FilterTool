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
        self.wo = 0

    def setParameters(self, type, aprox, denorm, minord, maxord, qmax, Ap, Aa, wp, wa, wo):
        self.type = self.type if type not in self.filter_types else self.filter_types.index(type)
        self.aprox = self.aprox if aprox not in self.aprox_types else self.aprox_types.index(aprox)
        self.denorm = denorm
        self.minord = minord
        self.maxord = maxord
        self.qmax = qmax
        self.Ap = Ap
        self.Aa = Aa
        self.wp = wp
        self.wa = wa
        self.wo = wo
