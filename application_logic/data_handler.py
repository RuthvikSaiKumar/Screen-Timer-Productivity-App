import pickle
import logging
from cryptography.fernet import Fernet

class DataHandler:
    def __init__(self, key):
        self.cipher = Fernet(key)
        
    def save_data(self, data, filename='data.pkl'):
        try:
            encrypted_data = self.cipher.encrypt(pickle.dumps(data))
            with open(filename, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f"Data successfully saved to {filename}.")
        except Exception as e:
            logging.error(f"Error saving data: {e}")
    
    def load_data(self, filename='data.pkl'):
        try:
            with open(filename, 'rb') as file:
                encrypted_data = file.read()
            data = pickle.loads(self.cipher.decrypt(encrypted_data))
            logging.info(f"Data successfully loaded from {filename}.")
            return data
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return []

