import numpy as np
import matplotlib.pyplot as plt

alpha = 45 # degrees
length = .5 # meters
radius = .1
ax = plt.figure().add_subplot(projection = '3d')

pitch = radius*np.tan(np.radians(alpha))
max_theta = length/pitch

theta = np.linspace(0, max_theta, int(np.degrees(max_theta)))

z = pitch*theta
y = radius*np.sin(theta)
x = radius*np.cos(theta)

ax.plot(x, y, z, label = 'filament')
ax.legend()

plt.show()

