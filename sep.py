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
from scipy import special
from scipy.stats import gamma
import pickle
from ase.io.trajectory import Trajectory
import iteround, itertools
from sklearn.model_selection import ParameterGrid
import sys
from os import path

def chi2_square(observed_N, expected_N):
    return np.sum((observed_N - expected_N)**2 / expected_N)

def chi2_yates(observed_N, expected_N):
    return np.sum((observed_N - expected_N - 0.5)**2 / expected_N)
def pdf(x,shape,scale):
    return (1/(special.gamma(shape)*scale**shape))*x**(shape-1)*np.exp(-x/scale)

def test():
    
    
    bondsele = ['Ag','Au','Ir','Pd','Pt']
    bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(bondsele, 2))])
    
    all_edges = np.load(f'gooder/chi_5_500_edges.npy')
    symbols = np.load(f'gooder/chi_5_500_symbols.npy')
        
    n_bonds = np.zeros(len(symbols))
    for edges in all_edges:
            n_bonds[edges[0]] += 1 
        
    testsize = 2000
    chi2 = np.zeros((13,testsize))
    chi2_sqyates = np.zeros((13,testsize))
    n_expected = np.zeros(13)
    for edge in n_bonds:
      n_expected[int(edge)] += 1 
      
    expected = []
    for bond in bonds:
        sets = np.array([set(a) for a in list(itertools.product(bondsele, bondsele))])
        expected.append(sum(bond == sets) / len(sets))
    
    print(expected)
    print(n_expected)
    

    
    for i in range(testsize):
        np.random.shuffle(symbols)
        observed = np.zeros((13,len(bonds)))
        obs_all = np.zeros(len(bonds))
        obs_ind = np.zeros((len(symbols),len(bonds)))
        for edge in all_edges:
            ind = int(n_bonds[edge[0]])
            observed[ind,np.argwhere(set(symbols[edge]) == bonds)] += 1  
            obs_all[np.argwhere(set(symbols[edge]) == bonds)] += 1
            #obs_ind[edge[0],np.argwhere(set(symbols[edge]) == bonds)] += 1

            
        chi2[0,i] = chi2_square(obs_all,np.array(expected)*sum(obs_all))
        chi2_sqyates[0,i] = chi2_yates(obs_all,np.array(expected)*sum(obs_all))
        for j in range(5,13):
            chi2[j,i]=chi2_square(observed[j],np.array(expected)*n_expected[j]*j)
            chi2_sqyates[j,i]=chi2_yates(observed[j],np.array(expected)*n_expected[j]*j)
        
        
       
    
    
    k = []
    t = []
    for i in range(5,13):
        t.append(np.var(chi2[i,:])/np.mean(chi2[i,:]))
        k.append(np.mean(chi2[i,:])**2/np.var(chi2[i,:]))
        
    colors = ['b','g','r','c','m','y','k','pink']
    fig, ax = plt.subplots(3, 1, figsize=(16, 8))
   
    ax[0].hist(chi2[12,:],bins=np.arange(np.min(chi2[12,:]),np.max(chi2[12,:]),1), histtype='bar', color='steelblue', alpha=1)
    ax[0].hist(chi2[9,:],bins=np.arange(np.min(chi2[12,:]),np.max(chi2[12,:]),1), histtype='bar', color='orange', alpha=0.7)
    ax[1].hist(chi2[0,:],bins=np.arange(np.min(chi2[12,:]),np.max(chi2[12,:]),1), histtype='bar', color='orange', alpha=0.7)
    for i in range(5,13):
        ax[2].hist(chi2[i,:],bins=np.arange(np.min(chi2[12,:]),np.max(chi2[12,:]),1), histtype='bar', color=colors[i-5], alpha=0.7)
    fig.legend(['12','9'])
    plt.show()
    fig.savefig(f"250_test.png")
    plt.close()
    
    fig, ax = plt.subplots(3, 1, figsize=(16, 8))
   
    ax[0].hist(chi2_sqyates[12,:],bins=np.arange(np.min(chi2_sqyates[12,:]),np.max(chi2_sqyates[12,:]),1), histtype='bar', color='steelblue', alpha=1)
    ax[0].hist(chi2_sqyates[9,:],bins=np.arange(np.min(chi2_sqyates[12,:]),np.max(chi2_sqyates[12,:]),1), histtype='bar', color='orange', alpha=0.7)
    ax[1].hist(chi2_sqyates[0,:],bins=np.arange(np.min(chi2_sqyates[12,:]),np.max(chi2_sqyates[12,:]),1), histtype='bar', color='orange', alpha=0.7)
    for i in range(5,13):
        ax[2].hist(chi2_sqyates[i,:],bins=np.arange(np.min(chi2_sqyates[12,:]),np.max(chi2_sqyates[12,:]),1), histtype='bar', color=colors[i-5], alpha=0.7)
    fig.legend(['12','9'])
    plt.show()
    fig.savefig(f"250_yates.png")
    plt.close()
    
    x = np.linspace(0,np.max(chi2[12,:]),1000)
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    
    for i in range(5,13):
        Y = pdf(x, k[i-5],t[i-5])
        #ax.hist(chi2[i,:], bins=100, histtype='bar', color=colors[i-5], alpha=0.7)
        ax.plot(x,Y,color=colors[i-5])
    ax.plot(x,pdf(x,(np.var(chi2[0,:])/np.mean(chi2[0,:])),(np.mean(chi2[0,:])**2/np.var(chi2[0,:]))),color="darkred")
    
    for i in range(5,13):
        Y = pdf(x, (np.var(chi2_sqyates[0,:])/np.mean(chi2_sqyates[0,:])),(np.mean(chi2_sqyates[0,:])**2/np.var(chi2_sqyates[0,:])))
        #ax.hist(chi2[i,:], bins=100, histtype='bar', color=colors[i-5], alpha=0.7)
        ax.plot(x,Y,'--',color=colors[i-5])
    ax.plot(x,pdf(x,(np.var(chi2_sqyates[0,:])/np.mean(chi2_sqyates[0,:])),(np.mean(chi2_sqyates[0,:])**2/np.var(chi2_sqyates[0,:]))),'--',color="darkred")
    fig.legend(['5','6','7','8','9','10','11','12','all'])
    fig.savefig('gamma_dist.png')
    plt.show()
    
    
    
    
test()