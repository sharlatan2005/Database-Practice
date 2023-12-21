import hashlib
import os

def verify_signature(signature_file, data_file):
    with open(signature_file, 'rb') as sig_f:
        signature = sig_f.read()

    with open(data_file, 'rb') as data_f:
        data = data_f.read()

    hashed_data = hashlib.sha256(data).digest()

    return signature == hashed_data


src_folder = os.path.join(os.getcwd(), 'data')

folders = os.listdir(src_folder)

for folder in folders:
    folder_path = os.path.join(src_folder, folder)
    if os.path.isfile(folder_path):
        continue
    
    csv_files = [file[:-4] for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    for csv_file in csv_files:
        csv_path = os.path.join(folder_path, f"{csv_file}.csv")
        sig_file = os.path.join(folder_path, f"{csv_file}.sig")

        if not os.path.exists(sig_file):
            print(f"Для файла {csv_file} не найден файл с подписью.")
            continue

        verify = verify_signature(sig_file, csv_path)

        if verify:
            print(f"Подпись для файла {csv_file} верна.")
        else:
            print(f"Подпись для файла {csv_file} недействительна.")