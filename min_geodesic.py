from gettext import bind_textdomain_codeset
from time import thread_time
import potpourri3d as pp3d
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import math

# V, F = pp3d.read_mesh('Body3.obj')
# shares precomputation for repeated solves
# path_solver = pp3d.EdgeFlipGeodesicSolver(V, F)
# path_pts = path_solver.find_geodesic_path(v_start=100, v_end=3000)
# path_pts is a Vx3 numpy array of points forming the path


def plot_3d_points(X, Y, Z, X1, Y1, Z1):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(X1[::1000], Y1[::1000], Z1[::1000], alpha=.1)
    ax.plot(X, Y, Z, 'r', linewidth=3)
    plt.show()
    return


def cart_coords(radius, theta):
    x = round(radius*math.cos(theta), 3)
    y = round(radius*math.sin(theta), 3)
    return x, y


def get_dims(V):
    X = np.around(V[:, 0], 2)
    Y = np.around(V[:, 1], 2)
    Z = np.around(V[:, 2], 2)

    Z_max = np.max(Z)
    Z_min = np.min(Z)

    index_min = []
    index_max = []
    X_max = []
    Y_max = []
    X_min = []
    Y_min = []

    for i in range(len(X)):
        if Z[i] == Z_max:
            X_max.append(X[i])
            Y_max.append(Y[i])
            index_max.append(i)
        if Z[i] == Z_min:
            X_min.append(X[i])
            Y_min.append(Y[i])
            index_min.append(i)
    r1 = round(max(X_min), 3)
    r2 = round(max(X_max), 3)

    return r1, r2, Z_min, Z_max


def get_values(lobes, radius, fiber_width):
    alpha = (180.00*(lobes-2))/lobes
    beta = alpha + (180*fiber_width)/(math.pi*radius)
    return alpha, beta


def is_close(a, b):
    if (b < a) & ((b+1) >= a):
        return 1
    if (b > a) & ((b-1) <= a):
        return 1

    return 0


def find_index(V, x, y, z):
    print('index search for')
    print(x, y, z)
    V = np.around(V, 1)
    x = np.around(x, 1)
    y = np.around(y, 1)
    z = np.around(z, 1)
    for i in range(len(V)):
        if (is_close(V[i][2], z)):
            if (is_close(V[i][1], y)):
                # print("close:", [V[i][0],V[i][1],V[i][2]])
                if (is_close(V[i][0], x)):
                    print("FOUND: ", [V[i][0], V[i][1], V[i][2]])
                    return i

    return "point not found"


def step(path, lobes, fiber_width, iterations):
    # load mesh
    V, F = pp3d.read_mesh(path)
    print('mesh loaded')
    r1, r2, z_min, z_max = get_dims(V)
    h = z_max - z_min
    # calc angles
    alpha, beta = get_values(lobes, r1, fiber_width)
    # find path
    for i in range(iterations):

        # Geodesic 1
        if i == 0:
            theta_start = 0
        x_start, y_start = cart_coords(r1, theta_start)
        z_start = 0


        x_end, y_end = cart_coords(r2, (theta_start)+(beta/2))
        z_end = h

        index_start = find_index(V, x_start, y_start, z_start)
        index_end = find_index(V, x_end, y_end, z_end)

        path_solver = pp3d.EdgeFlipGeodesicSolver(V, F)
        path1 = path_solver.find_geodesic_path(index_start, index_end)
        if i == 0:
            path = path1
        else:
            path = np.append(path, path1, axis=0)

        # linear path 1
        x_start, y_start, z_start = x_end, y_end, z_end

        x_end, y_end = cart_coords(r2, theta_start+(beta/2)+alpha*(1+i))
        z_end = h

        path2 = np.array([[x_start, y_start, z_start], [x_end, y_end, z_end]])
        path = np.append(path, path2, axis=0)
        # Geodesic 2
        x_start, y_start, z_start = x_end, y_end, z_end
        x_end, y_end = cart_coords(r1, theta_start+(beta/2)+2*alpha*(1+i))
        z_end = 0
        index_start = find_index(V, x_start, y_start, z_start)
        index_end = find_index(V, x_end, y_end, z_end)
        path3 = path_solver.find_geodesic_path(index_start, index_end)
        path = np.append(path, path3, axis=0)
        # linear path 2
        x_start, y_start, z_start = [x_end, y_end, z_end]
        x_end, y_end = cart_coords(r1, theta_start+(beta/2)+3*alpha*(1+i))
        theta_start = theta_start+(beta/2)+3*alpha*(1+i)
        z_end = 0
        path4 = np.array([[x_start, y_start, z_start], [x_end, y_end, z_end]])
        path = np.append(path, path4, axis=0)

    return path


width = 4
lobes = 6

path1 = step('Body3.obj', lobes, width, 5)
# x0, y0, z0 = V[:, 0], V[:, 1], V[:, 2]
x1, y1, z1 = path1[:, 0], path1[:, 1], path1[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# ax.scatter(x0[::100], y0[::100], z0[::100], alpha=.1)
ax.plot(x1, y1, z1)
plt.show()