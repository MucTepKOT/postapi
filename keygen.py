import uuid
from passlib.hash import pbkdf2_sha256

def hash(text):
    return pbkdf2_sha256.hash(text)
    
def verify_hash(text, hashed_text):
    return pbkdf2_sha256.verify(text, hashed_text)
