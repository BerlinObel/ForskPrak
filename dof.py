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
        ele =['ag','pd','pt','au','rh','Ir']
        bonds5 = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele, 2))])
        bonds4 = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[1:], 2))])
        bonds3 = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[2:], 2))])
        bonds2 = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[3:], 2))])
        bonds1 = np.array([set(a) for a in list(itertools.combinations_with_replacement(ele[4:], 2))])

        print(len(bonds5))
        print(len(bonds4))
        print(len(bonds3))
        print(len(bonds2))
        print(len(bonds1))

plot()