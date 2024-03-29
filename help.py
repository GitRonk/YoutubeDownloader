import os


class Help:
    @staticmethod
    def user_guide():
        os.system("cls")
        print("""При запуске программы на рабочем столе автоматически создается папка YoutubeDownload
куда и будут скачиваться все файлы. Также для каждого типа файлов создается отдельная 
папка в директории YoutubeDownload.
Тип скачиваемого файла определяет что будет загружаться видео - VIDEO или аудио - AUDIO
Например если хотите загрузить плейлист с музыкой, то установите тип скачиваемого файла на AUDIO
и скопируйте ссылку на плейлист в окно программы. То же самое и для отдельных файлов просто
устанавливаете нужный вам тип и предоставляете программе ссылку.
Программа не может получить доступ к закрытым плейлистам, поэтому перед загрузкой сделайте
плейлист доступным по ссылке или доступным для всех.
К сожалению на данный момент доступно только качество видео 720р""")
        input("\nНажмите Enter чтобы продолжить...")