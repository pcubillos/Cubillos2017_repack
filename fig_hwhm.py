import sys, os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

sys.path.append("../pyratbay")
import pyratbay as pb
import pyratbay.constants as pc


# Read Pyrat Bay objects:
pyrat = pb.pyrat.init("pyratbay_compress.cfg")
wn = pyrat.spec.wn     # Wavenumber (cm-1)
wl =1e4/pyrat.spec.wn  # Wavelength (micron)

# Calculate Doppler-width boundaries:
mass    = pyrat.mol.mass[ispec]
press   = pyrat.atm.press
nlayers = pyrat.atm.nlayers
q       = pyrat.atm.q[0]       # Abundances

temp1 = 2500.0
temp2 =  500.0

# Doppler profile HWHM:
dop1 = np.sqrt(2.0*pc.k*temp1/(mass*pc.amu)) * wn/pc.c
dop2 = np.sqrt(2.0*pc.k*temp2/(mass*pc.amu)) * wn/pc.c
# Lorentz profile HWHM:
dcoll = pyrat.mol.radius + pyrat.mol.radius[ispec]
fac = np.sum(dcoll**2 * q * np.sqrt(1.0/mass + 1.0/pyrat.mol.mass))
lor1 = np.sqrt(2/(np.pi*pc.k*temp1 * pc.amu)) * press/pc.c * fac
lor2 = np.sqrt(2/(np.pi*pc.k*temp2 * pc.amu)) * press/pc.c * fac

# Indices at wavelengths of 0.6 and 12 microns:
i1 = np.where(wl< 0.6)[0][0]
i2 = np.where(wl<12.0)[0][0]

# The plot:
lw = 2.0
plt.figure(-3, (7,6))
plt.clf()
plt.loglog(lor1, press/pc.bar, lw=lw, color="b", label='Lorentz')
plt.loglog(lor2, press/pc.bar, lw=lw, color="b", ls='--')
# Widths at 0.6 microns:
plt.plot(np.tile(dop1[i1], nlayers), press/pc.bar, lw=lw,
         color="orange", label='Doppler (0.6 um)')
plt.plot(np.tile(dop2[i1], nlayers), press/pc.bar, lw=lw,
         color="orange", ls="--")
# Widths at 12 microns:
plt.plot(np.tile(dop1[i2], nlayers), press/pc.bar, lw=lw,
         color="0.7", label='Doppler (12 um)')
plt.plot(np.tile(dop2[i2], nlayers), press/pc.bar, lw=lw,
         color="0.7", ls="--")
plt.ylim(1e2, 1e-5)
plt.xlabel("Line HWHM (cm-1)")
plt.ylabel("Pressure (bar)")
plt.legend(loc='best')
plt.savefig("../plots/broadening.ps")



