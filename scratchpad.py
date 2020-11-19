import matplotlib.ticker as mtick
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

# df = pd.DataFrame(np.random.randn(100, 5))
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(xaxis, yaxis)
yticks = mtick.PercentFormatter(xmax=4712) # largest number in remainingtop
ax.yaxis.set_major_formatter(yticks)
plt.show()
"""WORKING, DO NOT LOSE"""