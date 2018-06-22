from rest_framework import serializers
from src.bases.models import QuestBase, Folder, \
    Question, QuestionSettings, \
    AnswerOneAsk, AnswerManyAsk, AnswerInput, AnswerOrdering


class AnswerOneAskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOneAsk
        fields = ('pk', 'number', 'text', 'its_true')


class AnswerManyAskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerManyAsk
        fields = ('pk', 'number', 'text', 'its_true')


class AnswerInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerInput
        fields = ('pk', 'number', 'true_answer', 'is_register_dependent',
                  'is_integer_number', 'is_float_number')


class AnswerOrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOrdering
        fields = ('pk', 'number', 'order_number', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    """Вопрос вместе с вариантами ответов, которые отличаются в зависимости от типа вопроса"""

    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('pk', 'group', 'qtype', 'number', 'text', 'help_text', 'answers')
        read_only_fields = ('pk', 'answers')

    def get_answers(self, obj):
        if obj.qtype == 0:
            return AnswerOneAskSerializer(obj.getAnswers(), many=True).data
        elif obj.qtype == 1:
            return AnswerManyAskSerializer(obj.getAnswers(), many=True).data
        elif obj.qtype == 2:
            return AnswerInputSerializer(obj.getAnswers(), many=True).data
        elif obj.qtype == 3:
            return AnswerOrderingSerializer(obj.getAnswers(), many=True).data

class BaseShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestBase
        fields = ('base_id', 'title', 'klass', 'discipline', 'description', 'date_create',
                  'rating', 'copi_count', 'premium', 'copied', 'publik')
        read_only_fields = ('base_id', 'rating', 'copi_count', 'date_create',
                            'rating', 'copi_count', 'premium', 'copied')


class BaseFullSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = QuestBase
        fields = ('base_id', 'title', 'klass', 'discipline', 'description',
                  'date_create', 'date_change', 'rating', 'copi_count',
                  'premium', 'copied', 'publik', 'questions')
        read_only_fields = ('base_id', 'rating', 'copi_count', 'date_create',
                            'date_change', 'rating', 'copi_count', 'premium',
                            'copied', 'questions')
