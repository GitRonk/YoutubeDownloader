# -*- coding: utf-8 -*import

import os
from pytube import exceptions
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


def download_video(link):
    yt = verify_link(link, "v")
    if yt:
        st = yt.streams.get_highest_resolution()
        st.download()


def download_music(link):
    yt = verify_link(link, "m")
    if yt:
        st = yt.streams.get_audio_only()
        st.download()


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
    if download_type == "video":
        download_video(link)
    elif download_type == "music":
        download_music(link)


def user_guide():
    os.system("cls")
    print("""При запуске программы на рабочем столе автоматически создается папка YoutubeDownload
куда и будут скачиваться все файлы. Также для каждого типа файлов создается отдельная 
папка в директории YoutubeDownload.""")


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
            while new_type not in ["m", "v"]:
                new_type = input("m - music, v - video\n> ")
            current_type = Options(new_type)
        elif link == "h":
            user_guide()
        elif link.startswith("https://www.youtube.com"):
            if "playlist" in link:
                change_directory(Options.get_path() + "\\" + "playlist")
                download_playlist(link, current_type.download_type)
            else:
                download_base(link, current_type.download_type)
        else:
            print("Не известная команда!")


if __name__ == '__main__':
    main()
