import traceback
import json
# Lib imports
from jsonschema import validate

# Django imports
from django.conf import settings

# Local Imports
from ..datamodels.datamodels import Questionnaire
from .shared_keys import Key

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger()


class DataStore():
    """
    Loads data from json file name specified in settings
    Validates the structure using json schema 
    """
    MAX_ANSWERS = 5

    def __init__(self, validate_json=True):
        self.validate = validate_json
        self.__questionnaires = self.___read_file(
            settings.QUESIONNAIRE_DATA_FILE)
        self.__questionnaires_list = self.__get_all_questionnaire()

    def get_data(self):
        return self.__questionnaires, self.__questionnaires_list

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
            logger.error(msg=traceback.format_exc())
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
                                  "patternProperties":
                                  {"^[0-9]+$": {"type": "object",
                                                "properties": {
                                                    Key.ANSWER_TEXT:
                                                    {"type": "string"},
                                                    Key.NEXT_QUEST_ID:
                                                    {"type": "string"}
                                                },
                                                "required": [Key.ANSWER_TEXT,
                                                             Key.NEXT_QUEST_ID]
                                                }
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
            "patternProperties": {"^[0-9]+$": {"type": "object",
                                               "properties": {
                                                   Key.TITLE:
                                                   {"type": "string"},
                                                   Key.QUESTIONS:
                                                   schema_question
                                               },
                                               "required":
                                               [Key.TITLE, Key.QUESTIONS]},
                                  "additionalProperties": False}
        }

        validate(instance=data, schema=schema_questionnaire)
