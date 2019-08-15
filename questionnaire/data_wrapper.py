import json
import traceback

from .datamodels.datamodels import Questionnaire
# TODO Move the file name to external file
#from questionnaire.models import Questionnaire, Questions, Answers


class __DataStore():
    def __init__(self):
        self.__questionnaires = self.___read_file('questionnaires.json')

    def get_data(self):
        return self.__questionnaires
    # TODO add the file to path variables

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


__data = __DataStore().get_data()


def get_questionnaire_list():
    print(__data)
    data_list: Questionnaire = []
    for items in __data:
        data_list.append(Questionnaire(id=items["questionnaire_id"],
                                       title=items["title"]))
    return data_list

# Returns questionnaire from json array


def __get_questionnaire_by_id(id: int):
    data = None
    for item in __data:
        if item["questionnaire_id"] == id:
            data = item
            return data
    return data

# Retunrs a question specified by id


def __get_question_by_id(id: int, questionnaire):
    data = None
    for item in questionnaire["questions"]:
        if item["question_id"] == id:
            data = item
            return data
    return data


def get_first_question(questionnaire_id: int):
    first_question = None
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire != None:
        try:
            first_question = questionnaire["questions"][0]
            first_question["questionnaire_id"] = questionnaire_id
        except Exception:
            first_question = {}
    else:
        first_question = {}
    return first_question


def get_question_by_id(questionnaire_id: int, question_id: int):
    current_question = None
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire != None:
        question = __get_question_by_id(question_id, questionnaire)
        if(question != None):
            current_question = question
        else:
            current_question = {}
            return
    else:
        current_question = {}
    return current_question


def get_next_question_by_answer_id(questionnaire_id: int, question_id: int, answer_id):
    next_question = None
    questionnaire = __get_questionnaire_by_id(questionnaire_id)
    if questionnaire != None:
        question = __get_question_by_id(question_id, questionnaire)
        if(question != None):
            print(question)
            next_question_id = question["answers"][answer_id]["next_question_id"]
            print(next_question_id)
            next_question = __get_question_by_id(
                next_question_id, questionnaire)
            print("next question", next_question)
        else:
            return {}
    else:
        return {}
    if next_question is not None:
        print(next_question)
        next_question['questionnaire_id'] = questionnaire_id
        return next_question
    else:
        return{}
