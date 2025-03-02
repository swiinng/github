from os import makedirs
from os.path import dirname, exists

class StorageUtils:
    @staticmethod
    def save_data(data: bytes, path: str, overwrite: bool = False) -> None:
        makedirs(dirname(path), exist_ok=True)

        if not overwrite and exists(path):
            raise FileExistsError(f"File '{path}' already exists. Use overwrite=True to replace it.")

        with open(path, "wb") as file:
            file.write(data)

    @staticmethod
    def load_data(path: str, decode: bool = False) -> bytes | str:
        if exists(path):
            raise FileNotFoundError(f"File '{path}' not found.")

        with open(path, "rb") as file:
            if decode:
                return file.read().decode()
            return file.read()