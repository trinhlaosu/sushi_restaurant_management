from app.extensions import db
from app.models import DiningTable, MenuItem, Order, OrderDetail
from app.services.base_service import ABCWritableService
from app.services.discount_service import DiscountService
from app.services.inventory_service import RecipeService


TRANG_THAI_HOP_LE = ['dang_xu_ly', 'da_phuc_vu', 'da_thanh_toan', 'da_huy']


class OrderService(ABCWritableService):
    """Xu ly don goi mon."""

    def __init__(self):
        self._discount_service = DiscountService()
        self._recipe_service = RecipeService()

    def get_all(self):
        return Order.query.order_by(Order.id.desc()).all()

    def get_by_id(self, record_id):
        return Order.query.get_or_404(record_id)

    def create(self, data):
        table_id = data.get('table_id')
        customer_id = data.get('customer_id')
        user_id = data.get('user_id')
        items = data.get('items', [])

        if not items:
            raise ValueError('Đơn hàng phải có ít nhất một món')

        table = DiningTable.query.get(table_id)
        if not table:
            raise ValueError('Bàn không tồn tại')

        order = Order(
            table_id=table_id,
            customer_id=customer_id,
            created_by_user_id=user_id,
            status='dang_xu_ly'
        )
        db.session.add(order)
        db.session.flush()

        subtotal = self.__them_chi_tiet_don(order.id, items)
        discount = self._discount_service.get_active_by_code(data.get('discount_code'))
        discount_amount = 0
        if discount:
            discount_amount = self._discount_service.calculate_amount(discount, subtotal)
            self._discount_service.mark_used(discount)

        order.discount = discount
        order.discount_amount = discount_amount
        order.total_amount = subtotal - discount_amount
        table.status = 'dang_phuc_vu'
        db.session.commit()
        return order

    def update(self, record_id, data):
        order = self.get_by_id(record_id)
        db.session.commit()
        return order

    def delete(self, record_id):
        order = self.get_by_id(record_id)
        return self.cap_nhat_trang_thai(order, 'da_huy')

    def cap_nhat_trang_thai(self, order, trang_thai):
        self._validate_trang_thai(trang_thai)

        order.status = trang_thai

        if trang_thai in ['da_thanh_toan', 'da_huy'] and order.table:
            order.table.status = 'trong'

        db.session.commit()
        return order

    def _validate_trang_thai(self, trang_thai):
        if trang_thai not in TRANG_THAI_HOP_LE:
            raise ValueError(
                f'Trạng thái "{trang_thai}" không hợp lệ. '
                f'Chọn một trong: {TRANG_THAI_HOP_LE}'
            )

    def __them_chi_tiet_don(self, order_id, items):
        total = 0

        for item in items:
            menu_item_id = item.get('menu_item_id')
            quantity = int(item.get('quantity', 0))

            if quantity <= 0:
                raise ValueError('Số lượng món phải lớn hơn 0')

            menu_item = MenuItem.query.get(menu_item_id)
            if not menu_item or not menu_item.is_available:
                raise ValueError(
                    f'Món có id {menu_item_id} không tồn tại hoặc tạm ngưng bán'
                )

            self._recipe_service.ensure_stock_and_deduct(menu_item, quantity)

            subtotal = menu_item.price * quantity
            total += subtotal

            order_detail = OrderDetail(
                order_id=order_id,
                menu_item_id=menu_item.id,
                quantity=quantity,
                unit_price=menu_item.price,
                subtotal=subtotal
            )
            db.session.add(order_detail)

        return total

    def __str__(self):
        return 'OrderService()'
