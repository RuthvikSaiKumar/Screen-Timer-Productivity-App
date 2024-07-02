import pickle
from cryptography.fernet import Fernet
import logging


class DataHandler:
    def __init__(self, encryption_key):
        self.key = encryption_key
        self.cipher = Fernet(self.key)

    def save_data(self, data, filename):
        serialized_data = pickle.dumps(data)
        encrypted_data = self.cipher.encrypt(serialized_data)
        with open(filename, 'wb') as file:
            file.write(encrypted_data)
        logging.info(f"Data saved to {filename}")

    def load_data(self, filename):
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
        serialized_data = self.cipher.decrypt(encrypted_data)
        data = pickle.loads(serialized_data)
        logging.info(f"Data loaded from {filename}")
        return data
