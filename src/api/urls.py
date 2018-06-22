from django.urls import path, include
from rest_framework import routers
from . views import UserBases, QuestBaseView, BaseQuestions, BaseQuestionView, \
    QuestAnswers, QuestAnswerView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('bases/user/', UserBases.as_view()), #bases for user profile
    path('bases/<uuid:base_id>/', QuestBaseView.as_view()), #one base actions

    path('bases/<uuid:base_id>/questions/', BaseQuestions.as_view()),
    path('bases/<uuid:base_id>/questions/<int:quest_pk>/', BaseQuestionView.as_view()),

    path('bases/<uuid:base_id>/questions/<int:quest_pk>/answers/', QuestAnswers.as_view()),
    path('bases/<uuid:base_id>/questions/<int:quest_pk>/answers/<int:answer_pk>/', QuestAnswerView.as_view()),
    # path('bases/<pk>/questions/<quest_pk>/', MyQuestion.as_view()),
    #
    # path('bases/<pk>/questions/delete/', MyQuestionsDelete.as_view())
]
