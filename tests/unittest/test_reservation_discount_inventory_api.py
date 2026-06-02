from tests.unittest.base import ApiTestBase


class ReservationDiscountInventoryApiTest(ApiTestBase):
    def test_get_reservations(self):
        self._create_reservation()

        response = self.client.get('/api/reservations', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_post_reservation(self):
        response = self._create_reservation()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['reservation']['guest_count'], 2)

    def test_put_reservation(self):
        created = self._create_reservation()
        reservation_id = created.get_json()['reservation']['id']

        response = self.client.put(f'/api/reservations/{reservation_id}', headers=self.staff_headers(), json={
            'status': 'da_xac_nhan',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['reservation']['status'], 'da_xac_nhan')

    def test_put_reservation_rejects_guest_count_over_table_seats(self):
        created = self._create_reservation()
        reservation_id = created.get_json()['reservation']['id']

        response = self.client.put(f'/api/reservations/{reservation_id}', headers=self.staff_headers(), json={
            'guest_count': 99,
        })

        self.assertEqual(response.status_code, 400)

    def test_delete_reservation(self):
        created = self._create_reservation()
        reservation_id = created.get_json()['reservation']['id']

        response = self.client.delete(f'/api/reservations/{reservation_id}', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_get_discounts(self):
        self._create_discount()

        response = self.client.get('/api/discounts', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_post_discount(self):
        response = self._create_discount()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['discount']['code'], 'SALE10')

    def test_put_discount(self):
        created = self._create_discount()
        discount_id = created.get_json()['discount']['id']

        response = self.client.put(f'/api/discounts/{discount_id}', headers=self.login(), json={
            'value': 15,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['discount']['value'], 15)

    def test_delete_discount(self):
        created = self._create_discount()
        discount_id = created.get_json()['discount']['id']

        response = self.client.delete(f'/api/discounts/{discount_id}', headers=self.login())

        self.assertEqual(response.status_code, 200)

    def test_get_ingredients(self):
        self._create_ingredient()

        response = self.client.get('/api/ingredients', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_post_ingredient(self):
        response = self._create_ingredient()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['ingredient']['name'], 'Salmon')

    def test_put_ingredient(self):
        created = self._create_ingredient()
        ingredient_id = created.get_json()['ingredient']['id']

        response = self.client.put(f'/api/ingredients/{ingredient_id}', headers=self.login(), json={
            'min_quantity': 5,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['ingredient']['min_quantity'], 5.0)

    def test_delete_ingredient(self):
        created = self._create_ingredient()
        ingredient_id = created.get_json()['ingredient']['id']

        response = self.client.delete(f'/api/ingredients/{ingredient_id}', headers=self.login())

        self.assertEqual(response.status_code, 200)

    def _create_reservation(self):
        return self.client.post('/api/reservations', headers=self.staff_headers(), json={
            'table_id': 1,
            'customer_id': 1,
            'reservation_time': '2030-01-01T18:00:00',
            'guest_count': 2,
        })

    def _create_discount(self):
        return self.client.post('/api/discounts', headers=self.login(), json={
            'code': 'SALE10',
            'discount_type': 'percent',
            'value': 10,
        })

    def _create_ingredient(self):
        return self.client.post('/api/ingredients', headers=self.login(), json={
            'name': 'Salmon',
            'unit': 'gram',
            'stock_quantity': 100,
        })
