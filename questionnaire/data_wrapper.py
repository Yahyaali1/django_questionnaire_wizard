import json
import traceback
import copy

from .datamodels.datamodels import Questionnaire
# TODO Move the file name to external file
# from questionnaire.models import Questionnaire, Questions, Answers
KEY_TITLE = "title"
KEY_QUESTIONS = "questions"
KEY_QUESTION_ID = "question_id"
KEY_ANSWERS = "answers"
KEY_ANSWER_TEXT = "answer_text"
KEY_ANSWER_ID = "answer_id"
KEY_NEXT_QUEST_ID = "next_question_id"
KEY_QUESTIONNAIRE_ID = "questionnaire_id"
KEY_ERROR = "error"
STRING_ERROR_QUESTION_ID = "No question found with this id"
STRING_ERROR_ANSWER_ID = "No answer found with this id"
STRING_ERROR_QUESTIONNAIRE_ID = "No questionnaire found with this id"
ERROR_QUESTION_ID_DICT = {KEY_ERROR: STRING_ERROR_QUESTION_ID}
ERROR_ANSWER_ID_DICT = {KEY_ERROR: STRING_ERROR_ANSWER_ID}
ERROR_QUESTIONNAIRE_ID_DICT = {KEY_ERROR: STRING_ERROR_QUESTIONNAIRE_ID}


class __DataStore():
    def __init__(self):
        self.__questionnaires = self.___read_file('questionnaires.json')
        self.__questionnaires_list = self.__get_all_questionnaire()

    def get_data(self):
        return self.__questionnaires, self.__questionnaires_list
    # TODO add the file to path variables

    def __get_all_questionnaire(self):
        data = []
        for key, value in self.__questionnaires.items():
            data.append(Questionnaire(id=key, title=value[KEY_TITLE]))
        return data

    def ___read_file(self, file_name):
        data = {}
        try:
            with open(file_name, 'r') as json_file:
                data = json.load(json_file)
                json_file.close()
        except Exception:
            print(traceback.format_exc())
        return data

    # def load(self):
    #     for item in self.__questionnaires:
    #         Questionnaire.objects.all().delete()
    #         questionnaire = Questionnaire(title=item["title"])
    #         questionnaire.save()
    #         for item_question in item["questions"]:
    #             question = Questions(questionnaire=questionnaire,
    #                                  question_id=item_question["question_id"],
    #                                  title=item_question["question_text"],
    #                                  first_question=item_question["first_question"])
    #             question.save()
    #             for item_answers in item_question["answers"]:
    #                 answers = Answers(
    #                     question=question, title=item_answers["answer_text"], next_question_id=item_answers["next_question_id"])
    #                 answers.save()
    #         print(item)


__DATA_STORE_OBJECT = __DataStore()
__DATA, __ALL_QUESTIONNIRES = __DATA_STORE_OBJECT.get_data()
print(__DATA)


def get_questionnaire_list():
    print(__ALL_QUESTIONNIRES)
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
    if id in questionnaire[KEY_QUESTIONS]:
        data = questionnaire[KEY_QUESTIONS][id]
    return data


def prepare_question_response(question: dict, question_id: int, questionnaire_id: int):
    data_answers = []
    question = copy.deepcopy(question)
    if KEY_ANSWERS in question:

        for key, value in question[KEY_ANSWERS].items():
            temp = value
            temp[KEY_ANSWER_ID] = key
            data_answers.append(temp)

        question[KEY_ANSWERS] = data_answers
        question[KEY_QUESTIONNAIRE_ID] = questionnaire_id
        question[KEY_QUESTION_ID] = question_id
        return question
    else:
        return {}


def get_first_question(questionnaire_id):
    first_question = {}
    question_id = None
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    print(questionnaire)
    if questionnaire:
        for key, value in questionnaire[KEY_QUESTIONS].items():
            first_question = value
            print(first_question)
            question_id = key
            break

    return prepare_question_response(first_question, question_id, questionnaire_id)


def get_question_by_id(questionnaire_id: str, question_id: str):
    current_question = {}
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    print(questionnaire)
    if questionnaire and question_id in questionnaire[KEY_QUESTIONS]:
        question = __get_question_by_id(question_id, questionnaire)
        print(question)
        current_question = prepare_question_response(
            question, question_id, questionnaire_id)

    return current_question


def get_next_question_by_answer_id(questionnaire_id: str, question_id: str, answer_id):
    next_question = {}
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire:
        question = __get_question_by_id(question_id, questionnaire)

        if question:
            answers = question[KEY_ANSWERS]

            if answer_id in answers:
                next_question_id = answers[answer_id][KEY_NEXT_QUEST_ID]
                next_question = __get_question_by_id(
                    next_question_id, questionnaire)
                next_question = prepare_question_response(
                    next_question, next_question_id, questionnaire_id)

                if next_question:
                    return next_question
                else:
                    ERROR_QUESTION_ID_DICT

            else:
                return ERROR_ANSWER_ID_DICT

        else:
            return ERROR_QUESTION_ID_DICT
    else:
        return ERROR_QUESTIONNAIRE_ID_DICT
