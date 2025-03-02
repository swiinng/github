from dotenv import load_dotenv
from os import getenv
from github import Auth

from utils.encryption_utils import EncryptionUtils
from utils.token_utils import TokenUtils


class AuthUtils:

  @staticmethod
  def with_token(user: str, name: str) -> Auth:
    load_dotenv()
    tokens_repo = getenv("TOKENS_REPO")
    secret_path = getenv("SECRET_PATH")

    secret = EncryptionUtils.get_secret(secret_path)

    return Auth.Token(token=TokenUtils.load_token(user=user, name=name, secret=secret, base_path=tokens_repo))