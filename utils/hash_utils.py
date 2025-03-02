from hashlib import md5

class HashUtils:
    
  @staticmethod
  def hash_md5(data: bytes | str, decode: bool = True) -> bytes | str:
    if isinstance(data, str):
      data = data.encode()
    hashed = md5(data).digest()
    return hashed.hex() if decode else hashed