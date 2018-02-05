from matplotlib import pyplot as plt
import numpy as np
import h5py
from scipy.optimize import curve_fit

def func(x, a, b, c, d, e, f):
    return a*np.exp(-(x-c)/b)*np.exp(e*(np.exp(-(x-c)/f)-1)) + d

directory = 'D:\Data\Fluxonium #13\T1'
fname = '091817_T2E_YOKO_90.98mA_Cav7.3692GHz_-30dBm_Qubit0.8308GHz_25dBm_PiPulse239ns_Count30_TimeStep1000_Avg_10000.h5'
path = directory + '\\' + fname
pts_num = 50
time_step = 1000
t1_guess = 200e-6
t1_qp_guess = 10e-6
time = np.linspace(0, pts_num*time_step, pts_num)

#Read data and fit
with h5py.File(path,'r') as hf:
    print('List of arrays in this file: \n', hf.keys())
    count = np.array(hf.get('count'))
    phase_raw = hf.get('PHASEMAG_Phase0')
    # print phase_raw
    phase = phase_raw[0, 0]
    phase = np.unwrap(phase)*180/np.pi
    phase = phase - np.min(phase)
    phase = abs(phase[0::])
plt.plot(time, phase, 'rd')

guess = [phase[0]-phase[-1], t1_guess, 0, phase[-1], 1, t1_qp_guess]
popt, pcov = curve_fit(func, time*1e-9, phase, guess)
a,b,c,d,e,f = popt #b is T1
time_nice = np.linspace(0, pts_num*time_step, pts_num*100)
phase_fit = func(time_nice*1e-9, a, b, c, d, e, f)
perr = np.sqrt(abs(np.diag(pcov)))
plt.plot(time_nice, phase_fit)
plt.title(str( b*1e6)+ r'$\pm$' +str(perr[1]*1e6) + '\n' + str(f*1e6)+ r'$\pm$' +str(perr[5]*1e6)+ ';   ' + str(e))

plt.show()