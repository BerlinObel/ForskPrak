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

def cdf(x,shape,scale):
    return special.gammainc(shape,(x/scale))

def plot():
    ele =['ag','pd','pt','au','rh']
    sizes = [250,500,1000,2000]
    bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[2:], 2))])
    elements = 3
    pvals = []
    for size in sizes:
        heap_size = size
        
        pval_bootstrap = np.loadtxt(f"{elements}_{heap_size}.txt")
        pvals.append(pval_bootstrap)

    Y =[]
    sf = []

    X = np.linspace(0,20,1000)
    #X = np.linspace(0,np.max(pvals[1]),1000)
    for i in range(len(sizes)):
        mean = np.mean(pvals[i])
        var = np.var(pvals[i])
        theta =  var/mean
        k = mean/theta
        Y.append(pdf(X,k,theta))
        sf.append(1-cdf(X,k,theta))
        print(f'{i}_shape: {k} and scale: {theta}')
        print(f' adjusted shape: {mean/2}')
    bondb = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[3:], 2))])
    Yb = pdf(X,len(bondb)/2,2)
    sfb = (1-cdf(X,len(bondb)/2,2))
    b95 = np.where(sfb <= 0.05)
    #k2 = mean/2
    #Y2 = pdf(X,k2,2)
    Yd = stats.chi2.pdf(X, len(bonds)-1)
    sfd = stats.chi2.sf(X,len(bonds)-1)
    p95 = np.where(sf[2]<= 0.05)
    c95 = np.where(sfd <= 0.05)
    print(X[p95[0][0]])
    print(X[c95[0][0]])
    print(X[b95[0][0]])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.plot(X,Y[0],'-.',color='seagreen')
    ax.plot(X,Y[1],'--',color='orange')
    ax.plot(X,Y[2],'-.',color='red')
    ax.plot(X,Y[3],'b')
    ax.plot(X,Yd,'darkviolet')
    ax.plot(X,Yb,'lightseagreen')
    #ax.hist(pval_bootstrap, bins=np.arange(0,50,0.25), histtype='bar', color='steelblue', alpha=0.7)
    #ax.hist(pval_bootstrap, bins=np.arange(0,50,0.25), histtype='step', color='steelblue')
    #ax2 = ax.twinx()
    #ax2.plot(X,Y,color='seagreen')
    #ax2.plot(X,Y2,'--',color='orange')
    #ax2.plot(X,Y3,'-.',color='red')
    ax.vlines(X[p95[0][0]],0, ax.get_ylim()[1], color='c')
    ax.vlines(X[c95[0][0]],0, ax.get_ylim()[1], color='m')
    ax.vlines(X[b95[0][0]],0, ax.get_ylim()[1], color='gold')
    #ax.vlines(np.percentile(pval_bootstrap,99),0, ax.get_ylim()[1], color='seagreen')
    ax.set(ylim=(0, ax.get_ylim()[1] * 1.2))
    #ax2.set(ylim=(0, ax2.get_ylim()[1] * 1.2))
    #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+'\n'+r'N$_{hops}$: '+f'{kwargs["n_hops"]}'+f'\nBond modifier: {kwargs["het_mod"]:.2f}' +\
    #f'\nMedian p-value = {np.median(pval_bootstrap):.2f} '+f'\nAdded atoms: ' + f'{kwargs["heanp_size"]}', family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
    #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{elements}'+ f"\nNP size: {heap_size}"+f'\nShape:{k}\n'+f'Scale:{theta}'+f'\nShape: {k2}'  , family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
    ax.legend([f'250 Atoms',f'500 Atoms',f'1000 Atoms', '2000 Atoms', r'$\chi^2$ Dist','Periodic Bulk Dist', '95% 1000 atoms', r'95% $\chi^2$ Dist', '95% periodic bulk'])
    #'\nMedian p-value = {np.median(pval_bootstrap):.2f}'+f"\n95%: {np.percentile(pval_bootstrap,95,method='inverted_cdf')}"+f"\n99%: {np.percentile(pval_bootstrap,99,method='inverted_cdf')}"
    ax.set_xlabel(r"$\chi^2$", fontsize=16)
    #ax.set_ylabel('Frequency', fontsize=16)
    ax.set_ylabel('Probability', fontsize=16)
    plt.title('3 Element cluster PDF')
    fig.savefig(f'Data/cluster/cluster_{elements}_pdf.png')

    plt.close()

plot()