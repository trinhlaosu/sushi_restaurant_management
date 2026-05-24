from abc import ABC, abstractmethod


class ABCBaseService(ABC):
    """Các hàm chung cho service."""

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, record_id):
        pass


class ABCWritableService(ABCBaseService):
    """Service nào có thêm/sửa/xóa thì dùng class này."""

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def update(self, record_id, data):
        pass

    @abstractmethod
    def delete(self, record_id):
        pass
