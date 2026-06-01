from tests.base import ApiTestBase


class PeopleTableApiTest(ApiTestBase):
    def test_get_tables(self):
        response = self.client.get('/api/tables', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_post_table(self):
        response = self.client.post('/api/tables', headers=self.login(), json={
            'table_number': 'B02',
            'seats': 6,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['table']['seats'], 6)

    def test_put_table(self):
        created = self.client.post('/api/tables', headers=self.login(), json={'table_number': 'B02'})
        table_id = created.get_json()['table']['id']

        response = self.client.put(f'/api/tables/{table_id}', headers=self.staff_headers(), json={
            'status': 'dang_phuc_vu',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['table']['status'], 'dang_phuc_vu')

    def test_delete_table(self):
        created = self.client.post('/api/tables', headers=self.login(), json={'table_number': 'B02'})
        table_id = created.get_json()['table']['id']

        response = self.client.delete(f'/api/tables/{table_id}', headers=self.login())

        self.assertEqual(response.status_code, 200)

    def test_get_customers(self):
        response = self.client.get('/api/customers', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_post_customer(self):
        response = self.client.post('/api/customers', headers=self.staff_headers(), json={
            'full_name': 'Nguyen Van A',
            'phone': '0900000001',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['customer']['phone'], '0900000001')

    def test_put_customer(self):
        created = self.client.post('/api/customers', headers=self.staff_headers(), json={
            'full_name': 'Nguyen Van A',
            'phone': '0900000001',
        })
        customer_id = created.get_json()['customer']['id']

        response = self.client.put(f'/api/customers/{customer_id}', headers=self.staff_headers(), json={
            'note': 'VIP',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['customer']['note'], 'VIP')

    def test_delete_customer(self):
        created = self.client.post('/api/customers', headers=self.staff_headers(), json={
            'full_name': 'Nguyen Van A',
            'phone': '0900000001',
        })
        customer_id = created.get_json()['customer']['id']

        response = self.client.delete(f'/api/customers/{customer_id}', headers=self.login())

        self.assertEqual(response.status_code, 200)
