from cryptography.fernet import Fernet

from utils.storage_utils import StorageUtils

class EncryptionUtils:

  @staticmethod
  def get_secret(path: str) -> bytes:
    return StorageUtils.load_data(path=path)
     
  @staticmethod
  def generate_secret(path: str) -> bytes:
    secret = Fernet.generate_key()
    StorageUtils.save_data(data=secret, path=path, overwrite=True)
    return secret

  @staticmethod
  def encrypt_data(data, secret: bytes | str) -> bytes:
      fernet = Fernet(secret)
      return fernet.encrypt(data.encode())

  @staticmethod
  def decrypt_data(data, secret: bytes | str, decode: bool = True) -> bytes | str:
    fernet = Fernet(secret)
    decrypted_data = fernet.decrypt(data)

    if decode:
       return decrypted_data.decode()
    return decrypted_data