import numpy as np
import matplotlib.pyplot as plt

def replot()
    np.load(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_bulk',bulk_chi)
    np.load(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_outer',outer_chi)
    np.load(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_alt',alt_outer)
    np.load(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_both',bulkouter)
            
        
        mean_bulk = np.mean(bulk_chi)
        mean_outer = np.mean(outer_chi)
        mean_comb = np.mean(bulkouter)
        var_bulk = np.var(bulk_chi)
        var_outer = np.var(outer_chi)
        var_comb = np.var(bulkouter)
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


        X = np.linspace(-3.5,3.5,1000)
        Y_b = stats.norm.pdf(X,mean_bulk,sigma_b)
        Y_o = stats.norm.pdf(X,mean_outer,sigma_o)
        Y_c = stats.norm.pdf(X,mean_comb,sigma_c)




        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        ax.hist(bulk_chi, bins=100, histtype='bar', color='steelblue', alpha=0.9)
        ax.hist(bulkouter, bins=100, histtype='bar', color='orange', alpha=0.6)
        #ax[1].hist(bulk_chi, bins=100, histtype='bar', color='steelblue', alpha=1)
        #ax[1].hist(outer_chi, bins=100, histtype='step', color='orange', alpha=0.7)
        #ax[2].hist(bulk_chi, bins=100, histtype='bar', color='steelblue', alpha=0.7)
        ax2 = ax.twinx()
        #ax[2].plot(X,Y_b,color='seagreen')
        #ax[2].plot(X,Y_o,'--',color='orange')
        #ax[2].plot(X,Y_c,'-.',color='red')
        #ax.vlines(np.median(pval_bootstrap), 0, ax.get_ylim()[1], color='firebrick')
        #ax.vlines(np.percentile(pval_bootstrap,95),0, ax.get_ylim()[1], color='darkviolet')
        #ax.vlines(np.percentile(pval_bootstrap,99),0, ax.get_ylim()[1], color='seagreen')
        ax.set(ylim=(0, ax.get_ylim()[1] * 1.2))
        #ax[1].set(ylim=(0, ax[1].get_ylim()[1] * 1.2))
        #ax[2].set(ylim=(0, ax[2].get_ylim()[1] * 1.2))
        ax2.set(ylim=(0, ax2.get_ylim()[1] * 1.2))
        ax2.plot(X,Y_b,color='seagreen')
        #ax[2].plot(X,Y_o,'--',color='orange')
        ax2.plot(X,Y_c,'-.',color='red')
        #ax.text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+'\n'+r'N$_{hops}$: '+f'{kwargs["n_hops"]}'+f'\nBond modifier: {kwargs["het_mod"]:.2f}' +\
        #f'\nMedian p-value = {np.median(pval_bootstrap):.2f} '+f'\nAdded atoms: ' + f'{kwargs["heanp_size"]}', family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
        #ax[0].text(0.02, 0.98,r'N$_{elements}$: '+f'{len(kwargs["elements"])}'+ f"\nNP size: {kwargs['heanp_size']}"+f'\nShape:{k}\n'+f'Scale:{theta}'+f'\nShape: {k2}'  , family='monospace', fontsize=13, transform=ax[0].transAxes,verticalalignment='top')
       
        #'\nMedian p-value = {np.median(pval_bootstrap):.2f}'+f"\n95%: {np.percentile(pval_bootstrap,95,method='inverted_cdf')}"+f"\n99%: {np.percentile(pval_bootstrap,99,method='inverted_cdf')}"
        ax.set_xlabel(r"$\chi$" + " combined", fontsize=16)
        ax.text(0.02, 0.98,f"Mean, Var \n Bulk: {mean_bulk:.2f}, {var_bulk:.2f}\n Comb: {mean_comb:.2f}, {var_comb:.2f} ", family='monospace', fontsize=13, transform=ax.transAxes,verticalalignment='top')
       
        #ax[1].set_xlabel(r"$\chi$" + " outer", fontsize=16)
        #ax[2].set_xlabel(r"$\chi$" + " Normal dist", fontsize=16)
        ax.set_ylabel('Frequency', fontsize=16)
        ax.legend(['Bulk_chi','combined'], loc='right')
        #ax[1].legend(['Bulk_chi','outer'], loc='right')
        #ax[2].legend(['Bulk','Outer','Combined'], loc='right')
        #ax2.set_ylabel('Probability', fontsize=16)
        #fig.savefig(f'pvals/{len(kwargs["elements"])}_{kwargs["n_hops"]}_{kwargs["het_mod"]:.2f}_{kwargs["heanp_size"]}.png')
        #fig.savefig(f'pvals/{len(kwargs["elements"])}_{kwargs["heanp_size"]}.png')
        fig.savefig(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_s')
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_bulk',bulk_chi)
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_outer',outer_chi)
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_alt',alt_outer)
        np.savetxt(f'chi_{len(kwargs["elements"])}_{kwargs["heanp_size"]}_both',bulk_chi)