import hashlib
def hash_code(code):
    code1 = hashlib.blake2b(code.encode()).hexdigest()
    code2 = hashlib.blake2s(code1.encode()).hexdigest()
    return code2