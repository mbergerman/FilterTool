class DesignConfig:
    def __init__(self, type=0, aprox=0, denorm=0, minord=0, maxord=0, qmax=0, Ap=0, Aa=0, wp=0, wa=0, wp2=0, wa2=0, tau=0, wrg=0, gamma=0):
        self.filter_types = ['Pasa Bajos', 'Pasa Altos', 'Pasa Banda', 'Rechaza Banda', 'Retardo de Grupo']
        self.aprox_types = ['Butterworth', 'Chebyshev I', 'Chebyshev II', 'Bessel', 'Cauer', 'Legendre', 'Gauss']

        self.type = type
        self.aprox = aprox
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
        self.tau = tau
        self.wrg = wrg
        self.gamma = gamma

    def setType(self, type):
        self.type = self.type if type not in self.filter_types else self.filter_types.index(type)

    def setAprox(self, aprox):
        self.aprox = self.aprox if aprox not in self.aprox_types else self.aprox_types.index(aprox)

    def getType(self):
        return self.filter_types[self.type]

    def getAprox(self):
        return self.filter_types[self.aprox]

    def setParameters(self, type, aprox, denorm, minord, maxord, qmax, Ap, Aa, wp, wa, wp2, wa2, tau, wrg, gamma):
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
        self.tau = tau
        self.wrg = wrg
        self.gamma = gamma

    def __str__(self):
        return str(self.type) + '\n' + \
                str(self.aprox) + '\n' + \
                str(self.denorm) + '\n' + \
                str(self.minord) + '\n' + \
                str(self.maxord) + '\n' + \
                str(self.qmax) + '\n' + \
                str(self.Ap) + '\n' + \
                str(self.Aa) + '\n' + \
                str(self.wp) + '\n' + \
                str(self.wa) + '\n' + \
                str(self.wp2) + '\n' + \
                str(self.wa2) + '\n' + \
                str(self.tau) + '\n' + \
                str(self.wrg) + '\n' + \
                str(self.gamma) + '\n'