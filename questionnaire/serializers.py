from rest_framework import serializers


class QuestionnaireListSerializer(serializers.Serializer):
    """
    Prepares questionnaire object for json response
    """
    questionnaire_id = serializers.IntegerField()
    title = serializers.CharField()


class ResponseLogSerializer(serializers.Serializer):
    """
    Prepares ResponseModelForLog to be stored in 
    response object under session 
    """
    questionnaire_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()
