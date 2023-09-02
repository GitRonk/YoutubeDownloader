# -*- coding: utf-8 -*import

import os
from pytube import YouTube
from pytube import Playlist
from option import Options


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
            yt = YouTube(link)
            return yt
        pl = Playlist(link)
        return pl
    except:
        print()


def download_video(link):
    yt = verify_link(link, "v")
    st = yt.streams.get_highest_resolution()
    st.download()


def download_music(link):
    yt = verify_link(link, "m")
    st = yt.streams.get_audio_only()
    st.download()


def download_playlist(link):
    pl = verify_link(link, "p")
    pl_name = pl.title
    change_directory(pl_name)
    pl_type = input("Если хотите скачать только аудио введите 'm'\n"
                    "иначе просто нажмите Enter: ")
    if pl_type.lower() == "m":
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
    if download_type == "video":
        download_video(link)
    elif download_type == "music":
        download_music(link)
    else:
        download_playlist(link)


def user_guide():
    os.system("cls")
    print()


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
            while new_type not in ["m", "v", "p"]:
                new_type = input("m - music, v - video, p - playlist\n> ")
            current_type = Options(new_type)
        elif link == "h":
            pass
        elif link.startswith("https://www.youtube.com"):
            download_base(link, current_type.download_type)


if __name__ == '__main__':
    main()
