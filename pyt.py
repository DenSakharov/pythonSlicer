import sys
import numpy as np
from stl import mesh
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt

class GCodeVisualizer(QMainWindow):
    def __init__(self, stl_file, layer_height):
        super().__init__()
        self.stl_file = stl_file
        self.layer_height = layer_height

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Визуализация G-кода")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Слой', 'Координата Z'])
        self.layout.addWidget(self.table)

        self.table.itemSelectionChanged.connect(self.on_item_selection_changed)

        self.visualizeGCode()

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
                for layer in np.arange(0, max_z, self.layer_height):
                    layer_gcode = process_layer(layer)
                    f.write(layer_gcode)

            f.write("; Конец G-кода\n")
            return gcode_points

    def visualizeGCode(self):
        gcode_points = self.generate_gcode()
        gcode_points = np.array(gcode_points)

        fig, ax = plt.subplots()
        ax.plot(gcode_points[:, 0], gcode_points[:, 1], 'r', linewidth=0.1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.title('Визуализация траектории G-кода')

        # Записываем график во временный файл
        tmp_file = 'temp_plot.png'
        plt.savefig(tmp_file)

        # Отображаем график в виджете QWebEngineView
        self.web_view.setHtml(f'<img src="{tmp_file}">')

        # Создаем данные для таблицы (предполагается, что у вас есть данные)
        table_data = [(f'Слой {i+1}', z) for i, z in enumerate(gcode_points[:, 2])]
        self.populate_table(table_data)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for i, (layer, z) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(layer))
            self.table.setItem(i, 1, QTableWidgetItem(str(z)))

    def on_item_selection_changed(self):
        # Обработка выделения строк в таблице
        selected_rows = [item.row() for item in self.table.selectedItems()]
        # Выделение соответствующих слоев на графике
        if selected_rows:
            selected_layers = [int(self.table.item(row, 0).text().split()[-1]) for row in selected_rows]
            plt.cla()
            plt.plot(gcode_points[:, 0], gcode_points[:, 1], 'r', linewidth=0.1)
            for layer in selected_layers:
                # Подсветить выбранные слои на графике
                plt.plot(gcode_points[layer, 0], gcode_points[layer, 1], 'go', markersize=5)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            self.web_view.setHtml(f'<img src="{tmp_file}">')
        else:
            # Восстановить исходный вид графика
            plt.plot(gcode_points[:, 0], gcode_points[:, 1], 'r', linewidth=0.1)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            self.web_view.setHtml(f'<img src="{tmp_file}')

app = QApplication(sys.argv)
window = GCodeVisualizer('bolt.stl', 10)
window.show()
sys.exit(app.exec_())
