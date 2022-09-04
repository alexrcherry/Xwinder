from __future__ import annotations
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


def plot_3d_points(X, Y, Z):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(X, Y, Z)
    plt.show()
    return


def plot_STL(path):
    your_mesh = mesh.Mesh.from_file(path)
    # Create a new plot
    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)

    # add the vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    plt.show()
    return


def get_STL_profile(path):
    your_mesh = mesh.Mesh.from_file(path)
    volume, cog, inertia = your_mesh.get_mass_properties()
    points = your_mesh.vectors

    # inefficent, use numpy slicing instead
    X = []
    Y = []
    Z = []
    for i in range(len(points)):
        for j in range(3):
            X.append(points[i][j][0])
            Y.append(points[i][j][1])
            Z.append(points[i][j][2])

    X = np.around(np.array(X), 3)
    Y = np.around(np.array(Y), 3)
    Z = np.around(np.array(Z), 3)

    # plot_3d_points(X, Y, Z)
    y_set = set(Y)
    y_sorted = list(y_set)
    y_sorted.sort()
    print(len(y_sorted))
    x_max = [0]*len(y_sorted)

    for i in range(len(y_sorted)):
        for j in range(len(X)):
            if Y[j] == y_sorted[i]:
                if x_max[i] < X[j]:
                    x_max[i] = X[j]
    # close boundary
    x_max.append(0)
    y_sorted.append(max(y_sorted))
    x_max.append(0)
    y_sorted.append(min(y_sorted))
    x_max = [0] + x_max
    y_sorted = [min(y_sorted)] + y_sorted
    return x_max, y_sorted


X, Y = get_STL_profile('Body1.obj')

fig, ax = plt.subplots()
ax.plot(X, Y)
# set aspect ratio to 1
ratio = max(Y)/max(X)
x_left, x_right = ax.get_xlim()
y_low, y_high = ax.get_ylim()
ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)

# display plot
plt.show()




