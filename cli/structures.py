import yaml, os


class Job(dict):
    path: str
    data: dict

    def __init__(self, path: str, data=None) -> None:
        super().__init__()
        self.path = path
        self.data = data
        if not data:
            with open(path, 'r') as f:
                self.data = yaml.full_load(f)

    def write(self):
        with open(self.path, 'w') as f:
            yaml.dump(self.data, f)

    def exists(self):
        return os.path.exists(self.path)

    def get(self, key: str, default):
        return self.data.get(key, default)

    def __delitem__(self, key):
        del self.data[key]

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
