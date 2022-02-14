from django.template import base
from django.urls import include, path
from .views import (
    SurveyViewSet,
    NestedSurveyQuestionViewSet,
    SurveyQuestionViewSet,
    SurveySubmissionViewSet,
    NestedSurveySubmissionViewSet,
    CodeToSurveyViewSet,
    SurveyToCodeViewSet
)
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(
    r'surveys',
    SurveyViewSet,
    basename='survey'
)
router.register(
    r'questions',
    SurveyQuestionViewSet,
    basename='questions'
)
router.register(
    r'submissions',
    SurveySubmissionViewSet,
    basename='submissions'
)
questions_router = routers.NestedSimpleRouter(
    router,
    r'surveys',
    lookup='survey'
)
questions_router.register(
    r'questions',
    NestedSurveyQuestionViewSet,
    basename='survey-questions'
)


submissions_router = routers.NestedSimpleRouter(
    router,
    r'surveys',
    lookup='survey'
)
submissions_router.register(
    r'submissions',
    NestedSurveySubmissionViewSet,
    basename='survey-submissions'
)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(questions_router.urls)),
    path(r'', include(submissions_router.urls)),
    path(r'mapping/codes/<int:pk>', CodeToSurveyViewSet.as_view(), name="codes"),
    path(r'mapping/surveys/<int:pk>', SurveyToCodeViewSet.as_view(), name="surveys"),
]
