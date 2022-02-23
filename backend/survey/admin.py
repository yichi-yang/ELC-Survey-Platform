from django.contrib import admin
from .models import (Survey, SurveyQuestion, SurveyQuestionChoice,
                     SurveySubmission, SurveyResponse, SurveySession)

# Register your models here.


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at',)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


@admin.register(SurveyQuestionChoice)
class SurveyQuestionChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'submission_time',)


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )

@admin.register(SurveySession)
class SurveySessionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )