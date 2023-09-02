import getpass


class Options:
    _current_user = getpass.getuser()
    _default_path = "C:\\Users\\" + _current_user + "\\Desktop\\YouTube Download"

    @classmethod
    def get_path(cls):
        return cls._default_path

    def __init__(self, download_type):
        self.cuts = {"v": "video",
                     "m": "music",
                     "p": "playlist"}
        self._download_type = self.cuts[download_type]
        self._current_directory = __class__.get_path() + "\\" + self.cuts[download_type]

    @property
    def current_directory(self):
        return self._current_directory

    @property
    def download_type(self):
        return self._download_type

    @download_type.setter
    def download_type(self, new_type):
        self._download_type = self.cuts[new_type]
        self._current_directory = __class__.get_path() + "\\" + self.cuts[new_type]
