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
from app.services.auth_service      import AuthService
from app.services.user_service      import UserService
from app.services.table_service     import TableService
from app.services.customer_service  import CustomerService
from app.services.invoice_service   import InvoiceService

__all__ = [
    'AuthService',
    'OrderService',
    'PaymentService',
    'StatisticService',
    'CategoryService',
    'MenuItemService',
    'UserService',
    'TableService',
    'CustomerService',
    'InvoiceService',
]
