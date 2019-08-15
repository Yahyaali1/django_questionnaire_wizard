class Questionnaire():
    def __init__(self, id, title):
        self.questionnaire_id = id
        self.title = title


class ResponseModelForLog():
    def __init__(self, questionnair_id, question_id, answer_id):
        self.questionnair_id = questionnair_id
        self.question_id = question_id
        self.answer_id = answer_id
