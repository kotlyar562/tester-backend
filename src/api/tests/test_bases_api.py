import json
from django.test import TestCase
from src.accounts.models import User
from src.bases.models import QuestBase
from django.test import Client
from .. serializers.bases_serializer import BaseShortInfoSerializer, BaseFullSerializer

class BasesApiTest(TestCase):

    def setUp(self):
        u = User.objects.create(email='test1@test.ru', password='12345678')
        u.is_active = True
        u.save()
        u2 = User.objects.create(email='test2@test.ru', password='12345678')
        u2.is_active = True
        u2.save()
        self.publicBase = QuestBase.objects.create(title='Public Base', user=u,
                                 publik=True, good=True)#1
        self.noPublicBase = QuestBase.objects.create(title='No Public Base', user=u) #2
        self.copiedBase = QuestBase.objects.create(title='Copied Publik Base', user=u,
                                 publik=True, good=True, copied=True) #3

    def testGetPostUserBases(self):
        user = User.objects.get(email='test1@test.ru')
        c = Client()
        respNotAuthorized = c.get('/api/v1/bases/user/')
        self.assertEqual(respNotAuthorized.status_code, 401)
        c.force_login(user)
        respGet = c.get('/api/v1/bases/user/')
        userBases = QuestBase.objects.filter(user=user)
        serializer = BaseShortInfoSerializer(userBases, many=True)
        self.assertEqual(respGet.data, serializer.data)
        respCreateBase = c.post('/api/v1/bases/user/',
                                data=json.dumps({'title': 'New Base'}),
                                content_type='application/json')
        self.assertEqual(respCreateBase.status_code, 201)

    def testGetPatchDeleteBase(self):
        user = User.objects.get(email='test1@test.ru')
        c1 = Client()
        respNoAuth1 = c1.get('/api/v1/bases/'+str(self.noPublicBase.base_id)+'/')
        self.assertEqual(respNoAuth1.status_code, 401)
        respNoAuth2 = c1.get('/api/v1/bases/'+str(self.publicBase.base_id)+'/')
        self.assertEqual(respNoAuth2.status_code, 200)
        respNoAuth3 = c1.get('/api/v1/bases/'+str(self.copiedBase.base_id)+'/')
        self.assertEqual(respNoAuth3.status_code, 401)
        c1.force_login(user)
        respAuth = c1.get('/api/v1/bases/'+str(self.noPublicBase.base_id)+'/')
        serializer = BaseFullSerializer(self.noPublicBase)
        self.assertEqual(respAuth.status_code, 200)
        self.assertEqual(serializer.data, respAuth.data)
        respPatch1 = c1.patch('/api/v1/bases/' + str(self.publicBase.base_id) + '/',
                              data=json.dumps({'title': 'New Title'}),
                              content_type='application/json')
        self.assertEqual(respPatch1.status_code, 200)
        self.assertEqual(respPatch1.data['title'], 'New Title')
        respDelete1 = c1.delete('/api/v1/bases/' + str(self.publicBase.base_id) + '/')
        self.assertEqual(respDelete1.status_code, 204)
        
