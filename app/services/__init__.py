"""
app/services/__init__.py
Export tất cả service để import thuận tiện từ controller.

Ví dụ:
    from app.services import OrderService, PaymentService
"""

from app.services.order_service     import OrderService
from app.services.payment_service   import PaymentService
from app.services.statistic_service import StatisticService
from app.services.menu_service      import CategoryService, MenuItemService

__all__ = [
    'OrderService',
    'PaymentService',
    'StatisticService',
    'CategoryService',
    'MenuItemService',
]
