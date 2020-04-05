# Скрипт перезапуста точек доступа Ubiquiti, подключенных к UnifiController

Для использования данного скрипта необходимо:

  - Клонировать репозиторий ``` https://github.com/maximishchenko/unifi_devices.git ``` 
  - Перейти в каталог скрипта ``` cd /path/to/script ```
  - Скопировать файл config/config.ini.sample в config/config.ini ``` cp config/config.ini.sample config/config.ini ```
  - указать в файле config/config.ini актуальные данные (адрес unifi контроллер, имя пользователя, пароль)
  - запустить скрпит ``` python3 /path/to/main.py ```