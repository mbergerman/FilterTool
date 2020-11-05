from src.DesignConfig import *
from src.FilterStage import *


class FilterDesign:

    def __init__(self, dc = None, stages = None, poles = [], zeros = []):
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
        with open(filename, "w") as f:
            f.write('# Electronic Filter Design Tool v0.1\n')

            f.write('DesignConfig\n')
            if self.dc != None:
                f.write(str(self.dc))

            f.write('FilterStages\n')
            if self.stages != None:
                for stage in self.stages.values():
                    f.write(str(stage))

            f.write('Poles\n')
            if len(self.poles) > 0:
                for p in self.poles:
                    f.write(str(p))
                    f.write('\n')

            f.write('Zeros\n')
            if len(self.zeros) > 0:
                for z in self.zeros:
                    f.write(str(z))
                    f.write('\n')

    def open(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip()
            i = 0
            while lines[i] != 'DesignConfig': i+=1
            type = int(lines[i+1])
            aprox = int(lines[i+2])
            denorm = float(lines[i+3])
            minord = int(lines[i+4])
            maxord = int(lines[i+5])
            qmax = float(lines[i+6])
            Ap = float(lines[i+7])
            Aa = float(lines[i+8])
            wp = float(lines[i+9])
            wa = float(lines[i+10])
            wp2 = float(lines[i+11])
            wa2 = float(lines[i+12])
            tau = float(lines[i+13])
            wrg = float(lines[i+14])
            gamma = float(lines[i+15])
            i = i+16
    
            self.dc = DesignConfig(type, aprox, denorm, minord, maxord, qmax, Ap, Aa, wp, wa, wp2, wa2, tau, wrg, gamma)

            while lines[i] != 'FilterStages': i+=1
            i += 1
            self.stages = list()
            while lines[i] != 'Poles':
                pole1 = int(lines[i])
                pole2 = int(lines[i+1])
                zero1 = int(lines[i+2])
                zero2 = int(lines[i+3])
                Q = float(lines[i+4])
                self.stages.append(FilterStage(pole1, pole2, zero1, zero2, Q))
                i += 5
            i += 1
            self.poles = list()
            while lines[i] != 'Zeros':
                self.poles.append(complex(lines[i]))
                i += 1
            i += 1
            while i < len(lines) and len(lines[i]) > 0:
                self.zeros.append(complex(lines[i]))
                i += 1
        return
