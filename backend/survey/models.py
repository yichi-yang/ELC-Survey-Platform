from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField
from django.utils import timezone
from .utils import build_auto_salt
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

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
    prev_active= models.BooleanField(default=False)
    start_date_time = models.DateTimeField(null=True, blank=True)
    end_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Survey id={self.id} title={self.title!r}'

    @property
    def is_active(self) -> bool:
        now = timezone.now()
        if self.start_date_time and now < self.start_date_time:
            return False
        if self.end_date_time and now > self.end_date_time:
            return False
        return self.active

    @property
    def required_questions(self):
        return self.questions.filter(required=True)

# post save for Survey active state
# adds new row to SurveyCode on active
# deletes row on SurveyCode on not active
@receiver(post_save, sender=Survey, dispatch_uid="active")
def update_stock(sender, instance, **kwargs):
    if instance.active != instance.prev_active:
        if instance.active:
            # get random 4 digit code
            # query table to see if id exists
            # stop loop until row found
            code = random.randint(1000,9999)
            while SurveyCode.objects.filter(id=code).exists():
                code = random.randint(1000,9999)
            mapping = SurveyCode(id=code, survey=instance)
            mapping.save()
        else:
            SurveyCode.objects.filter(survey=instance.id).delete()
    # update prev active state to current state
    # use this method instead of .save() to avoid infinite recursion
    Survey.objects.filter(id=instance.id).update(prev_active=instance.active)


class SurveyQuestion(models.Model):

    class QuestionType(models.TextChoices):
        MULTICHOICE = 'MC', _('Multiple Choice')
        CHECKBOXES = 'CB', _('Checkboxes')
        DROPDOWN = 'DP', _('Dropdown')
        SCALE = 'SC', _('Scale')
        SHORT_ANSWER = 'SA', _('Short Answer')
        PARAGRAPH = 'PA', _('Long Answer')

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
    # used for SCALE type
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

class SurveyCode(models.Model):
    id = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)