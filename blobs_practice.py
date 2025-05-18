import porespy as ps
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

# im = ps.generators.blobs(shape=[200,200,200], porosity = 0.2, blobiness=0.5)
# fig, ax = plt.subplots(figsize=[10, 10])
# ax.imshow(ps.visualization.show_3D(im), interpolation='none')
# ax.axis(False);

# Set the desired pore (sphere) radius
pore_radius = 5  # Change this value to control pore size

# Generate 3D image with tunable pore size
im = ps.generators.overlapping_spheres(
    shape=[200, 200, 200],
    r=pore_radius,
    porosity=0.2,
    maxiter=0
)
# Visualize the generated image
fig, ax = plt.subplots(figsize=[10, 10])
ax.imshow(ps.visualization.show_3D(im), interpolation='none')
ax.axis(False);
