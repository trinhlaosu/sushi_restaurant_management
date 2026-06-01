import os
import unittest
from datetime import date, timedelta

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app
from app.extensions import db
from app.models import Category, Customer, DiningTable, MenuItem, Role, User
from app.models.dining_table import now_utc


class SushiApiTestCase(unittest.TestCase):
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
        admin_role = Role(name='admin', description='Quản trị viên')
        staff_role = Role(name='staff', description='Nhân viên')
        db.session.add_all([admin_role, staff_role])
        db.session.flush()

        admin = User(full_name='Quản trị viên', username='admin', role_id=admin_role.id)
        admin.set_password('admin123')
        staff = User(full_name='Nhân viên bán hàng', username='staff', role_id=staff_role.id)
        staff.set_password('staff123')

        category = Category(name='Sushi', description='Các món sushi')
        db.session.add_all([admin, staff, category])
        db.session.flush()

        db.session.add_all([
            MenuItem(
                name='Cá hồi Nigiri',
                description='Sushi cá hồi',
                price=45000,
                category_id=category.id,
            ),
            DiningTable(table_number='B01', seats=4, status='trong'),
            Customer(full_name='Khách lẻ', phone=None, note='Khách không đăng ký'),
            Customer(
                full_name='Khách thành viên',
                phone='0901000001',
                note='Thành viên sinh nhật tháng 5',
                customer_type='thanh_vien',
                member_tier='vip',
                birth_date=date(1998, 5, 12),
            ),
        ])
        db.session.commit()

    def _login(self, username='admin', password='admin123'):
        response = self.client.post('/api/auth/login', json={
            'username': username,
            'password': password,
        })
        self.assertEqual(response.status_code, 200)
        return {'Authorization': f"Bearer {response.get_json()['token']}"}

    def test_health_check(self):
        response = self.client.get('/api/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Sushi Restaurant API is running')

    def test_login_success_and_fail(self):
        success = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'admin123',
        })
        failed = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'sai-mat-khau',
        })

        self.assertEqual(success.status_code, 200)
        self.assertIn('token', success.get_json())
        self.assertEqual(failed.status_code, 401)

    def test_admin_can_create_menu_item(self):
        headers = self._login()

        response = self.client.post('/api/menu-items', headers=headers, json={
            'name': 'Sashimi cá hồi',
            'description': 'Cá hồi tươi cắt lát',
            'price': 129000,
            'category_id': 1,
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()['menu_item']
        self.assertEqual(data['name'], 'Sashimi cá hồi')
        self.assertEqual(data['price'], 129000)

    def test_staff_cannot_create_menu_item(self):
        headers = self._login('staff', 'staff123')

        response = self.client.post('/api/menu-items', headers=headers, json={
            'name': 'Món không hợp lệ',
            'price': 10000,
            'category_id': 1,
        })

        self.assertEqual(response.status_code, 403)

    def test_create_order_calculates_total_amount(self):
        headers = self._login('staff', 'staff123')

        response = self.client.post('/api/orders', headers=headers, json={
            'table_id': 1,
            'customer_id': 1,
            'items': [
                {'menu_item_id': 1, 'quantity': 2},
            ],
        })

        self.assertEqual(response.status_code, 201)
        order = response.get_json()['order']
        self.assertEqual(order['total_amount'], 90000)
        self.assertEqual(order['details'][0]['subtotal'], 90000)

    def test_payment_marks_order_paid(self):
        headers = self._login('staff', 'staff123')
        order_response = self.client.post('/api/orders', headers=headers, json={
            'table_id': 1,
            'customer_id': 1,
            'items': [
                {'menu_item_id': 1, 'quantity': 2},
            ],
        })
        order_id = order_response.get_json()['order']['id']

        payment_response = self.client.post('/api/payments', headers=headers, json={
            'order_id': order_id,
            'payment_method': 'tien_mat',
        })
        order_detail_response = self.client.get(f'/api/orders/{order_id}', headers=headers)

        self.assertEqual(payment_response.status_code, 201)
        self.assertEqual(payment_response.get_json()['payment']['amount'], 90000)
        self.assertEqual(order_detail_response.get_json()['status'], 'da_thanh_toan')

    def test_birthday_member_gets_10_percent_discount_only(self):
        headers = self._login('staff', 'staff123')

        response = self.client.post('/api/orders', headers=headers, json={
            'table_id': 1,
            'customer_id': 2,
            'items': [
                {'menu_item_id': 1, 'quantity': 2},
            ],
        })

        self.assertEqual(response.status_code, 201)
        order = response.get_json()['order']
        self.assertEqual(order['total_amount'], 90000)
        self.assertEqual(order['discount_percent'], 10)
        self.assertEqual(order['discount_amount'], 9000)
        self.assertEqual(order['final_amount'], 81000)
        self.assertIsNone(order['gift_item'])

    def test_reserve_table_sets_15_minute_hold(self):
        headers = self._login('staff', 'staff123')

        response = self.client.put('/api/tables/1', headers=headers, json={
            'status': 'da_dat',
        })

        self.assertEqual(response.status_code, 200)
        table = response.get_json()['table']
        self.assertEqual(table['status'], 'da_dat')
        self.assertIsNotNone(table['reserved_at'])
        self.assertIsNotNone(table['reserved_until'])

    def test_expired_reservation_returns_table_to_available(self):
        headers = self._login('staff', 'staff123')
        table = DiningTable.query.get(1)
        table.status = 'da_dat'
        table.reserved_at = now_utc() - timedelta(minutes=20)
        table.reserved_until = now_utc() - timedelta(minutes=5)
        db.session.commit()

        response = self.client.get('/api/tables', headers=headers)

        self.assertEqual(response.status_code, 200)
        table_data = next(item for item in response.get_json() if item['id'] == 1)
        self.assertEqual(table_data['status'], 'trong')
        self.assertIsNone(table_data['reserved_at'])
        self.assertIsNone(table_data['reserved_until'])


if __name__ == '__main__':
    unittest.main()
