from __future__ import annotations
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# your_mesh = mesh.Mesh.from_file('Solidworks.STL')
your_mesh = mesh.Mesh.from_file('Test.stl')


volume, cog, inertia = your_mesh.get_mass_properties()

print("Volume                                  = {0}".format(volume))
print("Position of the center of gravity (COG) = {0}".format(cog))
print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0, :]))
print("                                          {0}".format(inertia[1, :]))
print("                                          {0}".format(inertia[2, :]))

print(type(your_mesh.vectors))
print(np.shape(your_mesh.vectors))

if cog[0] < 1*10**-7:
    print('X small enough')
if cog[1] < 1*10**-7:
    print('Y small enough')
if cog[2] < 1*10**-7:
    print('Z small enough')


def plot3d(self):
    # Create a new plot
    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)

    # add the vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.vectors))

    # Auto scale to the mesh size
    scale = self.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    plt.show()
    return


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
print('X:', len(X))
print('Y:', len(Y))
plt.scatter(X, Y)


y_set = set()
edge_points_X = []
edge_points_Y = []
for i in range(len(Y)):
    y_set.add(Y[i])
y_sorted = list(y_set)
y_sorted.sort()

x_max = [0]*len(y_sorted)

for i in range(len(y_sorted)):
    for j in range(len(X)):
        if Y[j] == y_sorted[i]:
            if x_max[i] < X[j]:
                x_max[i] = X[j]
annotations = [0]*len(x_max)
for i in range(len(x_max)):
    annotations[i] = str(round(x_max[i]))+" "+str(round(y_sorted[i]))
plt.scatter(x_max, y_sorted)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Profile of STL", fontsize=15)
for i, label in enumerate(annotations):
    plt.annotate(label, (x_max[i], y_sorted[i]))
plt.show()
