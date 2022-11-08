import numpy as np
import matplotlib
import matplotlib.pyplot as plt

file1 = open('gridcharge.txt', 'r')
lines = file1.readlines()

n_hops = range(8)
het_mod = np.linspace(-0.5,0.5,9)
charges = np.linspace(0,1,5)
het_mod = [str(round(het,2)) for het in het_mod]
pvals = np.zeros(shape=(len(charges),len(n_hops),len(het_mod)),dtype=float)
pvals_ch2 = np.zeros(shape=(len(charges),len(n_hops),len(het_mod)),dtype=float)
pvals_ch3 = np.zeros(shape=(len(charges),len(n_hops),len(het_mod)),dtype=float)
Z =0
X = -1
old_ch = 0.0
for line in lines:
        ele, hop, mod, pval, charge_sc, charge_n, ch_pval  = line.split(",")
        Y = int(hop)
        if float(charge_sc) > old_ch:
                old_ch = float(charge_sc)
                Z += 1
                X = -1
        if Y == 0:
                X += 1
        pvals[Z,Y,X]=float(pval)
        if int(charge_n) == 2:
                pvals_ch2[Z,Y,X]=float(ch_pval)
        else:
                pvals_ch3[Z,Y,X]=float(ch_pval)
        


fig, ax = plt.subplots(3,5)
ax[0,0].imshow(pvals[0,:,:])
ax[1,0].imshow(pvals_ch2[0,:,:])
ax[2,0].imshow(pvals_ch3[0,:,:])
ax[0,1].imshow(pvals[1,:,:])
ax[1,1].imshow(pvals_ch2[1,:,:])
ax[2,1].imshow(pvals_ch3[1,:,:])
ax[0,2].imshow(pvals[2,:,:])
ax[1,2].imshow(pvals_ch2[2,:,:])
ax[2,2].imshow(pvals_ch3[2,:,:])
ax[0,3].imshow(pvals[3,:,:])
ax[1,3].imshow(pvals_ch2[3,:,:])
ax[2,3].imshow(pvals_ch3[3,:,:])
ax[0,4].imshow(pvals[4,:,:])
ax[1,4].imshow(pvals_ch2[4,:,:])
ax[2,4].imshow(pvals_ch3[4,:,:])
ax[0,0].set_title(f"Ch_mod: {charges[0]}")
ax[0,1].set_title(f"Ch_mod: {charges[1]}")
ax[0,2].set_title(f"Ch_mod: {charges[2]}")
ax[0,3].set_title(f"Ch_mod: {charges[3]}")
ax[0,4].set_title(f"Ch_mod: {charges[4]}")



# Show all ticks and label them with the respective list entries
#ax[0,0].set_xticks(np.arange(len(het_mod)), labels=het_mod)
#ax[0,0].set_yticks(np.arange(len(n_hops)), labels=n_hops)

# Rotate the tick labels and set their alignment.
#plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
 #        rotation_mode="anchor")

# Loop over data dimensions and create text annotations.

fig.tight_layout()
plt.savefig("charges.png")
plt.show()
plt.close()

# Loop over data dimensions and create text annotations.

