import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

desired_angle = 57 # degrees
dz = .01 # interpolation distance inches

z_coords = [0,   4,   10, 14 ] #z coords where radius changes
x_coords = [1.6, 1.6, 5, 5] #radius at z coord

z_interp = np.arange(0,z_coords[-1], dz)
x_interp = np.interp(z_interp, z_coords, x_coords)

num_sections = len(z_interp)-1



angle = [0]
z = [0]

for i in range(num_sections):
    pitch = np.pi*2*x_interp[i]*np.tan(np.radians(desired_angle))

    d_angle = 360*dz/pitch

    z.append(z[-1]+dz)
    angle.append(angle[-1]+d_angle)




#theta in degrees
def plot_3d_points(r, theta, Z):
    X = r*np.cos(np.radians(theta))
    Y = r*np.sin(np.radians(theta))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1.0, 1.0, max(Z)/max(X), 1]))


    ax.plot(X, Y, Z)
    plt.show()
    return

# plot_3d_points(x_interp, angle, z)

X = x_interp*np.cos(np.radians(angle))
Y = x_interp*np.sin(np.radians(angle))

plt.plot(X,Y)
plt.show()
