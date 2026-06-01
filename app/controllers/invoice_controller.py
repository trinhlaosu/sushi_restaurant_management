from flask import Blueprint
from app.services import InvoiceService
from app.utils.auth import auth_required
from app.utils.response import data_response, service_error_response

invoice_bp = Blueprint('invoice_bp', __name__, url_prefix='/api/invoices')
_svc = InvoiceService()


@invoice_bp.get('/<int:order_id>')
@auth_required('admin', 'staff', 'cashier')
def get_invoice(order_id):
    try:
        return data_response(_svc.get_invoice(order_id))
    except ValueError as e:
        return service_error_response(e)
