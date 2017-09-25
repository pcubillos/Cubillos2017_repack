#! /usr/bin/env python

import sys, os
import matplotlib
import numpy as np
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

lw = 1.0
xran = 0.55, 33
fs = 12

plt.figure(-4, (8.5, 8))
plt.clf()
plt.subplots_adjust(0.1, 0.07, 0.97, 0.98, hspace=0.15)
ax = plt.subplot(311)
plt.semilogy(wl, ec1[0], lw=lw, color="b", label='Full LBL')
plt.semilogy(wl, ec2[0], lw=lw, color="r", label='LBL repack')
plt.semilogy(wl, ec2[1], lw=lw, color="limegreen", label='Continuum repack',
              alpha=0.8)
plt.ylabel("Extinction coefficient (cm-1)")
ax.set_xscale('log')
plt.xlim(xran)
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
ax.set_yticks(np.logspace(-20, -10, 6))
plt.ylim(1e-20, 3e-10)
plt.legend(loc="lower right", fontsize=fs)
# Difference:
ax = plt.subplot(312)
plt.plot([0.3, 33.0], [0.0, 0.0], "--", color="0.6")
plt.plot(wl, 100*(ec2[0]-ec1[0])/ec1[0], ".", ms=2, lw=lw, color="orange")
plt.plot(wl, 100*(ec4[0]-ec3[0])/ec3[0], ".", ms=2, lw=lw, color="k")
plt.plot([0,0],[1,1], ".", color="orange", label="0.1 bar")
plt.plot([0,0],[1,1], ".", color="black",  label="50 bar")
plt.ylabel("LBL repack $-$ full LBL (%)")
plt.xlim(xran)
plt.ylim(-11, 1)
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
plt.legend(loc="lower right", fontsize=fs)
ax = plt.subplot(313)
plt.plot([0.3, 33.0], [0.0, 0.0], "--", color="0.6")
plt.plot(wl, 100*(ec2[0]+ec2[1]-ec1[0])/ec1[0], ".", ms=2, lw=lw,
         color="orange")
plt.plot(wl, 100*(ec4[0]+ec4[1]-ec3[0])/ec3[0], ".", ms=2, lw=lw,
         color="k", zorder=0)
plt.ylabel(r"LBL+cont repack $-$ full LBL (%)", fontsize=12)
plt.xlim(xran)
plt.ylim(-11, 11)
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
plt.xlabel("Wavelength (um)")

plt.savefig("../plots/HCN_spectra.png", dpi=300)
plt.savefig("../plots/HCN_spectra.ps")
plt.savefig("../plots/HCN_spectra.pdf")
