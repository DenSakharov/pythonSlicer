# Пример парсера для файлов SLC

def parse_slc_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    geological_data = []

    for line in lines:
        # Ваш код для анализа строк файла SLC и извлечения необходимых данных
        # Пример: извлечение кодов и символов геологических пород.
        geological_data.append(line.strip())  # Просто добавляет строки в список

    return geological_data

# Пример использования парсера
slc_file_path = 'Box_s.slc'
parsed_data = parse_slc_file(slc_file_path)

for data_entry in parsed_data:
    print(data_entry)
