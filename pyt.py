import sys
import numpy as np
from stl import mesh
from concurrent.futures import ThreadPoolExecutor
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
            current_x, current_y, current_z = 0, 0, 0
            gcode_points = []

            def process_layer(z):
                nonlocal current_x, current_y, current_z
                layer_gcode = []

                for vertex in vertices:
                    x, y, vertex_z = vertex
                    if z <= vertex_z < z + self.layer_height:
                        layer_gcode.append(f"G1 X{x} Y{y} Z{z}\n")
                        current_x, current_y, current_z = x, y, z
                        gcode_points.append((x, y, z))

                layer_gcode.append(f"G1 Z{current_z + self.layer_height}\n")
                return ''.join(layer_gcode)

            max_z = vertices[:, 2].max()
            layer_count = int(np.ceil(max_z / self.layer_height))
            with ThreadPoolExecutor() as executor:
                for layer in tqdm(np.arange(0, max_z, self.layer_height), total=layer_count):
                    layer_gcode = process_layer(layer)
                    f.write(layer_gcode)

            f.write("; Конец G-кода\n")

        return gcode_points

    def visualizeGCode(self):
        gcode_points = self.generate_gcode()
        gcode_points = np.array(gcode_points)

        self.selected_layers = set()

        def update_plot():
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            for i, (x, y, z) in enumerate(gcode_points):
                if z in self.selected_layers:
                    ax.plot([x], [y], [z], 'r', marker='o', markersize=5)
                else:
                    ax.plot([x], [y], [z], 'b', linewidth=0.1)

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.title('Визуализация траектории G-кода')
            plt.show()

        def on_item_selection_changed():
            selected_items = self.table.selectedItems()
            selected_layers = set()
            for item in selected_items:
                text = item.text()
                if text.startswith("Layer"):
                    layer_number = int(text.split(" ")[1])
                    selected_layers.add(layer_number)

            self.selected_layers = selected_layers
            update_plot()

        self.table.itemSelectionChanged.connect(on_item_selection_changed)

        update_plot()

app = QApplication(sys.argv)
window = GCodeVisualizer('bolt.stl', 10)
window.show()
sys.exit(app.exec_())
