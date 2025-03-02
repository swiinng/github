from cryptography.fernet import Fernet

class EncryptionUtils:

  @staticmethod
  def get_secret(path: str) -> bytes:
     with open(path, "rb") as key_file:
        return key_file.read()

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