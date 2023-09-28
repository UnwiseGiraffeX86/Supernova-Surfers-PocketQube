import numpy as np
import matplotlib.pyplot as plt

# Load data from file
path_to_file = "D:\TEST.TXT"
data = np.loadtxt(path_to_file)

MagX = data[:, 0]
MagY = data[:, 1]
MagZ = data[:, 2]

# Normalize the magnetic field vectors
magnitude = np.sqrt(MagX**2 + MagY**2 + MagZ**2)
normMagX = MagX / magnitude
normMagY = MagY / magnitude
normMagZ = MagZ / magnitude

# Create a figure
fig = plt.figure()

# Set dark theme colors for the figure
fig.patch.set_facecolor('#2e2e2e')

# 3D subplot
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#2e2e2e')
ax.set_title('3D Magnetic Field on Sphere', color='#ffffff')

# Drawing a wireframe sphere
u = np.linspace(0, 2 * np.pi, 24)
v = np.linspace(0, np.pi, 24)
x = 10 * np.outer(np.cos(u), np.sin(v))
y = 10 * np.outer(np.sin(u), np.sin(v))
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_wireframe(x, y, z, color='white')

# Plot the normalized magnetic data as dots on the sphere
sphere_radius = 10
ax.scatter(normMagX * sphere_radius, normMagY * sphere_radius, normMagZ * sphere_radius, c='r', marker='o')

# Set the colors for the axes
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.tick_params(axis='z', colors='white')


plt.show()
