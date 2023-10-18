import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from mayavi import mlab

class TwoTableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Two Tables with 3D Visualization')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Создание первой таблицы
        self.table1 = QTableWidget()
        self.table1.setColumnCount(2)
        self.table1.setHorizontalHeaderLabels(['Column 1', 'Column 2'])
        layout.addWidget(self.table1)

        # Создание второй таблицы
        self.table2 = QTableWidget()
        self.table2.setColumnCount(2)
        self.table2.setHorizontalHeaderLabels(['Column A', 'Column B'])
        layout.addWidget(self.table2)

        # Кнопка для добавления информации
        add_button = QPushButton('Добавить информацию')
        add_button.clicked.connect(self.addInfo)
        layout.addWidget(add_button)

        # Кнопка для считывания информации из файла
        load_button = QPushButton('Загрузить из файла')
        load_button.clicked.connect(self.loadFromFile)
        layout.addWidget(load_button)

        # Кнопка для 3D визуализации
        visualize_button = QPushButton('Визуализировать 3D модель')
        visualize_button.clicked.connect(self.visualize3D)
        layout.addWidget(visualize_button)

        central_widget.setLayout(layout)

        # Инициализация 3D визуализации
        self.mlab_widget = mlab.figure(figure=None, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
        self.mlab_widget.scene.disable_render = True

    def addInfo(self):
        # Создание новой строки и добавление данных в первую таблицу
        rowPosition = self.table1.rowCount()
        self.table1.insertRow(rowPosition)
        self.table1.setItem(rowPosition, 0, QTableWidgetItem("Новое значение 1"))
        self.table1.setItem(rowPosition, 1, QTableWidgetItem("Новое значение 2"))

        # Создание новой строки и добавление данных во вторую таблицу
        rowPosition = self.table2.rowCount()
        self.table2.insertRow(rowPosition)
        self.table2.setItem(rowPosition, 0, QTableWidgetItem("New Value A"))
        self.table2.setItem(rowPosition, 1, QTableWidgetItem("New Value B"))

    def loadFromFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'r') as file:
                data = file.read().splitlines()
                for line in data:
                    # Создание новой строки и добавление данных в первую таблицу
                    rowPosition1 = self.table1.rowCount()
                    self.table1.insertRow(rowPosition1)
                    values = line.split(',')
                    if len(values) >= 2:
                        self.table1.setItem(rowPosition1, 0, QTableWidgetItem(values[0]))
                        self.table1.setItem(rowPosition1, 1, QTableWidgetItem(values[1]))

                    # Создание новой строки и добавление данных во вторую таблицу
                    rowPosition2 = self.table2.rowCount()
                    self.table2.insertRow(rowPosition2)
                    if len(values) >= 2:
                        self.table2.setItem(rowPosition2, 0, QTableWidgetItem(values[0]))
                        self.table2.setItem(rowPosition2, 1, QTableWidgetItem(values[1]))

    def visualize3D(self):
        # Очищаем сцену
        mlab.clf(figure=self.mlab_widget)

        # Замените путь на ваш STL-файл
        stl_file = "bolt.stl"

        # Загружаем STL-модель
        surface = mlab.pipeline.open(stl_file)

        # Визуализируем модель
        mlab.pipeline.surface(surface, color=(0.7, 0.7, 0.7))
        mlab.view(azimuth=0, elevation=90, distance='auto')

        # Показываем визуализацию
        mlab.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TwoTableApp()
    window.show()
    sys.exit(app.exec_())
