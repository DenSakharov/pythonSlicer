import sys
import numpy as np
from stl import mesh
from concurrent.futures import ThreadPoolExecutor  # Добавьте импорт
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QPushButton
from tqdm import tqdm

class GCodeVisualizer(QMainWindow):
    def __init__(self, stl_file, layer_height):
        super().__init__()
        self.stl_file = stl_file
        self.layer_height = layer_height

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Визуализация G-кода")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Слой', 'Координата Z'])
        self.layout.addWidget(self.table)

        self.visualize_button = QPushButton('Визуализировать G-код')
        self.layout.addWidget(self.visualize_button)
        self.visualize_button.clicked.connect(self.visualizeGCode)

    def generate_gcode(self):
        with open('layer_contour.gcode', 'w') as f:
            f.write("; Начало G-кода\n")

            your_mesh = mesh.Mesh.from_file(self.stl_file)
            vertices = your_mesh.v0
            current_z = None
            layer_count = 0
            gcode_points = []  # Список для хранения точек

            for vertex in vertices:
                x, y, vertex_z = vertex
                if current_z is None:
                    current_z = vertex_z
                    f.write(f"; Начало слоя {layer_count + 1}\n")
                    layer_count += 1
                elif vertex_z != current_z:
                    f.write(f"; Конец слоя {layer_count}\n")
                    current_z = vertex_z
                    f.write(f"; Начало слоя {layer_count + 1}\n")
                    layer_count += 1
                f.write(f"G1 X{x} Y{y} Z{vertex_z}\n")

                # Сохранение точек
                gcode_points.append((x, y, vertex_z))

            f.write("; Конец G-кода\n")

        return gcode_points  # Возвращает список точек

    def visualizeGCode(self):
        gcode_points = self.generate_gcode()
        gcode_points = np.array(gcode_points)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')  # Один график 3D

        ax.plot(gcode_points[:, 0], gcode_points[:, 1], gcode_points[:, 2], 'r', linewidth=0.1)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title('Визуализация траектории G-кода')

        # Создать таблицу
        layer_count = len(np.unique(gcode_points[:, 2]))
        self.table.setRowCount(layer_count)
        for i, z in enumerate(np.unique(gcode_points[:, 2])):
            self.table.setItem(i, 0, QTableWidgetItem(f'Layer {i + 1} (Z = {z})'))

        plt.show()


app = QApplication(sys.argv)
window = GCodeVisualizer('bolt.stl', 10)
window.show()
sys.exit(app.exec_())
