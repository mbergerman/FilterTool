from scipy import signal
import numpy as np
from src.DesignConfig import *

def Butterworth(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'lowpass', 'Pasa Altos': 'highpass', 'Pasa Banda': 'bandpass', 'Rechaza Banda': 'bandstop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.buttord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.buttord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa], designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]

    return signal.butter(N, Wn, btype=signaltypes[type], analog=True, output='zpk')

def ChebyshevI(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'lowpass', 'Pasa Altos': 'highpass', 'Pasa Banda': 'bandpass', 'Rechaza Banda': 'bandstop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.cheb1ord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.cheb1ord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa], designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]

    return signal.cheby1(N, designconfig.Ap, Wn, btype=signaltypes[type], analog=True, output='zpk')

def ChebyshevII(designconfig):
    type = designconfig.getType()
    signaltypes = {'Pasa Bajos': 'lowpass', 'Pasa Altos': 'highpass', 'Pasa Banda': 'bandpass', 'Rechaza Banda': 'bandstop'}
    if type == 'Pasa Bajos' or type == 'Pasa Altos':
        N, Wn = signal.cheb2ord(designconfig.wp, designconfig.wa, designconfig.Ap, designconfig.Aa, True)
    elif type == 'Pasa Banda' or type == 'Rechaza Banda':
        N, Wn = signal.cheb2ord([designconfig.wp2, designconfig.wp], [designconfig.wa2, designconfig.wa], designconfig.Ap, designconfig.Aa, True)
    else:
        return [[], [], 0]

    return signal.cheby2(N, designconfig.Ap, Wn, btype=signaltypes[type], analog=True, output='zpk')