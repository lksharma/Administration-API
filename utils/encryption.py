import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_data(encryption_mode, encryption_key, plaintext_payload):
    """
    Encrypts the given plaintext payload using the specified encryption mode and key.

    Args:
        encryption_mode (str): The encryption mode to use ('AES + ECB' or 'AES + CBC').
        encryption_key (str): The base64-encoded encryption key.
        plaintext_payload (str): The plaintext data to be encrypted.

    Returns:
        str: The base64-encoded encrypted data.

    Raises:
        ValueError: If an unsupported encryption mode is specified.
    """
    key = base64.b64decode(encryption_key)
    plaintext_data = plaintext_payload.encode('utf-8')

    if encryption_mode == 'AES + ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_data = base64.b64encode(cipher.encrypt(pad(plaintext_data, AES.block_size)))
    elif encryption_mode == 'AES + CBC':
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted_data = base64.b64encode(iv + cipher.encrypt(pad(plaintext_data, AES.block_size)))
    else:
        raise ValueError("Unsupported encryption mode")

    return encrypted_data.decode('utf-8')

def decrypt_data(encryption_mode, encryption_key, encrypted_payload):
    """
    Decrypts the given encrypted payload using the specified encryption mode and key.

    Args:
        encryption_mode (str): The encryption mode to use ('AES + ECB' or 'AES + CBC').
        encryption_key (str): The base64-encoded encryption key.
        encrypted_payload (str): The base64-encoded encrypted data to be decrypted.

    Returns:
        str: The decrypted plaintext data.

    Raises:
        ValueError: If an unsupported encryption mode is specified.
    """
    key = base64.b64decode(encryption_key)
    encrypted_data = base64.b64decode(encrypted_payload)

    if encryption_mode == 'AES + ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
    elif encryption_mode == 'AES + CBC':
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size).decode('utf-8')
    else:
        raise ValueError("Unsupported encryption mode")

    return decrypted_data
