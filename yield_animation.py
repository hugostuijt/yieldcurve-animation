import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

data = pd.read_excel(r'yieldcurve.xlsx')
#drop the 30y
data = data.drop(columns='30y')

dates = data['Date'].tolist()

data = data.set_index('Date', drop=True)
data = data.reset_index(drop=True)

cols = data.columns.tolist()
colIndex = [30, 60, 90, 180, 365, 730, 1095, 1825, 2555, 3650, 7300]

data.columns = colIndex

x = colIndex
y = data.iloc[0, :].tolist()
x = np.asarray(x)
y = np.asarray(y)
ymask = np.isfinite(y)

txt = None
fig, ax = plt.subplots()
line, = ax.plot(x[ymask], y[ymask], 'r-o')
plt.ylim([0, 12])
plt.grid()

# create custom ticks
x2 = [30, 730, 1095, 1825, 2555, 3650, 7300]#, 10950]
xlabel = ['1m', '2y', '3y', '5y', '7y', '10y', '20y']# ,'30y'] 
plt.xticks(x2, xlabel)

txt = plt.text(100, .2, str(dates[0].year))

def init():
    y = np.asarray([np.nan] * len(x))
    line.set_ydata(y)
    return line, 

def animate(i):
    global txt
    txt.remove()
    # print current year
    txt = plt.text(100, .2, str(dates[i].year))
    y = np.asarray(data.iloc[i, :].tolist())
    ax.set_ylim(0, np.nanmax(y) + 2)
    ymask = np.isfinite(y)
    line.set_xdata(x[ymask])
    line.set_ydata(y[ymask])
    return line,

ani = animation.FuncAnimation(fig, animate, frames=range(0,len(data),50), init_func=init, interval=1, blit=False, save_count=2000, repeat=True,repeat_delay=500)

writer = PillowWriter(fps=1500)
ani.save("us_yieldcurve.gif", writer=writer)

plt.show()
