from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .data_wrapper import get_questionnaire_list, get_question_by_id, get_first_question
from .serializers import QuestionnaireListSerializer, QuestionSerializer


class FetchListApi(APIView):
    def get(self, args):
        data_list = get_questionnaire_list()
        if not data_list:
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)
        serialized_data = QuestionnaireListSerializer(
            data_list, many=True).data
        return Response(data=serialized_data, status=status.HTTP_200_OK)


# TODO cases for input variables
# TODO case to reterive and update data in session object
# TODO log once the answer object is empty for next question


def submit(request, questionnaire_id, question_id=None, answer_id=None):
    serialized_data = QuestionSerializer(
        get_first_question(2)).data
    return HttpResponse(JSONRenderer().render(serialized_data))
