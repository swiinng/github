import pytest
from cryptography.fernet import Fernet
from unittest.mock import MagicMock

from utils.encryption_utils import EncryptionUtils
from utils.storage_utils import StorageUtils

# mock StorageUtils
@pytest.fixture
def mock_storage(mocker):
    mock_storage = mocker.patch.object(StorageUtils, 'load_data')
    mocker.patch.object(StorageUtils, 'save_data')
    return mock_storage

def test_generate_secret(mock_storage):
    mock_storage.save_data.return_value = None

    secret_path = "test_secret.key"

    secret = EncryptionUtils.generate_secret(secret_path)
    
    assert isinstance(secret, bytes)
    assert len(secret) == 44  # fernet keys 44 chars in base64

    StorageUtils.save_data.assert_called_once_with(data=secret, path=secret_path, overwrite=True)

def test_get_secret(mock_storage):
    secret = Fernet.generate_key()
    mock_storage.return_value = secret

    secret_path = "test_secret.key"

    loaded_secret = EncryptionUtils.get_secret(secret_path)

    assert loaded_secret == secret
    StorageUtils.load_data.assert_called_once_with(path=secret_path)

def test_encrypt_data():
    secret = Fernet.generate_key()
    data = "Hello World"

    encrypted_data = EncryptionUtils.encrypt_data(data, secret)

    assert isinstance(encrypted_data, bytes)
    assert encrypted_data != data.encode()

def test_decrypt_data():
    secret = Fernet.generate_key()
    data = "Hello World"

    encrypted_data = EncryptionUtils.encrypt_data(data, secret)
    decrypted_data = EncryptionUtils.decrypt_data(encrypted_data, secret, decode=True)

    assert decrypted_data == data

def test_decrypt_data_invalid_secret():
    secret = Fernet.generate_key()
    invalid_secret = Fernet.generate_key()

    data = "Hello World"
    encrypted_data = EncryptionUtils.encrypt_data(data, secret)

    with pytest.raises(Exception):
        EncryptionUtils.decrypt_data(encrypted_data, invalid_secret)

def test_empty_data():
    secret = Fernet.generate_key()

    encrypted_data = EncryptionUtils.encrypt_data("", secret)
    decrypted_data = EncryptionUtils.decrypt_data(encrypted_data, secret)

    assert decrypted_data == ""

def test_get_secret_file_not_found():
    mock_storage = MagicMock()
    mock_storage.load_data.side_effect = FileNotFoundError
    
    secret_path = "non_existent_secret.key"
    
    with pytest.raises(FileNotFoundError):
        EncryptionUtils.get_secret(secret_path)
