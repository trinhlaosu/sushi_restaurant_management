import os
import unittest
from uuid import uuid4

from app import create_app
from app.extensions import db
from app.models import (
    ActivityLog,
    Category,
    Customer,
    DiningTable,
    Discount,
    Ingredient,
    MenuItem,
    MenuItemIngredient,
    Order,
    Payment,
    Reservation,
    Role,
    Shift,
    User,
)


@unittest.skipUnless(
    os.environ.get('RUN_REAL_DB_TESTS') == '1',
    'Set RUN_REAL_DB_TESTS=1 to run tests against the real configured database.',
)
class AllApiFlowTest(unittest.TestCase):
    """Integration test duyet luong tong hop cua cac API voi database that.

    Test nay co ghi vao DB that, nen duoc skip mac dinh. Khi can chay:

        $env:RUN_REAL_DB_TESTS='1'
        python -m unittest tests.test_all_api -v
    """

    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        db.create_all()
        self.suffix = uuid4().hex[:8]
        self.created = {
            'activity_logs': [],
            'payments': [],
            'orders': [],
            'shifts': [],
            'reservations': [],
            'menu_item_ingredients': [],
            'ingredients': [],
            'discounts': [],
            'menu_items': [],
            'customers': [],
            'tables': [],
            'categories': [],
            'users': [],
        }
        self._seed_minimum_data()

    def tearDown(self):
        self._cleanup_created_data()
        db.session.remove()
        self.ctx.pop()

    def test_full_flow_and_verify_real_database_state(self):
        staff_headers = self._login(self.staff_username, 'staff123')

        order_response = self.client.post('/api/orders', headers=staff_headers, json={
            'table_id': self.table.id,
            'customer_id': self.customer.id,
            'discount_code': self.discount.code,
            'items': [
                {'menu_item_id': self.menu_item.id, 'quantity': 2},
            ],
        })
        self.assertEqual(order_response.status_code, 201)
        order_id = order_response.get_json()['order']['id']
        self.created['orders'].append(order_id)

        payment_response = self.client.post('/api/payments', headers=staff_headers, json={
            'order_id': order_id,
            'payment_method': 'tien_mat',
        })
        self.assertEqual(payment_response.status_code, 201)
        payment_id = payment_response.get_json()['payment']['id']
        self.created['payments'].append(payment_id)

        reservation_response = self.client.post('/api/reservations', headers=staff_headers, json={
            'table_id': self.table.id,
            'customer_id': self.customer.id,
            'reservation_time': '2035-01-01T18:00:00',
            'guest_count': 2,
            'note': f'real-db-{self.suffix}',
        })
        self.assertEqual(reservation_response.status_code, 201)
        reservation_id = reservation_response.get_json()['reservation']['id']
        self.created['reservations'].append(reservation_id)

        shift_response = self.client.post('/api/shifts/check-in', headers=staff_headers, json={
            'user_id': self.staff.id,
            'note': f'real-db-{self.suffix}',
        })
        self.assertEqual(shift_response.status_code, 201)
        shift_id = shift_response.get_json()['shift']['id']
        self.created['shifts'].append(shift_id)
        checkout_response = self.client.post(f'/api/shifts/{shift_id}/check-out', headers=staff_headers)
        self.assertEqual(checkout_response.status_code, 200)

        invoice_response = self.client.get(f'/api/invoices/{order_id}', headers=staff_headers)
        self.assertEqual(invoice_response.status_code, 200)
        self.assertEqual(invoice_response.get_json()['total_amount'], 81000)

        db.session.expire_all()

        order = db.session.get(Order, order_id)
        payment = db.session.get(Payment, payment_id)
        table = db.session.get(DiningTable, self.table.id)
        ingredient = db.session.get(Ingredient, self.ingredient.id)
        discount = db.session.get(Discount, self.discount.id)
        reservation = db.session.get(Reservation, reservation_id)
        shift = db.session.get(Shift, shift_id)
        activity_log = ActivityLog.query.filter_by(
            action='create_payment',
            target_type='payment',
            target_id=payment_id,
        ).first()

        self.assertIsNotNone(order)
        self.assertEqual(order.status, 'da_thanh_toan')
        self.assertEqual(order.discount_amount, 9000)
        self.assertEqual(order.total_amount, 90000)
        self.assertEqual(order.final_amount, 81000)
        self.assertIsNotNone(payment)
        self.assertEqual(payment.amount, 81000)
        self.assertEqual(table.status, 'trong')
        self.assertEqual(ingredient.stock_quantity, 80.0)
        self.assertEqual(discount.used_count, 1)
        self.assertEqual(reservation.status, 'cho_xac_nhan')
        self.assertIsNotNone(shift.end_time)
        self.assertIsNotNone(activity_log)
        self.created['activity_logs'].append(activity_log.id)

    def _seed_minimum_data(self):
        admin_role = self._get_or_create_role('admin', 'Admin')
        staff_role = self._get_or_create_role('staff', 'Staff')

        self.staff_username = f'real_staff_{self.suffix}'
        self.staff = User(
            full_name='Real DB Staff',
            username=self.staff_username,
            role_id=staff_role.id,
        )
        self.staff.set_password('staff123')
        db.session.add(self.staff)
        db.session.flush()
        self.created['users'].append(self.staff.id)

        self.admin = User(
            full_name='Real DB Admin',
            username=f'real_admin_{self.suffix}',
            role_id=admin_role.id,
        )
        self.admin.set_password('admin123')
        db.session.add(self.admin)
        db.session.flush()
        self.created['users'].append(self.admin.id)

        self.category = Category(name=f'Real Category {self.suffix}', description='Real DB test')
        db.session.add(self.category)
        db.session.flush()
        self.created['categories'].append(self.category.id)

        self.menu_item = MenuItem(
            name=f'Real Salmon Nigiri {self.suffix}',
            description='Real DB test item',
            price=45000,
            category_id=self.category.id,
        )
        db.session.add(self.menu_item)
        db.session.flush()
        self.created['menu_items'].append(self.menu_item.id)

        self.table = DiningTable(table_number=f'R{self.suffix[:6]}', seats=4, status='trong')
        db.session.add(self.table)
        db.session.flush()
        self.created['tables'].append(self.table.id)

        self.customer = Customer(
            full_name=f'Real Customer {self.suffix}',
            phone=f'09{self.suffix[:8]}',
            note='Real DB test customer',
        )
        db.session.add(self.customer)
        db.session.flush()
        self.created['customers'].append(self.customer.id)

        self.ingredient = Ingredient(
            name=f'Real Ingredient {self.suffix}',
            unit='gram',
            stock_quantity=100,
            min_quantity=10,
        )
        db.session.add(self.ingredient)
        db.session.flush()
        self.created['ingredients'].append(self.ingredient.id)

        recipe = MenuItemIngredient(
            menu_item_id=self.menu_item.id,
            ingredient_id=self.ingredient.id,
            quantity=10,
        )
        db.session.add(recipe)
        db.session.flush()
        self.created['menu_item_ingredients'].append(recipe.id)

        self.discount = Discount(
            code=f'REAL{self.suffix}'.upper(),
            discount_type='percent',
            value=10,
            usage_limit=1,
        )
        db.session.add(self.discount)
        db.session.flush()
        self.created['discounts'].append(self.discount.id)

        db.session.commit()

    def _get_or_create_role(self, name, description):
        role = Role.query.filter_by(name=name).first()
        if role:
            return role
        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.flush()
        return role

    def _login(self, username, password):
        response = self.client.post('/api/auth/login', json={
            'username': username,
            'password': password,
        })
        self.assertEqual(response.status_code, 200)
        return {'Authorization': f"Bearer {response.get_json()['token']}"}

    def _cleanup_created_data(self):
        delete_order = [
            (ActivityLog, 'activity_logs'),
            (Payment, 'payments'),
            (Order, 'orders'),
            (Shift, 'shifts'),
            (Reservation, 'reservations'),
            (MenuItemIngredient, 'menu_item_ingredients'),
            (Ingredient, 'ingredients'),
            (Discount, 'discounts'),
            (MenuItem, 'menu_items'),
            (Customer, 'customers'),
            (DiningTable, 'tables'),
            (Category, 'categories'),
            (User, 'users'),
        ]
        for model, key in delete_order:
            for record_id in self.created[key]:
                record = db.session.get(model, record_id)
                if record:
                    db.session.delete(record)
        db.session.commit()
