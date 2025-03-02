from github import Auth
from github import Github

from utils.encryption_utils import EncryptionUtils
from utils.hash_utils import HashUtils
from utils.storage_utils import StorageUtils

class TokenUtils:

  @staticmethod
  def _get_token_path(user: str, name: str, base_path: str) -> str:
     return f'{base_path}/{user}/{HashUtils.hash_md5(name)}'

  @staticmethod
  def add_token(user: str, name: str, value: str, secret: bytes | str, base_path: str) -> None:
    encrypted_token = EncryptionUtils.encrypt_data(data=value, secret=secret)
    token_path = TokenUtils._get_token_path(user=user, name=name, base_path=base_path)
    StorageUtils.save_data(data=encrypted_token, path=token_path, overwrite=True)

  @staticmethod
  def remove_token(user: str, name: str, base_path: str) -> None:
    token_path = TokenUtils._get_token_path(user=user, name=name, base_path=base_path)
    StorageUtils.delete_file(path=token_path)
  
  @staticmethod
  def load_token(user: str, name: str, secret: bytes | str, base_path: str) -> str:
    token_path = TokenUtils._get_token_path(user=user, name=name, base_path=base_path)
    encrypted_token = StorageUtils.load_data(path=token_path)
    return EncryptionUtils.decrypt_data(data=encrypted_token, secret=secret)
  
  @staticmethod
  def validate_token(user: str, value: str) -> bool:
    try:
      auth_user = Github(auth=Auth.Token(token=value)).get_user()
      if not auth_user.name == user:
        print(f'GitHub Accounts do not match: Token account `{auth_user.name}` v. User `{user}`')
    except Exception as e:
      print('Unable to validate token: ', e)
      return False
    return True