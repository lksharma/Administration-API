import unittest
from utils.encryption import encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):
    
    def setUp(self):
        self.encryption_key = 'p2iW1rL0WwjbkBFv6Er67Q=='
        self.plaintext_payload = 'Some test data'
        self.encryption_mode_ecb = 'AES + ECB'
        self.encryption_mode_cbc = 'AES + CBC'

    def test_encrypt_decrypt_ecb(self):
        encrypted_payload = encrypt_data(self.encryption_mode_ecb, self.encryption_key, self.plaintext_payload)
        decrypted_payload = decrypt_data(self.encryption_mode_ecb, self.encryption_key, encrypted_payload)
        self.assertEqual(self.plaintext_payload, decrypted_payload)

    def test_encrypt_decrypt_cbc(self):
        encrypted_payload = encrypt_data(self.encryption_mode_cbc, self.encryption_key, self.plaintext_payload)
        decrypted_payload = decrypt_data(self.encryption_mode_cbc, self.encryption_key, encrypted_payload)
        self.assertEqual(self.plaintext_payload, decrypted_payload)

    def test_decrypt_invalid_data(self):
        with self.assertRaises(ValueError):
            decrypt_data(self.encryption_mode_ecb, self.encryption_key, 'invalid_payload')

if __name__ == '__main__':
    unittest.main()
