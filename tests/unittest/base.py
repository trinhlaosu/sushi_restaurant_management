import os
import unittest

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app
from app.extensions import db
from app.models import Category, Customer, DiningTable, MenuItem, Role, User


class ApiTestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        db.create_all()
        self._seed_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _seed_data(self):
        admin_role = Role(name='admin', description='Admin')
        staff_role = Role(name='staff', description='Staff')
        cashier_role = Role(name='cashier', description='Cashier')
        db.session.add_all([admin_role, staff_role, cashier_role])
        db.session.flush()

        admin = User(full_name='Admin User', username='admin', role_id=admin_role.id)
        admin.set_password('admin123')
        staff = User(full_name='Staff User', username='staff', role_id=staff_role.id)
        staff.set_password('staff123')
        cashier = User(full_name='Cashier User', username='cashier', role_id=cashier_role.id)
        cashier.set_password('cashier123')

        category = Category(name='Sushi', description='Sushi items')
        db.session.add_all([admin, staff, cashier, category])
        db.session.flush()

        db.session.add_all([
            MenuItem(
                name='Salmon Nigiri',
                description='Salmon sushi',
                price=45000,
                category_id=category.id,
            ),
            DiningTable(table_number='B01', seats=4, status='trong'),
            Customer(full_name='Walk-in Guest', phone=None, note='No membership'),
        ])
        db.session.commit()

    def login(self, username='admin', password='admin123'):
        response = self.client.post('/api/auth/login', json={
            'username': username,
            'password': password,
        })
        self.assertEqual(response.status_code, 200)
        return {'Authorization': f"Bearer {response.get_json()['token']}"}

    def staff_headers(self):
        return self.login('staff', 'staff123')

    def cashier_headers(self):
        return self.login('cashier', 'cashier123')

    def create_order(self, headers=None, quantity=2, extra=None):
        payload = {
            'table_id': 1,
            'customer_id': 1,
            'items': [
                {'menu_item_id': 1, 'quantity': quantity},
            ],
        }
        if extra:
            payload.update(extra)
        response = self.client.post('/api/orders', headers=headers or self.staff_headers(), json=payload)
        self.assertEqual(response.status_code, 201)
        return response.get_json()['order']

    def pay_order(self, order_id, headers=None):
        response = self.client.post('/api/payments', headers=headers or self.staff_headers(), json={
            'order_id': order_id,
            'payment_method': 'tien_mat',
        })
        self.assertEqual(response.status_code, 201)
        return response.get_json()['payment']
