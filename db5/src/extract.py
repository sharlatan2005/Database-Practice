import zipfile
import os

src_folder = os.path.join(os.getcwd(), 'src/HkK7HD8QJm4SM4dTf4Q1pKVZ3dUAEhxszTnLkaXooVNN_2023-09-08_0000-0100_2_1')
output_folder = os.path.join(os.getcwd(), 'data')

files = os.listdir(src_folder)
for file in files:
    if file.endswith('.zip'):
        zip_path = os.path.join(src_folder, file)
        
        # Извлекаем название даты из названия архива
        directory_name = file.split('_')
        directoty_date = directory_name[1]
        directory_time = directory_name[2].split('.')[0]
        date = directoty_date + "_" + directory_time
        
        # Путь для извлечения данных
        extraction_path = os.path.join(output_folder, date)
        
        # Создаем папку с именем даты, если она не существует
        if not os.path.exists(extraction_path):
            os.makedirs(extraction_path)
        
        # Извлекаем содержимое архива в папку с соответствующей датой
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_path)

            # Получаем список извлеченных файлов
            extracted_files = zip_ref.namelist()
            
