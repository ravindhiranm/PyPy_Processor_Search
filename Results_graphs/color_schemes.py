import matplotlib.pyplot as plt
import brewer2mpl
import numpy as np

# Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
set2 = brewer2mpl.get_map('Set1', 'qualitative', 9).mpl_colors

# Set the random seed for consistency
np.random.seed(12)

# Save a nice dark grey as a variable
almost_black = '#262626'

fig, ax = plt.subplots(1)

# Show the whole color range
for i in range(9):
    x = np.random.normal(loc=i, size=1000)
    y = np.random.normal(loc=i, size=1000)
    color = set2[i]
    ax.scatter(x, y, label=str(i), alpha=0.5, edgecolor=almost_black, facecolor=color, linewidth=0.15)

# Remove top and right axes lines ("spines")
spines_to_remove = ['top', 'right']
for spine in spines_to_remove:
    ax.spines[spine].set_visible(False)

# Get rid of ticks. The position of the numbers is informative enough of
# the position of the value.
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# For remaining spines, thin out their line and change the black to a slightly off-black dark grey
almost_black = '#262626'
spines_to_keep = ['bottom', 'left']
for spine in spines_to_keep:
    ax.spines[spine].set_linewidth(0.5)
    ax.spines[spine].set_color(almost_black)

# Change the labels to the off-black
ax.xaxis.label.set_color(almost_black)
ax.yaxis.label.set_color(almost_black)

# Change the axis title to off-black
ax.title.set_color(almost_black)

# Remove the line around the legend box, and instead fill it with a light grey
# Also only use one point for the scatterplot legend because the user will 
# get the idea after just one, they don't need three.
light_grey = np.array([float(248)/float(255)]*3)
legend = ax.legend(frameon=True, scatterpoints=1)
rect = legend.get_frame()
rect.set_facecolor(light_grey)
rect.set_linewidth(0.0)

# Change the legend label colors to almost black, too
texts = legend.texts
for t in texts:
    t.set_color(almost_black)


ax.set_title('prettyplotlib `scatter` example\nshowing improved matplotlib `scatter`')
fig.savefig('scatter_matplotlib_improved_10_pretty_legend.png')
