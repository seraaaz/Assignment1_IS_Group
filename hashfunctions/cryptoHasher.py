from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import bcrypt
from os import path
import os

class Hasher():

    def __init__(self) -> None:
        self.nonce = b"\x00" * 16

    def pad_block(self, data):
        if(len(data) % 8 != 0):
            data += b"\x00" * (8 - len(data) % 8)
        return data
    
    def get128BitKey(self, key):
        if len(key) < 16:
            key = key + '0' * (16 - len(key))
        elif len(key) > 16:
            key = key[-16:]
        return key.encode('utf-8')

    def deleteFile(self, fpath, ext):
        old_path = path.splitext(fpath)[0] + ext
        print("Old Path: ", old_path)
        if path.exists(old_path):
            print("Deleting file: ", old_path)
            os.remove(old_path)
        else:
            print("The file does not exist")
    
    def encryptFile(self, fpath, algo, key = '1234567890123456'):
        # get file directiory without the extension
        key = self.get128BitKey(key)
        encrypted_path = path.splitext(fpath)[0] + ".enc"
        print("Encrypted Path: ", encrypted_path)
        with open(fpath, "rb") as f:
            data = f.read()
        if(algo == "DES"):
            encrypted = self.DES_Encrypt(key, data)
            self.saveFile(encrypted_path, encrypted)
            return encrypted_path
        elif(algo == "AES"):
            encrypted = self.AES_Encrypt(key, data)
            self.saveFile(encrypted_path, encrypted)
            return encrypted_path
        elif(algo == "ARC4"):
            encrypted = self.ARC4_Encrypt(key, data)
            self.saveFile(encrypted_path, encrypted)
            return encrypted_path
        else:
            return None
    
    def decryptFile(self, fpath, algo,  key = '1234567890123456'):
        key = self.get128BitKey(key)

        decrypted_path = path.splitext(fpath)[0] + "Dec.png"
        with open(fpath, "rb") as f:
            data = f.read()
        if(algo == "DES"):
            decryped = self.DES_Decrypt(key, data)
            # self.saveFile(decrypted_path, decryped)
            return decryped, decrypted_path
        elif(algo == "AES"):
            decryped = self.AES_Decrypt(key, data)
            # self.saveFile(decrypted_path, decryped)
            return decryped, decrypted_path
        elif(algo == "ARC4"):
            decryped = self.ARC4_Decrypt(key, data)
            # self.saveFile(decrypted_path, decryped)
            return decryped, decrypted_path
        else:
            return None
        
    def saveFile(self, path, data):
        with open(path, "wb") as f:
            f.write(data)

    def Hash_Password(self, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(hashed)
        return hashed
    
    def Check_Password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)


    def DES_Encrypt(self, key, data):
        nonce = b"\x00" * 8
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(nonce))
        encryptor = cipher.encryptor()
        return encryptor.update(self.pad_block(data)) + encryptor.finalize()

    def DES_Decrypt(self, key, data):
        nonce = b"\x00" * 8
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(nonce))
        decryptor = cipher.decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data.rstrip(b"\x00") 

    def AES_Encrypt(self, key, data):
        cipher = Cipher(algorithms.AES(key), modes.CTR(self.nonce))
        encryptor = cipher.encryptor()
        return encryptor.update(self. pad_block(data)) + encryptor.finalize()

    def AES_Decrypt(self, key, data):
        cipher = Cipher(algorithms.AES(key), modes.CTR(self.nonce))
        decryptor = cipher.decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data.rstrip(b"\x00")

    def ARC4_Encrypt(self, key, data):
        cipher = Cipher(algorithms.ARC4(key), None)
        encryptor = cipher.encryptor()
        return encryptor.update(self.pad_block(data)) + encryptor.finalize()

    def ARC4_Decrypt(self, key, data):
        cipher = Cipher(algorithms.ARC4(key), None)
        decryptor = cipher.decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data.rstrip(b"\x00")

# hasher = Hasher()
# hasher.Hash_Password("Hello World")

# print("DES")
# encrypted = hasher.DES_Encrypt(b"1234567890123456", b"Hello World")
# print(encrypted)
# print(hasher.DES_Decrypt(b"1234567890123456", encrypted))

# print("AES")
# encrypted = hasher.AES_Encrypt(b"1234567890123456", b"Hello World")
# print(encrypted)
# print(hasher.AES_Decrypt(b"1234567890123456", encrypted))

# print("ARC4")
# encrypted = hasher.ARC4_Encrypt(b"1234567890123456", b"Hello World")
# print(encrypted)
# print(hasher.ARC4_Decrypt(b"1234567890123456", encrypted))