# -*- coding: utf-8 -*import

import os
import sys
import time
import logging
import urllib.error

import requests
from pytube import exceptions
from pytube import YouTube
from pytube import Playlist
from option import Options
from help import Help


file_size = 0


def progress_function(chunk, file_handle, bytes_remaining):
    global file_size
    current = ((file_size - bytes_remaining)/file_size)
    percent = f"{round(current*100, 1)}"
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(f' ↳ |{status}| {percent}%\r')
    sys.stdout.flush()


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def change_directory(folder=None):
    if not folder:
        create_folder(Options.get_path())
        os.chdir(Options.get_path())
        return None
    create_folder(folder)
    os.chdir(folder)


def downloader(link, download_type):
    logging.info("[+] Function downloader was called...\n")
    global file_size
    try:
        yt = YouTube(link, on_progress_callback=progress_function)
        if "playlist" in link:
            download_playlist(link, download_type)
        elif download_type == "video":
            st = yt.streams.get_highest_resolution()
            file_size = st.filesize
            print("Загрузка...")
            st.download()
            print("\nЗагрузка завершена")
            time.sleep(1)
        elif download_type == "audio":
            st = yt.streams.get_audio_only()
            file_size = st.filesize
            st.download()
            print("\nЗагрузка завершена")
            time.sleep(1)
    except exceptions.RegexMatchError:
        print("Проверьте корректность ссылки и попытайтесь снова")
        logging.info(f"Link Except: link - {link}")

    except urllib.error.URLError:
        print("Не возможно соединиться с 'www.youtube.com' пожалуйста проверьте интернет соединение!")
        try_connect = check_connect()
        logging.info(f"URLError: connect - {try_connect}")


def download_playlist(link, download_type):
    logging.info("[+] Function download_playlist was called...\n")
    global file_size
    change_directory(Options.get_path() + "\\" + "playlist")
    pl = Playlist(link)
    if pl:
        pl_name = pl.title
        change_directory(pl_name)
        if download_type == "music":
            for count, url in enumerate(pl.video_urls):
                print(f"\nЗагрузка {count + 1} из {len(pl.videos)}\n")
                yt = YouTube(url, on_progress_callback=progress_function)
                st = yt.streams.get_audio_only()
                file_size = st.filesize
                st.download()
        else:
            for count, url in enumerate(pl.video_urls):
                print(f"\nЗагрузка {count + 1} из {len(pl.videos)}\n")
                yt = YouTube(url, on_progress_callback=progress_function)
                st = yt.streams.get_highest_resolution()
                file_size = st.filesize
                st.download()
    print("\nЗагрузка завершена")
    time.sleep(1)


def check_connect():
    try:
        requests.get("https://www.youtube.com")
    except requests.exceptions.ConnectionError:
        return False
    else:
        return True


def main():
    change_directory()
    lod_directory = os.path.join(Options.get_path(), "py_log.log")
    logging.basicConfig(filename=lod_directory, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    current_type = Options("v")

    while True:
        os.system("cls")
        if os.getcwd() != current_type.current_directory:
            change_directory(current_type.current_directory)
        print(f"Текущий тип скачиваемого файла '{current_type.download_type.upper()}'")
        print("Список доступных команд\n"
              "t - смена типа скачиваемого файла, h - руководство")
        link = input("Введите ссылку или название команды:> ").strip()

        if link == "t":
            new_type = ""
            while new_type not in ["a", "v"]:
                new_type = input("a - audio, v - video\n> ")
            current_type = Options(new_type)

        elif link == "h":
            Help.user_guide()

        elif link.startswith("https://www.youtube.com"):
            logging.info(link)
            if "playlist" in link:
                download_playlist(link, current_type.download_type)
            else:
                downloader(link, current_type.download_type)

        else:
            logging.info(f"[-] Unknown link - {link}\n")
            print("Не известная команда!")
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os.system("cls")
        print("Произошла не известная ошибка! Сведения об ошибке записаны в лог-файл. "
              "Пожалуйста отправьте лог-файл разработчику!")
        connect = check_connect()
        logging.critical(f"Critical Error: connect-{connect}", exc_info=True)
        input("Нажмите Enter для закрытия программы...")

