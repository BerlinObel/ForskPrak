import numpy as np
import matplotlib
import matplotlib.pyplot as plt

file1 = open('gridstruc.txt', 'r')
lines = file1.readlines()

n_hops = range(8)
het_mod = np.linspace(-0.75,0.75,13)
bonds = np.linspace(0,1,5)
het_mod = [str(round(het,2)) for het in het_mod]
pvals = np.zeros(shape=(len(bonds),len(n_hops),len(het_mod)),dtype=float)
Z =0
X = -1
old_bond = 0.0
for line in lines:
        ele, hop, mod, pval, bond_sc  = line.split(",")
        Y = int(hop)
        if float(bond_sc) > old_bond:
                old_bond = float(bond_sc)
                Z += 1
                X = -1
        if Y == 0:
                X += 1
        pvals[Z,Y,X]=float(pval)
        
        
        
        



fig, ax = plt.subplots(3,2)
ax[0,0].imshow(pvals[0,:,:])
ax[0,1].imshow(pvals[1,:,:])
ax[1,0].imshow(pvals[2,:,:])
ax[1,1].imshow(pvals[3,:,:])
ax[2,1].imshow(pvals[4,:,:])
ax[0,0].set_title(f"Bond Score: {bonds[0]}")
ax[0,1].set_title(f"Bond Score: {bonds[1]}")
ax[1,0].set_title(f"Bond Score: {bonds[2]}")
ax[1,1].set_title(f"Bond Score: {bonds[3]}")
ax[2,1].set_title(f"Bond Score: {bonds[4]}")


# Show all ticks and label them with the respective list entries
#ax[0,0].set_xticks(np.arange(len(het_mod)), labels=het_mod)
#ax[0,0].set_yticks(np.arange(len(n_hops)), labels=n_hops)

# Rotate the tick labels and set their alignment.
#plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
 #        rotation_mode="anchor")

# Loop over data dimensions and create text annotations.

fig.tight_layout()
plt.savefig("Structure.png")
plt.show()
plt.close()

# Loop over data dimensions and create text annotations.

