from django.urls import path, include
from rest_framework import routers
from . views import UserBases, QuestBaseView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('bases/user/', UserBases.as_view()), #bases for user profile
    path('bases/<pk>/', QuestBaseView.as_view()), #one base actions
    # path('bases/<pk>/questions/', MyQuestions.as_view()),
    #
    # path('bases/<pk>/questions/<quest_pk>/', MyQuestion.as_view()),
    #
    # path('bases/<pk>/questions/delete/', MyQuestionsDelete.as_view())
]
