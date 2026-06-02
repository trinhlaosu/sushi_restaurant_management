from app.services.order_service import OrderService


class InvoiceService:
    def __init__(self):
        self._order_service = OrderService()

    def get_invoice(self, order_id):
        order = self._order_service.get_by_id(order_id)
        if not order.payment:
            raise ValueError('Đơn hàng chưa thanh toán')

        return {
            'invoice_code': f'HD{order.id:06d}',
            'order_id': order.id,
            'table': order.table.to_dict() if order.table else None,
            'customer': order.customer.to_dict() if order.customer else None,
            'items': [detail.to_dict() for detail in order.details],
            'subtotal': sum(detail.subtotal for detail in order.details),
            'discount_code': order.discount.code if order.discount else None,
            'discount_amount': order.discount_amount,
            'total_amount': order.final_amount or order.total_amount,
            'payment': order.payment.to_dict(),
            'created_at': order.created_at.isoformat() if order.created_at else None,
        }
