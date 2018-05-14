from django.test import TestCase
from django.contrib.auth.tokens import default_token_generator

from djoser import utils

from src.accounts.models import User


class UserActionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='kotlyar562@gmail.com', password='123456789', first_name='Andre', last_name='Kotlin',)

    def test_register_user(self):
        resp = self.client.post('/api/v1/auth/users/create/', data={'email': 'test-activate@gmail.com', 'password': '123456789'})
        self.assertEqual(resp.json()['email'], 'test-activate@gmail.com')
        email = resp.json()['email']
        user = User.objects.get(email=email)
        self.assertFalse(user.is_active)
        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        print (uid, token)
        resp1 = self.client.post("/api/v1/auth/users/activate/", data={"uid": str(uid), "token": str(token)})
        self.assertEqual(resp1.status_code, 204)


    def test_login_user(self):
        pass
