"""Convenience exports for service classes used by controllers."""

from app.services.auth_service import AuthService
from app.services.customer_service import CustomerService
from app.services.invoice_service import InvoiceService
from app.services.menu_service import CategoryService, MenuItemService
from app.services.order_service import OrderService
from app.services.statistic_service import StatisticService
from app.services.table_service import TableService
from app.services.user_service import UserService


__all__ = [
    'AuthService',
    'CategoryService',
    'CustomerService',
    'InvoiceService',
    'MenuItemService',
    'OrderService',
    'StatisticService',
    'TableService',
    'UserService',
]
