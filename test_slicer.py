import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from stl import mesh

# Загрузка STL файла
mesh = mesh.Mesh.from_file('bolt.stl')  # Замените 'bolt.stl' на путь к вашему STL файлу

# Определение количества слоев и их толщины
num_layers = 70  # Измените на нужное количество слоев
z_min = np.min(mesh.v0[:, 2])  # Минимальная Z-координата
z_max = np.max(mesh.v0[:, 2])  # Максимальная Z-координата
layer_thickness = (z_max - z_min) / num_layers

# Количество точек для каждого слоя (увеличенное заполнение)
num_points_per_layer = 1000000  # Измените на нужное количество точек

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

# Создание окна для отображения пути
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

layer_idx = 0

def update(val):
    global layer_idx
    layer_idx = int(val)
    ax.clear()

    if layer_idx < len(path_coordinates):
        x = path_coordinates[layer_idx][:, 0]
        y = path_coordinates[layer_idx][:, 1]
        ax.scatter(x, y, s=1)  # Используем scatter для отображения точек
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())

    plt.draw()

slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(slider_ax, 'Layer', 0, num_layers - 1, valinit=0, valstep=1)
slider.on_changed(update)

update(layer_idx)  # Отображение начального слоя

plt.show()
