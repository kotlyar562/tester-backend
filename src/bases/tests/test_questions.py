from django.test import TestCase
from src.accounts.models import User
from src.bases.models import QuestBase, Question, QuestionSettings, AnswerOneAsk, AnswerManyAsk, AnswerInput, AnswerOrdering


class GetAnswersTest(TestCase):

    def setUp(self):
        user = User.objects.create(email="test@test.ru", password="12345678")
        base = QuestBase.objects.create(user=user, title="test base")
        self.question = Question.objects.create(base=base, qtype=0, text="Text")
        AnswerOneAsk.objects.create(question=self.question, text="Answer 1", its_true=False)
        AnswerOneAsk.objects.create(question=self.question, text="Answer 2", its_true=True)

    def testGetAnswerFunction(self):
        answers = AnswerOneAsk.objects.filter(question=self.question)
        self.assertEqual(list(answers), self.question.getAnswers())

class OneAnswerTest(TestCase):
    """ Test for questions with one answer variant"""

    def setUp(self):
        user = User.objects.create(email="test@test.ru", password="12345678")
        base = QuestBase.objects.create(user=user, title="test base")
        self.questionOneAnswer = Question.objects.create(base=base, qtype=0,
                                    number=1, text="One Answer Quest")
        QuestionSettings.objects.create(question=self.questionOneAnswer)
        self.trueAnswer = AnswerOneAsk.objects.create(question=self.questionOneAnswer,
                                      number=1, text="True Answer", its_true=True)
        self.wrongAnswer = AnswerOneAsk.objects.create(question=self.questionOneAnswer,
                                      number=2, text="Wrong Answer", its_true=False)

    def testCheckOneAnswer(self):
        self.assertEqual(self.questionOneAnswer.checkQuestion(self.trueAnswer.pk), 1)
        self.assertEqual(self.questionOneAnswer.checkQuestion(self.wrongAnswer.pk), 0)
        self.assertEqual(self.questionOneAnswer.checkQuestion(100), 0)
        self.assertEqual(self.questionOneAnswer.checkQuestion(), 0)
        self.assertEqual(self.questionOneAnswer.checkQuestion("text"), 0)


class ManyAnswersTest(TestCase):

    def setUp(self):
        user = User.objects.create(email="test@test.ru", password="12345678")
        base = QuestBase.objects.create(user=user, title="test base")
        self.questionManyAnswer = Question.objects.create(base=base, qtype=1,
                                            number=1, text="Many Answer Quest")
        QuestionSettings.objects.create(question=self.questionManyAnswer)
        self.trueAnswer1 = AnswerManyAsk.objects.create(question=self.questionManyAnswer,
                            number=1, text="AnswerMany 1", its_true=True)
        self.trueAnswer2 = AnswerManyAsk.objects.create(question=self.questionManyAnswer,
                            number=2, text="AnswerMany 2", its_true=True)
        self.wrongAnswer = AnswerManyAsk.objects.create(question=self.questionManyAnswer,
                            number=3, text="AnswerMany 3", its_true=False)

    def testCheckManyAnswer(self):
        pk1, pk2, pk3 = self.trueAnswer1.pk, self.trueAnswer2.pk, self.wrongAnswer.pk
        self.assertEqual(self.questionManyAnswer.checkQuestion([pk1, pk2]), 1)
        self.assertEqual(self.questionManyAnswer.checkQuestion([pk1]), 0.5)
        self.assertEqual(self.questionManyAnswer.checkQuestion([pk1, pk2, pk3]), 0.5)
        self.assertEqual(self.questionManyAnswer.checkQuestion([pk1, pk2, 1000]), 0.5)
        self.assertEqual(self.questionManyAnswer.checkQuestion([pk3]), 0)
        self.assertEqual(self.questionManyAnswer.checkQuestion([]), 0)
        self.assertEqual(self.questionManyAnswer.checkQuestion([1000]), 0)
        self.assertEqual(self.questionManyAnswer.checkQuestion(["text1", "text2"]), 0)


class InputAnswerTest(TestCase):

    def setUp(self):
        user = User.objects.create(email="test@test.ru", password="12345678")
        base = QuestBase.objects.create(user=user, title="test base")
        self.questionInputText = Question.objects.create(base=base, qtype=2,
                                number=1, text="Input Answer")
        QuestionSettings.objects.create(question=self.questionInputText)
        self.answerText = AnswerInput.objects.create(question=self.questionInputText,
                        true_answer="NoReGisTer", is_register_dependent=False)
        self.answerRegisterText = AnswerInput.objects.create(question=self.questionInputText,
                        true_answer="ReGisTer", is_register_dependent=True)
        self.answerInteger = AnswerInput.objects.create(question=self.questionInputText,
                        true_answer="123", is_integer_number=True)
        self.answerFloat = AnswerInput.objects.create(question=self.questionInputText,
                        true_answer="0.9", is_float_number=True)

    def testCheckInputTextAnswer(self):
        print("test input answer question")
        self.assertEqual(self.questionInputText.checkQuestion("NoRegister"), 1)
        self.assertEqual(self.questionInputText.checkQuestion("noregister"), 1)
        self.assertEqual(self.questionInputText.checkQuestion("NOREGISTER"), 1)
        self.assertEqual(self.questionInputText.checkQuestion("No Register"), 0)
        self.assertEqual(self.questionInputText.checkQuestion("WrongAnswer"), 0)
        self.assertEqual(self.questionInputText.checkQuestion(""), 0)

    def testCheckInputRegisterAnswer(self):
        print("test input register dependent answer question")
        self.assertEqual(self.questionInputText.checkQuestion("ReGisTer"), 1)
        self.assertEqual(self.questionInputText.checkQuestion("register"), 0)
        self.assertEqual(self.questionInputText.checkQuestion("REGISTER"), 0)
        self.assertEqual(self.questionInputText.checkQuestion("Wrong"), 0)
        self.assertEqual(self.questionInputText.checkQuestion(""), 0)

    def testCheckInputIntegerAnswer(self):
        print("test input integer answer question")
        self.assertEqual(self.questionInputText.checkQuestion("123"), 1)
        self.assertEqual(self.questionInputText.checkQuestion("124"), 0)
        self.assertEqual(self.questionInputText.checkQuestion(123), 1)
        self.assertEqual(self.questionInputText.checkQuestion("123.00"), 0)
        self.assertEqual(self.questionInputText.checkQuestion(), 0)
        self.assertEqual(self.questionInputText.checkQuestion("text"), 0)

    def testCheckInputFloatAnswer(self):
        print("test input float answer question")
        self.assertEqual(self.questionInputText.checkQuestion("0.9"), 1)
        self.assertEqual(self.questionInputText.checkQuestion(0.9), 1)
        self.assertEqual(self.questionInputText.checkQuestion("0.9000"), 1)
        self.assertEqual(self.questionInputText.checkQuestion(0.9000), 1)
        self.assertEqual(self.questionInputText.checkQuestion(1), 0)
        self.assertEqual(self.questionInputText.checkQuestion(), 0)
        self.assertEqual(self.questionInputText.checkQuestion("text"), 0)


class OrderAnswerTest(TestCase):

    def setUp(self):
        user = User.objects.create(email="test@test.ru", password="12345678")
        base = QuestBase.objects.create(user=user, title="test base")
        self.questionOrder = Question.objects.create(base=base, qtype=3,
                                number=1, text="Order Answer")
        QuestionSettings.objects.create(question=self.questionOrder)
        self.answer1 = AnswerOrdering.objects.create(question=self.questionOrder,
                                order_number=1, text="order 1")
        self.answer2 = AnswerOrdering.objects.create(question=self.questionOrder,
                                order_number=2, text="order 2")
        self.answer3 = AnswerOrdering.objects.create(question=self.questionOrder,
                                order_number=3, text="order 3")

    def testCheckOrderAnswer(self):
        pk1, pk2, pk3 = self.answer1.pk, self.answer2.pk, self.answer3.pk
        self.assertEqual(self.questionOrder.checkQuestion([pk1, pk2, pk3]), 1)
        self.assertEqual(self.questionOrder.checkQuestion([pk2, pk1, pk3]), 0)
        self.assertEqual(self.questionOrder.checkQuestion([pk1, pk2, pk2]), 0)
        self.assertEqual(self.questionOrder.checkQuestion([pk1, pk2]), 0)
        self.assertEqual(self.questionOrder.checkQuestion([]), 0)
