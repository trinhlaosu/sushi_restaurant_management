from app.extensions import db
from app.models import Discount, Ingredient
from tests.unittest.base import ApiTestBase


class OrderPaymentApiTest(ApiTestBase):
    def test_get_orders(self):
        self.create_order()

        response = self.client.get('/api/orders', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('details', response.get_json()[0])

    def test_get_order_detail(self):
        order = self.create_order()

        response = self.client.get(f"/api/orders/{order['id']}", headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], order['id'])

    def test_post_order(self):
        response = self.client.post('/api/orders', headers=self.staff_headers(), json={
            'table_id': 1,
            'customer_id': 1,
            'items': [
                {'menu_item_id': 1, 'quantity': 2},
            ],
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['order']['total_amount'], 90000)

    def test_put_order_status(self):
        order = self.create_order()

        response = self.client.put(f"/api/orders/{order['id']}/status", headers=self.staff_headers(), json={
            'status': 'da_phuc_vu',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['order']['status'], 'da_phuc_vu')

    def test_post_payment(self):
        order = self.create_order(quantity=1)

        response = self.client.post('/api/payments', headers=self.cashier_headers(), json={
            'order_id': order['id'],
            'payment_method': 'tien_mat',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['payment']['amount'], 45000)

    def test_cannot_pay_cancelled_order(self):
        order = self.create_order(quantity=1)
        cancel = self.client.put(f"/api/orders/{order['id']}/status", headers=self.staff_headers(), json={
            'status': 'da_huy',
        })
        self.assertEqual(cancel.status_code, 200)

        response = self.client.post('/api/payments', headers=self.cashier_headers(), json={
            'order_id': order['id'],
            'payment_method': 'tien_mat',
        })

        self.assertEqual(response.status_code, 400)

    def test_cancel_order_restores_stock_and_discount_usage(self):
        ingredient = self.client.post('/api/ingredients', headers=self.login(), json={
            'name': 'Rollback Salmon',
            'unit': 'gram',
            'stock_quantity': 100,
        }).get_json()['ingredient']
        self.client.post('/api/menu-items/1/ingredients', headers=self.login(), json={
            'ingredients': [
                {'ingredient_id': ingredient['id'], 'quantity': 10},
            ],
        })
        discount = self.client.post('/api/discounts', headers=self.login(), json={
            'code': 'RESTORE10',
            'discount_type': 'percent',
            'value': 10,
        }).get_json()['discount']
        order = self.create_order(quantity=2, extra={'discount_code': 'RESTORE10'})

        response = self.client.put(f"/api/orders/{order['id']}/status", headers=self.staff_headers(), json={
            'status': 'da_huy',
        })
        db.session.expire_all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(db.session.get(Ingredient, ingredient['id']).stock_quantity, 100)
        self.assertEqual(db.session.get(Discount, discount['id']).used_count, 0)

    def test_get_payments(self):
        order = self.create_order(quantity=1)
        self.pay_order(order['id'])

        response = self.client.get('/api/payments', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_invoice(self):
        order = self.create_order(quantity=1)
        self.pay_order(order['id'])

        response = self.client.get(f"/api/invoices/{order['id']}", headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['invoice_code'], 'HD000001')
