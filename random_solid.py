# import porespy as ps
# import matplotlib.pyplot as plt
# import numpy as np
# import openpnm as op
# import scipy.ndimage as ndi

# # Generate a random solid field
# im = ps.generators.blobs(shape=[100, 100, 100], porosity=0.7, blobiness=0.7)

# # Invert so solid is True (1), pore is False (0)
# solid = ~im

# # Label connected solid regions
# labeled, num = ndi.label(solid)

# # Find the largest solid object
# sizes = ndi.sum(solid, labeled, range(1, num+1))
# largest_label = np.argmax(sizes) + 1
# single_object = (labeled == largest_label)

# # Visualize the single random solid object
# fig, ax = plt.subplots(figsize=[8, 8])
# ax.imshow(np.max(single_object, axis=2), cmap='gray')
# ax.set_title('Projection of Single Random Solid Object')
# ax.axis('off')
# plt.show()

# # Visualize the generated image (3D)
# fig, ax = plt.subplots(figsize=[10, 10])
# ax.imshow(ps.visualization.show_3D(single_object), interpolation='none')
# ax.axis(False)

# # If you want to use this as "im" for further analysis, invert back if needed:
# im = ~single_object  # Now "im" is a binary image with a single random solid object

import pyvista as pv
import numpy as np
from pyvista import UniformGrid

# Assume single_object is your 3D boolean array
# Convert to uint8 for visualization
volume = single_object.astype(np.uint8)

# Create a pyvista UniformGrid
grid = pv.UniformGrid()
grid.dimensions = np.array(volume.shape) + 1
grid.origin = (0, 0, 0)
grid.spacing = (1, 1, 1)
grid.cell_data["values"] = volume.flatten(order="F")

# Plot the 3D object
grid.threshold(0.5).plot(show_edges=True)