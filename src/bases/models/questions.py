from django.db import models
from django.utils.translation import gettext_lazy as _
from . bases import QuestBase


TYPES = (
    (0, _('Один вариант ответа')),
    (1, _('Несколько вариантов ответа')),
    (2, _('Ввод ответа')),
    (3, _('Установить порядок следования')),
)


class Question(models.Model):
    base = models.ForeignKey(QuestBase, on_delete=models.CASCADE,
                             verbose_name=_('База вопросов'),
                             related_name='questions')
    group = models.CharField(_('Группа'), max_length=100, default=_('Группа 1'),
                             help_text=_('Разбиение вопросов'
                             ' на группы используется при создании тестов') )
    qtype = models.IntegerField(_('Тип вопроса'), choices=TYPES, default=0)
    number = models.IntegerField(_('Номер вопроса'), default=1)
    text = models.TextField(_('Текст вопроса'))
    help_text = models.TextField(_('Комментарий, подсказка'),
                             blank=True, null=True)

    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'
        ordering = ('number',)

    def __str__(self):
        return self.text

    def checkOneAnswer(self, answer_pk):
        try:
            answer = self.answers.get(pk=answer_pk)
            if answer.answeroneask.its_true:
                return self.questionsettings.ball
            else:
                return 0
        except:
                return 0
        return 0

    def checkManyAnswer(self, answers_array):
        error_count = 0
        user_answers = set(answers_array)
        true_answers = []
        for ans in self.answers.all():
            if ans.answermanyask.its_true:
                true_answers.append(ans.answermanyask.pk)
        true_answers = set(true_answers)
        error_count = len((user_answers | true_answers) - (user_answers & true_answers))
        if error_count == 0:
            return self.questionsettings.ball
        elif error_count == 1:
            return self.questionsettings.ball / 2
        else:
            return 0

    def checkAnswerInput(self, answer):
        answer = str(answer).strip()
        true_answers = self.answers.all()
        for ans in true_answers:
            if ans.answerinput.true_answer.strip() == answer:
                return self.questionsettings.ball
            elif (not ans.answerinput.is_register_dependent == True) and ans.answerinput.true_answer.strip().lower() == answer.lower():
                return self.questionsettings.ball
            elif ans.answerinput.is_integer_number == True:
                try:
                    if int(ans.answerinput.true_answer) == int(answer):
                        return self.questionsettings.ball
                    else:
                        return 0
                except:
                    pass
            elif ans.answerinput.is_float_number:
                try:
                    if float(ans.answerinput.true_answer) == float(answer):
                        return self.questionsettings.ball
                    else:
                        return 0
                except:
                    return 0
        return 0

    def checkOrdering(self, answer_array):
        true_answers = [answer.answerordering.pk for answer in self.answers.all()]
        if len(true_answers) != len(answer_array):
            return 0
        for i in range(len(true_answers)):
            if true_answers[i] != answer_array[i]:
                return 0
        else:
            return self.questionsettings.ball

    def checkQuestion(self, answer=None):
        if answer == None or answer == "" or answer == []:
            return 0
        if self.qtype == 0:
            return self.checkOneAnswer(answer) #answer - pk number
        elif self.qtype == 1:
            return self.checkManyAnswer(answer) #answer - array of pk
        elif self.qtype == 2:
            return self.checkAnswerInput(answer) #answer - string
        elif self.qtype == 3:
            return self.checkOrdering(answer) #answer - array of pk
        else:
            return 0

    def getAnswers(self):
        answers = self.answers.all()
        if self.qtype == 0:
            return [answer.answeroneask for answer in answers]
        if self.qtype == 1:
            return [answer.answermanyask for answer in answers]
        if self.qtype == 0:
            return [answer.answerinput for answer in answers]
        if self.qtype == 0:
            return [answer.answerordering for answer in answers]


class QuestionSettings(models.Model):
    question = models.OneToOneField(Question, verbose_name=_('Вопрос'),
                                on_delete=models.CASCADE)
    ball = models.IntegerField(_('Баллов за правильный ответ на вопрос'),
                                default=1)
    quest_time = models.PositiveIntegerField(_('Время для ответа на этот вопрос'),
                                default=0,
                                help_text=_('В секундах, 0 - неограничено'))
    random_answers = models.BooleanField(_('Варианты ответов в случайном порядке'),
                                default=True)

    class Meta:
        verbose_name = _('Настройки вопроса')
        verbose_name_plural = _('Настройки вопросов')

    def __str__(self):
        return self.quest.text[:20] + ' settings'
