class Questionnaire():
    def __init__(self, id, title):
        self.questionnaire_id = id
        self.title = title


class ResponseModelForLog():
    def __init__(self, questionnaire_id, question_id, answer_id):
        self.questionnaire_id = questionnaire_id
        self.question_id = question_id
        self.answer_id = answer_id
