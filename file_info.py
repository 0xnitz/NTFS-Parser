class File:
    def __init__(self, name, data):
        self._name = name
        self._data = data

    def get_name(self):
        return self._name

    def get_data(self):
        return self._data
