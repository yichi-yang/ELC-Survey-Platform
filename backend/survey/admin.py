from django.contrib import admin
from .models import (Survey, SurveyQuestion, SurveyQuestionChoice,
                     SurveyQuestionScaleMeta, SurveySubmission, SurveyResponse)

# Register your models here.


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at',)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(SurveyQuestionChoice)
class SurveyQuestionChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(SurveyQuestionScaleMeta)
class SurveyQuestionScaleMetaAdmin(admin.ModelAdmin):
    pass


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('submission_time',)


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    pass
