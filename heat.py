import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import special
import sys
from sklearn.model_selection import ParameterGrid

def chi2(observed_N, expected_N):
    return np.sum((observed_N - expected_N) ** 2 / expected_N)

kwarg_grid = {'test': [sys.argv[1]],
              'elements': [sys.argv[2]],
              'n_hops': range(7),
              'het_mod': [-0.75,-0.5,-0.25,0,0.25,0.5,0.75],
              'heanp_size':[sys.argv[3]]}

def het(mod):
    x = int((mod+0.75)/0.25)
    return x

CDF_pvals = np.zeros(shape=(len(kwarg_grid['n_hops']),len(kwarg_grid['het_mod'])),dtype=float)
CDF_heat = np.zeros(shape=(len(kwarg_grid['n_hops']),len(kwarg_grid['het_mod'])),dtype=float)
pvals = np.zeros(shape=(len(kwarg_grid['n_hops']),len(kwarg_grid['het_mod'])),dtype=float)


test = "charge"
if int(kwarg_grid['test'][0]) == 0: test = "size"


for kwargs in ParameterGrid(kwarg_grid):

    pval_boot = np.load(f'{test}/{kwargs["elements"]}_{kwargs["heanp_size"]}_{kwargs["n_hops"]}_{kwargs["het_mod"]:.2f}.npy')
    testpvals = np.load(f"{test}/{test}pvals_{kwargs['elements']}_{kwargs['heanp_size']}.npy")
    noppvals = np.load(f'{test}/{kwargs["elements"]}_{kwargs["heanp_size"]}_0_{kwargs["het_mod"]:.2f}.npy')
    med = np.median(pval_boot)
    mean = np.mean(testpvals)
    var = np.var(testpvals)
    theta =  var/mean
    k = mean/theta
    CDF = special.gammainc(k,(med/theta))
    mean1 = np.mean(noppvals)
    var1 = np.var(noppvals)
    theta1 =  var1/mean1
    k1 = mean1/theta1
    CDF1 = special.gammainc(k1,(med/theta1))
    pvals[kwargs["n_hops"],het(kwargs["het_mod"])] = med
    CDF_pvals[kwargs["n_hops"],het(kwargs["het_mod"])] = CDF1
    CDF_heat[kwargs["n_hops"],het(kwargs["het_mod"])] = CDF


fig, ax = plt.subplots()
im = ax.imshow(pvals)
ax.set_xticks(np.arange(7), labels=kwarg_grid['het_mod'])
ax.set_yticks(np.arange(7), labels=kwarg_grid['n_hops'])
ax.set_title(f"Elements {kwarg_grid['elements'][0]} - Size {kwargs['heanp_size']}")
cbar = ax.figure.colorbar(im, ax=ax)
fig.tight_layout()
plt.savefig(f"Data/pval/pval_{test}_ele_{kwarg_grid['elements'][0]}_size_{kwargs['heanp_size']}.png")
plt.close()

fig, ax = plt.subplots()
im = ax.imshow(CDF_heat)
ax.set_xticks(np.arange(7), labels=kwarg_grid['het_mod'])
ax.set_yticks(np.arange(7), labels=kwarg_grid['n_hops'])
cbar = ax.figure.colorbar(im, ax=ax)
ax.set_title(f"Elements {kwarg_grid['elements'][0]} - Size {kwargs['heanp_size']}")
fig.tight_layout()
plt.savefig(f"Data/CDF/CDF_{test}_ele_{kwarg_grid['elements'][0]}_size_{kwargs['heanp_size']}.png")
plt.close()
fig, ax = plt.subplots()
im = ax.imshow(CDF_pvals)
ax.set_xticks(np.arange(7), labels=kwarg_grid['het_mod'])
ax.set_yticks(np.arange(7), labels=kwarg_grid['n_hops'])
cbar = ax.figure.colorbar(im, ax=ax)
ax.set_title(f"Elements {kwarg_grid['elements'][0]} - Size {kwargs['heanp_size']}")
fig.tight_layout()
plt.savefig(f"Data/pval/CDF_{test}_ele_{kwarg_grid['elements'][0]}_size_{kwargs['heanp_size']}.png")
plt.close()

