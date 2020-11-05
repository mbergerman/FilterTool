from scipy import signal
import numpy as np
from src.DesignConfig import *


def Butterworth(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'lowpass', 'Pasa Altos': 'highpass', 'Pasa Banda': 'bandpass',
                   'Rechaza Banda': 'bandstop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.buttord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.buttord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa],
                               designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]
    N = max(min(N, designconfig.maxord), designconfig.minord)

    z, p, k = signal.butter(N, Wn, btype=signaltypes[type], analog=True, output='zpk')

    p = setMaxQ(designconfig.qmax, p)

    return z, p, k


def ChebyshevI(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'lowpass', 'Pasa Altos': 'highpass', 'Pasa Banda': 'bandpass',
                   'Rechaza Banda': 'bandstop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.cheb1ord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.cheb1ord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa],
                                designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]
    N = max(min(N, designconfig.maxord), designconfig.minord)

    z, p, k = signal.cheby1(N, designconfig.Ap, Wn, btype=signaltypes[type], analog=True, output='zpk')

    p = setMaxQ(designconfig.qmax, p)

    return z, p, k


def ChebyshevII(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'lowpass', 'Pasa Altos': 'highpass', 'Pasa Banda': 'bandpass',
                   'Rechaza Banda': 'bandstop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.cheb2ord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.cheb2ord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa],
                                designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]
    N = max(min(N, designconfig.maxord), designconfig.minord)

    z, p, k = signal.cheby2(N, designconfig.Ap, Wn, btype=signaltypes[type], analog=True, output='zpk')

    p = setMaxQ(designconfig.qmax, p)

    return z, p, k


def Bessel(designconfig):
    n = 1
    wrgN = designconfig.tau * designconfig.wrg
    tb, ta = signal.bessel(N=n, Wn=1, btype='low', analog=True, output='ba', norm='delay')
    w = np.linspace(wrgN - 0.5, wrgN + 0.5, 1000)
    w, th = signal.freqs(tb, ta, w)
    gd = -np.diff(np.unwrap(np.angle(th))) / np.diff(w)
    while gd[500] < (1 - (designconfig.gamma / 100)):
        n += 1
        tb, ta = signal.bessel(N=n, Wn=1, btype='low', analog=True, output='ba', norm='delay')
        w = np.linspace(wrgN - 0.5, wrgN + 0.5, 1000)
        w, th = signal.freqs(tb, ta, w)
        gd = -np.diff(np.unwrap(np.angle(th))) / np.diff(w)

    if n < designconfig.minord: n = designconfig.minord
    if n > designconfig.maxord: n = designconfig.maxord

    z, p, k = signal.bessel(n, 1, 'low', analog=True, output='zpk', norm='delay')

    for i in range(len(p)):
        p[i] = p[i] / designconfig.tau

    for i in range(len(z)):
        z[i] = z[i] / designconfig.tau

    k = k / (designconfig.tau ** (n - len(z)))

    p = setMaxQ(designconfig.qmax, p)

    return z, p, k

def Cauer(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'low', 'Pasa Altos': 'high', 'Pasa Banda': 'pass',
                   'Rechaza Banda': 'stop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.ellipord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.ellipord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa],
                               designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]
    N = max(min(N, designconfig.maxord), designconfig.minord)
    return signal.ellip(N, designconfig.Ap, designconfig.Aa, Wn, btype=signaltypes[type], analog=True, output='zpk')


def setMaxQ(maxQ, poles):
    for i in range(len(poles)):
        w0 = abs(poles[i])
        a = abs(poles[i].real)
        Q = w0 / (2 * a)
        if Q > maxQ:
            w0st = (maxQ-0.05) * 2 * a
            ast = w0 / (2 * (maxQ-0.05))
            pst1 = [-a, np.sign(poles[i].imag) * ((w0st ** 2 - a ** 2) ** (1 / 2))]
            pst2 = [-ast, poles[i].imag]

            m = (pst2[1] - pst1[1]) / (pst2[0] - pst1[0])
            line = lambda x: m * (x - pst1[0]) + pst1[1]
            xs = np.linspace(min(-a, -ast), max(-a, -ast), 1000)
            ys = line(xs)
            difs = np.zeros(len(xs))

            min_dif = w0
            value = 0
            for n in range(len(xs)):
                difs[n] = ((xs[n] - poles[i].real) ** 2 + (ys[n] - poles[i].imag) ** 2) ** (1 / 2)
                if difs[n] < min_dif:
                    value = n
                    min_dif = difs[n]

            poles[i] = xs[value] + 1j*ys[value]

    return poles
