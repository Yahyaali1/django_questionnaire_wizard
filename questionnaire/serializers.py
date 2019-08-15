from rest_framework import serializers


class QuestionnaireListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class AnswerSerializer(serializers.Serializer):
    answer_text = serializers.CharField()
    next_question_id = serializers.IntegerField()


class QuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    question_text = serializers.CharField()
    questionnaire_id = serializers.IntegerField()
    answers = serializers.ListField(child=AnswerSerializer())
