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
    pbc = True
    heap_size = 1560
    pvalsT = []
    pvalsF = []
    for i in sizes:
        bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[1:], 2))])
        elements = 4
        pval_bootstrap = np.loadtxt(f"bulk_{elements}_{i}_{pbc}.txt")
        pvalsT.append(pval_bootstrap)
        try:
            pval_bootstrap = np.loadtxt(f"bulk_{elements}_{i}_{False}.txt")
        except OSError as Error:
            print(Error)
            continue
        pvalsF.append(pval_bootstrap)

    X = np.linspace(0.01,25,1000)
    Yt = []
    Yf = []
    for i in range(3):
        mean = np.mean(pvalsT[i])
        var = np.var(pvalsT[i])
        theta =  var/mean
        k = mean/theta
        Yt.append(pdf(X,k,theta))
        if i == 2: continue
        mean = np.mean(pvalsF[i])
        var = np.var(pvalsF[i])
        theta =  var/mean
        k = mean/theta
        Yf.append(pdf(X,k,theta))
        #k2 = mean/2
        #Y2 = pdf(X,k2,2)
    #Y3 = stats.chi2.pdf(X, len(bonds)-1)

    fig, ax2 = plt.subplots(1, 1, figsize=(8, 8))
    ax = ax2.twinx()
    
    ax2.hist(pvalsT[0], bins=np.arange(0,25,0.25), histtype='bar', color='steelblue', alpha=0.7)
    ax2.hist(pvalsT[1], bins=np.arange(0,25,0.25), histtype='bar', color='steelblue', alpha=0.7)
    ax2.hist(pvalsT[2], bins=np.arange(0,25,0.25), histtype='bar', color='steelblue', alpha=0.7)
    #ax2.hist(pvalsF[1], bins=np.arange(0,25,0.25), histtype='bar', color='orange',alpha=0.5)
    #ax2.hist(pvalsF[0], bins=np.arange(0,25,0.25), histtype='bar', color='orange',alpha=0.5)
    #ax.plot(X,Yf[2],color='navy')
    #ax.plot(X,Yf[0],color='seagreen')
    ax.plot(X,Yt[0],'--',color='green')
    #ax.plot(X,Yf[1],color='firebrick')
    ax.plot(X,Yt[1],'--',color='red')
    ax.plot(X,Yt[2],'--',color='blue')
    ax.plot(X,stats.chi2.pdf(X, 9),color='blueviolet')
    #ax.vlines(np.median(pval_bootstrap), 0, ax.get_ylim()[1], color='firebrick')
    #ax.vlines(np.percentile(pval_bootstrap,95),0, ax.get_ylim()[1], color='darkviolet')
    #ax.vlines(np.percentile(pval_bootstrap,99),0, ax.get_ylim()[1], color='seagreen')
    ax.set(ylim=(0, ax.get_ylim()[1] * 1.2))
    ax2.set(ylim=(0, ax2.get_ylim()[1] * 1.2))
    #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+'\n'+r'N$_{hops}$: '+f'{kwargs["n_hops"]}'+f'\nBond modifier: {kwargs["het_mod"]:.2f}' +\
    #f'\nMedian p-value = {np.median(pval_bootstrap):.2f} '+f'\nAdded atoms: ' + f'{kwargs["heanp_size"]}', family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
    #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{elements}'+ f"\nNP size: {heap_size}"+f'\nPeriodicity:{pbc}\n'+f'Scale:{theta}'  , family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
    ax.legend([f'640 Atoms not Periodic',f'640 Atoms Periodic','1560 Atoms not Periodic',f'1560 Atoms Periodic',f'2160 Atoms Periodic',r'4 element $\chi^2$'])
    ax.legend([f'640 Atoms Periodic',f'1560 Atoms Periodic',f'2160 Atoms Periodic',r'4 element $\chi^2$'])
    #'\nMedian p-value = {np.median(pval_bootstrap):.2f}'+f"\n95%: {np.percentile(pval_bootstrap,95,method='inverted_cdf')}"+f"\n99%: {np.percentile(pval_bootstrap,99,method='inverted_cdf')}"
    ax2.set_xlabel(r"$\chi^2$", fontsize=16)
    ax2.set_ylabel('Frequency', fontsize=16)
    ax.set_ylabel('Probability', fontsize=16)

    fig.savefig(f'Data/bulk/bulk_4_comparision_true.png')

    plt.close()

plot()