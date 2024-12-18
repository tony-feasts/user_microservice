from framework.resources.base_resource import BaseResource
from app.services.service_factory import ServiceFactory
from app.models import UserInfo

class UserInfoResource(BaseResource):
    def __init__(self):
        self.data_service = ServiceFactory.get_service('DataService')
        self.database = self.data_service.config.get_config('DB_NAME')
        self.collection = 'user_info'
        self.key_field = 'username'

    def get_by_key(self, key):
        data = self.data_service.get_data_object(
            self.database, self.collection, self.key_field, key)
        return UserInfo(**data) if data else None

    def create(self, data):
        self.data_service.create_data_object(
            self.database, self.collection, data.model_dump(exclude={'links'}))

    def update(self, key, data):
        self.data_service.update_data_object(
            self.database, self.collection, self.key_field, key,
            data.model_dump(exclude={'links'}))

    def delete(self, key):
        self.data_service.delete_data_object(
            self.database, self.collection, self.key_field, key)
