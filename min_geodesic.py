from gettext import bind_textdomain_codeset
from textwrap import fill
from time import thread_time
import potpourri3d as pp3d
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import math
import time

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
    x = round(radius*math.cos(math.radians(theta)), 3)
    y = round(radius*math.sin(math.radians(theta)), 3)
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
    alpha = 360.0/lobes
    beta = (180*fiber_width)/(math.pi*radius)
    return alpha, beta


def is_close(a, b):
    if (b < a) & ((b+0.7) >= a):
        return 1
    if (b > a) & ((b-0.7) <= a):
        return 1

    return 0


def find_index_top(V, x, y, z):
    # print('index search for')
    # print(x, y, z)
    start_time = time.time()
    V = np.around(V, 1)
    x = np.around(x, 1)
    y = np.around(y, 1)
    z = np.around(z, 1)
    for i in range(len(V)):
        if (is_close(V[i][2], z)):
            if (is_close(V[i][1], y)):
                # print("close:", [V[i][0],V[i][1],V[i][2]])
                if (is_close(V[i][0], x)):
                    print(time.time()-start_time, 'Z:', V[i][2])
                    return i

    return "point not found"


def find_index_bottom(V, x, y, z):
    # print('index search for')
    # print(x, y, z)
    start_time = time.time()
    V = np.around(V, 1)
    x = np.around(x, 1)
    y = np.around(y, 1)
    z = np.around(z, 1)
    for i in range(len(V)-1, 0, -1):
        if (is_close(V[i][2], z)):
            if (is_close(V[i][1], y)):
                # print("close:", [V[i][0],V[i][1],V[i][2]])
                if (is_close(V[i][0], x)):
                    print(time.time()-start_time, 'Z:', V[i][2])
                    return i

    return "point not found"


def step(path, lobes, fiber_width):
    # load mesh
    V, F = pp3d.read_mesh(path)
    path_solver = pp3d.EdgeFlipGeodesicSolver(V, F)
    print('mesh and solver loaded')
    r1, r2, z_min, z_max = get_dims(V)
    h = z_max - z_min
    # calc angles
    alpha, beta = get_values(lobes, r1, fiber_width)
    # calc num of iterations
    iterations = math.ceil(360.0/beta)
    print('num of iterations required is: ', iterations)
    # find path
    for i in range(iterations):

        # Geodesic 1
        if i == 0:
            theta_start = 0
            r_start = r1
            z_start = 0
            x_start, y_start = cart_coords(r_start, theta_start)
        else:
            x_start, y_start, z_start = x_end, y_end, z_end
            theta_start = theta_end

        theta_end = theta_start+alpha
        r_end = r2
        z_end = h
        x_end, y_end = cart_coords(r_end, theta_end)

        index_start = find_index_bottom(V, x_start, y_start, z_start)
        index_end = find_index_top(V, x_end, y_end, z_end)

        path1 = path_solver.find_geodesic_path(index_start, index_end)
        if i == 0:
            path = path1
        else:
            path = np.append(path, path1, axis=0)
        # print("start 1:", [r_start, theta_start, z_start])
        # print("end 1:", [r_end, theta_end, z_end])

        # linear path 1
        x_start, y_start, z_start = x_end, y_end, z_end
        theta_start = theta_end

        r_end = r2
        theta_end = theta_start + beta/2 + alpha
        z_end = h
        x_end, y_end = cart_coords(r_end, theta_end)

        path2 = np.array([[x_start, y_start, z_start], [x_end, y_end, z_end]])
        path = np.append(path, path2, axis=0)
        # print("start 2:", [r_start, theta_start, z_start])
        # print("end 2:", [r_end, theta_end, z_end])
        # Geodesic 2 needs

        x_start, y_start, z_start = x_end, y_end, z_end
        theta_start = theta_end

        r_end = r1
        theta_end = theta_start + alpha
        z_end = 0
        x_end, y_end = cart_coords(r_end, theta_end)

        index_start = find_index_top(V, x_start, y_start, z_start)
        index_end = find_index_bottom(V, x_end, y_end, z_end)

        path3 = path_solver.find_geodesic_path(index_start, index_end)
        path = np.append(path, path3, axis=0)
        # print("start 3:", [r_start, theta_start, z_start])
        # print("end 3:", [r_end, theta_end, z_end])
        # linear path 2
        x_start, y_start, z_start = x_end, y_end, z_end
        theta_start = theta_end

        r_end = r1
        theta_end = theta_start + beta/2 + alpha
        z_end = 0
        x_end, y_end = cart_coords(r_end, theta_end)

        path4 = np.array([[x_start, y_start, z_start], [x_end, y_end, z_end]])
        path = np.append(path, path4, axis=0)
        # print("start 4:", [r_start, theta_start, z_start])
        # print("end 4:", [r_end, theta_end, z_end])
    return path



width = 8
lobes = 3

path1 = step('Body3.obj', lobes, width)
# x0, y0, z0 = V[:, 0], V[:, 1], V[:, 2]
x1, y1, z1 = path1[:, 0], path1[:, 1], path1[:, 2]

# 3d plotting
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# ax.scatter(x0[::100], y0[::100], z0[::100], alpha=.1)
ax.plot(x1, y1, z1)
plt.show()


# # 2d plotting
# circle1 = plt.Circle((0, 0), 25, color='g', fill=False)
# circle2 = plt.Circle((0, 0), 50, color='r', fill=False)

# ax = plt.gca()
# ax.cla() # clear things for fresh plot
# ax.add_patch(circle1)
# ax.add_patch(circle2)
# ax.plot(x1, y1)
# plt.show()