from cryptography.fernet import Fernet

key = b'yY_AVjn2gADtFOyMFW_YS9NiKAa9Kb_vIU4DwT4x04Y='
cipher_suite = Fernet(key)

def pass_encrypt(password):
    bytes_password = str_to_byte(password)
    ciphered_text = cipher_suite.encrypt(bytes_password)
    return ciphered_text

def pass_dcrypt(enpass):
    unciphered_text = (cipher_suite.decrypt(enpass))
    return byte_to_str(unciphered_text)

def str_to_byte(data):
    return  bytes(data, 'utf-8')

def byte_to_str(data):
    return  str(data, 'utf-8')
