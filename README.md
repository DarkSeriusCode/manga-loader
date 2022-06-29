# Manga Loader
Маленькая утилита, позволяющая скачивать мангу с таких сайтов как: **https://readmanga.live**, **https://mintmanga.live**, **https://readmanga.io**.

## Установка
Для работы нужен **Python3.8** или выше.

### Linux
1. `git clone https://github.com/DarkSeriusCode/manga-loader`
2. `python3.8 -m pip install -r requirements.txt`
3. `python3.8 main.py -h`


## Использование
Запуск: `python3 main.py URL [-s] [-e] [--pdf] [--pdf-only] [--vol-start] [--vol-end]`

`URL` - ссылка на мангу

`-s` - номер главы с которой будет начинаться скачивание

`-e` - номер главы на которой будет заканчиваться скачивание

`--info-only` - выводит информацию о манге без её скачивания

`--pdf` - собрать мангу в `.pdf` после скачивания (собирает каждый том в отдельный файл)

`--pdf-only` - собрать мангу без скачивания

`--vol-start` - номер тома с которого начнётся сборка

`--vol-end` - номер тома на котором сборка закончится
