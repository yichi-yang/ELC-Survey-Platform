from django.urls import include, path
from .views import (
    SurveyViewSet,
    NestedSurveyQuestionViewSet,
    NestedSurveySubmissionViewSet,
    NestedSurveySessionViewSet
)
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(
    r'surveys',
    SurveyViewSet,
    basename='survey'
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
sessions_router = routers.NestedSimpleRouter(
    router,
    r'surveys',
    lookup='survey'
)
sessions_router.register(
    r'sessions',
    NestedSurveySessionViewSet,
    basename='survey-sessions'
)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(questions_router.urls)),
    path(r'', include(submissions_router.urls)),
    path(r'', include(sessions_router.urls))
]
