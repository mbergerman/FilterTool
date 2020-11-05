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
    return signal.butter(N, Wn, btype=signaltypes[type], analog=True, output='zpk')


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
    return signal.cheby1(N, designconfig.Ap, Wn, btype=signaltypes[type], analog=True, output='zpk')


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
    return signal.cheby2(N, designconfig.Ap, Wn, btype=signaltypes[type], analog=True, output='zpk')


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

    z, p, k = signal.bessel(n, 1, 'low', analog=True, output='zpk', norm='delay')

    for i in range(len(p)):
        p[i] = p[i] / designconfig.tau

    for i in range(len(z)):
        z[i] = z[i] / designconfig.tau

    k = k / (designconfig.tau ** (n - len(z)))

    return z, p, k
