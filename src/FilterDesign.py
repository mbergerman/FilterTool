from src.DesignConfig import *
from src.FilterStage import *


class FilterDesign:

    def __init__(self, dc = None, stages = None, poles = None, zeros = None):
        self.dc = dc
        self.stages = stages
        self.poles = poles
        self.zeros = zeros
        # Diseño circuital

    def setPolesAndZeros(self, p, z):
        self.poles = p.copy()
        self.zeros = z.copy()

    def setDesignConfig(self, dc):
        self.dc = dc

    def setFilterStages(self, stages):
        self.stages = stages

    def save(self, filename):
        f = open(filename + '.filter', "w")
        f.write('# Electronic Filter Design Tool v0.1\n')

        f.write('{}\n'.format(self.dc.type))
        f.write('{}\n'.format(self.dc.aprox))
        f.write('{}\n'.format(self.dc.denorm))
        f.write('{}\n'.format(self.dc.minord))
        f.write('{}\n'.format(self.dc.maxord))
        f.write('{}\n'.format(self.dc.qmax))
        f.write('{}\n'.format(self.dc.Ap))
        f.write('{}\n'.format(self.dc.Aa))
        f.write('{}\n'.format(self.dc.wp))
        f.write('{}\n'.format(self.dc.wa))
        f.write('{}\n'.format(self.dc.wp2))
        f.write('{}\n'.format(self.dc.type))
        f.write('{}\n'.format(self.dc.wa2))
        f.write('{}\n'.format(self.dc.tau))
        f.write('{}\n'.format(self.dc.wrg))
        f.write('{}\n'.format(self.dc.gamma))

        for stage in self.stages:
            f.write('{}\n'.format(stage.pole1))
            f.write('{}\n'.format(stage.pole2))
            f.write('{}\n'.format(stage.zero1))
            f.write('{}\n'.format(stage.zero2))

        f.close()

    def open(self, filename):
        f = open(filename, "r")
        lines = f.readlines()
        for i, line in enumerate(lines):
            lines[i].strip('\n')

        type = int(line[1])
        aprox = int(line[2])
        denorm = float(line[3])
        minord = int(line[4])
        maxord = int(line[5])
        qmax = float(line[6])
        Ap = float(line[7])
        Aa = float(line[8])
        wp = float(line[9])
        wa = float(line[10])
        wp2 = float(line[11])
        wa2 = float(line[12])
        tau = float(line[13])
        wrg = float(line[14])
        gamma = float(line[15])

        self.dc = DesignConfig()
        self.dc.setParameters(type, aprox, denorm, minord, maxord, qmax, Ap, Aa, wp, wa, wp2, wa2, tau, wrg, gamma)

        self.stages = list()
        i = 16
        while i < len(lines):
            pole1 = complex(line[i])
            pole2 = complex(line[i+1])
            zero1 = complex(line[i+2])
            zero2 = complex(line[i+3])
            self.stages.append(FilterStage(pole1, pole2, zero1, zero2))
            i += 4

        f.close()
