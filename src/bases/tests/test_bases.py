from django.test import TestCase
from src.accounts.models import User
from src.bases.models import QuestBase


class BasesTest(TestCase):

    def setUp(self):
        user = User.objects.create(email="test@test.ru", password="12345678")
        QuestBase.objects.create(user=user, title="test base", klass="8 klass",
                                discipline="Informatik", rating=5)

    def test_increment_rating(self):
        base = QuestBase.objects.get(pk=1)
        base.inc_rating()
        self.assertEqual(base.rating, 6)
        base.dec_rating()
        base.dec_rating()
        self.assertEqual(base.rating, 4)
