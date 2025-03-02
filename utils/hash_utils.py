from hashlib import md5

class HashUtils:

  @staticmethod
  def _prepare_data(data, *args) -> bytes | str:
    if isinstance(data, str):
      data = data.encode()

    for arg in args:
        if isinstance(arg, str):
            arg = arg.encode()
        data += arg
    
    return data
    
  @staticmethod
  def hash_md5(data, decode: bool = True, *args) -> bytes | str:
    hashed = md5(HashUtils._prepare_data(data, args)).digest()
    return hashed.hex() if decode else hashed