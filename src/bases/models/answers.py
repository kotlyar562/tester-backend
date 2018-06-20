from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from . questions import Question


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                             verbose_name=_('Вопрос'), related_name='answers')
    number = models.IntegerField(_("Номер"), default=1)

    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответов')
        ordering = ('number',)

    def __str__(self):
        return self.question.text[:20]


class AnswerOneAsk(Answer):
    """ Один вариант ответа """
    text = models.TextField(_('Текст'))
    its_true = models.BooleanField(_('Правильный ответ'), default=False)

    class Meta:
        verbose_name = _('Один вариант ответа')
        verbose_name_plural = _('Один вариант ответа')

    def __str__(self):
        return self.text[:50]


class AnswerManyAsk(Answer):
    """Несколько вариантов ответов"""
    text = models.TextField(_('Текст'))
    its_true = models.BooleanField(_("Правильный ответ"), default=False)

    class Meta:
        verbose_name = _("Несколько вариантов ответа")
        verbose_name_plural = _("Несколько вариантов ответа")

    def __str__(self):
        return self.text[:50]


class AnswerInput(Answer):
    """Ввод ответа"""
    true_answer = models.CharField(_("Правильный ответ"), max_length=100)
    is_register_dependent = models.BooleanField(_("Регистрозависимый текст?"),
                        default=False)
    is_integer_number = models.BooleanField(_("Целое число?"), default=False)
    is_float_number = models.BooleanField(_("Вещественное число?"),
                        default=False, help_text=_("Используйте точку вместо запятой"))

    class Meta:
        verbose_name = _('Ввод ответа')
        verbose_name_plural = _('Ввод ответа')

    def __str__(self):
        return self.true_answer


class AnswerOrdering(Answer):
    order_number = models.PositiveIntegerField(_('Порядковый номер'), default=1)
    text = models.TextField(_('Текст'))

    class Meta:
        verbose_name = _('Элемент по порядку')
        verbose_name_plural = _("Элементы по порядку")
        ordering = ('order_number',)

    def __str__(self):
        return self.text[:50]


# class AnswerAccord(Answer):
#     title1 = models.CharField(_('Название первого списка'), max_length=100)
#     title2 = models.CharField(_('Название второго списка'), max_length=100)
#
#     class Meta:
#         verbose_name = _('Установить соответсвие')
#         verbose_name_plural = _("Установить соответсвия")
#
#     def __str__(self):
#         return '%s - %s' % (self.title1, self.title2)
#
#     def cheking(self, data):
#         #todo cheking and tests this function
#         """data - object of key - pk from first column, value - list from second column"""
#         first_list = self.firstcol.all()
#         for key in data.keys():
#             try:
#                 first_list_item = first_list.get(pk=key)
#                 set_true = set(first_list_item.answeraccordsecondcolumn_set.all())
#                 set_answer = set(data[key])
#                 res = set_true - set_answer
#                 return self.answer_ball if len(res) else 0
#             except:
#                 return 0
#
#
# class AnswerAccordFirstColumn(models.Model):
#     answer = models.ForeignKey(AnswerAccord, verbose_name=_("Установить соответствие"),
#                                on_delete=models.CASCADE, related_name='firstcol')
#     text = models.TextField(_('Текст'))
#     number = models.IntegerField(_('Номер'), default=0)
#
#     class Meta:
#         db_table = 'firstcol'
#         verbose_name = _("Элемент первого списка")
#         verbose_name_plural = _("Элементы первого списка")
#
#     def __str__(self):
#         return self.text[:50]
#
#
# class AnswerAccordSecondColumn(models.Model):
#     answer = models.ForeignKey(AnswerAccord, verbose_name=_("Установить соответствие"),
#                                on_delete=models.CASCADE, related_name='secondcol')
#     text = models.TextField(_('Текст'))
#     number = models.IntegerField(_('Номер'), default=0)
#     links = models.ManyToManyField(AnswerAccordFirstColumn, verbose_name=_("Соответствующий элемент"), blank=True)
#
#     class Meta:
#         db_table = 'secondcol'
#         verbose_name = _("Элемент второго списка")
#         verbose_name_plural = _("Элементы второго списка")
