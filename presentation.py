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

def score(id,edges,rnd_symbol,symbols,bond_score,het_score,hom_score):
    score = 0
    edges = edges[:,:,1]
    for edge in edges:
        edge_symbol = symbols[edge[0]]
        if edge_symbol =='H': continue
        score += bond_score
        if rnd_symbol != edge_symbol:
            score += het_score
        elif rnd_symbol == edge_symbol:
            score += hom_score
    return score

def grid_particle(elements,n_atoms_added,n_hops,bond_score,het_score,hom_score):

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

def charge_grid_particle(elements,n_atoms_added,n_hops,bond_score,het_score,hom_score):

    surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
    layers = [11,11,11]
    lc = 3.8
    atoms = FaceCenteredCubic('H', surfaces, layers, latticeconstant=lc)

    # neighbor library, symbol list and possible bonds
    edge_lib = np.array(neighbor_list('ij',atoms,cutoff=lc*0.9)).transpose()
    symbol_lib = atoms.get_chemical_symbols()
    bonds = np.array([set(a) for a in list(itertools.combinations_with_replacement(elements, 2))])

    if len(elements) % 2 == 1: print("uneven element amount")

    # find ids of initial particle by distance from center
    pos = atoms.get_positions()
    center_coords = atoms.get_cell()[[0,1,2],[0,1,2]]/2

    center_id = np.argwhere(np.all(np.isclose(pos,center_coords),axis=1))[0][0]

    dist = atoms.get_distances(center_id,range(len(atoms)))

    ids_ranked = np.arange(len(atoms))[dist.argsort()]

    # establish starting graph
    #graph = edge_lib[np.all(np.isin(edge_lib[:],ids_ranked[:starting_size]),axis=1)]


    n_positive_elements = {e: n_atoms_added/len(elements) for e in elements[:int(len(elements)/2)]}
    n_negative_elements = {e: n_atoms_added/len(elements) for e in elements[int(len(elements)/2):]}
    n_positive_elements = iteround.saferound(n_positive_elements, 0)
    n_negative_elements = iteround.saferound(n_negative_elements, 0)

    # Shuffle list of surface element ids and set up 3D grid
    positive_element_list = list(itertools.chain.from_iterable([[metal_idx] * int(n) for metal_idx, n in n_positive_elements.items()]))
    negative_element_list = list(itertools.chain.from_iterable([[metal_idx] * int(n) for metal_idx, n in n_negative_elements.items()]))
    np.random.shuffle(negative_element_list)
    np.random.shuffle(positive_element_list)
    for id in ids_ranked:
        # choice of element added
        if symbol_lib[id] != 'H': continue
        symbol_lib[id] = positive_element_list.pop()
        edges = edge_lib[np.argwhere(edge_lib[:,0] == id)]
        edge_id = np.random.choice(edges[:,0,1])
        symbol_lib[edge_id] = negative_element_list.pop()

        if not bool(positive_element_list): break
    

    for hop in range(n_hops):
        for id in ids_ranked:
            rnd_symbol = symbol_lib[id]
            if symbol_lib[id] != 'H':
                edges = edge_lib[np.argwhere(edge_lib[:,0] == id)]
                candidates, cand_score= [], []
                candidates.append(id)
                cand_score.append(score(id,edges,rnd_symbol,symbol_lib, bond_score, het_score, hom_score))


                avail_hops = edges[:,:,1].T[0]
                    #print(f"avail_hops: {avail_hops}")
                if avail_hops.any():
                    for hops in avail_hops:
                        edges_hop = edge_lib[np.argwhere(edge_lib[:,0] == hops)]
                        candidates.append(hops)
                        cand_score.append(score(hops, edges_hop, symbol_lib[hops], symbol_lib, bond_score, het_score, hom_score))
                else:
                    continue

                best_cand = candidates[np.argmax(cand_score)]

                if id == best_cand: continue
                # update symbol library
                symbol_lib[id] = symbol_lib[best_cand]
                symbol_lib[best_cand] = rnd_symbol

    # set symbols for the atoms object and delete ghost atoms
    atoms.set_chemical_symbols(symbol_lib)

    del atoms[[atom.index for atom in atoms if atom.symbol=='H']]

    return atoms

kwarg_grid = {'elements': [sys.argv[1:]],#[elements[:i+2] for i in range(4)],
              'n_hops': range(7),
              'het_mod': [-0.75],
              'heanp_size':[400]}


for kwargs in ParameterGrid(kwarg_grid):

        atoms = grid_particle(kwargs['elements'],kwargs['heanp_size'],kwargs['n_hops'],1.0,kwargs['het_mod'],0.0)
        view(atoms)
        #charge_atoms = charge_grid_particle(kwargs['elements'],kwargs['heanp_size'],kwargs['n_hops'],1.0,kwargs['het_mod'],0.0)
        #view(charge_atoms)
       
        