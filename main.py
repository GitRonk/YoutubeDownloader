# -*- coding: utf-8 -*import

import os
import requests
from pytube import exceptions
from pytube import YouTube
from pytube import Playlist
from option import Options
from help import Help


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


def verify_link(link, link_type):
    try:
        if link_type in ["v", "m"]:
            YouTube(link)
        else:
            Playlist(link)
    except exceptions.RegexMatchError:
        print("Проверьте корректность ссылки и попытайтесь снова")
        return None
    else:
        if link_type in ["v", "m"]:
            return YouTube(link)
        return Playlist(link)


def download_playlist(link, download_type):
    pl = verify_link(link, "p")
    if pl:
        pl_name = pl.title
        change_directory(pl_name)
        if download_type == "music":
            for count, video in enumerate(pl.videos):
                os.system("cls")
                print(f"Загрузка {count + 1} из {len(pl.videos)}")
                st = video.streams.get_audio_only()
                st.download()
        else:
            for count, video in enumerate(pl.videos):
                os.system("cls")
                print(f"Загрузка {count + 1} из {len(pl.videos)}")
                st = video.streams.get_highest_resolution()
                st.download()


def download_base(link, download_type):
    yt = verify_link(link, "v")
    if yt:
        print("Загрузка...")
        if download_type == "video":
            st = yt.streams.get_highest_resolution()
            st.download()
        else:
            st = yt.streams.get_audio_only()
            st.download()


def check_connect():
    try:
        requests.get("https://www.youtube.com")
    except requests.exceptions.ConnectionError:
        os.system("cls")
        print("Не возможно подключиться к 'youtube.com' "
              "пожалуйста проверьте интернет соединение и повторите попытку!")
        input("Нажмите Enter чтобы продолжить")
        return False
    else:
        return True


def main():
    change_directory()
    current_type = Options("v")

    while True:
        os.system("cls")
        if os.getcwd() != current_type.current_directory:
            change_directory(current_type.current_directory)
        print(f"Текущий тип скачиваемого файла '{current_type.download_type.upper()}'")
        print("Список доступных команд\n"
              "t - смена типа скачиваемого файла, h - руководство")
        link = input("Введите ссылку или название команды:> ")

        if link == "t":
            new_type = ""
            while new_type not in ["a", "v"]:
                new_type = input("a - audio, v - video\n> ")
            current_type = Options(new_type)
        elif link == "h":
            Help.user_guide()
        elif link.startswith("https://www.youtube.com"):
            connect = check_connect()
            if not connect:
                continue
            if "playlist" in link:
                change_directory(Options.get_path() + "\\" + "playlist")
                download_playlist(link, current_type.download_type)
            else:
                download_base(link, current_type.download_type)
        else:
            print("Не известная команда!")


if __name__ == '__main__':
    main()
