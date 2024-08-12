import numpy as np
from skimage.measure import marching_cubes
import pyvista as pv
from scipy.ndimage import gaussian_filter

def spider_cage(x, y, z, a=0.9):
    x2 = x * x
    y2 = y * y
    x2_y2 = x2 + y2
    return (np.sqrt((x2 - y2) ** 2 / x2_y2 + 3 * (z * np.sin(a)) ** 2) - 3) ** 2 + 6 * (
        np.sqrt((x * y) ** 2 / x2_y2 + (z * np.cos(a)) ** 2) - 1.5
    ) ** 2

def sphere(x, y, z):
    return x**2 + y**2 + z**2


# create a uniform grid to sample the function with
n = 100
r = n//4
x_min, y_min, z_min = 0, 0, 0
x0, y0, z0 = n//2, n//2, n//2  # 球心坐标
grid = pv.ImageData(
    dimensions=(n, n, n),
    spacing=(1, 1, 1),
    origin=(x_min, y_min, z_min),
)
x, y, z = grid.points.T
print("Spacing:", grid.spacing)

# sample and plot
volume = ((x - x0)**2 + (y - y0)**2 + (z - z0)**2 - r**2 < 0).astype(float)
print("Volume shape:", volume.shape)
mesh = grid.contour([.5], volume, method='marching_cubes')
smoothed_volume = gaussian_filter(np.reshape(volume, (n, n, n)), sigma=1.0, mode='wrap').flatten()
smoothed_mesh = grid.contour([.5], smoothed_volume, method='marching_cubes')

# 输出结果
# 输出结果
print("Vertices shape:", mesh.points.shape)
print("Faces shape:", mesh.regular_faces.shape)


# 使用Loop细分曲面算法
subdivided_mesh = mesh.subdivide(2, 'loop')
subdivided_smoothed_mesh = smoothed_mesh.subdivide(2, 'loop')

# 创建一个Plotter对象
plotter = pv.Plotter(shape=(2, 2))

# 添加PolyData对象到Plotter
plotter.subplot(0, 0)
plotter.add_mesh(mesh, opacity=0.75, color='lightblue', smooth_shading=True)
plotter.subplot(0, 1)
plotter.add_mesh(smoothed_mesh, opacity=0.75, color='lightblue', smooth_shading=True)
plotter.subplot(1, 0)
plotter.add_mesh(subdivided_mesh, opacity=.75, color='lightblue', smooth_shading=True, show_edges=True)
plotter.subplot(1, 1)
plotter.add_mesh(subdivided_smoothed_mesh, opacity=.75, color='lightblue', smooth_shading=True, show_edges=True)

# 显示图形
plotter.show()
