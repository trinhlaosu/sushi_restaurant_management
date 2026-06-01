from tests.base import ApiTestBase


class HealthAuthUserApiTest(ApiTestBase):
    def test_get_health(self):
        response = self.client.get('/api/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Sushi Restaurant API is running')

    def test_post_auth_register(self):
        response = self.client.post('/api/auth/register', json={
            'full_name': 'New Staff',
            'username': 'new_staff',
            'password': 'new123',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['user']['role'], 'staff')

    def test_post_auth_login(self):
        response = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'admin123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_post_auth_logout(self):
        headers = self.login()

        response = self.client.post('/api/auth/logout', headers=headers)
        after_logout = self.client.get('/api/users', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(after_logout.status_code, 401)

    def test_get_users(self):
        response = self.client.get('/api/users', headers=self.login())

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 3)

    def test_put_user_role(self):
        response = self.client.put('/api/users/2/role', headers=self.login(), json={
            'role': 'admin',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['user']['role'], 'admin')

    def test_auth_guard_missing_token(self):
        response = self.client.get('/api/users')

        self.assertEqual(response.status_code, 401)

    def test_auth_guard_wrong_role(self):
        response = self.client.get('/api/users', headers=self.staff_headers())

        self.assertEqual(response.status_code, 403)
