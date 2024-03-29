from .shared_keys import Key


class ErrorDict:
    """
    Standard Error Dict for Api Response.
    """
    QUESTION_ID_DICT = {Key.ERROR: Key.STRING_ERROR_QUESTION_ID}
    ANSWER_ID_DICT = {Key.ERROR: Key.STRING_ERROR_ANSWER_ID}
    QUESTIONNAIRE_ID_DICT = {
        Key.ERROR: Key.STRING_ERROR_QUESTIONNAIRE_ID}
    NO_QUESTIONNAIRES_FOUND = {Key.ERROR: Key.STRING_ERROR_NO_QUESTIONNAIRES}
