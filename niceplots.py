import numpy as np
import matplotlib
import matplotlib.pyplot as plt

file1 = open('trash/grid2.txt', 'r')
lines = file1.readlines()
def num_atom(n):
        if n == 0: return 100
        if n == 1: return 464
        if n == 2: return 2000

n_hops = range(8)
het_mod = np.linspace(-0.75,0.75,13)
het_mod = [str(round(het,2)) for het in het_mod]
pvals = np.zeros(shape=(3,len(n_hops),len(het_mod)),dtype=float)
count =0
for line in lines:
        ele, hop, mod, pval, size  = line.split(",")
        X = int(hop)
        Y = int(np.floor(count/8))
        count += 1
        if int(np.floor(count/8)) == 13:
                count =0
        if size.rstrip() == "100.0":
                pvals[0,X,Y] = float(pval)
        elif size.rstrip() == "464.15888336127773":
                pvals[1,X,Y] = float(pval)
        else:
                pvals[2,X,Y] = float(pval)



fig, ax = plt.subplots(1,3,figsize=(16, 6),sharey=True)


for i in range(3):
        im = ax[i].imshow(pvals[i,:,:])
        # Show all ticks and label them with the respective list entries
        ax[i].set_xticks(np.arange(len(het_mod)), labels=het_mod)
        ax[i].set_yticks(np.arange(len(n_hops)), labels=n_hops)
        ax[i].set_title(f"# of Atoms: {num_atom(i)}" )
# Rotate the tick labels and set their alignment.
        plt.setp(ax[i].get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
        ax[0].set_ylabel('# of hops')
        ax[i].set_xlabel('heterogeneous modifier')

cbar = fig.colorbar(im,ax=ax.ravel().tolist(), shrink=0.5)
cbar.ax.set_ylabel('P-values', rotation=-90, va="bottom")
#fig.tight_layout()
plt.savefig("Data/Size_4_elements.png")
plt.close()
