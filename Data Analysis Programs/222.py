import numpy as np
import matplotlib.pyplot as plt

# Load data from file
path_to_file = "D:\MPU.TXT"
data = np.loadtxt(path_to_file)
path_to_file2 = "D:\BMP.TXT"
data2 = np.loadtxt(path_to_file2)

MagX, MagY, MagZ = data[:, 6], data[:, 7], data[:, 8]
AccX, AccY, AccZ = data[:, 0], data[:, 1], data[:, 2]
GyroX, GyroY, GyroZ = data[:, 3], data[:, 4], data[:, 5]

temp, pressure=data2[:,0]+273.15, data2[:,1]
sea_level_pressure=1013.25
# Calculate altitude based on pressure

altitude = (temp / 0.0065) * (1 - (pressure / sea_level_pressure) ** (1 / 5.255))

# Create a figure and specify grid
fig = plt.figure(figsize=(15, 8))
gs = fig.add_gridspec(3, 2)

# Set dark theme for the figure
fig.patch.set_facecolor('#2e2e2e')

# 3D subplot for magnetic field on a sphere
ax0 = fig.add_subplot(gs[:, 0], projection='3d')
ax0.set_facecolor('#2e2e2e')
ax0.set_title('Camp Magnetic 3D intr-o sfera', color='#ffffff')

# Generate a sphere using parametric equations
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 10 * np.outer(np.cos(u), np.sin(v))
y = 10 * np.outer(np.sin(u), np.sin(v))
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
ax0.plot_wireframe(x, y, z, color='white', rstride=5, cstride=5)  # Wireframe sphere
# Normalize magnetometer readings
magnitude = np.sqrt(MagX**2 + MagY**2 + MagZ**2)
MagX_normalized = MagX / magnitude * 10  # assuming sphere of radius 10
MagY_normalized = MagY / magnitude * 10
MagZ_normalized = MagZ / magnitude * 10

# Now scatter this data on the 3D subplot
ax0.scatter(MagX_normalized, MagY_normalized, MagZ_normalized, c='r', marker='o')


# Plotting acceleration in a 2D subplot
ax1 = fig.add_subplot(gs[0, 1])
ax1.plot(AccX, label="AccX", color="r")
ax1.plot(AccY, label="AccY", color="g")
ax1.plot(AccZ, label="AccZ", color="b")
ax1.legend()
ax1.set_title("Acceleration", color='#ffffff')
ax1.set_facecolor('#2e2e2e')
ax1.xaxis.label.set_color('white')
ax1.yaxis.label.set_color('white')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.set_xlabel('Timp(ms)')
ax1.set_ylabel('G-uri')
ax1.grid(True)

# Plotting gyroscope in a 2D subplot
ax2 = fig.add_subplot(gs[1, 1])
ax2.plot(GyroX, label="GyroX", color="r")
ax2.plot(GyroY, label="GyroY", color="g")
ax2.plot(GyroZ, label="GyroZ", color="b")
ax2.legend()
ax2.set_title("Orientare prin Giroscop", color='#ffffff')
ax2.set_facecolor('#2e2e2e')
ax2.xaxis.label.set_color('white')
ax2.yaxis.label.set_color('white')
ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')
ax2.set_xlabel('Timp(ms)')
ax2.set_ylabel('Grade')
ax2.grid(True)

# Plotting altitude in a 2D subplot
ax3 = fig.add_subplot(gs[2, 1])
ax3.plot(altitude, color='#a678d2', label='Altitudine (m)')
ax3.set_title('Altitudine bazata pe presiune', color='#ffffff')
ax3.set_facecolor('#2e2e2e')
ax3.xaxis.label.set_color('white')
ax3.yaxis.label.set_color('white')
ax3.tick_params(axis='y', colors='white')
ax3.tick_params(axis='x', colors='white')
ax3.set_xlabel('Timp(ms)')
ax3.set_ylabel('Altitudine (m)')
ax3.legend()
ax3.grid(True)

# Set 3D subplot axes color
ax0.xaxis.label.set_color('white')
ax0.yaxis.label.set_color('white')
ax0.zaxis.label.set_color('white')
ax0.tick_params(axis='x', colors='white')
ax0.tick_params(axis='y', colors='white')
ax0.tick_params(axis='z', colors='white')

plt.tight_layout()
plt.show()
