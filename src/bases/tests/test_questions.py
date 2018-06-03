from django.test import TestCase
from src.accounts.models import User
from src.bases.models.bases import QuestBase
from src.bases.models.questions import Question, QuestionSettings
from src.bases.models.answers import AnswerOneAsk, AnswerManyAsk, AnswerInput, AnswerOrdering


class QuestionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="test@test.ru", password="12345678")
        base = QuestBase.objects.create(user=user, title="test base")
        questionOneAnswer = Question.objects.create(base=base, qtype=0, #1
                                    number=1, text="One Answer Quest")
        QuestionSettings.objects.create(question=questionOneAnswer)

        questionManyAnswer = Question.objects.create(base=base, qtype=1, #2
                                    number=2, text="Many Answer Quest")
        QuestionSettings.objects.create(question=questionManyAnswer)

        questionInputTextAnswer = Question.objects.create(base=base, qtype=2, #3
                                    number=3, text="Input Text Answer Quest")
        QuestionSettings.objects.create(question=questionInputTextAnswer)

        questionInputRegisterTextAnswer = Question.objects.create(base=base, #4
                                    qtype=2, number=4,
                                    text="Input Register Text Answer Quest")
        QuestionSettings.objects.create(question=questionInputRegisterTextAnswer)

        questionInputIntegerAnswer = Question.objects.create(base=base, qtype=2, #5
                                    number=5, text="Input Integer Answer Quest")
        QuestionSettings.objects.create(question=questionInputIntegerAnswer)

        questionInputFloatAnswer = Question.objects.create(base=base, qtype=2, #6
                                    number=6, text="Input Float Answer Quest")
        QuestionSettings.objects.create(question=questionInputFloatAnswer)

        questionOrderAnswer = Question.objects.create(base=base, qtype=3, #7
                                    number=7, text="Ordering Answer Quest")
        QuestionSettings.objects.create(question=questionOrderAnswer)

        AnswerInput.objects.create(question=questionInputTextAnswer, number=1,
                                   true_answer="Answer1") #1
        AnswerInput.objects.create(question=questionInputTextAnswer, number=2,
                                   true_answer="Answer2") #2

        AnswerInput.objects.create(question=questionInputRegisterTextAnswer, number=1,
                                   true_answer="Answer1",
                                   is_register_dependent=True) #3
        AnswerInput.objects.create(question=questionInputRegisterTextAnswer, number=2,
                                   true_answer="Answer2",
                                   is_register_dependent=True) #4

        AnswerInput.objects.create(question=questionInputIntegerAnswer, number=1,
                                   true_answer="23")      #5
        AnswerInput.objects.create(question=questionInputIntegerAnswer, number=2,
                                   true_answer="0")      #6

        AnswerInput.objects.create(question=questionInputFloatAnswer, number=1,
                                   true_answer="2.4",
                                   is_float_number=True) #7
        AnswerInput.objects.create(question=questionInputFloatAnswer, number=2,
                                   true_answer="0",
                                   is_float_number=True) #8
        for i in range(6):
            AnswerOneAsk.objects.create(question=questionOneAnswer, number=i+1,
                                        text="Answer0"+str(i), its_true=(i==0)) #9
            AnswerManyAsk.objects.create(question=questionManyAnswer, number=i+1,
                                         text="Answer1"+str(i), its_true=(i%2==0)) #10
            AnswerOrdering.objects.create(question=questionOrderAnswer, number=i+1,
                                        order_number=i+1, text="Answer"+str(i)) #11...

    def testChekOneAnswer(self):
        print("test check one answer question")
        question = Question.objects.get(pk=1)
        self.assertEqual(question.checkQuestion(9), 1)
        self.assertEqual(question.checkQuestion(4), 0)
        self.assertEqual(question.checkQuestion(100), 0)
        self.assertEqual(question.checkQuestion(), 0)
        self.assertEqual(question.checkQuestion("text"), 0)

    def testCheckManyAnswer(self):
        print("test check many answer question")
        question = Question.objects.get(pk=2)
        self.assertEqual(question.checkQuestion([10, 16, 22]), 1)
        self.assertEqual(question.checkQuestion([10, 16]), 0.5)
        self.assertEqual(question.checkQuestion([10, 16, 22, 9]), 0.5)
        self.assertEqual(question.checkQuestion([10, 16, 22, 100]), 0.5)
        self.assertEqual(question.checkQuestion([10]), 0)
        self.assertEqual(question.checkQuestion([]), 0)
        self.assertEqual(question.checkQuestion([100]), 0)
        self.assertEqual(question.checkQuestion(["10", "16", "22"]), 0)
        self.assertEqual(question.checkQuestion(["test1", "test2"]), 0)

    def testCheckInputTextAnswer(self):
        print("test input answer question")
        question = Question.objects.get(pk=3)
        self.assertEqual(question.checkQuestion("Answer1"), 1)
        self.assertEqual(question.checkQuestion(" Answer1 "), 1)
        self.assertEqual(question.checkQuestion("answer1"), 1)
        self.assertEqual(question.checkQuestion("Answer2"), 1)
        self.assertEqual(question.checkQuestion(""), 0)

    def testCheckInputRegisterAnswer(self):
        print("test input register dependent answer question")
        question = Question.objects.get(pk=4)
        self.assertEqual(question.checkQuestion("Answer1"), 1)
        self.assertEqual(question.checkQuestion("  Answer2 "), 1)
        self.assertEqual(question.checkQuestion("answer1"), 0)
        self.assertEqual(question.checkQuestion("AnsweR2"), 0)
        self.assertEqual(question.checkQuestion(""), 0)

    def testCheckInputIntegerAnswer(self):
        print("test input integer answer question")
        question = Question.objects.get(pk=5)
        self.assertEqual(question.checkQuestion("23"), 1)
        self.assertEqual(question.checkQuestion("0"), 1)
        self.assertEqual(question.checkQuestion(23), 1)
        self.assertEqual(question.checkQuestion(0), 1)
        self.assertEqual(question.checkQuestion(23.1), 0)
        self.assertEqual(question.checkQuestion(), 0)
        self.assertEqual(question.checkQuestion("text"), 0)

    def testCheckInputFloatAnswer(self):
        print("test input float answer question")
        question = Question.objects.get(pk=6)
        self.assertEqual(question.checkQuestion(2.4), 1)
        self.assertEqual(question.checkQuestion(0), 1)
        self.assertEqual(question.checkQuestion("2.4"), 1)
        self.assertEqual(question.checkQuestion("0"), 1)
        self.assertEqual(question.checkQuestion(2.4000), 1)
        self.assertEqual(question.checkQuestion(0000), 1)
        self.assertEqual(question.checkQuestion(24), 0)
        self.assertEqual(question.checkQuestion(), 0)

    def testCheckOrderAnswer(self):
        print("test input ordering answer question")
        question = Question.objects.get(pk=7)
        self.assertEqual(question.checkQuestion([1, 2, 3, 4, 5, 6]), 1)
        self.assertEqual(question.checkQuestion(["1", "2", "3", "4", "5", "6"]), 0)
        self.assertEqual(question.checkQuestion([1, 2, 3, 4, 5]), 0)
        self.assertEqual(question.checkQuestion([2, 1, 3, 4, 5, 6]), 0)
        self.assertEqual(question.checkQuestion([1, 2, 3, 4, 5, 10]), 0)
        self.assertEqual(question.checkQuestion(["text1", 2, 3, 4, 5, 6]), 0)
