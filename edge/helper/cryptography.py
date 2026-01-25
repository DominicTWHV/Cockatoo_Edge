import hashlib
import argon2

from argon2 import PasswordHasher

ph = PasswordHasher()

class SHA256:

    @staticmethod
    async def generate(input_str: str) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_str.encode('utf-8'))
        return sha256_hash.hexdigest()
    
    @staticmethod
    async def verify(input_str: str, hash_str: str) -> bool:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_str.encode('utf-8'))
        return sha256_hash.hexdigest() == hash_str #== True if matches, False otherwise
    
class Argon2ID:

    @staticmethod
    async def generate(input_str: str) -> str:
        return ph.hash(input_str)
    
    @staticmethod
    async def verify(input_str: str, hash_str: str) -> bool:
        try:
            ph.verify(hash_str, input_str)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False