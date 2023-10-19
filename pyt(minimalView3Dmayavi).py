import mayavi.mlab as mlab

# Создайте новое окно
mlab.figure()

# Загрузите STL-файл
your_model = mlab.pipeline.open('cyl.stl')

# Отобразите модель
mlab.pipeline.surface(your_model)

# Настройте вид
mlab.view(azimuth=0, elevation=90, distance=50)

# Отобразите окно
mlab.show()
