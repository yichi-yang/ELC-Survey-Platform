from django.urls import include, path
from .views import (
    SurveyViewSet,
    NestedSurveyQuestionViewSet,
    NestedSurveySubmissionViewSet,
    CodeToSessionViewSet,
    SurveySessionViewSet
)
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(
    r'surveys',
    SurveyViewSet,
    basename='survey'
)
router.register(
    r'sessions',
    SurveySessionViewSet,
    basename='session'
)
survey_router = routers.NestedSimpleRouter(
    router,
    r'surveys',
    lookup='survey'
)
survey_router.register(
    r'questions',
    NestedSurveyQuestionViewSet,
    basename='survey-question'
)

session_router = routers.NestedSimpleRouter(
    router,
    r'sessions',
    lookup='session'
)
session_router.register(
    r'submissions',
    NestedSurveySubmissionViewSet,
    basename='survey-submission'
)

router.register(
    r'codes',
    CodeToSessionViewSet,
    basename='code'
)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(survey_router.urls)),
    path(r'', include(session_router.urls)),
]
