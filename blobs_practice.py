import porespy as ps
import matplotlib.pyplot as plt
import numpy as np
import openpnm as op

# im = ps.generators.blobs(shape=[200,200,200], porosity = 0.4, blobiness=0.5)
# fig, ax = plt.subplots(figsize=[10, 10])
# ax.imshow(ps.visualization.show_3D(im), interpolation='none')
# ax.axis(False);

# Set the desired pore (sphere) radius
pore_radius = 12  # Change this value to control pore size

# Generate 3D image with tunable pore size
im = ps.generators.overlapping_spheres(
    shape=[200, 200, 200],
    r=pore_radius,
    porosity=0.2,
    maxiter=0
)

# Calculate porosity (in percent)
porosity = ps.metrics.porosity(im)
print(f"Porosity: {porosity*100:.2f}%")

# Calculate tortuosity along the x-direction
tortuosity = ps.simulations.tortuosity_fd(im, axis=0)
#print(f"Tortuosity (x-direction): {tortuosity:.3f}")
print(tortuosity)

# Visualize the generated image (3D)
fig, ax = plt.subplots(figsize=[10, 10])
ax.imshow(ps.visualization.show_3D(im), interpolation='none')
ax.axis(False)

# --- 2D visualization of the first layer ---
plt.figure(figsize=(6, 6))
plt.imshow(im[:, :, 0], cmap='gray', interpolation='none')
plt.title('First Layer (z=0)')
plt.axis('off')

# --- Pore size distribution ---
pore_sizes = ps.metrics.pore_size_distribution(im, bins=30, log=False)
plt.figure()
plt.bar(pore_sizes.bin_centers, pore_sizes.pdf, width=pore_sizes.bin_widths)
plt.xlabel('Pore diameter (voxels)')
plt.ylabel('Probability Density')
plt.title('Pore Size Distribution')

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

# Throat diameter histogram
plt.figure()
plt.hist(pn['throat.diameter'], bins=30)
plt.xlabel('Throat diameter (voxels)')
plt.ylabel('Count')
plt.title('Throat Size Distribution')

plt.show()
