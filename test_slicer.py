import numpy as np
from stl import mesh
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Загрузка STL файла
mesh = mesh.Mesh.from_file('bolt.stl')  # Замените 'bolt.stl' на путь к вашему STL файлу

# Определение количества слоев и их толщины
num_layers = 140  # Измените на нужное количество слоев
z_min = np.min(mesh.v0[:, 2])  # Минимальная Z-координата
z_max = np.max(mesh.v0[:, 2])  # Максимальная Z-координата
layer_thickness = (z_max - z_min) / num_layers

# Количество точек для каждого слоя (увеличенное заполнение)
num_points_per_layer = 1000  # Измените на нужное количество точек

# Создание списка для хранения координат пути
path_coordinates = []

for layer_num in range(num_layers):
    z_level = z_min + layer_thickness * (layer_num + 0.5)  # Перемещение по Z-координате в середину слоя

    # Выбираем вершины, которые находятся в пределах текущего слоя
    layer_vertices = mesh.v0[
        (mesh.v0[:, 2] >= z_level - layer_thickness / 2) & (mesh.v0[:, 2] <= z_level + layer_thickness / 2)]

    if len(layer_vertices) > 0:
        # Рассчитываем координаты пути от центра к краю плоскости
        layer_center = np.mean(layer_vertices, axis=0)[:2]

        # Выбираем только определенное количество точек для слоя
        step = max(1, len(layer_vertices) // num_points_per_layer)
        selected_vertices = layer_vertices[::step]

        layer_coords = selected_vertices[:, :2] - layer_center

        # Сортируем координаты пути по углу для получения "змейки"
        angles = np.arctan2(layer_coords[:, 1], layer_coords[:, 0])
        sorted_indices = np.argsort(angles)
        sorted_path = layer_coords[sorted_indices]

        # Добавляем координаты пути для текущего слоя
        path_coordinates.append(sorted_path)

# Создание G-кода
gcode = "G28 ; Home all axes\n"
gcode += "G21 ; Set units to millimeters\n"
gcode += "G90 ; Set to absolute positioning\n"

# Начальные координаты
current_x, current_y, current_z = 0, 0, 0

for layer_num in range(len(path_coordinates)):
    z_level = z_min + layer_thickness * (layer_num + 0.5)  # Перемещение по Z-координате в середину слоя

    for point in path_coordinates[layer_num]:
        x, y = point
        gcode += f"G1 X{x:.2f} Y{y:.2f} Z{z_level:.2f}\n"
        current_x, current_y, current_z = x, y, z_level

# Завершаем G-код
gcode += "G28 ; Home all axes\n"

# Сохраняем G-код в файл
with open('3d_print.gcode', 'w') as gcode_file:
    gcode_file.write(gcode)

# Создание 3D визуализации
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for layer_num in range(len(path_coordinates)):
    z_level = z_min + layer_thickness * (layer_num + 0.5)
    x = path_coordinates[layer_num][:, 0]
    y = path_coordinates[layer_num][:, 1]
    ax.plot(x, y, np.full_like(x, z_level))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
