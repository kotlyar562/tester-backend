import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.accounts.models import User


class Folder(models.Model):
    """ Пользовательская папка с базами вопросов """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('Пользователь'))
    title = models.CharField(_('Название'), max_length=250)
    color = models.CharField(_('Цвет'), max_length=20, default='white')

    class Meta:
        verbose_name = _('Каталог')
        verbose_name_plural = _('Каталоги')

    def __str__(self):
        return self.title


class QuestBase(models.Model):
    """ Пользовательская база вопросов """
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             verbose_name=_('Пользователь'),
                             blank=True, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL,
                               verbose_name=_('Каталог'),
                               blank=True, null=True)
    base_id = models.UUIDField(_('Base UUID'), default=uuid.uuid4, unique=True,
                               editable=False)
    title = models.CharField(_('Название базы вопросов'), max_length=250)
    klass = models.CharField(_('Класс'), max_length=100, blank=True, null=True)
    discipline = models.CharField(_('Учебный предмет'), max_length=100,
                                  blank=True, null=True)
    description = models.TextField(_('Описание'), blank=True, null=True)
    rating = models.IntegerField(_('Рейтинг'), default=0)
    copi_count = models.IntegerField(_('Скопировали раз'), default=0)
    premium = models.BooleanField(_('Премиумная'), default=False)
    copied = models.BooleanField(_('Скопированная'), default=False)
    publik = models.BooleanField(_('Опубликованная'), default=False,
                help_text=_('Разрешить другим '
                'пользователям просматривать и копировать себе базу вопросов'))
    good = models.BooleanField(_('Одобрено'), default=False)
    date_create = models.DateField(_('Дата создания'), auto_now_add=True)
    date_change = models.DateField(_('Дата редактирования'), auto_now=True)

    class Meta:
        verbose_name = _('Пользовательская база вопросов')
        verbose_name_plural = _('Пользовательские базы вопросов')

    def __str__(self):
        return self.title

    def inc_rating(self):
        self.rating += 1
        self.save()

    def dec_rating(self):
        self.rating -= 1
        self.save()
