from tests.base import ApiTestBase


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
