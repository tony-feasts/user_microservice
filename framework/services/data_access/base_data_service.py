# framework/services/base_data_service.py

from abc import ABC, abstractmethod

class BaseDataService(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_data_object(self, database_name, collection_name, key_field,
                        key_value):
        pass

    @abstractmethod
    def create_data_object(self, database_name, collection_name, data):
        pass

    @abstractmethod
    def update_data_object(self, database_name, collection_name, key_field,
                           key_value, data):
        pass

    @abstractmethod
    def delete_data_object(self, database_name, collection_name, key_field,
                           key_value):
        pass
