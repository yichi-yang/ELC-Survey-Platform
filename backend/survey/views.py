from django.db.models import Q, QuerySet
from django.utils import timezone
from rest_framework import viewsets, mixins, generics
from rest_framework.generics import get_object_or_404
from .models import Survey, SurveyQuestion, SurveySubmission, SurveyCode
from .serializers import (
    SurveyCodeSerializer,
    SurveySerializer,
    SurveyQuestionSerializer,
    NestedSurveyQuestionSerializer,
    SurveySubmissionSerializer,
    NestedSurveySubmissionSerializer,
    SurveyCodeSerializer
)
from .utils import handle_invalid_hashid
from .permissions import (
    IsSurveyOwner,
    ReadOnlyWhenSurveyActive,
    IsParentSurveyOwner,
    ReadOnlyWhenParentSurveyActive,
    CreateOnlyWhenParentSurveyActive
)


class NestedViewMixIn:
    """
    Sets self.parent_instance based on captured parent pk.
    """
    parent_model_queryset = None
    parent_pk_name = None

    def initial(self, request, *args, **kwargs):

        assert self.parent_model_queryset is not None, (
            "'%s' should include a `parent_model_queryset` attribute."
            % self.__class__.__name__
        )

        assert self.parent_pk_name is not None, (
            "'%s' should include a `parent_pk_name` attribute."
            % self.__class__.__name__
        )

        queryset = self.parent_model_queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        self.parent_instance = get_object_or_404(
            queryset,
            pk=self.kwargs[self.parent_pk_name]
        )

        super().initial(request, *args, **kwargs)


class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows surveys to be viewed or edited.

    ## Field Description

    - **id:** The survey's unique id. [*readonly*]
    - **title:** The survey's title.
    - **description:** The survey's description. [*optional*]
    - **created_at:** The survey's creation time. [*readonly*]
    - **active:** Whether the survey is active. Only when a survey is active
        people other than the owner can view and submit responses to the survey.
    - **start_date_time:** If set to a value other than `null`, other people
        can only view and submit responses to the survey after the
        specified time. [*optional*]
    - **end_date_time:** Similar to `start_date_time`, but controls the date
        time when the survey ends. [*optional*]

    ## Examples

    To create a survey, `POST` the following to `/api/surveys/`:  

    ``` json
        {  
            "title": "Survey Name",  
            "description": "A very interesting survey",  
            "active": false  
        }
    ```

    """
    serializer_class = SurveySerializer
    permission_classes = [IsSurveyOwner | ReadOnlyWhenSurveyActive]

    def get_queryset(self):
        if self.action == 'list':
            now = timezone.now()
            return Survey.objects.filter(
                # either user is the owner
                Q(owner=self.request.user.id) |
                # or the survey is active
                (
                    Q(active=True)
                    & (Q(start_date_time=None) | Q(start_date_time__lte=now))
                    & (Q(end_date_time=None) | Q(start_date_time__gte=now))
                )
            )
        return Survey.objects.all()


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows survey questions to be viewed or edited.
    """
    queryset = SurveyQuestion.objects\
        .select_related('survey')\
        .all()\
        .prefetch_related('choices')
    serializer_class = SurveyQuestionSerializer
    permission_classes = [IsParentSurveyOwner | ReadOnlyWhenParentSurveyActive]

    def get_queryset(self):

        query_set = SurveyQuestion.objects.select_related('survey')

        if self.action == 'list':
            now = timezone.now()
            query_set = query_set.filter(
                # either user is the owner
                Q(survey__owner=self.request.user.id) |
                # or the survey is active
                (
                    Q(survey__active=True)
                    & (Q(survey__start_date_time=None) | Q(survey__start_date_time__lte=now))
                    & (Q(survey__end_date_time=None) | Q(survey__start_date_time__gte=now))
                )
            )
        else:
            query_set = query_set.all()

        return query_set.prefetch_related('choices')


class NestedSurveyQuestionViewSet(NestedViewMixIn, viewsets.ModelViewSet):
    """
    API endpoint that allows questions of a particular survey to be viewed or edited.
    """
    serializer_class = NestedSurveyQuestionSerializer
    permission_classes = [IsParentSurveyOwner | ReadOnlyWhenParentSurveyActive]

    # NestedViewMixIn will set
    # self.parent_instance = Survey.objects.get(pk=self.kwargs['survey_pk'])
    # before .get, .post, etc. are called.
    parent_model_queryset = Survey.objects.all()
    parent_pk_name = 'survey_pk'

    @handle_invalid_hashid('Survey')
    def get_queryset(self):
        return SurveyQuestion.objects\
            .select_related('survey')\
            .filter(survey=self.kwargs['survey_pk'])\
            .prefetch_related('choices')


class SurveySubmissionViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    API endpoint that allows survey submissions to be created or viewed.
    Editing a submission is not supported.
    """
    serializer_class = SurveySubmissionSerializer
    permission_classes = [
        IsParentSurveyOwner | CreateOnlyWhenParentSurveyActive
    ]

    def get_queryset(self):

        query_set = SurveySubmission.objects.select_related('survey')

        if self.action == 'list':
            now = timezone.now()
            query_set = query_set.filter(
                # either user is the owner
                Q(survey__owner=self.request.user.id) |
                # or the survey is active
                (
                    Q(survey__active=True)
                    & (Q(survey__start_date_time=None) | Q(survey__start_date_time__lte=now))
                    & (Q(survey__end_date_time=None) | Q(survey__start_date_time__gte=now))
                )
            )
        else:
            query_set = query_set.all()

        return query_set.prefetch_related('responses')


class NestedSurveySubmissionViewSet(NestedViewMixIn,
                                    mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """
    API endpoint that allows survey submissions to be created or viewed.
    Editing a submission is not supported.
    """
    serializer_class = NestedSurveySubmissionSerializer
    permission_classes = [
        IsParentSurveyOwner | CreateOnlyWhenParentSurveyActive
    ]

    # NestedViewMixIn will set
    # self.parent_instance = Survey.objects.get(pk=self.kwargs['survey_pk'])
    # before .get, .post, etc. are called.
    parent_model_queryset = Survey.objects.all()
    parent_pk_name = 'survey_pk'

    @handle_invalid_hashid('Survey')
    def get_queryset(self):
        return SurveySubmission.objects\
            .select_related('survey')\
            .filter(survey=self.kwargs['survey_pk'])\
            .prefetch_related('responses')

class CodeToSurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns all mappings of 4 digit codes to survey ID
    or a particular survey ID from a 4 digit code
    """
    serializer_class = SurveyCodeSerializer
    # permission_classes = [ReadOnlyWhenSurveyActive]

    def get_queryset(self):
        return SurveyCode.objects.all()

# turn into generics.ListCreateAPIView
class SurveyToCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns all mappings of 4 digit codes to survey ID
    or a particular 4 digit code from a survey ID
    """
    serializer_class = SurveyCodeSerializer
    lookup_field ='survey'
    # permission_classes = [ReadOnlyWhenSurveyActive]

    def get_queryset(self):
        return SurveyCode.objects.all()
