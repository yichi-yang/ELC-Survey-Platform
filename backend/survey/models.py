from tkinter import CASCADE
from django.db import models
from hashid_field import HashidAutoField
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .utils import build_auto_salt


class Survey(models.Model):

    id = HashidAutoField(primary_key=True, salt=build_auto_salt('Survey'))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    start_date_time = models.DateTimeField(null=True, blank=True)
    end_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Survey id={self.id} title={self.title!r}'


class SurveyQuestion(models.Model):

    class QuestionType(models.TextChoices):
        MULTICHOICE = 'MC', _('Multiple Choice')
        CHECKBOXES = 'CB', _('Checkboxes')
        DROPDOWN = 'DP', _('Dropdown')
        SCALE = 'SC', _('Scale')
        SHORT_ANSWER = 'SA', _('Short Answer')
        PARAGRAPH = 'PA', _('LONG Answer')

    id = HashidAutoField(
        primary_key=True, salt=build_auto_salt('SurveyQuestion'))
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    required = models.BooleanField()
    hidden = models.BooleanField(default=False)
    type = models.CharField(
        max_length=2,
        choices=QuestionType.choices
    )

    def __str__(self):
        return f'SurveyQuestion id={self.id} survey={self.survey.id} title={self.title!r}'


class SurveyQuestionChoice(models.Model):

    id = HashidAutoField(
        primary_key=True,
        salt=build_auto_salt('SurveyQuestionChoice')
    )
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    value = models.CharField(max_length=32)
    description = models.CharField(max_length=200)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'SurveyQuestionChoice question={self.question.id} value={self.value!r}'


class SurveyQuestionScaleMeta(models.Model):

    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    min = models.FloatField()
    max = models.FloatField()
    default = models.FloatField()
    step = models.FloatField(default=1)

    def __str__(self):
        return f'SurveyQuestionScaleMeta question={self.question.id}'


class SurveySubmission(models.Model):

    id = HashidAutoField(
        primary_key=True,
        salt=build_auto_salt('SurveySubmission')
    )
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'SurveySubmission id={self.id} survey={self.survey.id}'


class SurveyResponse(models.Model):

    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(
        SurveyQuestionChoice,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    text = models.TextField(blank=True, null=True)
    numeric_value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'SurveyResponse submission={self.submission.id} question={self.question.id}'
