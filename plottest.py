import numpy as np
import matplotlib
import matplotlib.pyplot as plt

file1 = open('grid2.txt', 'r')
lines = file1.readlines()

n_hops = range(8)
het_mod = np.linspace(-0.75,0.75,13)
het_mod = [str(round(het,2)) for het in het_mod]
print(het_mod)
pvals = np.zeros(shape=(len(n_hops),len(het_mod)),dtype=float)
pvals400 = np.zeros(shape=(len(n_hops),len(het_mod)),dtype=float)
pvals2000 = np.zeros(shape=(len(n_hops),len(het_mod)),dtype=float)
count =0
for line in lines:
        ele, hop, mod, pval, size  = line.split(",")
        X = int(hop)
        Y = int(np.floor(count/8))
        count += 1
        if int(np.floor(count/8)) == 13:
                count =0
        if size.rstrip() == "100.0":
                pvals[X,Y] = float(pval)
        elif size.rstrip() == "464.15888336127773":
                pvals400[X,Y] = float(pval)
        else:
                pvals2000[X,Y] = float(pval)



fig, ax = plt.subplots()
im = ax.imshow(pvals400)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(het_mod)), labels=het_mod)
ax.set_yticks(np.arange(len(n_hops)), labels=n_hops)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.

ax.set_title("Elements 4 - Size 460")
fig.tight_layout()
plt.savefig("ele4size460.png")
plt.close()


fig, ax = plt.subplots()
im = ax.imshow(pvals)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(het_mod)), labels=het_mod)
ax.set_yticks(np.arange(len(n_hops)), labels=n_hops)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.

ax.set_title("Elements 4 - Size 100")
fig.tight_layout()
plt.savefig("ele4size100.png")
plt.close()


fig, ax = plt.subplots()
im = ax.imshow(pvals2000)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(het_mod)), labels=het_mod)
ax.set_yticks(np.arange(len(n_hops)), labels=n_hops)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.

ax.set_title("Elements 4 - Size 2000")
fig.tight_layout()
plt.savefig("ele4size2000.png")
plt.close()
