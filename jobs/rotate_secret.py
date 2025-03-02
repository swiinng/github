from dotenv import load_dotenv
from os import getenv

from utils.encryption_utils import EncryptionUtils

def rotate_secret():
  if not load_dotenv():
    print("Failed to load enviromnent")
    return
  
  secret_path = getenv("SECRET_PATH")
  if not secret_path:
    print("Failed to get secret path")

  EncryptionUtils.generate_secret(secret_path)
  
if __name__ == '__main__':
  rotate_secret()