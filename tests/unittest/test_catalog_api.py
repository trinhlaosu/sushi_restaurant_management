from tests.unittest.base import ApiTestBase


class CategoryMenuApiTest(ApiTestBase):
    def test_get_categories(self):
        response = self.client.get('/api/categories', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)

    def test_get_category_detail(self):
        response = self.client.get('/api/categories/1', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Sushi')

    def test_post_category(self):
        response = self.client.post('/api/categories', headers=self.login(), json={
            'name': 'Sashimi',
            'description': 'Raw fish',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['category']['name'], 'Sashimi')

    def test_put_category(self):
        created = self.client.post('/api/categories', headers=self.login(), json={'name': 'Temp'})
        category_id = created.get_json()['category']['id']

        response = self.client.put(f'/api/categories/{category_id}', headers=self.login(), json={
            'name': 'Updated Temp',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['category']['name'], 'Updated Temp')

    def test_delete_category(self):
        created = self.client.post('/api/categories', headers=self.login(), json={'name': 'Delete Me'})
        category_id = created.get_json()['category']['id']

        response = self.client.delete(f'/api/categories/{category_id}', headers=self.login())

        self.assertEqual(response.status_code, 200)

    def test_get_menu_items(self):
        response = self.client.get('/api/menu-items')

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_get_menu_item_detail(self):
        response = self.client.get('/api/menu-items/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Salmon Nigiri')

    def test_post_menu_item(self):
        response = self.client.post('/api/menu-items', headers=self.login(), json={
            'name': 'Tuna Nigiri',
            'description': 'Tuna sushi',
            'price': 42000,
            'category_id': 1,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['menu_item']['price'], 42000)

    def test_put_menu_item(self):
        response = self.client.put('/api/menu-items/1', headers=self.login(), json={
            'price': 50000,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['menu_item']['price'], 50000)

    def test_delete_menu_item(self):
        response = self.client.delete('/api/menu-items/1', headers=self.login())
        detail = self.client.get('/api/menu-items/1')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(detail.get_json()['is_available'])
