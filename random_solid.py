import porespy as ps
import matplotlib.pyplot as plt
import numpy as np
import openpnm as op
import random

# Set the shape and sphere parameters
shape = [200, 200, 200]
center = np.array(shape) // 2
radius = min(shape) // 2  # Largest sphere that fits

# Step 1: Create a solid sphere mask
zz, yy, xx = np.ogrid[:shape[0], :shape[1], :shape[2]]
distance = np.sqrt((zz - center[0])**2 + (yy - center[1])**2 + (xx - center[2])**2)
sphere_mask = distance <= radius

# Step 2: Generate pores only inside the sphere
pore_radius = 12  # Change this value to control pore size
# Generate a full-cube image, then restrict to the sphere
im_full = ps.generators.overlapping_spheres(
    shape=shape,
    r=pore_radius,
    porosity=0.2,
    maxiter=0
)
# Only keep pores inside the sphere
im = im_full & sphere_mask

# Visualize the generated image (3D)
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
# Downsample for visualization if needed (for speed)
step = 2  # Increase for faster rendering, decrease for more detail
ax.voxels(im[::step, ::step, ::step], facecolors='blue', edgecolor='k', alpha=0.5)
ax.set_title('3D Sphere with Pores')
plt.show()

# Calculate porosity (in percent)
porosity = ps.metrics.porosity(im)
print(f"Porosity: {porosity*100:.2f}%")

# Calculate tortuosity along the x-direction
tortuosity = ps.simulations.tortuosity_fd(im, axis=0)
print(tortuosity)

# --- 2D visualization of the first layer ---
plt.figure(figsize=(6, 6))
plt.imshow(im[:, :, 0], cmap='gray', interpolation='none')
plt.title('First Layer (z=0)')
plt.axis('off')

# --- Throat size distribution (network extraction required) ---
net = ps.networks.snow2(im, boundary_width=0).network
pn = op.io.network_from_porespy(net)
pn['pore.diameter'] = net['pore.inscribed_diameter']
pn['throat.diameter'] = net['throat.inscribed_diameter']

# Assign models for throat length, pore volume, and throat volume (cuboid/cube for voxel images)
pn.add_model(propname='throat.length', model=op.models.geometry.throat_length.cubes_and_cuboids, regen_mode='normal')
pn.add_model(propname='pore.volume', model=op.models.geometry.pore_volume.cube, regen_mode='normal')
pn.add_model(propname='throat.volume', model=op.models.geometry.throat_volume.cuboid, regen_mode='normal')
pn.regenerate_models()

# Calculate and print pore and throat volumes
pore_volumes = pn['pore.volume']
throat_volumes = pn['throat.volume']
print(f"Mean pore volume: {np.mean(pore_volumes):.2f} voxels³")
print(f"Mean throat volume: {np.mean(throat_volumes):.2f} voxels³")
print(f"Total pore volume: {np.sum(pore_volumes):.2f} voxels³")
print(f"Total throat volume: {np.sum(throat_volumes):.2f} voxels³")

# Pore diameter histogram
plt.figure()
plt.hist(pn['pore.diameter'], bins=30)
plt.xlabel('Pore diameter (voxels)')
plt.ylabel('Count')
plt.title('Pore Size Distribution')

plt.show()

# Throat diameter histogram
plt.figure()
plt.hist(pn['throat.diameter'], bins=30)
plt.xlabel('Throat diameter (voxels)')
plt.ylabel('Count')
plt.title('Throat Size Distribution')

plt.show()



