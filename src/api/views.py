from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from src.accounts.models import User
from src.bases.models import QuestBase, Question, \
    AnswerOneAsk, AnswerManyAsk, AnswerInput, AnswerOrdering
from src.api.serializers.user_serializer import UserInfoSerializer
from src.api.serializers.bases_serializer import BaseShortInfoSerializer, BaseFullSerializer, QuestionSerializer, \
    AnswerOneAskSerializer, AnswerManyAskSerializer, \
    AnswerInputSerializer, AnswerOrderingSerializer
from . permissions import IsOwnerOrIsPublic


class UserBases(generics.ListCreateAPIView):
    """Список всех баз вопросов аторизованного пользователя"""
    queryset = QuestBase.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BaseShortInfoSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        serialisers = BaseShortInfoSerializer(self.queryset, many=True)
        return Response(serialisers.data)

    def post(self, request, *args, **kwargs):
        """Создание новой базы вопросов"""
        serializer = BaseShortInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestBaseView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение, удаление конкретной базы вопросов пользователя"""
    queryset = QuestBase.objects.all()
    permission_classes = [IsOwnerOrIsPublic]
    serializer_class = BaseFullSerializer

    def get(self, request, base_id, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        self.check_object_permissions(self.request, base)
        serializer = BaseFullSerializer(base)
        return Response(serializer.data)

    def patch(self, request, base_id, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        self.check_object_permissions(self.request, base)
        serializer = BaseShortInfoSerializer(instance=base, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, base_id, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        self.check_object_permissions(self.request, base)
        base.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def create_answers(quest, answers):
    if quest.qtype == 0:
        for answer in answers:
            serializer = AnswerOneAskSerializer(data=answer)
            if serializer.is_valid():
                serializer.save(question=quest)
    elif quest.qtype == 1:
        for answer in answers:
            serializer = AnswerManyAskSerializer(data=answer)
            if serializer.is_valid():
                serializer.save(question=quest)
    elif quest.qtype == 2:
        for answer in answers:
            serializer = AnswerInput(data=answer)
            if serializer.is_valid():
                serializer.save(question=quest)
    elif quest.qtype == 3:
        for answer in answers:
            serializer = AnswerOrderingSerializer(data=answer)
            if serializer.is_valid():
                serializer.save(question=quest)

class BaseQuestions(generics.ListCreateAPIView):
    """Просмотр всех вопросов и создание нового вопроса"""
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def get(self, request, base_id, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        if base.user == request.user:
            questions = base.questions.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, base_id, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(base=base)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BaseQuestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def get(self, request, base_id, quest_pk, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        question = get_object_or_404(Question, pk=quest_pk)
        if base.user == request.user and question.base == base:
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, base_id, quest_pk, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        question = get_object_or_404(Question, pk=quest_pk)
        if base.user == request.user and question.base == base:
            serializer = QuestionSerializer(instance=question, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, base_id, quest_pk, *args, **kwargs):
        base = get_object_or_404(QuestBase, base_id=base_id)
        question = get_object_or_404(Question, pk=quest_pk)
        if base.user == request.user and question.base == base:
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
