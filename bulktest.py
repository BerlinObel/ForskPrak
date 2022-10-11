# ----------IMPORT----------
import numpy as np
from ase.build import bulk, stack
from ase.visualize import view
from ase.neighborlist import neighbor_list
from ase.geometry import analysis
import iteround, itertools
import sys
from scipy import special
import matplotlib.pyplot as plt
from collections import Counter

def score(id,edges,rnd_symbol,symbols,bond_score,het_score,hom_score):
    score = 0
    for edge in edges[np.isin(edges[:,1],id)]:
        score += bond_score
        if rnd_symbol != symbols[edge[0]]:
            score += het_score
        elif rnd_symbol == symbols[edge[0]]:
            score += hom_score
    return score

def build_bulk(elements):
    layers = (7, 6, 6)
    lc = 3.8
    atoms = bulk('Au', 'fcc', lc)*(7, 6, 6)


    # neighbor library, symbol list and possible bonds
    edge_lib = np.array(neighbor_list('ij',atoms,cutoff=lc*0.9)).transpose()
    symbol_lib = atoms.get_chemical_symbols()



    # find ids of initial particle by distance from center
    pos = atoms.get_positions()
    center_coords = atoms.get_cell()[[0,1,2],[0,1,2]]/2

    center_id = np.argwhere(np.all(np.isclose(pos,center_coords),axis=1))[0][0]

    dist = atoms.get_distances(center_id,range(len(atoms)),mic=True)

    ids_ranked = np.arange(len(atoms))[dist.argsort()]

    n_each_element = {e: 252/len(elements) for e in elements}
    n_each_element = iteround.saferound(n_each_element, 0)

    # Shuffle list of surface element ids and set up 3D grid
    element_list = list(itertools.chain.from_iterable([[metal_idx] * int(n) for metal_idx, n in n_each_element.items()]))

    np.random.shuffle(element_list)

    for id in ids_ranked:
        # choice of element added
        symbol_lib[id] = element_list.pop()

        # all edges involving particle ids
        
    # set symbols for the atoms object and delete ghost atoms
    atoms.set_chemical_symbols(symbol_lib)

    return atoms

def chi2(observed_N, expected_N):
    return np.sum((observed_N - expected_N) ** 2 / expected_N)

def pdf(x,shape,scale):
    return (1/(special.gamma(shape)*scale**shape))*x**(shape-1)*np.exp(-x/scale)

def bulk_test(elements):
    pval_bulk = []

    bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(elements, 2))])
    atoms = build_bulk(elements)


    ana_object = analysis.Analysis(atoms, bothways=False)
    all_edges = np.c_[np.array(list(ana_object.adjacency_matrix[0].keys()), dtype=np.dtype('int,int'))['f0'],
                    np.array(list(ana_object.adjacency_matrix[0].keys()), dtype=np.dtype('int,int'))['f1']]

    #remove self-to-self edges
    all_edges = all_edges[all_edges[:, 0] != all_edges[:, 1]]

    #get symbol libary
    symbols = np.array(atoms.get_chemical_symbols())


    for i in range(1000):
        np.random.shuffle(symbols)
        observed = np.zeros(len(bonds))
        for edge in all_edges:
            observed[np.argwhere(set(symbols[edge]) == bonds)[0][0]] += 1

        expected = []
        for bond in bonds:
            sets = np.array([set(a) for a in list(itertools.product(elements, elements))])
            expected.append(sum(bond == sets) / len(sets) * sum(observed))

        pval = chi2(observed, expected)

        pval_bulk.append(pval)

    mean = np.mean(pval_bulk)
    var = np.var(pval_bulk)

    theta = var/mean
    k = mean/theta
    X = np.linspace(0,50,1000)
    Y = pdf(X,k,theta)

    k2 = mean/2
    Y2 = pdf(X,k2,2)
    Y3 = pdf(X,7,2)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.hist(pval_bulk, bins=np.arange(0,50,0.25), histtype='bar', color='steelblue', alpha=0.7)
    ax.hist(pval_bulk, bins=np.arange(0,50,0.25), histtype='step', color='steelblue')
    ax2 = ax.twinx()
    ax2.plot(X,Y,color='seagreen')
    ax2.plot(X,Y2,'--',color='orange')
    ax2.plot(X,Y3,'-.',color='red')
    ax.set(ylim=(0, ax.get_ylim()[1] * 1.2))
    ax2.set(ylim=(0, ax2.get_ylim()[1] * 1.2))
    ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(elements)}'+ f"\nNP size: {252}"+f'\nShape:{k}\n'+f'Scale:{theta}'+f'\nShape: {k2}'  , family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
       
    ax.set_xlabel(r"$\chi^2$", fontsize=16)
    ax.set_ylabel('Frequency', fontsize=16)
    ax2.set_ylabel('Probability', fontsize=16)

    fig.savefig(f'pvals/bulk_{len(elements)}_{252}.png')

    np.savetxt(f"bulk_{len(elements)}_{252}",pval_bulk)

    plt.close()


bulk_test(sys.argv[1:])