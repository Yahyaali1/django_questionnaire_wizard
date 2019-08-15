from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .data_wrapper import get_questionnaire_list, get_question_by_id, get_first_question, get_next_question_by_answer_id
from .serializers import QuestionnaireListSerializer, QuestionSerializer

import json


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
    if question_id is None and answer_id is None:
        response = get_first_question(str(questionnaire_id))
    elif question_id is not None and answer_id is None:
        response = get_question_by_id(str(questionnaire_id), str(question_id))
    elif question_id is not None and answer_id is not None:
        response = get_next_question_by_answer_id(
            str(questionnaire_id), str(question_id), str(answer_id))

    print(questionnaire_id, question_id, answer_id)
    return HttpResponse(json.dumps(response))
