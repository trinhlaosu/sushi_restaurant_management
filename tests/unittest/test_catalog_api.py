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

    def test_get_menu_item_ingredients(self):
        ingredient = self._create_ingredient()
        self._set_recipe(ingredient['id'])

        response = self.client.get('/api/menu-items/1/ingredients', headers=self.staff_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]['ingredient_id'], ingredient['id'])

    def test_post_menu_item_ingredients(self):
        ingredient = self._create_ingredient()

        response = self._set_recipe(ingredient['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['recipe'][0]['quantity'], 10)

    def _create_ingredient(self):
        response = self.client.post('/api/ingredients', headers=self.login(), json={
            'name': 'Salmon',
            'unit': 'gram',
            'stock_quantity': 100,
        })
        self.assertEqual(response.status_code, 201)
        return response.get_json()['ingredient']

    def _set_recipe(self, ingredient_id):
        return self.client.post('/api/menu-items/1/ingredients', headers=self.login(), json={
            'ingredients': [
                {'ingredient_id': ingredient_id, 'quantity': 10},
            ],
        })
