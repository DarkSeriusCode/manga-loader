# Manga Loader
Скрипт, позволяющий скачивать мангу с таких сайтов как: **https://readmanga.live**, **https://mintmanga.live**, **https://readmanga.io**.

## Установка
Для работы скрипта нужен **Python3.8** или выше.
Для установки пакетов в терминале:
`pip install requirements.txt`


## Использование
Запуск: `python3 main.py URL [-s] [-e] [--pdf] [--pdf-only] [--vol-start] [--vol-end]`

`URL` - ссылка на мангу
`-s` - номер главы с которой будет начинаться скачивание
`-e` - номер главы на которой будет заканчиваться скачивание
`--pdf` - собрать мангу в `.pdf` после скачивания (собирает каждый том в отдельный файл)
`--pdf-only` - собрать мангу без скачивания
`--vol-start` - номер тома с которого начнётся сборка
`--vol-end` - номер тома на котором сборка закончится