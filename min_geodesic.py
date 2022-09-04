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
    # val = int(len(X_max)/4)
    # X_max.pop(val)
    # Y_max.pop(val)
    # X_min.pop(1)
    # Y_min.pop(1)
    # print(len(X_max))
    # plt.scatter(X_max, Y_max)
    # plt.scatter(X_max[50], Y_max[50])
    # plt.scatter(X_min, Y_min)
    # plt.show()
    r1 = round(max(X_min), 3)
    r2 = round(max(X_max), 3)
    # print('The diameter of the first circle is:', r1*2, 'mm')
    # print('The diameter of the second circle is:', r2*2, 'mm')
    # print('The distance between points for the first circle is:',
    #       r1*2*3.14/len(index_min), 'mm')
    # print('The distance between points for the second circle is:',
    #       r2*2*3.14/len(index_max), 'mm')
    return r1, r2, Z_min, Z_max


def get_values(lobes, radius, fiber_width):
    alpha = (180.00*(lobes-2))/lobes
    beta = alpha + (180*fiber_width)/(math.pi*radius)
    return alpha, beta


def is_close(a,b):
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
                print("close:", [V[i][0],V[i][1],V[i][2]])
                if (is_close(V[i][0], x)):
                    print("FOUND: ",[V[i][0],V[i][1],V[i][2]])
                    return i

    return "point not found"


# r1, r2, z_min, z_max = get_dims(V)
# width = 4
# lobes = 6
# radius = r1
# alpha, beta = get_values(lobes, radius, width)
# x_end, y_end = cart_coords(r2, beta)
# theoretical_start = [r1, 0, 0]
# print(beta)
# theoretical_end = [x_end, y_end, z_max-z_min]
# print('start:', theoretical_start)
# print('end:', theoretical_end)
# start_index = find_index(V, theoretical_start[0], theoretical_start[1],
#                          theoretical_start[2])
# end_index = find_index(V, theoretical_end[0], theoretical_end[1],
#                        theoretical_end[2])

# print(type(start_index), " ", start_index)
# print(type(end_index), " ", end_index)

# path_solver = pp3d.EdgeFlipGeodesicSolver(V, F)
# path_pts = path_solver.find_geodesic_path(v_start=start_index, v_end=end_index)
# plot_3d_points(path_pts[:, 0], path_pts[:, 1], path_pts[:, 2],
#                V[:, 0], V[:, 1], V[:, 2])


def step(V, F, r1, r2, alpha, beta, h, r_start, theta_start, z_start):
    # Geodesic 1
    x_start, y_start = cart_coords(r_start, theta_start)
    x_end, y_end = cart_coords(r2, beta)
    z_end = h
    index_start = find_index(V, x_start, y_start, z_start)
    index_end = find_index(V, x_end, y_end, z_end)
    print('start', x_start, y_start, z_start)
    print('end', x_end, y_end, z_end)
    path_solver = pp3d.EdgeFlipGeodesicSolver(V, F)
    path1 = path_solver.find_geodesic_path(index_start, index_end)
    # linear path 1
    x_start, y_start, z_start = x_end, y_end, z_end
    x_end, y_end = cart_coords(r2, beta+alpha)
    z_end = h
    path2 = np.array([[x_start, y_start, z_start], [x_end, y_end, z_end]])
    # Geodesic 2
    x_start, y_start, z_start = x_end, y_end, z_end
    x_end, y_end = cart_coords(r1, beta+2*alpha)
    z_end = 0
    index_start = find_index(V, x_start, y_start, z_start)
    index_end = find_index(V, x_end, y_end, z_end)
    path3 = path_solver.find_geodesic_path(index_start, index_end)
    # linear path 2
    x_start, y_start, z_start = [x_end, y_end, z_end]
    x_end, y_end = cart_coords(r1, beta+3*alpha)
    z_end = 0
    path4 = np.array([[x_start, y_start, z_start], [x_end, y_end, z_end]])

    return path1, path2, path3, path4


V, F = pp3d.read_mesh('Body3.obj')
print('mesh loaded')
r1, r2, z_min, z_max = get_dims(V)
width = 4
lobes = 6
radius = r1
alpha, beta = get_values(lobes, radius, width)
path1, path2, path3, path4 = step(V, F, r1, r2, alpha, beta, z_max-z_min, r1, 0, z_min)
x1, y1, z1 = path1[:, 0], path1[:, 1], path1[:, 2]
x2, y2, z2 = path2[:, 0], path2[:, 1], path2[:, 2]
x3, y3, z3 = path3[:, 0], path3[:, 1], path3[:, 2]
x4, y4, z4 = path4[:, 0], path4[:, 1], path4[:, 2]
x0, y0, z0 = V[:, 0], V[:, 1], V[:, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x0[::100], y0[::100], z0[::100], alpha=.1)
ax.plot(x1, y1, z1)
ax.plot(x2, y2, z2)
ax.plot(x3, y3, z3)
ax.plot(x4, y4, z4)
plt.show()

