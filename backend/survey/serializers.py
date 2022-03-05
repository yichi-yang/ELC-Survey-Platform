from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from django.utils.translation import gettext_lazy as _
from collections import defaultdict
from .models import (Survey, SurveyQuestion, SurveyQuestionChoice,
                     SurveyResponse, SurveySubmission, Survey, SurveySession)
from .validators import OwnedByRequestUser


class SerializerContextDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Retrieves a value from serializer context as the default value.
    """
    requires_context = True

    def __init__(self, get_value):
        self.get_value = get_value

    def __call__(self, serializer_field):
        return self.get_value(serializer_field.context)


class SurveySerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(
        source_field='survey.Survey.id',
        read_only=True
    )
    group_by_question = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field='survey.SurveyQuestion.id'),
        queryset=SurveyQuestion.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description',
                  'draft', 'group_by_question', 'created_at']

    def validate_group_by_question(self, question):
        """
        Check that the question belongs to current survey.
        """
        if question is None:
            return question

        if question.survey != self.instance:
            raise serializers.ValidationError(
                "group_by_question doesn't belong to this survey"
            )
        if question.type not in [
            SurveyQuestion.QuestionType.MULTICHOICE.value,
            SurveyQuestion.QuestionType.DROPDOWN.value
        ]:
            raise serializers.ValidationError(
                "group_by_question must be a multiple choice or dropdown question"
            )
        return question


class NestedSurveyQuestionChoiceSerializer(serializers.ModelSerializer):
    # can't be readonly because we need the id for updating choices
    id = HashidSerializerCharField(
        source_field='survey.SurveyQuestionChoice.id', required=False
    )

    class Meta:
        model = SurveyQuestionChoice
        fields = ['id', 'value', 'description']


class NestedSurveyQuestionSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(
        source_field='survey.Survey.id',
        read_only=True
    )
    survey = serializers.HiddenField(
        default=SerializerContextDefault(
            lambda context: context['view'].parent_instance
        ),
        validators=[OwnedByRequestUser()]
    )
    choices = NestedSurveyQuestionChoiceSerializer(many=True, required=False)

    # some fields are only required by certain question types
    conditional_fields = {
        'choices': [
            SurveyQuestion.QuestionType.MULTICHOICE,
            SurveyQuestion.QuestionType.CHECKBOXES,
            SurveyQuestion.QuestionType.DROPDOWN,
            SurveyQuestion.QuestionType.RANKING,
        ],
        'range_min': [
            SurveyQuestion.QuestionType.SCALE,
            SurveyQuestion.QuestionType.RANKING,
        ],
        'range_max': [
            SurveyQuestion.QuestionType.SCALE,
            SurveyQuestion.QuestionType.RANKING,
        ],
        'range_default': [
            SurveyQuestion.QuestionType.SCALE,
            SurveyQuestion.QuestionType.RANKING,
        ],
        'range_step': [
            SurveyQuestion.QuestionType.SCALE,
            SurveyQuestion.QuestionType.RANKING,
        ]
    }

    class Meta:
        model = SurveyQuestion
        fields = ['id', 'survey', 'number', 'title', 'required', 'type',
                  'range_min', 'range_max', 'range_default', 'range_step', 'choices']

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        for field, type_list in self.conditional_fields.items():
            if representation['type'] not in type_list:
                representation.pop(field)
        return representation

    def validate(self, data):
        """
        Check if required fields exist based on question types.
        """
        # check required fields exists
        instance_question_type = self.instance.type if self.instance else None
        question_type = data.get('type', instance_question_type)
        for field, required_by_type in self.conditional_fields.items():
            field_data = data.get(field, None)
            if question_type in required_by_type and field_data is None:
                raise serializers.ValidationError(
                    {field: f'{field!r} is required for question type {question_type!r}'}
                )
            elif question_type not in required_by_type and field_data is not None:
                raise serializers.ValidationError(
                    {field: f'{field!r} is redundant for question type {question_type!r}'}
                )

        if data.get("range_min", None) is not None:
            if not (data['range_min'] <= data['range_max']):
                raise serializers.ValidationError(
                    {
                        'range_min': _('range_min must be less than or equal to range_max.'),
                        'range_max':  _('range_max must be greater than or equal to range_min.')
                    }
                )
            if not (data['range_min'] <= data['range_default']):
                raise serializers.ValidationError(
                    {
                        'range_default':  _('range_default must be greater than or equal to range_min.')
                    }
                )
            if not (data['range_max'] >= data['range_default']):
                raise serializers.ValidationError(
                    {
                        'range_default':  _('range_default must be less than or equal to range_max.')
                    }
                )
        return data

    def create(self, validated_data):
        """
        Create the SurveyQuestion and its SurveyQuestionChoices.
        """
        choices = validated_data.pop('choices', [])
        question = super().create(validated_data)
        for choice_data in choices:
            # remove the id if exists - id will be auto created
            choice_data.pop('id', None)
            SurveyQuestionChoice.objects.create(
                question=question, **choice_data
            )
        return question

    def update(self, instance, validated_data):
        """
        Update the SurveyQuestion and its SurveyQuestionChoices.
        """

        choices = validated_data.pop('choices', [])

        # If a choice already has an id, we will update it with the new values.
        # We should create new choices for those in the list that have no id.
        create_choices = []
        update_choices = {}
        for choice in choices:
            if 'id' in choice:
                update_choices[choice['id']] = choice
            else:
                create_choices.append(choice)

        for choice in instance.choices.all():
            if choice.id in update_choices:
                for attr, value in update_choices[choice.id].items():
                    setattr(choice, attr, value)
                choice.save()
            else:
                # remove those not in the update list
                choice.delete()

        for choice_data in create_choices:
            SurveyQuestionChoice.objects.create(
                question=instance, **choice_data)

        # update the SurveyQuestion instance
        super().update(instance, validated_data)

        return instance


class NestedSurveyResponseSerializer(serializers.ModelSerializer):

    question = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field='survey.SurveyQuestion.id'
        ),
        queryset=SurveyQuestion.objects.all()
    )
    choice = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field='survey.SurveyQuestionChoice.id'
        ),
        queryset=SurveyQuestionChoice.objects.all(),
        required=False
    )

    conditional_fields = {
        'choice': [
            SurveyQuestion.QuestionType.MULTICHOICE,
            SurveyQuestion.QuestionType.CHECKBOXES,
            SurveyQuestion.QuestionType.DROPDOWN,
            SurveyQuestion.QuestionType.RANKING
        ],
        'text': [
            SurveyQuestion.QuestionType.SHORT_ANSWER,
            SurveyQuestion.QuestionType.PARAGRAPH
        ],
        'numeric_value': [
            SurveyQuestion.QuestionType.SCALE,
            SurveyQuestion.QuestionType.RANKING
        ]
    }

    class Meta:
        model = SurveyResponse
        fields = ['question', 'choice', 'text', 'numeric_value']

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        for field, type_list in self.conditional_fields.items():
            if obj.question.type not in type_list:
                representation.pop(field)
        return representation

    def validate(self, data):
        """
        Check if required fields exist based on question types
        and make sure the choice matches question.
        """

        question = data['question']

        # check if required fields exist based on question types
        for field, type_list in self.conditional_fields.items():
            field_data = data.get(field, None)
            if question.type in type_list and field_data is None:
                raise serializers.ValidationError(
                    {field: f'{field!r} is required for question type {question.type!r}'}
                )
            elif question.type not in type_list and field_data is not None:
                raise serializers.ValidationError(
                    {field: f'{field!r} is invalid for question type {question.type!r}'}
                )

        if 'choice' in data:
            # make sure that the choice is valid for the question
            # if we want to set/update either (or both)
            if data['choice'].question != question:
                raise serializers.ValidationError(
                    {'choice': f'Invalid choice for question {question.id}'}
                )

        if 'numeric_value' in data:
            # make sure the value is in range
            if not (question.range_min <= data['numeric_value'] <= question.range_max):
                raise serializers.ValidationError(
                    {'numeric_value': f'Value must be between {question.range_min} and {question.range_max}.'}
                )

        return data

    def update(self, instance, validated_data):
        """
        Updating a response is not supported.
        """
        raise NotImplementedError('Updating a response is not supported.')


class NestedSurveySubmissionSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(
        source_field='survey.SurveySubmission.id',
        read_only=True
    )
    session = serializers.HiddenField(
        default=SerializerContextDefault(
            lambda context: context['view'].parent_instance
        )
    )
    responses = NestedSurveyResponseSerializer(many=True)

    class Meta:
        model = SurveySubmission
        fields = ['id', 'session', 'submission_time', 'responses']

    def validate(self, data):
        """
        Make sure all responses are associated with the given survey and
        all required questions are answered.
        """

        existing_choices = set()
        question_response_count = defaultdict(int)

        for response in data['responses']:
            # count how many responses a question have
            question_response_count[response['question'].id] += 1

            # make sure choices are unique
            if 'choice' in response:
                if response['choice'].id in existing_choices:
                    raise serializers.ValidationError(
                        "Selected choices must be unique (choice {id})."
                        .format(id=response['choice'].id)
                    )
                else:
                    existing_choices.add(response['choice'].id)

        for question in data['session'].survey.questions.all():
            # number of responses for current question
            response_count = question_response_count[question.id]

            # make sure a response is provided if the question is required
            if question.required and response_count == 0:
                raise serializers.ValidationError(
                    "Question {id} is required.".format(id=question.id)
                )

            if response_count != 0:
                q_type = SurveyQuestion.QuestionType(question.type).label
                # check for too many responses
                if response_count < question.min_responses:
                    raise serializers.ValidationError(
                        "Not enough responses for {type!r} {id}.".format(
                            type=q_type,
                            id=question.id
                        )
                    )
                elif response_count > question.max_responses:
                    raise serializers.ValidationError(
                        "Too many responses for {type!r} {id}.".format(
                            type=q_type,
                            id=question.id
                        )
                    )

            question_response_count.pop(question.id)

        # check for questions that don't belong to the given survey
        if len(question_response_count) > 0:
            question_ids = question_response_count.keys()
            raise serializers.ValidationError(
                _("Questions {q_ids} are invalid for survey {s_id}.").format(
                    q_ids=','.join(str(q.id) for q in question_ids),
                    s_id=data['survey'].id
                )
            )

        return data

    def create(self, validated_data):
        """
        Create the SurveySubmission and its SurveyResponses.
        """
        responses = validated_data.pop('responses', [])
        submission = super().create(validated_data)
        for response_data in responses:
            SurveyResponse.objects.create(
                submission=submission, **response_data)
        return submission

    def update(self, instance, validated_data):
        """
        Updating a submission is not supported.
        """
        raise NotImplementedError('Updating a submission is not supported.')


class SurveySessionSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(
        source_field='survey.Survey.id',
        read_only=True
    )
    survey = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field='survey.Survey.id'),
        queryset=Survey.objects.all()
    )
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #code = serializers.IntegerField(allow_null=True)

    class Meta:
        model = SurveySession
        fields = ['id', 'code', 'survey', 'owner']
        read_only_fields = ('survey', 'owner', 'code')
