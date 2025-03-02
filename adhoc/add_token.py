from argparse import ArgumentParser
from dotenv import load_dotenv
from os import getenv

from utils.encryption_utils import EncryptionUtils
from utils.token_utils import TokenUtils 

def _add_token(user: str, name: str, value: str):
  if not load_dotenv():
    print("Failed to load enviromnent")
    return
  
  tokens_repo = getenv("TOKENS_REPO")
  secret_path = getenv("SECRET_PATH")
  if not tokens_repo or not secret_path:
    print("Failed to load environment variables")
    return
  
  if not TokenUtils.validate_token(user=user, value=value):
    print('Unable to validate token. Not attaching!')
    return

  secret = EncryptionUtils.get_secret(secret_path)

  try:
    TokenUtils.add_token(user=user, name=name, value=value, secret=secret, base_path=tokens_repo)
    print(f'Successfully attached token `{name}` to user `{user}`')
  except Exception as e:
    print(f'Failed to add token {user} - {name} - {value}: ', e)

if __name__ == '__main__':
  parser = ArgumentParser(description="Save Token")
  parser.add_argument(
      "-u", "--user", "--username", required=True, type=str, help="User"
  )
  parser.add_argument(
      "-n", "--name", "--tokenname", required=True, type=str, help="Token Name"
  )
  value = input('Enter the genrated token: ').strip()
  while not value:
    print("Token cannot be empty!")
    value = input('Enter the genrated token: ').strip()

  args = parser.parse_args()

  _add_token(user=args.user, name=args.name, value=value)