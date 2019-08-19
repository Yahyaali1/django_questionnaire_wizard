import traceback
import json
# Lib imports
from jsonschema import validate

# Django imports
from django.conf import settings

# Local Imports
from ..datamodels.datamodels import Questionnaire
from .shared_keys import Key


class DataStore():
    MAX_ANSWERS = 5

    def __init__(self, validate_json=True):
        self.validate = validate_json
        self.__questionnaires = self.___read_file(
            settings.QUESIONNAIRE_DATA_FILE)
        self.__questionnaires_list = self.__get_all_questionnaire()

    def get_data(self):
        return self.__questionnaires, self.__questionnaires_list
    # TODO add the file to path variables

    def __get_all_questionnaire(self):
        data = []
        for key, value in self.__questionnaires.items():
            data.append(Questionnaire(id=key, title=value[Key.TITLE]))
        return data

    def ___read_file(self, file_name):
        data = {}
        try:
            with open(file_name, 'r') as json_file:
                data = json.load(json_file)
                if self.validate:
                    self.__validate_json(data)
                json_file.close()
        except Exception:
            print(traceback.format_exc())
        return data

    def __validate_json(self, data):
        schema_question = {
            "type": "object",
            "patternProperties": {"^[0-9]+$": {
                "type": "object",
                "properties": {
                    Key.QUESTION_TEXT: {"type": "string"},
                    Key.ANSWERS: {"type": "object",
                                  "maxProperties": self.MAX_ANSWERS,
                                  "patternProperties": {"^[0-9]+$": {"type": "object",
                                                                     "properties": {
                                                                         Key.ANSWER_TEXT: {"type": "string"},
                                                                         Key.NEXT_QUEST_ID: {
                                                                             "type": "string"}
                                                                     },
                                                                     "required": [Key.ANSWER_TEXT, Key.NEXT_QUEST_ID]}
                                                        },
                                  "additionalProperties": False
                                  }
                },
                "required": [Key.QUESTION_TEXT, Key.ANSWERS]
            }
            }
        }
        schema_questionnaire = {
            "type": "object",
            "patternProperties": {"^[0-9]+$": {"type": "object", "properties": {
                Key.TITLE: {"type": "string"},
                Key.QUESTIONS: schema_question
            },
                "required": [Key.TITLE, Key.QUESTIONS]}, "additionalProperties": False}
        }

        validate(instance=data, schema=schema_questionnaire)

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
