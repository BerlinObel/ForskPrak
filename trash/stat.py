# ----------IMPORT----------
import numpy as np
from ase.visualize import view
from ase.neighborlist import neighbor_list
from time import time
from ase.cluster.cubic import FaceCenteredCubic
import itertools
from collections import Counter
from ase.geometry import analysis
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
import pickle
from ase.io.trajectory import Trajectory
import iteround, itertools
from sklearn.model_selection import ParameterGrid
import sys


# bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(['Ag','Pd','Pt','Au','Ir'], 2))])

def chi2_uncert(observed_frac,expected_frac,uncertainties):
        chi2 = np.sum((observed_frac-expected_frac)**2/uncertainties**2)
        Ndof = len(observed_frac) -1
        prob_chi2 = stats.chi2.sf(chi2, Ndof)
        return chi2, Ndof, prob_chi2

def pearsons_chi2(observed_N, expected_N,size):
    chi2 = (np.sum((observed_N - expected_N) ** 2 / expected_N))/size
    Ndof = len(observed_N) - 1
    prob_chi2 = stats.chi2.sf(chi2, Ndof)
    return chi2, Ndof, prob_chi2

def chi(observed_N, expected_N):
    return np.sum((observed_N - expected_N) ** 2 / expected_N)

df2 = 2
df3 = 5
df4 = 9
df5 = 14
x2 = np.linspace(stats.chi2.ppf(0.01,df2),stats.chi2.ppf(0.99,df2),100)
x3 = np.linspace(stats.chi2.ppf(0.01,df3),stats.chi2.ppf(0.99,df3),100)
x4 = np.linspace(stats.chi2.ppf(0.01,df4),stats.chi2.ppf(0.99,df4),100)
x5 = np.linspace(stats.chi2.ppf(0.01,df5),stats.chi2.ppf(0.99,df5),100)

#fig, ax = plt.subplots(1,1)

#ax.plot(x2,1-stats.chi2.cdf(x2,df2),'r-',lw=5,alpha=0.6,label='chi2 pdf')
#ax.plot(x3,1-stats.chi2.cdf(x3,df3),'b--',lw=5,alpha=0.6,label='chi2 pdf')
#ax.plot(x4,1-stats.chi2.cdf(x4,df4),'g-',lw=5,alpha=0.6,label='chi2 pdf')
#ax.plot(x5,1-stats.chi2.cdf(x5,df5),'c--',lw=5,alpha=0.6,label='chi2 pdf')
#r=stats.chi2.rvs(4,size=1000)
#r2=stats.chi2.rvs(2,size=500)

#ax[0].hist(r, density=True, histtype='stepfilled', alpha=0.2)
#ax[1].hist(r2, density=True, histtype='stepfilled', alpha=0.2)
#plt.show()

chiz=[]
chis=[]
dubchis=[]
trichis=[]
"""
for i in range(100):
    npobs = np.array([i/2,100-i,i/2])
    npexp = np.array([25,50,25])
    chis.append(chi(npobs,npexp)/100)
    chiz.append(chi(npobs,npexp))
    dubchis.append(chi(2*npobs,2*npexp)/200)
    trichis.append(chi(3*npobs,3*npexp)/300)
"""

for i in range(100):
    npobs = np.array([i/2,100-i,i/2])
    npexp = np.array([25,50,25])
    _,_,a = pearsons_chi2(npobs,npexp,1)
    _,_,b = pearsons_chi2(2*npobs,2*npexp,1)
    _,_,c = pearsons_chi2(3*npobs,3*npexp,1)
    chis.append(a)
    #chiz.append(chi(npobs,npexp))
    dubchis.append(b)
    trichis.append(c)

fig, ax = plt.subplots(1,1)
ax.plot(range(100),chis,'r-',lw=5,alpha=0.6,label='chi2 pdf')
#ax.plot(range(100),chiz,'g-',lw=5,alpha=0.6,label='chi2 pdf')
ax.plot(range(100),dubchis,'b-',lw=5,alpha=0.6,label='chi2 pdf')
ax.plot(range(100),trichis,'g--',lw=5,alpha=0.6,label='chi2 pdf')
plt.show()