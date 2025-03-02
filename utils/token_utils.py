from utils.encryption_utils import EncryptionUtils
from utils.hash_utils import HashUtils

from utils.storage_utils import StorageUtils

class TokenUtils:

  @staticmethod
  def _get_token_path(user: str, name: str, base_path: str) -> str:
     return f'{base_path}/{user}/{HashUtils.hash_md5(name)}'

  @staticmethod
  def save_token(user: str, name: str, value: str, secret: bytes | str, base_path: str) -> None:
    encrypted_token = EncryptionUtils.encrypt_data(data=value, secret=secret)
    token_path = TokenUtils._get_token_path(user=user, name=name, base_path=base_path)
    StorageUtils.save_data(data=encrypted_token, path=token_path, overwrite=True)
  
  @staticmethod
  def load_token(user: str, name: str, secret: bytes | str, base_path: str) -> str:
    token_path = TokenUtils._get_token_path(user=user, name=name, base_path=base_path)
    encrypted_token = StorageUtils.load_data(path=token_path)
    return EncryptionUtils.decrypt_data(data=encrypted_token, secret=secret)
  