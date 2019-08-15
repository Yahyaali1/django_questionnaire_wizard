from django.db import models


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)


class Questions(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    title = models.CharField(max_length=255)
    first_question = models.BooleanField(default=False)


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    next_question_id = models.IntegerField()
