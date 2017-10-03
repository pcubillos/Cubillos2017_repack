#! /usr/bin/env python

import sys, os
import matplotlib
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d as gaussf
import matplotlib.pyplot as plt
plt.ion()

sys.path.append("../pyratbay")
import pyratbay as pb
import pyratbay.constants as pc


# Read Pyrat Bay objects:
pyrat1 = pb.pyrat.init("pyratbay_control.cfg")
pyrat2 = pb.pyrat.init("pyratbay_compress.cfg")
pressure = pyrat1.atm.press/pc.bar
wl =1e4/pyrat1.spec.wn


# The plot:
layer = 57  # 0.1 bar
ec1, label1 = pyrat1.get_ec(layer)
ec2, label2 = pyrat2.get_ec(layer)
layer = 95  # 50 bar
ec3, label3 = pyrat1.get_ec(layer)
ec4, label4 = pyrat2.get_ec(layer)

# Instrumental resolution (dnu=nu/R):
dnu = 1.0
# Sampling rate:
deltanu = np.abs(np.mean(np.ediff1d(pyrat1.spec.wn)))
sigma = (dnu/deltanu)/2.355
# Instrumental down grade:
efull1 = gaussf(ec1[0], sigma)
efull3 = gaussf(ec3[0], sigma)
elbl2  = gaussf(ec2[0], sigma)
econ2  = gaussf(ec2[1], sigma)
elbl4  = gaussf(ec4[0], sigma)
ecom2  = gaussf(ec2[0]+ec2[1], sigma)
ecom4  = gaussf(ec4[0]+ec4[1], sigma)

lw = 1.0
xran = 0.55, 33
fs = 12  # Fontsize
t  =  6  # Thinning

plt.figure(-5, (8.5, 8))
plt.clf()
plt.subplots_adjust(0.1, 0.07, 0.97, 0.98, hspace=0.15)
ax = plt.subplot(311)
plt.plot(wl[::t], ec1[0,::t], lw=lw, color="b", label='Full LBL')
plt.plot(wl[::t], ec2[0,::t], lw=lw, color="r", label='Compress LBL')
plt.plot(wl[::t], ec2[1,::t], lw=lw, color="limegreen",
         label='Compress continuum', alpha=0.8)
plt.ylabel("Extinction coefficient (cm-1)")
ax.set_yscale('log')
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
ax.set_yticks(np.logspace(-20, -10, 6))
plt.ylim(1e-20, 3e-10)
plt.xlim(xran)
plt.legend(loc="lower right", fontsize=fs)
plt.subplots_adjust(0.1, 0.07, 0.97, 0.98, hspace=0.15)
ax = plt.subplot(312)
plt.plot(wl[::t], 100*(ecom2/efull1-1)[::t], ".", ms=2, color="orange")
plt.plot(wl[::t], 100*(elbl2/efull1-1)[::t], ".", ms=2, color="black")
plt.plot([0,0],[1,1], ".", color="orange", label="LBL+continuum")
plt.plot([0,0],[1,1], ".", color="black",  label="LBL only")
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
plt.ylabel("Ext. coeff. difference (%)")
plt.text(20, -3, "P=0.1 bar")
plt.ylim(-5, 1)
plt.xlim(xran)
plt.legend(loc="lower right", fontsize=fs)
ax = plt.subplot(313)
plt.plot(wl[::t], 100*(ecom4/efull3-1)[::t], ".", ms=2, color="orange")
plt.plot(wl[::t], 100*(elbl4/efull3-1)[::t], ".", ms=2, color="black")
plt.ylabel("Ext. coeff. difference (%)")
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
plt.text(20, -3.5, "P=50 bar")
plt.ylim(-4, 3)
plt.xlim(xran)
plt.xlabel("Wavelength (um)")

plt.savefig("../plots/HCN_spectra.png", dpi=300)
plt.savefig("../plots/HCN_spectra.ps")
#plt.savefig("../plots/HCN_spectra.pdf")
