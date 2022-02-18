from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from django.utils.translation import gettext_lazy as _
from .models import (Survey, SurveyQuestion, SurveyQuestionChoice,
                     SurveyResponse, SurveySubmission, Survey)
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
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Survey
        fields = ['id', 'owner', 'title', 'description', 'created_at',
                  'active', 'start_date_time', 'end_date_time']


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

    conditional_fields = {
        'choices': [
            SurveyQuestion.QuestionType.MULTICHOICE,
            SurveyQuestion.QuestionType.CHECKBOXES,
            SurveyQuestion.QuestionType.DROPDOWN
        ],
        'range_min': [SurveyQuestion.QuestionType.SCALE],
        'range_max': [SurveyQuestion.QuestionType.SCALE],
        'range_default': [SurveyQuestion.QuestionType.SCALE],
        'range_step': [SurveyQuestion.QuestionType.SCALE]
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
        instance_question_type = self.instance.type if self.instance else None
        question_type = data.get('type', instance_question_type)
        for field, type_list in self.conditional_fields.items():
            field_data = data.get(field, None)
            if question_type in type_list and field_data is None:
                raise serializers.ValidationError(
                    {field: f'{field!r} is required for question type {question_type!r}'}
                )
            elif question_type not in type_list and field_data is not None:
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


class SurveyQuestionSerializer(NestedSurveyQuestionSerializer):
    survey = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field='survey.Survey.id'),
        queryset=Survey.objects.all()
    )

    class Meta(NestedSurveyQuestionSerializer.Meta):
        pass


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
            SurveyQuestion.QuestionType.DROPDOWN
        ],
        'text': [
            SurveyQuestion.QuestionType.SHORT_ANSWER,
            SurveyQuestion.QuestionType.PARAGRAPH
        ],
        'numeric_value': [SurveyQuestion.QuestionType.SCALE]
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
        and make sure choice matches question.
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
    survey = serializers.HiddenField(
        default=SerializerContextDefault(
            lambda context: context['view'].parent_instance
        )
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    responses = NestedSurveyResponseSerializer(many=True)

    class Meta:
        model = SurveySubmission
        fields = ['id', 'survey', 'user', 'submission_time', 'responses']

    def validate(self, data):
        """
        Make sure all responses are associated with the given survey and
        all required questions are answered.
        """

        count = dict()
        seen_choices = set()

        for response in data['responses']:
            question = response['question']
            count[question] = count.get(question, 0) + 1
            if question.choice is not None:
                if question.choice in seen_choices:
                    raise serializers.ValidationError(
                        _("Can't select the same choice (id={c_id}) twice.").format(
                            c_id=question.choice.id
                        )
                    )
                seen_choices.add(question.choice)

        for question in data['survey'].questions.all():
            if question in count:
                # check for duplicate answers
                if question.type != SurveyQuestion.QuestionType.CHECKBOXES and count[question] > 1:
                    raise serializers.ValidationError(
                        _("Duplicate answers not allowed for {question_type!r}(id={q_id}).").format(
                            question_type=question.type,
                            q_id=question.id
                        )
                    )
                count.pop(question)
            # required but not provided
            elif question.required:
                raise serializers.ValidationError(
                    _("Question {q_id} is required.").format(q_id=question.id)
                )

        # check for questions that don't belong to the given survey
        if len(count) > 0:
            raise serializers.ValidationError(
                _("Questions {q_ids} are invalid for survey {s_id}.").format(
                    q_ids=','.join(str(q.id) for q in count.keys()),
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


class SurveySubmissionSerializer(NestedSurveySubmissionSerializer):
    survey = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field='survey.Survey.id'),
        queryset=Survey.objects.all()
    )

    class Meta(NestedSurveySubmissionSerializer.Meta):
        pass
