"""
app/services/base_service.py
============================
Lớp trừu tượng gốc (Abstract Base Class) cho tất cả Service trong hệ thống.

Mục đích:
- Định nghĩa interface chung: mọi Service đều phải có get_all(), get_by_id()
- Áp dụng tính trừu tượng (Abstraction) và kế thừa (Inheritance) của OOP
- Các lớp con (OrderService, PaymentService...) bắt buộc phải implement
  các phương thức @abstractmethod, nếu không sẽ bị lỗi ngay khi khởi tạo
"""

from abc import ABC, abstractmethod


class ABCBaseService(ABC):
    """
    Interface gốc – tất cả Service đều phải kế thừa class này.

    Áp dụng Abstraction: che giấu chi tiết cài đặt,
    chỉ lộ ra interface (tên phương thức + tham số).
    """

    @abstractmethod
    def get_all(self):
        """Lấy toàn bộ danh sách bản ghi."""
        pass

    @abstractmethod
    def get_by_id(self, record_id):
        """Lấy một bản ghi theo ID."""
        pass


class ABCWritableService(ABCBaseService):
    """
    Mở rộng ABCBaseService – thêm khả năng ghi (tạo, sửa, xóa).
    Các service có thao tác CRUD đầy đủ sẽ kế thừa class này.

    Minh họa kế thừa đa tầng (multi-level inheritance):
        ABCBaseService → ABCWritableService → OrderService
    """

    @abstractmethod
    def create(self, data):
        """Tạo bản ghi mới."""
        pass

    @abstractmethod
    def update(self, record_id, data):
        """Cập nhật bản ghi theo ID."""
        pass

    @abstractmethod
    def delete(self, record_id):
        """Xóa bản ghi theo ID."""
        pass
