from github import Auth
from token_utils import TokenUtils

class AuthUtils:

  @staticmethod
  def with_token(user: str, name: str) -> Auth:
    return Auth.Token(token=TokenUtils.load_token(user=user, name=name))