from hashfunctions import cryptoHasher

hasher = cryptoHasher.Hasher()

path = "/Users/selomitazhafiirah/Assignment1_PrivateDatabse_IS_Group-main/Assignment1_PrivateDatabse_IS_Group-main/media/id_cards/screen-12.11.1729.08.2020.png"

photo = hasher.encryptFile(path, "DES", key=r"$2b$12$ae8HjRlcTMyxHn8kzpqZ0.y88L5P/IXSpdMQlsL5K5Zo/me7TO1FC")

with open("/Users/selomitazhafiirah/Assignment1_PrivateDatabse_IS_Group-main/Assignment1_PrivateDatabse_IS_Group-main/media/id_cards/screen-12.11.1729.08.2020.enc", "wb") as f:
    f.write(photo.encode())

print (len(photo))


decrypted = hasher.decryptFile("/Users/selomitazhafiirah/Assignment1_PrivateDatabse_IS_Group-main/Assignment1_PrivateDatabse_IS_Group-main/media/id_cards/screen-12.11.1729.08.2020.enc", "DES", key=r"$2b$12$ae8HjRlcTMyxHn8kzpqZ0.y88L5P/IXSpdMQlsL5K5Zo/me7TO1FC")

with open("/Users/selomitazhafiirah/Assignment1_PrivateDatabse_IS_Group-main/Assignment1_PrivateDatabse_IS_Group-main/media/id_cards/screen-12.11.1729.08.2020_decrypted.png", "wb") as f:
    f.write(decrypted.encode())
