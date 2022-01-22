from rest_framework import viewsets, permissions, mixins
from .models import Survey, SurveyQuestion, SurveySubmission
from .serializers import (
    SurveySerializer,
    SurveyQuestionSerializer,
    NestedSurveyQuestionSerializer,
    SurveySubmissionSerializer,
    NestedSurveySubmissionSerializer
)
from .utils import handle_invalid_hashid


class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows surveys to be viewed or edited.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows survey questions to be viewed or edited.
    """
    queryset = SurveyQuestion.objects.all().prefetch_related('choices')
    serializer_class = SurveyQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class NestedSurveyQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows questions of a particular survey to be viewed or edited.
    """
    serializer_class = NestedSurveyQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @handle_invalid_hashid('Survey')
    def get_queryset(self):
        return SurveyQuestion.objects.filter(survey=self.kwargs['survey_pk']).prefetch_related('choices')


class SurveySubmissionViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    API endpoint that allows survey submissions to be created or viewed.
    Editing a submission is not supported.
    """
    queryset = SurveySubmission.objects.all().prefetch_related('responses')
    serializer_class = SurveySubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NestedSurveySubmissionViewSet(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """
    API endpoint that allows survey submissions to be created or viewed.
    Editing a submission is not supported.
    """
    serializer_class = NestedSurveySubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @handle_invalid_hashid('Survey')
    def get_queryset(self):
        return SurveySubmission.objects.filter(survey=self.kwargs['survey_pk']).prefetch_related('responses')
