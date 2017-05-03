import sys, os
import numpy as np
import scipy.constants as sc
import matplotlib.pyplot as plt

sys.path.append("./repack/")
import repack as r
u = r.utils
c = r.constants


# Load HCN data:
lblfiles = ["inputs/1H-12C-14N__Harris.trans",
            "inputs/1H-13C-14N__Larner.trans"]

suff, mol, iso1, pffile1, sfile1 = u.parse_file(lblfiles[0], "exomol")
suff, mol, iso2, pffile2, sfile2 = u.parse_file(lblfiles[1], "exomol")

# Read in data:
temp, pf1 = u.read_pf(pffile1)
temp, pf2 = u.read_pf(pffile2)

iratio, imass = u.read_iso(mol, [iso1, iso2])

e1, g1 = u.read_states(sfile1)
e2, g2 = u.read_states(sfile2)

gf1, elow1, wn1 = u.read_lbl(lblfiles[0], e1, g1)
gf2, elow2, wn2 = u.read_lbl(lblfiles[1], e2, g2)

# Select a narrow wn range:
iwn1 = (wn1 >= 5001.2) & (wn1 <= 5002.0)
iwn2 = (wn2 >= 5001.2) & (wn2 <= 5002.0)

wn1   = wn1  [iwn1]
elow1 = elow1[iwn1]
gf1   = gf1  [iwn1]

wn2   = wn2  [iwn2]
elow2 = elow2[iwn2]
gf2   = gf2  [iwn2]

# Stack isotopes together:
wn   = np.hstack([wn1,   wn2])
elow = np.hstack([elow1, elow2])
gf   = np.hstack([gf1,   gf2])
iiso = np.hstack([np.zeros(len(wn1), int), np.ones(len(wn2), int)])
# Sort by wn:
asort = np.argsort(wn)
gf   = gf  [asort]
elow = elow[asort]
wn   = wn  [asort]
iiso = iiso[asort]

# Partition function:
T = 1000.0
itemp = np.where(temp == T)[0][0]
Z = np.array([pf1[itemp], pf2[itemp]])

# Line intensity at 1000 K:
s = gf*iratio[iiso]/Z[iiso] * np.exp(-c.C2*elow/T) * (1-np.exp(-c.C2*wn/T))
# Line Doppler width:
alphad = wn/(100*sc.c) * np.sqrt(2.0*c.kB*T / (imass[iiso]*c.amu))

# Select strongest line in range:
i = np.argmax(s/alphad)
ran = (wn > wn[i]-6*alphad[i]) & (wn < wn[i]+6*alphad[i])
# Doppler broadening profile:
doppler = (s/alphad/np.sqrt(np.pi))[i] * np.exp(-(wn-wn[i])**2/alphad[i]**2)
# Flag out lines weaker than (broadened) selected line times sthresh:
sthresh=0.1
flag = s/alphad/np.sqrt(np.pi) > doppler*sthresh

# Figure 1:
plt.figure(-1, (8,5))
plt.clf()
ax = plt.subplot(111)
plt.plot(wn[ran], doppler[ran], "-", lw=1.25, color="r")
plt.plot(wn[ran], sthresh*doppler[ran], "-", lw=1.25, color="orange")
plt.semilogy(wn[flag],  (s/alphad/np.sqrt(np.pi))[flag],  ".k")
plt.semilogy(wn[~flag], (s/alphad/np.sqrt(np.pi))[~flag], ".", color="0.6")
plt.semilogy(wn[i], (s/alphad/np.sqrt(np.pi))[i], ".b")
ax.set_xticks([5001.2, 5001.4, 5001.6, 5001.8, 5002.0])
ax.set_xticklabels(["5001.2", "5001.4", "5001.6", "5001.8", "5002.0"], size=13)
ax.set_yticks([1e-20, 1e-18, 1e-16, 1e-14, 1e-12, 1e-10])
plt.yticks(size=13)
plt.ylim(3e-21, 1e-10)
plt.xlim(5001.2, 5002.0)
plt.xlabel(r"$\rm Wavenumber\ \ (cm^{-1})$", fontsize=14)
plt.ylabel(r"$\rm Line\ intensity/\delta_{\rm D}$", fontsize=14)
plt.savefig("plots/line-flagging.ps")






