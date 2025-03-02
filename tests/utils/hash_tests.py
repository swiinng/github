import pytest
from hashlib import md5
from utils.hash_utils import HashUtils

@pytest.mark.parametrize("data, expected_hex", [
    ("hello", md5(b"hello").hexdigest()),
    (b"hello", md5(b"hello").hexdigest()),
    ("", md5(b"").hexdigest()),
    (b"", md5(b"").hexdigest()),
])
def test_hash_md5_basic(data, expected_hex):
    assert HashUtils.hash_md5(data) == expected_hex

def test_hash_md5_decode_false():
    raw_hash = HashUtils.hash_md5("hello", decode=False)
    assert isinstance(raw_hash, bytes)
    assert raw_hash == md5(b"hello").digest()
