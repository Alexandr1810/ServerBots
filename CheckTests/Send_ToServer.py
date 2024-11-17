import os
import ftplib
import re

# Настройки FTP
FTP_HOST = 'speedinet-base.ru'
FTP_USER = 'u2529016'
FTP_PASS = 's36SFlBvLh0LwCL4'
LOCAL_DIRECTORY = 'Itogs'
REMOTE_BASE_DIRECTORY = '/www/speedinet-base.ru/DevPanel/Tests/Itogs/'

# Устанавливаем соединение с FTP-сервером
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

# Метод для создания папки на сервере
def create_remote_directory(directory):
    try:
        ftp.mkd(directory)
    except ftplib.error_perm as e:
        # Код 550 означает, что папка уже существует
        if not e.args[0].startswith('550'):
            raise  # Не игнорировать другие ошибки

# Перебор файлов в локальной папке Itogs
for filename in os.listdir(LOCAL_DIRECTORY):
    if filename.endswith('.html'):
        # Извлекаем ФИО агента из имени файла (последние два слова перед .html)
        match = re.search(r'(\S+\s+\S+)\.html$', filename)
        if match:
            fio = match.group(1).strip()
            remote_directory = os.path.join(REMOTE_BASE_DIRECTORY, fio)

            # Создаем папку на сервере, если она не существует
            create_remote_directory(remote_directory)

            # Смена текущей рабочей директории на удаленную папку
            ftp.cwd(remote_directory)

            # Загружаем файл в соответствующую папку
            local_file_path = os.path.join(LOCAL_DIRECTORY, filename)

            with open(local_file_path, 'rb') as file:
                ftp.storbinary(f'STOR {filename}', file)  # Теперь сохраняем файл по его оригинальному имени

# Закрываем соединение с FTP
ftp.quit()