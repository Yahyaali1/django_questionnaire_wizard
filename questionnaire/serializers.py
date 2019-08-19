from rest_framework import serializers


class QuestionnaireListSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField()
    title = serializers.CharField()


class ResponseLogSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()
