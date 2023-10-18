from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider
import sys
from mayavi import mlab

class TwoTableApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)  # Используем конструктор родительского класса
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Two Tables with 3D Visualization')
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
        self.mlab_widget = mlab.figure(figure=None, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
        self.mlab_widget.scene.disable_render = True

        # Загружаем STL-модель
        self.stl_file = "bolt.stl"
        self.surface = mlab.pipeline.open(self.stl_file)
        self.current_slice = 0

        # Первоначальное отображение
        self.updateSlice()

    def updateSlice(self):
        self.current_slice = self.layer_slider.value()
        self.mlab_widget.scene.disable_render = True

        # Очистка сцены
        mlab.clf(figure=self.mlab_widget)

        # Здесь вам нужно нарезать модель на нужный слой и установить прозрачность
        # Примерно так:
        cut_surface = self.surface
        # Нарезка и прозрачность

        mlab.view(azimuth=0, elevation=90, distance='auto')
        mlab.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TwoTableApp()
    window.show()
    sys.exit(app.exec_())
