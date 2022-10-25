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
from os import path

def score(id,edges,rnd_symbol,symbols,bond_score,het_score,hom_score):
    score = 0
    for edge in edges[np.isin(edges[:,1],id)]:
        score += bond_score
        if rnd_symbol != symbols[edge[0]]:
            score += het_score
        elif rnd_symbol == symbols[edge[0]]:
            score += hom_score
    return score

def grid_particle(elements,starting_size,n_atoms_added,n_hops,bond_score,het_score,hom_score,rnd_seed):

    # set random seed
    np.random.seed(rnd_seed)

    # make ghost particle
    surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
    layers = [18,18,18]
    lc = 3.8
    atoms = FaceCenteredCubic('H', surfaces, layers, latticeconstant=lc)

    # neighbor library, symbol list and possible bonds
    edge_lib = np.array(neighbor_list('ij',atoms,cutoff=lc*0.9)).transpose()
    symbol_lib = atoms.get_chemical_symbols()
    bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(elements, 2))])

    # find ids of initial particle by distance from center
    pos = atoms.get_positions()
    center_coords = atoms.get_cell()[[0,1,2],[0,1,2]]/2

    center_id = np.argwhere(np.all(np.isclose(pos,center_coords),axis=1))[0][0]

    dist = atoms.get_distances(center_id,range(len(atoms)))

    ids_ranked = np.arange(len(atoms))[dist.argsort()]

    # establish starting graph
    #graph = edge_lib[np.all(np.isin(edge_lib[:],ids_ranked[:starting_size]),axis=1)]

    n_each_element = {e: n_atoms_added/len(elements) for e in elements}
    n_each_element = iteround.saferound(n_each_element, 0)

    # Shuffle list of surface element ids and set up 3D grid
    element_list = list(itertools.chain.from_iterable([[metal_idx] * int(n) for metal_idx, n in n_each_element.items()]))
    np.random.shuffle(element_list)
    for id in ids_ranked:
        # choice of element added
        symbol_lib[id] = element_list.pop()
        if not bool(element_list): break
    # set symbols for the atoms object and delete ghost atoms
    atoms.set_chemical_symbols(symbol_lib)

    del atoms[[atom.index for atom in atoms if atom.symbol=='H']]

    return atoms

def chi2_uncert(observed_frac,expected_frac,uncertainties):
        chi2 = np.sum((observed_frac-expected_frac)**2/uncertainties**2)
        Ndof = len(observed_frac) -1
        prob_chi2 = stats.chi2.sf(chi2, Ndof)
        return chi2, Ndof, prob_chi2

def pearsons_chi2(observed_N, expected_N):
    chi2 = np.sum((observed_N - expected_N) ** 2 / expected_N**2)
    Ndof = len(observed_N) - 1
    prob_chi2 = stats.chi2.sf(chi2, Ndof)
    return chi2, Ndof, prob_chi2

def chi2_square(observed_N, expected_N):
    return np.sum((observed_N - expected_N) ** 2 / expected_N)

def chi2(observed_N, expected_N):
    expected_N *= sum(observed_N)
    a = (observed_N - expected_N)
    b = np.sqrt(expected_N)
    c = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    chi = np.sum(c)
    return chi

def chi22(observed_N, expected_N, oa):
    expected_N *= (12*oa)
    a = (observed_N - expected_N)
    b = np.sqrt(expected_N)
    c = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    chi = np.sum(c)
    return chi 

def pdf(x,shape,scale):
    return (1/(special.gamma(shape)*scale**shape))*x**(shape-1)*np.exp(-x/scale)


N_particles = 500
kwarg_grid = {'elements': [sys.argv[1:]],#[elements[:i+2] for i in range(4)],
              'n_hops': range(1),
              'het_mod': [0],
              'heanp_size':[250,500,1000,2000]}


for kwargs in ParameterGrid(kwarg_grid):


        bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(kwargs['elements'], 2))])
        pval_bootstrap = []

        bulk_chi = []
        outer_chi = []
        alt_outer = []
        bulkouter = []
        if not path.isfile(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_edges.npy'):
            atoms = grid_particle(kwargs['elements'],5,kwargs['heanp_size'],0,1.0,0,0.0,1)
            view(atoms)
            #traj = Trajectory(f'traj/{len(kwargs["elements"])}_{kwargs["n_hops"]}_{kwargs["het_mod"]:.2f}_{str(i).zfill(4)}.traj',atoms=None, mode='w')
            #traj.write(atoms)
            ana_object = analysis.Analysis(atoms, bothways=True)
            all_edges = np.c_[np.array(list(ana_object.adjacency_matrix[0].keys()), dtype=np.dtype('int,int'))['f0'],
                                np.array(list(ana_object.adjacency_matrix[0].keys()), dtype=np.dtype('int,int'))['f1']]

            #remove self-to-self edges
            all_edges = all_edges[all_edges[:, 0] != all_edges[:, 1]]
            np.save(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_edges',all_edges)
            symbols = np.array(atoms.get_chemical_symbols())
            np.save(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_symbols',symbols)
        else:
            all_edges = np.load(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_edges.npy')
            symbols = np.load(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_symbols.npy')
        
        n_bonds = np.zeros(len(symbols))
        for edges in all_edges:
            n_bonds[edges[0]] += 1 
        

        expected = []
        for bond in bonds:
            sets = np.array([set(a) for a in list(itertools.product(kwargs['elements'], kwargs['elements']))])
            expected.append(sum(bond == sets) / len(sets))
        
    
        """
        for i in range(100):
            np.random.shuffle(symbols)
            observed = np.zeros((len(symbols),len(bonds)))
            for edge in all_edges:
                observed[edge[0],np.argwhere(set(symbols[edge]) == bonds)[0][0]] += 1  

            #_, _, pval = pearsons_chi2(observed, expected)
            pval = chi2_square(observed, expected)
            pval_bootstrap.append(pval)
        """
        for i in range(50000):
            np.random.shuffle(symbols)
            outer_atoms = 0
            oa_list = []
            observed = np.zeros((2,len(bonds)))
            for edge in all_edges:
                if int(n_bonds[edge[0]]) == 12:
                    observed[0,np.argwhere(set(symbols[edge]) == bonds)[0][0]] += 1  
                else: 
                    observed[1,np.argwhere(set(symbols[edge]) == bonds)[0][0]] += 1  
                    outer_atoms += 1

            """
            print(np.average(observed[0,:]/observed[1,:]))
            print(sum(observed[0,:])/sum(observed[1,:]))

            r = np.cbrt((3/(4*np.pi))*kwargs['heanp_size'])
            A = 4*np.pi*(r**2)
            print(kwargs['heanp_size']/A)
            """

            both = np.zeros(len(bonds))
            both += observed[0]+observed[1]
            #print(both)

            bulk_chi.append(chi2(observed[0],np.array(expected)))
            outer_chi.append(chi2(observed[1],np.array(expected)))
            alt_outer.append(chi22(observed[1],np.array(expected),outer_atoms))
            bulkouter.append(chi2(both,np.array(expected)))
            
        
        mean_bulk = np.mean(bulk_chi)
        mean_outer = np.mean(outer_chi)
        mean_comb = np.mean(bulkouter)
        var_bulk = np.var(bulk_chi)
        var_outer = np.var(outer_chi)
        var_comb = np.var(bulkouter)
        var_alt = np.var(alt_outer)
        """
        t_b =  var_bulk/mean_bulk
        t_o =  var_outer/mean_outer
        t_c = var_comb/mean_comb
        k_b = mean_bulk/t_b
        k_o = mean_outer/t_o
        k_c = mean_comb/t_c
        X = np.linspace(-3.5,3.5,1000)
        Y_b = pdf(X,k_b,t_b)
        Y_o = pdf(X,k_o,t_o)
        Y_c = pdf(X,k_c,t_c)
        """
        sigma_b = np.sqrt(var_bulk)
        sigma_o = np.sqrt(var_outer)
        sigma_c = np.sqrt(var_comb)
        sigma_alt = np.sqrt(var_alt)
        mean_alt = np.mean(alt_outer)
        


        X = np.linspace(-3.5,3.5,1000)
        Y_b = stats.norm.pdf(X,mean_bulk,sigma_b)
        Y_o = stats.norm.pdf(X,mean_outer,sigma_o)
        Y_c = stats.norm.pdf(X,mean_comb,sigma_c)
        Y_alt = stats.norm.pdf(X,0,sigma_alt)




        fig, ax = plt.subplots(1, 3, figsize=(16, 8))
        ax[0].hist(bulk_chi, bins=100, histtype='bar', color='steelblue', alpha=1)
        ax[0].hist(bulkouter, bins=100, histtype='bar', color='orange', alpha=0.7)
        ax[1].hist(bulk_chi, bins=100, histtype='bar', color='steelblue', alpha=1)
        ax[1].hist(outer_chi, bins=100, histtype='bar', color='orange', alpha=0.7)
        #ax[2].hist(bulk_chi, bins=100, histtype='bar', color='steelblue', alpha=0.7)
        
        ax[2].plot(X,Y_b,color='seagreen')
        ax[2].plot(X,Y_o,'--',color='orange')
        ax[2].plot(X,Y_c,'-.',color='red')
        ax[2].plot(X,Y_alt,'-.',color='cyan')
        #ax.vlines(np.median(pval_bootstrap), 0, ax.get_ylim()[1], color='firebrick')
        #ax.vlines(np.percentile(pval_bootstrap,95),0, ax.get_ylim()[1], color='darkviolet')
        #ax.vlines(np.percentile(pval_bootstrap,99),0, ax.get_ylim()[1], color='seagreen')
        ax[0].set(ylim=(0, ax[0].get_ylim()[1] * 1.2))
        ax[1].set(ylim=(0, ax[1].get_ylim()[1] * 1.2))
        ax[2].set(ylim=(0, ax[2].get_ylim()[1] * 1.2))
        
        ax[2].text(0.02, 0.98,f'Mean, Var \n  Bulk: {mean_bulk:.2f}, {var_bulk:.2f}\n  Outer: {mean_outer:.2f}, {var_outer:.2f}\n  comb: {mean_comb:.2f}, {var_comb:.2f}\n  alt: {mean_alt:.2f}, {var_alt:.2f}', family='monospace', fontsize=13, transform=ax[2].transAxes,verticalalignment='top')
        
        #ax2.set(ylim=(0, ax2.get_ylim()[1] * 1.2))
        #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+'\n'+r'N$_{hops}$: '+f'{kwargs["n_hops"]}'+f'\nBond modifier: {kwargs["het_mod"]:.2f}' +\
        #f'\nMedian p-value = {np.median(pval_bootstrap):.2f} '+f'\nAdded atoms: ' + f'{kwargs["heanp_size"]}', family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
        #ax[0].text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+ f"\nNP size: {kwargs['heanp_size']}"+f'\nShape:{k}\n'+f'Scale:{theta}'+f'\nShape: {k2}'  , family='monospace', fontsize=13, transform=ax[0].transAxes,verticalalignment='top')
       
        #'\nMedian p-value = {np.median(pval_bootstrap):.2f}'+f"\n95%: {np.percentile(pval_bootstrap,95,method='inverted_cdf')}"+f"\n99%: {np.percentile(pval_bootstrap,99,method='inverted_cdf')}"
        ax[0].set_xlabel(r"$\chi$" + " combined", fontsize=16)
        ax[1].set_xlabel(r"$\chi$" + " outer", fontsize=16)
        ax[2].set_xlabel(r"$\chi$" + " Normal dist", fontsize=16)
        ax[0].set_ylabel('Frequency', fontsize=16)
        ax[0].legend(['Bulk_chi','combined'], loc='right')
        ax[1].legend(['Bulk_chi','outer'], loc='right')
        ax[2].legend(['Bulk','Outer','Combined','Alt'], loc='right')
        #ax2.set_ylabel('Probability', fontsize=16)
        #fig.savefig(f'pvals/{len(kwargs["elements"])}_{kwargs["n_hops"]}_{kwargs["het_mod"]:.2f}_{kwargs["heanp_size"]}.png')
        #fig.savefig(f'pvals/{len(kwargs["elements"])}_{kwargs["heanp_size"]}.png')
        fig.savefig(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_s')
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_bulk',bulk_chi)
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_outer',outer_chi)
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_alt',alt_outer)
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_both',bulkouter)




        #with open('grid.txt','a') as file:
            #file.write(f'{len(kwargs["elements"])},{kwargs["n_hops"]},{kwargs["het_mod"]:.2f},{np.median(pval_bootstrap):.2f},{kwargs["heanp_size"]}\n')
         #   file.write(f'{len(kwargs["elements"])}:.2f}\n')

        plt.close()





        """
        for i in range(N_particles):

            atoms = grid_particle(kwargs['elements'],13,kwargs["heanp_size"],kwargs['n_hops'],1.0,kwargs['het_mod'],0.0,i)
            #traj = Trajectory(f'traj/{len(kwargs["elements"])}_{kwargs["n_hops"]}_{kwargs["het_mod"]:.2f}_{str(i).zfill(4)}.traj',atoms=None, mode='w')
            #traj.write(atoms)
            ana_object = analysis.Analysis(atoms, bothways=False)
            all_edges = np.c_[np.array(list(ana_object.adjacency_matrix[0].keys()), dtype=np.dtype('int,int'))['f0'],
                              np.array(list(ana_object.adjacency_matrix[0].keys()), dtype=np.dtype('int,int'))['f1']]

            #remove self-to-self edges
            all_edges = all_edges[all_edges[:, 0] != all_edges[:, 1]]

            symbols = np.array(atoms.get_chemical_symbols())
            print(symbols)
            observed = np.zeros(len(bonds))
            for edge in all_edges:
                observed[np.argwhere(set(symbols[edge]) == bonds)[0][0]] += 1

            expected = []
            for bond in bonds:
                sets = np.array([set(a) for a in list(itertools.product(kwargs['elements'], kwargs['elements']))])
                expected.append(sum(bond == sets) / len(sets) * sum(observed))

            _, _, pval = pearsons_chi2(observed, expected)
            pval_bootstrap.append(pval)

        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        ax.hist(pval_bootstrap, bins=25, range=(0, 1), histtype='bar', color='steelblue', alpha=0.7)
        ax.hist(pval_bootstrap, bins=25, range=(0, 1), histtype='step', color='steelblue')
        ax.vlines(np.median(pval_bootstrap), 0, ax.get_ylim()[1], color='firebrick')
        ax.set(ylim=(0, ax.get_ylim()[1] * 1.2))
        ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+'\n'+r'N$_{hops}$: '+f'{kwargs["n_hops"]}'+f'\nBond modifier: {kwargs["het_mod"]:.2f}' +\
        f'\nMedian p-value = {np.median(pval_bootstrap):.2f} '+f'\nAdded atoms: ' + f'{kwargs["heanp_size"]}', family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
        ax.set_xlabel(r"Pearson's $\chi^2$ p-value", fontsize=16)
        ax.set_ylabel('Frequency', fontsize=16)
        fig.savefig(f'pvals/{len(kwargs["elements"])}_{kwargs["n_hops"]}_{kwargs["het_mod"]:.2f}_{kwargs["heanp_size"]}.png')
        with open('grid.txt','a') as file:
            file.write(f'{len(kwargs["elements"])},{kwargs["n_hops"]},{kwargs["het_mod"]:.2f},{np.median(pval_bootstrap):.2f},{kwargs["heanp_size"]}\n')
        plt.close()

        """
        """
        rand_frac = []
        for bond in bonds:
            sets = np.array([set(a) for a in list(itertools.product(elements,elements))])
            rand_frac.append(sum(bond == sets) / len(sets))

        mean_n_bonds = np.mean(np.sum(bond_count,axis=1))

        means = np.mean(bond_count/mean_n_bonds,axis=0)
        stds = np.std(bond_count/mean_n_bonds,axis=0)

        chi2, Ndof, pval = chi2_uncert(means,rand_frac,stds)
        master_array[j,k] = pval
        print(f'Reward: {reward}   Hops: {n_hops}   pval: {pval}')
        """
"""
# save array
with open(f'{len(elements)}e.array', 'wb') as output:
    pickle.dump(master_array, output)

# load array
with open(f'{len(elements)}e.array', 'rb') as input:
    master_array = pickle.load(input)
"""
