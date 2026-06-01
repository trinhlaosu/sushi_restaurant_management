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
from app.services.discount_service  import DiscountService
from app.services.inventory_service import IngredientService, RecipeService
from app.services.reservation_service import ReservationService
from app.services.invoice_service   import InvoiceService
from app.services.activity_log_service import ActivityLogService
from app.services.shift_service     import ShiftService

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
    'DiscountService',
    'IngredientService',
    'RecipeService',
    'ReservationService',
    'InvoiceService',
    'ActivityLogService',
    'ShiftService',
]
