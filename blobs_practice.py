import porespy as ps
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

im = ps.generators.blobs(shape=[200,200,200], porosity = 0.2, blobiness=0.5)
fig, ax = plt.subplots(figsize=[10, 10])
ax.imshow(ps.visualization.show_3D(im), interpolation='none')
ax.axis(False);

# # Get the coordinates of the non-zero (True) voxels
# x, y, z = np.where(im > 0)

# # Plot the 3D scatter plot
# fig = plt.figure(figsize=(10, 10))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, y, z, c=z, cmap='viridis', marker='o', s=1, alpha=0.5)

# # Set labels and title
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('3D Visualization of Blobs')

# plt.show()
