import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.interpolate import griddata

def plotting2D(elementsLibrary, nodesLibrary, T):

    # T - узловая температура

    dataForPlotting = dict()
    cmap = plt.get_cmap('turbo')
    # cmap = plt.get_cmap('gnuplot2')
    # cmap = plt.get_cmap('plasma')
    # cmap = plt.get_cmap('viridis')
    # cmap = plt.get_cmap('rainbow')
    # cmap = plt.get_cmap('magma')

    if max(T) == min(T):
        minTemperature = min(T)
        maxTemperature = minTemperature + 10
    else:
        minTemperature = min(T)
        maxTemperature = max(T)

    for elementNumber in elementsLibrary:
        x = []
        y = []
        temperature = []

        for node in elementsLibrary[elementNumber]:
            x.append(nodesLibrary[node][0])
            y.append(nodesLibrary[node][1])
            temperature.append(T[node-1])

        x_interp = np.linspace(min(x), max(x), 100)
        y_interp = np.linspace(min(y), max(y), 100)
        x_mesh, y_mesh = np.meshgrid(x_interp, y_interp)

        temperature_interp = griddata((x, y), temperature, (x_mesh, y_mesh), method='linear')
        
        dataForPlotting[elementNumber] = [temperature_interp, x_interp, y_interp, temperature]

        plt.imshow(dataForPlotting[elementNumber][0], cmap=cmap, extent=(min(dataForPlotting[elementNumber][1]), max(dataForPlotting[elementNumber][1]), min(dataForPlotting[elementNumber][2]), max(dataForPlotting[elementNumber][2])), origin='lower', vmin=minTemperature, vmax=maxTemperature)
        plt.scatter(x, y, c=dataForPlotting[elementNumber][3], cmap=cmap, edgecolor='none', vmin=minTemperature, vmax=maxTemperature)

    plt.colorbar(label='Temperature')
    plt.show()