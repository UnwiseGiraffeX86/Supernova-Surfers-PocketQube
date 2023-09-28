import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Number of data points
num_points = 10000

# Generate data points with some random variation for magnetic field
MagX = 1 + 0.1 * np.random.randn(num_points)
MagY = 1 + 0.1 * np.random.randn(num_points)
MagZ = -0.3 + 0.1 * np.random.randn(num_points)

# Generate data points with some random variation for acceleration (m/s^2)
AccX = 0 + 1.0 * np.random.randn(num_points)  # Acceleration around zero
AccY = 0 + 1.0 * np.random.randn(num_points)
AccZ = 9.81 + 1.0 * np.random.randn(num_points)  # Earth's gravitational acceleration

# Generate data points with some random variation for gyroscope (rad/s)
GyroX = 0 + 0.1 * np.random.randn(num_points)
GyroY = 0 + 0.1 * np.random.randn(num_points)
GyroZ = 0 + 0.1 * np.random.randn(num_points)

# Stack data
data = np.vstack((MagX, MagY, MagZ, AccX, AccY, AccZ, GyroX, GyroY, GyroZ)).T

# Save to TEST.TXT
path_to_file = "D:\TEST.TXT"
np.savetxt(path_to_file, data, fmt='%f %f %f %f %f %f %f %f %f')

print(f"Saved {len(data)} data points to {path_to_file}.")
