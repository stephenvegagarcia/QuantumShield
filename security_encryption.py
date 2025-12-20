"""
QuantumShield - Advanced AES-256 Encryption Module
Provides military-grade encryption for data at rest and in transit
"""

import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AESEncryption:
    """AES-256 encryption handler with PBKDF2 key derivation"""
    
    def __init__(self, master_key=None):
        """Initialize with master key or generate one"""
        if master_key is None:
            # Generate secure random master key
            master_key = os.environ.get('QUANTUM_MASTER_KEY', base64.b64encode(os.urandom(32)).decode())
        
        self.master_key = master_key.encode() if isinstance(master_key, str) else master_key
    
    def derive_key(self, salt):
        """Derive encryption key using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.master_key)
    
    def encrypt(self, plaintext):
        """
        Encrypt data using AES-256-CBC
        Returns: base64-encoded encrypted data with IV and salt
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # Generate random salt and IV
        salt = os.urandom(16)
        iv = os.urandom(16)
        
        # Derive encryption key
        key = self.derive_key(salt)
        
        # Pad plaintext to block size
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine salt + IV + ciphertext and encode
        encrypted_data = salt + iv + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, encrypted_data):
        """
        Decrypt AES-256-CBC encrypted data
        Returns: decrypted plaintext
        """
        # Decode from base64
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # Extract components
        salt = encrypted_bytes[:16]
        iv = encrypted_bytes[16:32]
        ciphertext = encrypted_bytes[32:]
        
        # Derive decryption key
        key = self.derive_key(salt)
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')
    
    def encrypt_dict(self, data):
        """Encrypt dictionary values"""
        encrypted = {}
        for key, value in data.items():
            if value is not None:
                encrypted[key] = self.encrypt(str(value))
            else:
                encrypted[key] = None
        return encrypted
    
    def decrypt_dict(self, encrypted_data):
        """Decrypt dictionary values"""
        decrypted = {}
        for key, value in encrypted_data.items():
            if value is not None:
                try:
                    decrypted[key] = self.decrypt(value)
                except:
                    decrypted[key] = value  # Return as-is if decryption fails
            else:
                decrypted[key] = None
        return decrypted


def generate_encryption_key():
    """Generate a new secure encryption key"""
    return base64.b64encode(os.urandom(32)).decode()


def test_encryption():
    """Test encryption functionality"""
    aes = AESEncryption()
    
    # Test string encryption
    test_data = "Sensitive security data: password123"
    encrypted = aes.encrypt(test_data)
    decrypted = aes.decrypt(encrypted)
    
    print(f"✅ AES-256 Encryption Test")
    print(f"Original:  {test_data}")
    print(f"Encrypted: {encrypted[:50]}...")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")
    
    # Test dict encryption
    test_dict = {
        "username": "admin",
        "password": "super_secret",
        "api_key": "sk-1234567890"
    }
    encrypted_dict = aes.encrypt_dict(test_dict)
    decrypted_dict = aes.decrypt_dict(encrypted_dict)
    
    print(f"\n✅ Dictionary Encryption Test")
    print(f"Original:  {test_dict}")
    print(f"Encrypted: {list(encrypted_dict.keys())}")
    print(f"Decrypted: {decrypted_dict}")
    print(f"Match: {test_dict == decrypted_dict}")


if __name__ == "__main__":
    test_encryption()
