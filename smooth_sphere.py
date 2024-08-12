import numpy as np
import mcubes

x, y, z = np.mgrid[:100, :100, :100]
binary_sphere = (x - 50)**2 + (y - 50)**2 + (z - 50)**2 - 25**2 < 0

# Extract the 0.5-levelset since the array is binary
vertices, faces = mcubes.marching_cubes(binary_sphere, 0.5)

# 输出结果
print("Vertices num:", len(vertices))
print("Faces num:", len(faces))

# Or export to an OBJ file
mcubes.export_obj(vertices, faces, 'sphere.obj')

smoothed_sphere = mcubes.smooth(binary_sphere, method='gaussian')

# Extract the 0-levelset (the 0-levelset of the output of mcubes.smooth is the
# smoothed version of the 0.5-levelset of the binary array).
vertices, faces = mcubes.marching_cubes(smoothed_sphere, 0)

# 输出结果
print("gaussian smooth Vertices num:", len(vertices))
print("gaussian smooth Faces num:", len(faces))

mcubes.export_obj(vertices, faces, 'gaussian_smooth_sphere.obj')

smoothed_sphere = mcubes.smooth(binary_sphere, method='constrained')

# Extract the 0-levelset (the 0-levelset of the output of mcubes.smooth is the
# smoothed version of the 0.5-levelset of the binary array).
vertices, faces = mcubes.marching_cubes(smoothed_sphere, 0)

# 输出结果
print("constrained smooth Vertices num:", len(vertices))
print("constrained smooth Faces num:", len(faces))

mcubes.export_obj(vertices, faces, 'constrained_smooth_sphere.obj')