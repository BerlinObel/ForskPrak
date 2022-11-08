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
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy import special
import pickle
from ase.io.trajectory import Trajectory
import iteround, itertools
from sklearn.model_selection import ParameterGrid
import sys
    

def pdf(x,shape,scale):
    return (1/(special.gamma(shape)*scale**shape))*x**(shape-1)*np.exp(-x/scale)



def plot():
    ele =['ag','pd','pt','au','rh']
    sizes = [640,1560,2160]
    TF = [True,False]
    for bo in TF:
        pbc = bo
        for size in sizes:
            heap_size = size
            for i in range(3):
                bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[i+1:], 2))])
                elements = 4-i
                pval_bootstrap = np.loadtxt(f"bulk_{elements}_{heap_size}_{pbc}.txt")


                mean = np.mean(pval_bootstrap)
                var = np.var(pval_bootstrap)
                theta =  var/mean
                k = mean/theta
                X = np.linspace(0,np.max(pval_bootstrap),1000)
                Y = pdf(X,k,theta)

                k2 = mean/2
                Y2 = pdf(X,k2,2)
                Y3 = stats.chi2.pdf(X, len(bonds)-1)

                fig, ax = plt.subplots(1, 1, figsize=(8, 8))
                ax.hist(pval_bootstrap, bins=np.arange(0,50,0.25), histtype='bar', color='steelblue', alpha=0.7)
                ax.hist(pval_bootstrap, bins=np.arange(0,50,0.25), histtype='step', color='steelblue')
                ax2 = ax.twinx()
                ax2.plot(X,Y,color='seagreen')
                ax2.plot(X,Y2,'--',color='orange')
                ax2.plot(X,Y3,'-.',color='red')
                #ax.vlines(np.median(pval_bootstrap), 0, ax.get_ylim()[1], color='firebrick')
                #ax.vlines(np.percentile(pval_bootstrap,95),0, ax.get_ylim()[1], color='darkviolet')
                #ax.vlines(np.percentile(pval_bootstrap,99),0, ax.get_ylim()[1], color='seagreen')
                ax.set(ylim=(0, ax.get_ylim()[1] * 1.2))
                ax2.set(ylim=(0, ax2.get_ylim()[1] * 1.2))
                #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+'\n'+r'N$_{hops}$: '+f'{kwargs["n_hops"]}'+f'\nBond modifier: {kwargs["het_mod"]:.2f}' +\
                #f'\nMedian p-value = {np.median(pval_bootstrap):.2f} '+f'\nAdded atoms: ' + f'{kwargs["heanp_size"]}', family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
                ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{elements}'+ f"\nNP size: {heap_size}"+f'\nPeriodicity:{pbc}\n'+f'Scale:{theta}'  , family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
                ax2.legend([f'Shape: {k}',f'Shape: {k2}',f'DoF: {(len(bonds)-1)}'])
                #'\nMedian p-value = {np.median(pval_bootstrap):.2f}'+f"\n95%: {np.percentile(pval_bootstrap,95,method='inverted_cdf')}"+f"\n99%: {np.percentile(pval_bootstrap,99,method='inverted_cdf')}"
                ax.set_xlabel(r"$\chi^2$", fontsize=16)
                ax.set_ylabel('Frequency', fontsize=16)
                ax2.set_ylabel('Probability', fontsize=16)

                fig.savefig(f'Data/bulk/bulk_{elements}_{heap_size}_{pbc}.png')

                plt.close()

plot()