import json
import copy
import logging
# Local Imports
from .datamodels.datamodels import Questionnaire, ResponseModelForLog
from .shared.shared_keys import Key
from .shared.errors_dict import ErrorDict
from .shared.data_store import DataStore

__DATA_STORE_OBJECT = DataStore()
__DATA, __ALL_QUESTIONNIRES = __DATA_STORE_OBJECT.get_data()


def get_questionnaire_list():
    return __ALL_QUESTIONNIRES

# Returns questionnaire from json array


def __get_questionnaire_by_id(id: int):
    data = {}
    if id in __DATA:
        data = __DATA[id]
    return data

# Retunrs a question specified by id


def __get_question_by_id(id: str, questionnaire):
    data = {}
    if id in questionnaire[Key.QUESTIONS]:
        data = questionnaire[Key.QUESTIONS][id]
    return data


def prepare_question_response(question: dict, question_id: int,
                              questionnaire_id: int):
    data_answers = []
    question = copy.deepcopy(question)
    if Key.ANSWERS in question:

        for key, value in question[Key.ANSWERS].items():
            temp = value
            temp[Key.ANSWER_ID] = key
            data_answers.append(temp)

        question[Key.ANSWERS] = data_answers
        question[Key.QUESTIONNAIRE_ID] = questionnaire_id
        question[Key.QUESTION_ID] = question_id
        return question
    else:
        return ErrorDict.QUESTION_ID_DICT


def get_first_question(questionnaire_id):
    first_question = {}
    question_id = None
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire:
        for key, value in questionnaire[Key.QUESTIONS].items():
            first_question = value
            question_id = key
            break
    else:
        return ErrorDict.QUESTIONNAIRE_ID_DICT

    return prepare_question_response(first_question, question_id,
                                     questionnaire_id)


def get_question_by_id(questionnaire_id: str, question_id: str):
    current_question = {}
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire and question_id in questionnaire[Key.QUESTIONS]:
        question = __get_question_by_id(question_id, questionnaire)
        current_question = prepare_question_response(
            question, question_id, questionnaire_id)
    else:
        current_question = ErrorDict.QUESTION_ID_DICT

    return current_question


def print_log(data: ResponseModelForLog):
    logging.log(1, "User Conversation")
    for items in data:
        questionnaire = __get_questionnaire_by_id(
            str(items[Key.QUESTIONNAIRE_ID]))
        question = questionnaire[Key.QUESTIONS][str(items[Key.QUESTION_ID])]
        logging.log(1, question[Key.QUESTION_TEXT], "->")
        logging.log(1, question[Key.ANSWERS][str(items[Key.ANSWER_ID])]
                    [Key.ANSWER_TEXT], "->")


def get_next_question_by_answer_id(questionnaire_id: str, question_id: str,
                                   answer_id):
    next_question = {}
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire:
        question = __get_question_by_id(question_id, questionnaire)

        if question:
            answers = question[Key.ANSWERS]

            if answer_id in answers:
                next_question_id = answers[answer_id][Key.NEXT_QUEST_ID]
                next_question = __get_question_by_id(
                    next_question_id, questionnaire)
                next_question = prepare_question_response(
                    next_question, next_question_id, questionnaire_id)

                if next_question:
                    return next_question
                else:
                    ErrorDict.QUESTION_ID_DICT

            else:
                return ErrorDict.ANSWER_ID_DICT

        else:
            return ErrorDict.QUESTION_ID_DICT
    else:
        return ErrorDict.QUESTIONNAIRE_ID_DICT
