#create a correlation matrix without the activity column dummies in it:
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="white")

d = ngos_sheldus[['income_adj_ln', 'assets_adj_ln', 'nonzero_assets_adj', 'gov_grants', 'ngo_age', 
                  'top_25', 'median_inc_ln',
                  'mean_inc_ln', 'poverty_rate', 'HRS2010', 'white', 'black']]
# Compute the correlation matrix
corr = d.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
