class File:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.content = content

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.content)
