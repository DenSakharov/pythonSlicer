import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider
import pyvista as pv

class TwoTableApp(QMainWindow):
    def __init__(self, stl_file):
        QMainWindow.__init__(self)
        self.stl_file = stl_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle('STL Model Visualization')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Создание слайдера для выбора слоя
        self.layer_slider = QSlider()
        self.layer_slider.setMinimum(0)
        self.layer_slider.setMaximum(100)  # Установите максимальное значение в зависимости от вашей модели
        self.layer_slider.valueChanged.connect(self.updateSlice)
        layout.addWidget(self.layer_slider)

        central_widget.setLayout(layout)

        # Инициализация 3D визуализации
        self.plotter = pv.Plotter(window_size=(800, 600))
        self.surface = pv.read(self.stl_file)
        self.current_slice = 0

        # Первоначальное отображение
        self.updateSlice()

    def updateSlice(self):
        self.current_slice = self.layer_slider.value()

        # Удаление предыдущего объекта
        self.plotter.clear()

        # Создание среза вдоль оси Z
        sliced_mesh = self.surface.slice_along_axis(n=self.current_slice, axis=(0, 0, 1))
        self.plotter.add_mesh(sliced_mesh, color=(0, 0, 1))

        # Визуализация 3D сцены
        self.plotter.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stl_file = "bolt.stl"  # Укажите путь к вашему STL-файлу
    window = TwoTableApp(stl_file)
    window.show()
    sys.exit(app.exec_())
