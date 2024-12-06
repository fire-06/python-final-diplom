from django.test import TestCase

# Create your tests here.
# from rest_framework.test import APITestCase
# from rest_framework import status
#
# class UserRegistrationAPITest(APITestCase):
#     def setUp(self):
#         self.register_url = '/api/v1/user/register/'
#         self.valid_user_data = {
#             'first_name': 'Имя',
#             'last_name': 'Фамилия',
#             'email': 'test@mail.ru',
#             'password': 'qwer1234A',
#             'company': 'asdads',
#             'position': '345345'
#         }
#
#     def test_user_registration_success(self):
#         """Тест успешной регистрации пользователя"""
#         response = self.client.post(self.register_url, data=self.valid_user_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['Status'], 'Success')
#         self.assertIn('Message', response.data)
#
#     def test_user_registration_missing_fields(self):
#         """Тест регистрации с отсутствием обязательных полей"""
#         invalid_data = self.valid_user_data.copy()
#         invalid_data.pop('email')  # Убираем email для проверки ошибки
#         response = self.client.post(self.register_url, data=invalid_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['Status'], 'Error')
#         self.assertIn('Error', response.data)
#
#     def test_user_registration_invalid_password(self):
#         """Тест регистрации с некорректным паролем"""
#         invalid_data = self.valid_user_data.copy()
#         invalid_data['password'] = '123'  # Указываем слабый пароль
#         response = self.client.post(self.register_url, data=invalid_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['Status'], 'Error')
#         self.assertIn('Error', response.data)




from rest_framework.test import APITestCase
from rest_framework import status

class UserRegistrationAPITest(APITestCase):
    def test_user_registration_success(self):
        response = self.client.post('/api/v1/user/register/', {
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Status'], 'Success')

    def test_user_registration_missing_fields(self):
        response = self.client.post('/api/v1/user/register/', {
            'email': 'test@example.com',
            'password': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Status'], 'Error')

    def test_user_registration_invalid_password(self):
        response = self.client.post('/api/v1/user/register/', {
            'email': 'test@example.com',
            'password': '123',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['Error'])
