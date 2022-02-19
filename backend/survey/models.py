from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField
from .utils import build_auto_salt
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Survey(models.Model):

    id = HashidAutoField(primary_key=True, salt=build_auto_salt('Survey'))

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Survey id={self.id} title={self.title!r}'

    @property
    def required_questions(self):
        return self.questions.filter(required=True)


class SurveySession(models.Model):
    # Let's have an id field because the code might be reused.
    # The id should always be unique.
    id = HashidAutoField(
        primary_key=True,
        salt=build_auto_salt('SurveySession')
    )
    code = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1000),
            # MaxValueValidator(9999) # not sure if we need this?
        ]
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'SurveySession survey={self.survey.id} code={self.code}'

    class Meta:
        unique_together = ('survey', 'owner')


class SurveyQuestion(models.Model):

    class QuestionType(models.TextChoices):
        MULTICHOICE = 'MC', _('Multiple Choice')
        CHECKBOXES = 'CB', _('Checkboxes')
        DROPDOWN = 'DP', _('Dropdown')
        SCALE = 'SC', _('Scale')
        SHORT_ANSWER = 'SA', _('Short Answer')
        PARAGRAPH = 'PA', _('Long Answer')
        RANKING = 'RK', _('Ranking')

    id = HashidAutoField(
        primary_key=True,
        salt=build_auto_salt('SurveyQuestion')
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    required = models.BooleanField()
    type = models.CharField(
        max_length=2,
        choices=QuestionType.choices
    )
    # used for SCALE & RANKING type
    range_min = models.FloatField(null=True, blank=True)
    range_max = models.FloatField(null=True, blank=True)
    range_default = models.FloatField(null=True, blank=True)
    range_step = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'SurveyQuestion id={self.id} survey={self.survey.id} title={self.title!r}'


class SurveyQuestionChoice(models.Model):

    id = HashidAutoField(
        primary_key=True,
        salt=build_auto_salt('SurveyQuestionChoice')
    )
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    value = models.CharField(max_length=32)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'SurveyQuestionChoice id={self.id} question={self.question.id} value={self.value!r}'


class SurveySubmission(models.Model):

    id = HashidAutoField(
        primary_key=True,
        salt=build_auto_salt('SurveySubmission')
    )
    session = models.ForeignKey(SurveySession, on_delete=models.CASCADE)
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

    submission = models.ForeignKey(
        SurveySubmission,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    choice = models.ForeignKey(
        SurveyQuestionChoice,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    text = models.TextField(blank=True, null=True)
    numeric_value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'SurveyResponse submission={self.submission.id} question={self.question.id}'
