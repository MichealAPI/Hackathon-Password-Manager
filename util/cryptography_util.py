from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate a random key for encryption and decryption
    :return: A random, byte-encoded, key
    """
    return Fernet.generate_key()
