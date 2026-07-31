from rest_framework.test import APITestCase
from django.urls import reverse


class HotelAPITestCase(APITestCase):

    def test_get_hotels(self):
        url = reverse('hotel_api')
        response = self.client.get(url)
        self.assertEqual(response.data['status'], True)
        self.assertIsInstance(response.data['data'], list)


class LoginAPITestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'first_name' : 'Test',
            'last_name' : 'User'
        }
        response = self.client.post(reverse('register_api'), self.user_data)
        print("********")
        print(response.data)
        print("********")

    def test_login(self):
        url = reverse('login_api')
        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
            
        }
        response = self.client.post(url, data)
        print("********")
        print(response.data)
        print("********")
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('refresh', response.data['token'])
        self.assertIn('access', response.data['token'])

    def test_login_invalid_credentials(self):
        url = reverse('login_api')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        #self.assertEqual(response.data['message'], 'Wrong password')
        self.assertEqual(response.data['status'], False)