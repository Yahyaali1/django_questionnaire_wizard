import json

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .data_wrapper import get_questionnaire_list, get_question_by_id, get_first_question, get_next_question_by_answer_id, print_log
from .serializers import QuestionnaireListSerializer, QuestionSerializer, ResponseLogSerializer
from .datamodels.datamodels import ResponseModelForLog
from .shared.shared_keys import Key
from .shared.errors_dict import ErrorDict


class FetchListApi(APIView):
    def get(self, args):
        data_list = get_questionnaire_list()
        if not data_list:
            return Response(data=ErrorDict.NO_QUESTIONNAIRES_FOUND, status=status.HTTP_404_NOT_FOUND)
        serialized_data = QuestionnaireListSerializer(
            data_list, many=True).data
        return Response(data=serialized_data, status=status.HTTP_200_OK)


def submit(request, questionnaire_id, question_id=None, answer_id=None):
    if question_id is None and answer_id is None:
        response = get_first_question(str(questionnaire_id))
    elif question_id is not None and answer_id is None:
        response = get_question_by_id(str(questionnaire_id), str(question_id))
    elif question_id is not None and answer_id is not None:
        response = get_next_question_by_answer_id(
            str(questionnaire_id), str(question_id), str(answer_id))
        if Key.ERROR not in response:
            if Key.TRACK not in request.session:
                data = []
                request.session[Key.TRACK] = data
            request.session[Key.TRACK].append(ResponseLogSerializer(ResponseModelForLog(
                questionnaire_id, question_id, answer_id)).data)
            print(request.session[Key.TRACK])
            if not response[Key.ANSWERS]:
                print_log(request.session[Key.TRACK])
                del request.session[Key.TRACK]

    if Key.ERROR in response:
        error_code = status.HTTP_404_NOT_FOUND
    else:
        error_code = status.HTTP_200_OK
    print(questionnaire_id, question_id, answer_id)
    return HttpResponse(json.dumps(response), status=error_code)
