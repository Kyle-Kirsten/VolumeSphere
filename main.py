import numpy as np
from skimage.measure import marching_cubes
import pyvista as pv
from scipy.ndimage import gaussian_filter
import mcubes

# 定义球体的参数
N = 100  # 体数据的尺寸
x0, y0, z0 = N//2, N//2, N//2  # 球心坐标
origin = np.array([x0, y0, z0])
r = N//4
# 生成球形体数据
# volume = np.zeros((N, N, N), dtype=np.float32)
# for i in range(N):
#     for j in range(N):
#         for k in range(N):
#             if np.sqrt((i - x0)**2 + (j - y0)**2 + (k - z0)**2) <= r:
#                 volume[i, j, k] = 1

x, y, z = np.mgrid[:N, :N, :N]
# volume = ((x - x0)**2 + (y - y0)**2 + (z - z0)**2 - r**2 < 0).astype(float)
volume = (x - x0)**2 + (y - y0)**2 + (z - z0)**2 - r**2

# 应用Marching Cubes算法
vertices, faces, normals, values = marching_cubes(volume, level=0.5)
# Extract the 0.5-levelset since the array is binary
# vertices, faces = mcubes.marching_cubes(volume, 0.5)

# 应用pyvista的MC
# grid = pv.ImageData(
#     dimensions=(N, N, N),
#     spacing=(1, 1, 1),
#     origin=(0, 0, 0),
# )
# mesh = grid.contour([.5], volume.flatten(), method='marching_cubes')
# vertices, faces = mesh.points, mesh.regular_faces

# 输出结果
print("Vertices shape:", vertices.shape)
print("Faces shape:", faces.shape)


# 假设 vertices 和 faces 是 Marching Cubes 算法生成的表面顶点和面

# 对顶点坐标进行高斯平滑
smoothed_volume = gaussian_filter(volume, sigma=1.0, mode='wrap')
smoothed_vertices, smoothed_faces, smoothed_normals, smoothed_values = marching_cubes(smoothed_volume, level=0.5)

# 约束平滑
# smoothed_volume = mcubes.smooth(volume, method='constrained')
# smoothed_vertices, smoothed_faces = mcubes.marching_cubes(smoothed_volume, 0)

# 现在 smoothed_vertices 和 smoothed_faces 可以用于渲染平滑的表面


# # 假设 vertices 和 faces 是 Marching Cubes 算法生成的表面顶点和面,faces的第一个数代表当前面的顶点数量
# # 添加每个面的顶点数量
# num_faces = faces.shape[0]
# faces_with_size = np.hstack([np.full((num_faces, 1), faces.shape[1]), faces])
# smoothed_num_faces = smoothed_faces.shape[0]
# smoothed_faces_with_size = np.hstack([np.full((smoothed_num_faces, 1), smoothed_faces.shape[1]), smoothed_faces])
# # 将faces数组展平
# faces_flat = faces_with_size.flatten()
# smoothed_faces_flat = smoothed_faces_with_size.flatten()


# 创建一个PolyData对象
# poly_data = pv.PolyData(vertices, faces_flat)
poly_data = pv.PolyData.from_regular_faces(vertices, faces)
# poly_data = poly_data.reconstruct_surface()
# poly_data.point_data['Normals'] = normals
# smoothed_poly_data = pv.PolyData(smoothed_vertices, smoothed_faces_flat)
smoothed_poly_data = pv.PolyData.from_regular_faces(smoothed_vertices, smoothed_faces)
# smoothed_poly_data.point_data['Normals'] = smoothed_normals

# 使用Loop细分曲面算法
subdivided_poly_data = poly_data.subdivide(2, 'loop')
# subdivided_poly_data = poly_data
subdivided_smoothed_poly_data = smoothed_poly_data.subdivide(2, 'loop')


# 创建一个Plotter对象
plotter = pv.Plotter(shape=(2, 2))

# 添加PolyData对象到Plotter
plotter.subplot(0, 0)
plotter.add_mesh(poly_data, opacity=0.75, color='lightblue', smooth_shading=True)
plotter.subplot(0, 1)
plotter.add_mesh(smoothed_poly_data, opacity=0.75, color='lightblue', smooth_shading=True)
plotter.subplot(1, 0)
plotter.add_mesh(subdivided_poly_data, opacity=.75, color='lightblue', smooth_shading=True, show_edges=True)
plotter.subplot(1, 1)
plotter.add_mesh(subdivided_smoothed_poly_data, opacity=.75, color='lightblue', smooth_shading=True, show_edges=True)

# 显示图形
plotter.show()