import subprocess

# Замените на путь к исполняемому файлу Slic3r
slic3r_executable = "C:\SLIC3R\Slic3r.exe"

# Замените на путь к вашему STL-файлу
input_stl = "bolt.stl"

# Замените на путь, куда вы хотите сохранить G-code
output_gcode = "output.gcode"

# Задайте параметры командной строки для Slic3r
command = [
    slic3r_executable,
    input_stl,
    "--output", output_gcode,
    # Другие параметры, если необходимо
]

# Вызов команды Slic3r
subprocess.run(command)

print("Готово. G-code сохранен в", output_gcode)
