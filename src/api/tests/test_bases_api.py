import json
from django.test import TestCase
from src.accounts.models import User
from src.bases.models import QuestBase, Question, AnswerOneAsk
from django.test import Client
from .. serializers.bases_serializer import BaseShortInfoSerializer, BaseFullSerializer, \
    QuestionSerializer, AnswerOneAskSerializer

class BasesApiTest(TestCase):

    def setUp(self):
        u = User.objects.create(email='test1@test.ru', password='12345678')
        u.is_active = True
        u.save()
        # u2 = User.objects.create(email='test2@test.ru', password='12345678')
        # u2.is_active = True
        # u2.save()
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


class QuestionsApiTest(TestCase):

    def setUp(self):
        user = User.objects.create(email='test1@test.ru', password='12345678')
        user.is_active = True
        user.save()
        self.base = QuestBase.objects.create(title='Test Base', user=user)
        self.quest0 = Question.objects.create(base=self.base, qtype=0, text='Any Answer')
        self.quest1 = Question.objects.create(base=self.base, qtype=1, text='Many Answer')
        self.quest2 = Question.objects.create(base=self.base, qtype=2, text='Input Answer')

    def testGetPostQurst(self):
        user = User.objects.get(email='test1@test.ru')
        c = Client()
        c.force_login(user)
        respGet = c.get('/api/v1/bases/' + str(self.base.base_id) + '/questions/')
        self.assertEqual(respGet.status_code, 200)
        questions = Question.objects.filter(base=self.base)
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(serializer.data, respGet.data)
        respPost = c.post('/api/v1/bases/' + str(self.base.base_id) + '/questions/',
                        data=json.dumps({'qtype': 3, 'text': 'Quest Text'}),
                        content_type='application/json')
        self.assertEqual(respPost.status_code, 201)
        self.assertEqual(respPost.data['text'], 'Quest Text')

    def testGetPatchDeleteQuest(self):
        user = User.objects.get(email='test1@test.ru')
        c = Client()
        c.force_login(user)
        respGet = c.get('/api/v1/bases/%s/questions/%s/' % (str(self.base.base_id), str(self.quest0.pk)))
        self.assertEqual(respGet.status_code, 200)
        serializer = QuestionSerializer(self.quest0)
        self.assertEqual(serializer.data, respGet.data)
        respPatch = c.patch('/api/v1/bases/%s/questions/%s/' % (str(self.base.base_id), str(self.quest0.pk)),
                           data=json.dumps({'qtype': 1, 'text': 'New Text'}),
                           content_type='application/json')
        self.assertEqual(respPatch.status_code, 200)
        self.assertEqual(respPatch.data['qtype'], 1)
        respDelete = c.delete('/api/v1/bases/%s/questions/%s/' % (str(self.base.base_id), str(self.quest0.pk)))
        self.assertEqual(respDelete.status_code, 204)


class AnswersApiTest(TestCase):

    def setUp(self):
        user = User.objects.create(email='test1@test.ru', password='12345678')
        user.is_active = True
        user.save()
        self.base = QuestBase.objects.create(title='Test Base', user=user)
        self.question = Question.objects.create(base=self.base, text="Qustion Text")
        self.answer1 = AnswerOneAsk.objects.create(question=self.question, text="Answer 1",
                                                   its_true=True)
        self.answer2 = AnswerOneAsk.objects.create(question=self.question, text="Answer 2",
                                                   its_true=False)

    def testGetPostAnswers(self):
        user = User.objects.get(email='test1@test.ru')
        c = Client()
        c.force_login(user)
        respGet = c.get('/api/v1/bases/%s/questions/%s/answers/' % (str(self.base.base_id), str(self.question.pk)))
        self.assertEqual(respGet.status_code, 200)
        serializer = AnswerOneAskSerializer(self.question.getAnswers(), many=True)
        self.assertEqual(serializer.data, respGet.data)
        respPost = c.post('/api/v1/bases/%s/questions/%s/answers/' % (str(self.base.base_id), str(self.question.pk)),
                          data=json.dumps({"text": "New Answer", "its_true": False}),
                          content_type='application/json')
        self.assertEqual(respPost.status_code, 201)
        self.assertEqual(respPost.data['text'], 'New Answer')
