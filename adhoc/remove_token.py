from argparse import ArgumentParser
from dotenv import load_dotenv
from os import getenv

from utils.token_utils import TokenUtils 

def _remove_token(user: str, name: str):
  if not load_dotenv():
    print("Failed to load enviromnent")
    return
  
  tokens_repo = getenv("TOKENS_REPO")
  secret_path = getenv("SECRET_PATH")
  if not tokens_repo or not secret_path:
    print("Failed to load environment variables")
    return

  try:
    TokenUtils.remove_token(user=user, name=name, base_path=tokens_repo)
  except Exception as e:
    print(f'Failed to remove token {user} - {name}: ', e)

if __name__ == '__main__':
  parser = ArgumentParser(description="Save Token")
  parser.add_argument(
      "-u", "--user", "--username", required=True, type=str, help="User"
  )
  parser.add_argument(
      "-n", "--name", "--tokenname", required=True, type=str, help="Token Name"
  )

  args = parser.parse_args()

  _remove_token(user=args.user, name=args.name)