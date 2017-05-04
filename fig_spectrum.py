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
plt.figure(-2, (8.5, 6))
plt.clf()
plt.subplots_adjust(0.1, 0.1, 0.97, 0.95)
ax = plt.subplot(211)
plt.semilogy(wl, ec1[0], lw=lw, color="b", label='Full LBL', alpha=0.6)
plt.semilogy(wl, ec2[0], lw=lw, color="r", label='repack LBL', zorder=0)
plt.semilogy(wl, ec2[1], lw=lw, color="limegreen", label='repack continuum',
             alpha=0.9)
plt.ylabel("Extinction coefficient (cm-1)")
ax.set_xscale('log')
plt.xlim(0.6, 33)
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
plt.ylim(1e-20, 3e-10)
plt.legend(loc="best")
# Difference:
ax = plt.subplot(212)
plt.plot([0.3, 33.0], [0.0, 0.0], "--", color="0.6")
plt.plot(wl, 100*(ec2[0]-ec1[0])/ec1[0], ".", ms=2, lw=lw, color="orange")
plt.plot(wl, 100*(ec4[0]-ec3[0])/ec3[0], ".", ms=2, lw=lw, color="k")
plt.plot([0,0],[1,1], ".", color="orange", label="0.1 bar")
plt.plot([0,0],[1,1], ".", color="black",  label="50 bar")
plt.ylabel("LBL difference (%)")
plt.xlim(0.6, 33)
plt.ylim(-10, 1)
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xticks([0.6, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0])
plt.xlabel("Wavelength (um)")
plt.legend(loc="best")
plt.savefig("../plots/HCN_spectra.png", dpi=600)
plt.savefig("../plots/HCN_spectra.ps")
plt.savefig("../plots/HCN_spectra.pdf")
