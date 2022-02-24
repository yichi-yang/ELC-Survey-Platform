from django.db.models import QuerySet
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from .models import Survey, SurveyQuestion, SurveySubmission
from .serializers import (
    SurveySerializer,
    NestedSurveyQuestionSerializer,
    NestedSurveySubmissionSerializer,
    NestedSurveySessionSerializer
)
from .models import Survey, SurveyQuestion, SurveySubmission, SurveySession
from .utils import handle_invalid_hashid, query_param_to_bool
from .permissions import (
    IsParentSurveyOwner,
    CreateOnlyWhenParentSurveyActive
)
from .exceptions import BadQueryParameter
import random


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

    # Field Description

    | Field               | Type     |          | Description                                                                  |
    | ------------------- | -------- | -------- | ---------------------------------------------------------------------------- |
    | `id`                | `string` | readonly | The survey's unique id.                                                      |
    | `title`             | `string` |          | The survey's title.                                                          |
    | `description`       | `string` | optional | The survey's description.                                                    |
    | `draft`             | `bool`   | optional | Whether the survey is a draft. Defaults to `true`.                           |
    | `group_by_question` | `string` | optional | The id of the question that should be used to split submissions into groups. |
    | `created_at`        | `string` | readonly | The survey's creation time in ISO 8601 format.                               |

    # Examples

    ## Create Survey

    To create a survey, `POST` the following to `/api/surveys/`:  

    ``` javascript
    // POST /api/surveys/
    {  
        "title": "Survey Name",  
        "description": "A very interesting survey", 
    }

    // HTTP 201 Created
    {
        "id": "x5zMkQe",
        "title": "Survey Name",
        "description": "A very interesting survey",
        "draft": true,
        "group_by_question": null,
        "created_at": "2022-02-14T02:01:16.168116Z"
    }
    ```

    ## List Surveys

    You can list all surveys by `GET /api/surveys/`.  

    ``` javascript
    // GET /api/surveys/

    // HTTP 200 OK
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "ZL9AOn3",
                "title": "My First Survey",
                "description": "123",
                "draft": true,
                "group_by_question": null,
                "created_at": "2022-02-14T02:00:43.454549Z"
            },
            {
                "id": "x5zMkQe",
                "title": "Survey Name",
                "description": "A very interesting survey",
                "draft": true,
                "group_by_question": null,
                "created_at": "2022-02-14T02:01:16.168116Z"
            }
        ]
    }
    ```

    You can use query parameters `limit` (default: 20, max: 100) and `offset` to
    navigate between different pages if there are too many surveys to
    fit in one page.

    ``` javascript
    // GET /api/surveys/?offset=2&limit=2

    // HTTP 200 OK
    {
        "count": 8,
        "next": "http://127.0.0.1:8000/api/surveys/?limit=2&offset=4",
        "previous": "http://127.0.0.1:8000/api/surveys/?limit=2",
        "results": [
            {
                "id": "13zlXze",
                "title": "Untitled Survey",
                "description": "",
                "draft": true,
                "group_by_question": null,
                "created_at": "2022-02-20T23:42:15.569130Z"
            },
            {
                "id": "vrzkOzD",
                "title": "Untitled Survey",
                "description": "",
                "draft": true,
                "group_by_question": null,
                "created_at": "2022-02-20T23:42:50.312421Z"
            }
        ]
    }
    ```

    You can use query parameters `keyword` to limit results to all surveys that
    have the keyword in their titles.

    ``` javascript
    // GET /api/surveys/?keyword=abc

    // HTTP 200 OK
    {
        // ...
        "results": [
            // surveys that have 'abc' in their titles
        ]
    }
    ```

    You can use query parameters `draft` to filter surveys by draft status.

    ``` javascript
    // GET /api/surveys/?draft=false

    // HTTP 200 OK
    {
        // ...
        "results": [
            // surveys that have .draft=false
        ]
    }
    ```

    ## Fetch Survey

    To fetch a specific survey, `GET /api/surveys/<id>/`.  

    ``` javascript
    // GET /api/surveys/x5zMkQe/

    // HTTP 200 OK
    {
        "id": "x5zMkQe",
        "title": "Survey Name",
        "description": "A very interesting survey",
        "draft": true,
        "group_by_question": null,
        "created_at": "2022-02-14T02:01:16.168116Z"
    }
    ```

    ## Edit Survey

    You can use `PATCH` (partial update) and `PUT` (full update) to edit a survey.  

    > Note: readonly fields cannot be changed.  

    ``` javascript
    // PATCH /api/surveys/x5zMkQe/
    {
        "description": "New description"
    }

    // HTTP 200 OK
    {
        "id": "x5zMkQe",
        "title": "Survey Name",
        "description": "New description",
        "draft": true,
        "group_by_question": null,
        "created_at": "2022-02-14T02:01:16.168116Z"
    }
    ```

    ## Delete Survey

    To delete a specific survey, `DELETE /api/surveys/<id>/`.  

    > Note: deleting a survey also removes all associated questions and responses.  

    ``` javascript
    // DELETE /api/surveys/x5zMkQe/

    // HTTP 204 No Content
    ```
    """
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Survey.objects.all()

        # filter by draft status
        draft = self.request.query_params.get('draft')
        if draft is not None:
            draft_bool = query_param_to_bool(draft)
            if draft_bool is None:
                raise BadQueryParameter(
                    "query parameter 'draft' must be either true or false."
                )
            queryset = queryset.filter(draft=draft_bool)

        # filter by keywords
        keyword = self.request.query_params.get('keyword')
        if keyword is not None:
            queryset = queryset.filter(title__icontains=keyword)

        return queryset


class NestedSurveyQuestionViewSet(NestedViewMixIn, viewsets.ModelViewSet):
    """
    API endpoint that allows questions of a particular survey to be viewed or edited.

    # Field Description

    | Field           | Type                         |           | Description                                                                                                                                   |
    | --------------- | ---------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
    | `id`            | `string`                     | readonly  | The question's unique id.                                                                                                                     |
    | `number`        | `int`                        |           | The question's number, e.g. `1` for question 1. The meaning of `number` is defined by the frontend, and there's no validation on the backend. |
    | `title`         | `string`                     |           | The question's body (max length: 200 characters).                                                                                             |
    | `required`      | `bool`                       |           | Whether the questions is required or not.                                                                                                     |
    | `type`          | `string`                     |           | The question's type code, see [question types](#question-types).                                                                              |  |
    | `range_min`     | `float`                      | optional* | The minimal value for question types that require a numeric answer, see [question types](#question-types).                                    |
    | `range_max`     | `float`                      | optional* | The maximum value for question types that require a numeric answer, see [question types](#question-types).                                    |
    | `range_default` | `float`                      | optional* | The default value for question types that require a numeric answer, see [question types](#question-types).                                    |
    | `range_step`    | `float`                      | optional* | The step size for question types that require a numeric answer, see [question types](#question-types).                                        |
    | `choices`       | [`[ChoiceObject]`](#choices) | optional* | A list of options for question types that involve choices, see [question types](#question-types).                                             |

    > Note: fields marked as **optional\*** may be required depending on the question `type`, see [question types](#question-types).

    # Choice Object

    | Field         | Type     |          | Description                                                                                                                             |
    | ------------- | -------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
    | `id`          | `string` | readonly | The choice's unique id.                                                                                                                 |
    | `value`       | `string` |          | The choice's tag, e.g. A, B, C or 1, 2, 3. The meaning of `value` is defined by the frontend, and there's no validation on the backend. |
    | `description` | `string` |          | The choice's text (max length: 200 characters).                                                                                         |

    # Question Types

    | Type            | Code   | Description                                                                                                                                       | Required Fields                                                    |
    | --------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
    | Multiple Choice | `'MC'` | A multiple choice question. Users can only pick a single option.                                                                                  | `choices`                                                          |
    | Checkboxes      | `'CB'` | Check one or more checkboxes.                                                                                                                     | `choices`                                                          |
    | Dropdown        | `'DP'` | Like `MC`, but should render a dropdown widget.                                                                                                   | `choices`                                                          |
    | Scale           | `'SC'` | A slider that allows picking a value between `range_min` and `range_max` in `range_step` increments. The default value should be `range_default`. | `range_min`, `range_max`, `range_default`, `range_step`            |
    | Short Answer    | `'SA'` | A black that allows users to input some text.                                                                                                     |                                                                    |
    | Long Answer     | `'PA'` | Like `'SA'`, but should render a `textarea`.                                                                                                      |                                                                    |
    | Ranking         | `'RK'` | Allows users to assign a score between `range_min` and `range_max` in `range_step` increments for each choice in `choices`.                       | `choices`, `range_min`, `range_max`, `range_default`, `range_step` |

    # Examples

    ## Add Question to a Survey

    To add a question to a survey, `POST /api/surveys/<survey_id>/questions/`.  

    > Note: for simplicity, we will assume a survey with id `Wl95e9L` already exists.

    Only authenticated users can create questions.  

    ### Multiple Choice

    ``` text
    1. Which is better?  
    A. Star Trek
    B. Star Wars
    ```
    To create a multiple choice problem that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 1,
        "title": "Which is better?",
        "required": true,
        "type": "MC",
        "choices": [
            {"value": "A", "description": "Star Trek"},
            {"value": "B", "description": "Star Wars"}
        ]
    }

    // HTTP 201 Created
    {
        "id": "9vVr7jo",
        "number": 1,
        "title": "Which is better?",
        "required": true,
        "type": "MC",
        "choices": [
            {
                "id": "k2Odnya",
                "value": "A",
                "description": "Star Trek"
            },
            {
                "id": "rbN8VoP",
                "value": "B",
                "description": "Star Wars"
            }
        ]
    }
    ```

    ### Checkboxes

    ``` text
    2. Select all valid statements.
    [] A. 1 + 1 = 2
    [] B. 1 + 2 = 3
    [] C. 1 - 1 = 1
    ```
    To create a checkboxes question that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 2,
        "title": "Select all valid statements.",
        "required": false, // assume this question is not required
        "type": "CB",
        "choices": [
            {"value": "A", "description": "1 + 1 = 2"},
            {"value": "B", "description": "1 + 2 = 3"},
            {"value": "C", "description": "1 - 1 = 1"}
        ]
    }

    // HTTP 201 Created
    {
        "id": "RrVYK58",
        "number": 2,
        "title": "Select all valid statements.",
        "required": false,
        "type": "CB",
        "choices": [
            {
                "id": "kno9kNY",
                "value": "A",
                "description": "1 + 1 = 2"
            },
            {
                "id": "z6olEOk",
                "value": "B",
                "description": "1 + 2 = 3"
            },
            {
                "id": "XdNm4OB",
                "value": "C",
                "description": "1 - 1 = 1"
            }
        ]
    }
    ```

    ### Dropdown

    ``` text
    3. Which breakout room are you in?
    1. breakout room 1
    2. breakout room 2
    3. breakout room 3
    4. breakout room 4
    5. breakout room 5
    (render as a dropdown select box)
    ```
    To create a dropdown question that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 3,
        "title": "Which breakout room are you in?",
        "required": true,
        "type": "DP",
        "choices": [
            {"value": "1", "description": "breakout room 1"},
            {"value": "2", "description": "breakout room 2"},
            {"value": "3", "description": "breakout room 3"},
            {"value": "4", "description": "breakout room 4"},
            {"value": "5", "description": "breakout room 5"}
        ]
    }

    // HTTP 201 Created
    {
        "id": "qn5nMjM",
        "number": 3,
        "title": "Which breakout room are you in?",
        "required": true,
        "type": "DP",
        "choices": [
            {
                "id": "kDyYMy4",
                "value": "1",
                "description": "breakout room 1"
            },
            {
                "id": "GRNgkNl",
                "value": "2",
                "description": "breakout room 2"
            },
            {
                "id": "R4O58o9",
                "value": "3",
                "description": "breakout room 3"
            },
            {
                "id": "KaNQKob",
                "value": "4",
                "description": "breakout room 4"
            },
            {
                "id": "rYyebo8",
                "value": "5",
                "description": "breakout room 5"
            }
        ]
    }
    ```

    ### Scale

    ``` text
    4. From 1 to 10, how's your day going?
    |--+--+--+--@--+--+--+--+--|
    1  2  3  4  5  6  7  8  9  10
    ```
    To create a scale question that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 4,
        "title": "From 1 to 10, how's your day going?",
        "required": true,
        "type": "SC",
        "range_min": 1.0,
        "range_max": 10.0,
        "range_default": 5.0,  // default slider value is 5
        "range_step": 1.0      // goes in 1 point increments
    }

    // HTTP 201 Created
    {
        "id": "axVG0jy",
        "number": 4,
        "title": "From 1 to 10, how's your day going?",
        "required": true,
        "type": "SC",
        "range_min": 1.0,
        "range_max": 10.0,
        "range_default": 5.0,
        "range_step": 1.0
    }
    ```

    ### Short Answer

    ``` text
    5. What is your favorite fruit? [_________]
    ```
    To create a short answer question that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 5,
        "title": "What is your favorite fruit?",
        "required": true,
        "type": "SA"
    }

    // HTTP 201 Created
    {
        "id": "EYVJMDv",
        "number": 5,
        "title": "What is your favorite fruit?",
        "required": true,
        "type": "SA"
    }
    ```

    ### Paragraph

    ``` text
    6. Describe the city you live in.
    [textarea]
    ```
    To create a paragraph question that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 6,
        "title": "Describe the city you live in.",
        "required": true,
        "type": "PA"
    }

    // HTTP 201 Created
    {
        "id": "OmjRaVR",
        "number": 6,
        "title": "Describe the city you live in.",
        "required": true,
        "type": "PA"
    }
    ```

    ### Ranking

    ``` text
    7. Please rank the following roles:
            1   2   3   4   5
    A. CEO ( ) ( ) ( ) ( ) ( )
    B. CFO ( ) ( ) ( ) ( ) ( )
    C. COO ( ) ( ) ( ) ( ) ( )
    ```
    To create a ranking question that looks like the one above, do:

    ``` javascript
    // POST /api/surveys/Wl95e9L/questions/
    {
        "number": 7,
        "title": "Please rank the following roles:",
        "required": true,
        "type": "RK",
        "range_min": 1.0,
        "range_max": 5.0,
        "range_default": 1.0,
        "range_step": 1.0,
        "choices": [
            {"value": "A", "description": "CEO"},
            {"value": "B", "description": "CFO"},
            {"value": "C", "description": "COO"}
        ]
    }

    // HTTP 201 Created
    {
        "id": "oAVpWDl",
        "number": 7,
        "title": "Please rank the following roles:",
        "required": true,
        "type": "RK",
        "range_min": 1.0,
        "range_max": 5.0,
        "range_default": 1.0,
        "range_step": 1.0,
        "choices": [
            {
                "id": "knoA9o5",
                "value": "A",
                "description": "CEO"
            },
            {
                "id": "8BOEJN6",
                "value": "B",
                "description": "CFO"
            },
            {
                "id": "PeyzMN4",
                "value": "C",
                "description": "COO"
            }
        ]
    }
    ```

    > Note: It's ok to ignore `range_default` in this case.

    ## List Questions

    You can list all questions that a specific survey has. 

    ``` javascript
    // GET /api/surveys/<survey_id>/questions/

    // HTTP 200 OK
    [
        {
            "id": "axVG0jy",
            "number": 4,
            "title": "From 1 to 10, how's your day going?",
            "required": true,
            "type": "SC",
            "range_min": 1.0,
            "range_max": 10.0,
            "range_default": 5.0,
            "range_step": 1.0
        },
        {
            "id": "EYVJMDv",
            "number": 5,
            "title": "What is your favorite fruit?",
            "required": true,
            "type": "SA"
        },
        {
            "id": "OmjRaVR",
            "number": 6,
            "title": "Describe the city you live in.",
            "required": true,
            "type": "PA"
        }
        // ...
    ]
    ```



    ## Fetch Question

    To fetch a specific question, `GET /api/surveys/<survey_id>/questions/<question_id>/`.  

    ``` javascript
    // GET /api/surveys/<survey_id>/questions/OmjRaVR/

    // HTTP 200 OK
    {
        "id": "OmjRaVR",
        "number": 6,
        "title": "Describe the city you live in.",
        "required": true,
        "type": "PA"
    }
    ```

    ## Edit Question

    You can use `PATCH` (partial update) and `PUT` (full update) to edit a question.
    Only authenticated users can edit questions.  
    > Note: readonly fields cannot be changed.  

    ``` javascript
    // GET /api/surveys/<survey_id>/questions/OmjRaVR/

    // HTTP 200 OK
    {
        "id": "OmjRaVR",
        "number": 6,
        "title": "Describe the city you live in.",
        "required": true,
        "type": "PA"
    }

    // PATCH /api/surveys/<survey_id>/questions/OmjRaVR/
    {
        "title": "New question title"
    }

    // HTTP 200 OK
    {
        "id": "OmjRaVR",
        "number": 6,
        "title": "New question title",
        "required": true,
        "type": "PA"
    }
    ```

    Choices can also be edited using `PATCH`, but the entire list of choices must be provided.

    ``` javascript
    // GET /api/surveys/<survey_id>/questions/9vVr7jo/

    // HTTP 200 OK
    {
        "id": "9vVr7jo",
        "number": 1,
        "title": "Which is better?",
        "required": true,
        "type": "MC",
        "choices": [
            {
                "id": "k2Odnya",
                "value": "A",
                "description": "Star Trek"
            },
            {
                "id": "rbN8VoP",
                "value": "B",
                "description": "Star Wars"
            }
        ]
    }

    // PATCH /api/surveys/<survey_id>/questions/9vVr7jo/
    {
        "choices": [
            { // to keep an existing choice, include it in the list
                "id": "k2Odnya",
                "value": "A",
                // optionally you can edit an existing choice
                "description": "Star Trek II: The Wrath of Khan"
            },
            { // a choice without an id will be created
                "value": "B (new)",
                "description": "Stargate"
            }
            // any existing choices not in the list will be deleted, e.g. rbN8VoP
        ]
    }

    // HTTP 200 OK
    {
        "id": "9vVr7jo",
        "number": 1,
        "title": "Which is better?",
        "required": true,
        "type": "MC",
        "choices": [
            {
                "id": "k2Odnya", // note the id remains unchanged
                "value": "A",
                "description": "Star Trek II: The Wrath of Khan"
            },
            {
                "id": "pgN4qyl",
                "value": "B (new)",
                "description": "Stargate"
            }
        ]
    }
    ```

    ## Delete Question

    To delete a specific question, `DELETE /api/surveys/<survey_id>/questions/<question_id>/`. 
    Only authenticated users can delete questions.  
    > Note: deleting a question also removes all associated responses. 

    ``` javascript
    // DELETE /api/surveys/<survey_id>/questions/OmjRaVR/

    // HTTP 204 No Content
    ```
    """
    serializer_class = NestedSurveyQuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # disable pagination

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


class NestedSurveySessionViewSet(NestedViewMixIn, viewsets.ModelViewSet):
    """
    API endpoint that allows survey sessions to be created or viewed.
    """
    serializer_class = NestedSurveySessionSerializer
    # we can change this later
    permission_classes = [IsAuthenticatedOrReadOnly]

    parent_model_queryset = Survey.objects.all()
    parent_pk_name = 'survey_pk'

    @handle_invalid_hashid('Survey')
    def get_queryset(self):
        return SurveySession.objects\
            .select_related('survey')\
            .filter(survey=self.kwargs['survey_pk'])

    def perform_create(self, serializer):
        code = random.randint(1000, 9999)
        while SurveySession.objects.filter(code=code).exists():
            code = random.randint(1000, 9999)
        serializer.save(code=code)


class CodeToSessionViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    API endpoint that looks up a SurveySession by its `code`.

    # Field Description

    See [SurveySession](/api/sessions/).

    # Examples

    ## Lookup Session by Code

    To fetch the session with a specific code, `GET /api/code/<code>/`.

    ``` javascript
    // GET /api/code/1234/

    // HTTP 200 OK
    {
        "id": "Dy07DNq",
        "code": 1234,
        "survey": "Wl95e9L"
    }

    ```
    """
    serializer_class = NestedSurveySessionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SurveySession.objects.all()
    lookup_field = 'code'
