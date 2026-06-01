from tests.base import ApiTestBase


class ShiftLogStatisticsApiTest(ApiTestBase):
    def test_get_shifts(self):
        self._check_in()

        response = self.client.get('/api/shifts', headers=self.login())

        self.assertEqual(response.status_code, 200)

    def test_post_shift_check_in(self):
        response = self._check_in()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.get_json()['shift']['is_active'])

    def test_post_shift_check_out(self):
        check_in = self._check_in()
        shift_id = check_in.get_json()['shift']['id']

        response = self.client.post(f'/api/shifts/{shift_id}/check-out', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()['shift']['is_active'])

    def test_get_activity_logs(self):
        order = self.create_order(quantity=1)
        self.pay_order(order['id'])

        response = self.client.get('/api/activity-logs', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]['action'], 'create_payment')

    def test_get_statistics_summary(self):
        order = self.create_order(quantity=2)
        self.pay_order(order['id'])

        response = self.client.get('/api/statistics', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['tong_doanh_thu'], 90000)

    def test_get_statistics_revenue(self):
        order = self.create_order(quantity=2)
        self.pay_order(order['id'])

        response = self.client.get('/api/statistics/revenue', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['tong_doanh_thu'], 90000)

    def test_get_statistics_popular_items(self):
        order = self.create_order(quantity=2)
        self.pay_order(order['id'])

        response = self.client.get('/api/statistics/popular-items?top=1', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]['tong_so_luong'], 2)

    def test_get_statistics_by_day(self):
        order = self.create_order(quantity=1)
        self.pay_order(order['id'])

        response = self.client.get('/api/statistics/by-day', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]['tong_doanh_thu'], 45000)

    def test_get_statistics_by_staff(self):
        order = self.create_order(quantity=1)
        self.pay_order(order['id'])

        response = self.client.get('/api/statistics/by-staff', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]['user_id'], 2)

    def _check_in(self):
        return self.client.post('/api/shifts/check-in', headers=self.staff_headers(), json={
            'user_id': 2,
            'note': 'Morning shift',
        })
