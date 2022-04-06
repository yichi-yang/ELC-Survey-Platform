from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from survey.models import Survey, SurveyQuestion, SurveyQuestionChoice


class SurveyQuestionViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('some user')
        self.survey = Survey(
            title='test survey',
            description='test description'
        )
        self.survey.save()

    def test_create_multiple_choice_question(self):
        """ authenticated users can add a multiple choice question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # multiple choice question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 1,
                "title": "Which is better?",
                "required": True,
                "type": "MC",
                "choices": [
                    {"value": "A", "description": "Star Trek"},
                    {"value": "B", "description": "Star Wars"}
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 1,
        #     "title": "Which is better?",
        #     "required": True,
        #     "type": "MC",
        #     "choices": [
        #         {"id": "<unique id>", "value": "A", "description": "Star Trek"},
        #         {"id": "<unique id>", "value": "B", "description": "Star Wars"}
        #     ]
        # },

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # also question.choices will have individual ids
        choices = question_data.pop('choices')
        for choice in choices:
            self.assertTrue(
                SurveyQuestionChoice.objects.filter(pk=choice.pop('id'))
                .exists()
            )
        # other than the ids, the response should look the same
        self.assertListEqual(
            choices,
            [
                {'value': 'A', 'description': 'Star Trek'},
                {'value': 'B', 'description': 'Star Wars'},
            ]
        )
        self.assertDictEqual(
            question_data,
            {
                'number': 1,
                'title': 'Which is better?',
                'required': True,
                'type': 'MC',
            }
        )

    def test_create_checkboxes_question(self):
        """ authenticated users can add a checkboxes question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # checkboxes question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 2,
                "title": "Select all valid statements.",
                "required": False,  # let's say this question is not required
                "type": "CB",
                "choices": [
                    {"value": "A", "description": "1 + 1 = 2"},
                    {"value": "B", "description": "1 + 2 = 3"},
                    {"value": "C", "description": "1 - 1 = 1"}
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 2,
        #     "title": "Select all valid statements.",
        #     "required": False,
        #     "type": "CB",
        #     "choices": [
        #         {"id": "<unique id>", "value": "A", "description": "1 + 1 = 2"},
        #         {"id": "<unique id>", "value": "B", "description": "1 + 2 = 3"},
        #         {"id": "<unique id>", "value": "C", "description": "1 - 1 = 1"}
        #     ]
        # }

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # also question.choices will have individual ids
        choices = question_data.pop('choices')
        for choice in choices:
            self.assertTrue(
                SurveyQuestionChoice.objects.filter(pk=choice.pop('id'))
                .exists()
            )
        # other than the ids, the response should look the same
        self.assertListEqual(
            choices,
            [
                {"value": "A", "description": "1 + 1 = 2"},
                {"value": "B", "description": "1 + 2 = 3"},
                {"value": "C", "description": "1 - 1 = 1"}
            ]
        )
        self.assertDictEqual(
            question_data,
            {
                "number": 2,
                "title": "Select all valid statements.",
                "required": False,
                "type": "CB",
            }
        )

    def test_create_dropdown_question(self):
        """ authenticated users can add a dropdown question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # dropdown question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 3,
                "title": "Which breakout room are you in?",
                "required": True,
                "type": "DP",
                "choices": [
                    {"value": "1", "description": "breakout room 1"},
                    {"value": "2", "description": "breakout room 2"},
                    {"value": "3", "description": "breakout room 3"},
                    {"value": "4", "description": "breakout room 4"},
                    {"value": "5", "description": "breakout room 5"}
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 3,
        #     "title": "Which breakout room are you in?",
        #     "required": True,
        #     "type": "DP",
        #     "choices": [
        #         {"id": "<unique id>", "value": "1", "description": "breakout room 1"},
        #         {"id": "<unique id>", "value": "2", "description": "breakout room 2"},
        #         {"id": "<unique id>", "value": "3", "description": "breakout room 3"},
        #         {"id": "<unique id>", "value": "4", "description": "breakout room 4"},
        #         {"id": "<unique id>", "value": "5", "description": "breakout room 5"}
        #     ]
        # }

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # also question.choices will have individual ids
        choices = question_data.pop('choices')
        for choice in choices:
            self.assertTrue(
                SurveyQuestionChoice.objects.filter(pk=choice.pop('id'))
                .exists()
            )
        # other than the ids, the response should look the same
        self.assertListEqual(
            choices,
            [
                {"value": "1", "description": "breakout room 1"},
                {"value": "2", "description": "breakout room 2"},
                {"value": "3", "description": "breakout room 3"},
                {"value": "4", "description": "breakout room 4"},
                {"value": "5", "description": "breakout room 5"}
            ]
        )
        self.assertDictEqual(
            question_data,
            {
                "number": 3,
                "title": "Which breakout room are you in?",
                "required": True,
                "type": "DP",
            }
        )

    def test_create_scale_question(self):
        """ authenticated users can add a scale question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # scale question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 4,
                "title": "From 1 to 10, how's your day going?",
                "required": True,
                "type": "SC",
                "range_min": 1.0,
                "range_max": 10.0,
                "range_default": 5.0,  # default slider value is 5
                "range_step": 1.0,  # goes in 1 point increments
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 4,
        #     "title": "From 1 to 10, how's your day going?",
        #     "required": True,
        #     "type": "SC",
        #     "range_min": 1.0,
        #     "range_max": 10.0,
        #     "range_default": 5.0,
        #     "range_step": 1.0,
        # }

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # other than the id, the response should look the same
        self.assertDictEqual(
            question_data,
            {
                "number": 4,
                "title": "From 1 to 10, how's your day going?",
                "required": True,
                "type": "SC",
                "range_min": 1.0,
                "range_max": 10.0,
                "range_default": 5.0,
                "range_step": 1.0,
            }
        )

    def test_create_short_answer_question(self):
        """ authenticated users can add a short answer question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # short answer question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 5,
                "title": "What is your favorite fruit?",
                "required": True,
                "type": "SA"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 5,
        #     "title": "What is your favorite fruit?",
        #     "required": True,
        #     "type": "SA"
        # }

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # other than the id, the response should look the same
        self.assertDictEqual(
            question_data,
            {
                "number": 5,
                "title": "What is your favorite fruit?",
                "required": True,
                "type": "SA"
            }
        )

    def test_create_paragraph_question(self):
        """ authenticated users can add a paragraph question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # paragraph question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 6,
                "title": "Describe the city you live in.",
                "required": True,
                "type": "PA"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 6,
        #     "title": "Describe the city you live in.",
        #     "required": True,
        #     "type": "PA"
        # }

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # other than the id, the response should look the same
        self.assertDictEqual(
            question_data,
            {
                "number": 6,
                "title": "Describe the city you live in.",
                "required": True,
                "type": "PA"
            }
        )

    def test_create_ranking_question(self):
        """ authenticated users can add a ranking question to the survey """

        # log the user in
        self.client.force_authenticate(self.user)

        # multiple choice question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 7,
                "title": "Please rank the following roles:",
                "required": True,
                "type": "RK",
                "range_min": 1.0,  # rank between 1 .. 7 in 1 point increments
                "range_max": 7.0,
                "range_default": 1.0,  # defaults to 1
                "range_step": 1.0,
                "choices": [
                    {"value": "A", "description": "CEO"},
                    {"value": "B", "description": "CFO"},
                    {"value": "C", "description": "COO"}
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # response should look like:
        # {
        #     "id": "<unique id>",
        #     "number": 1,
        #     "title": "Which is better?",
        #     "required": True,
        #     "type": "RK",
        #     "range_min": 1.0,
        #     "range_max": 7.0,
        #     "range_default": 1.0,
        #     "range_step": 1.0,
        #     "choices": [
        #         {"id": "<unique id>", "value": "A", "description": "CEO"},
        #         {"id": "<unique id>", "value": "B", "description": "CFO"},
        #         {"id": "<unique id>", "value": "C", "description": "COO"}
        #     ]
        # },

        # response will include question.id which we
        # don't know when we create the question
        question_data = response.data
        question_id = question_data.pop('id')
        self.assertTrue(SurveyQuestion.objects.filter(pk=question_id).exists())
        # also question.choices will have individual ids
        choices = question_data.pop('choices')
        for choice in choices:
            self.assertTrue(
                SurveyQuestionChoice.objects.filter(pk=choice.pop('id'))
                .exists()
            )
        # other than the ids, the response should look the same
        self.assertListEqual(
            choices,
            [
                {"value": "A", "description": "CEO"},
                {"value": "B", "description": "CFO"},
                {"value": "C", "description": "COO"}
            ]
        )
        self.assertDictEqual(
            question_data,
            {
                "number": 7,
                "title": "Please rank the following roles:",
                "required": True,
                "type": "RK",
                "range_min": 1.0,
                "range_max": 7.0,
                "range_default": 1.0,
                "range_step": 1.0,
            }
        )

    def test_create_multiple_choice_question_no_choices(self):
        """ multiple choice questions must have choices """

        # log the user in
        self.client.force_authenticate(self.user)

        # multiple choice question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 1,
                "title": "Which is better?",
                "required": True,
                "type": "MC",
                # "choices": [
                #     {"value": "A", "description": "Star Trek"},
                #     {"value": "B", "description": "Star Wars"}
                # ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_checkboxes_question_no_choices(self):
        """ checkboxes question must have choices """

        # log the user in
        self.client.force_authenticate(self.user)

        # checkboxes question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 2,
                "title": "Select all valid statements.",
                "required": False,  # let's say this question is not required
                "type": "CB",
                # "choices": [
                #     {"value": "A", "description": "1 + 1 = 2"},
                #     {"value": "B", "description": "1 + 2 = 3"},
                #     {"value": "C", "description": "1 - 1 = 1"}
                # ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_dropdown_question_no_choices(self):
        """ dropdown questions must have choices """

        # log the user in
        self.client.force_authenticate(self.user)

        # dropdown question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 3,
                "title": "Which breakout room are you in?",
                "required": True,
                "type": "DP",
                # "choices": [
                #     {"value": "1", "description": "breakout room 1"},
                #     {"value": "2", "description": "breakout room 2"},
                #     {"value": "3", "description": "breakout room 3"},
                #     {"value": "4", "description": "breakout room 4"},
                #     {"value": "5", "description": "breakout room 5"}
                # ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_scale_question_no_min_max_default_step(self):
        """ scale question must have min, max, default and step """

        # log the user in
        self.client.force_authenticate(self.user)

        # scale question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 4,
                "title": "From 1 to 10, how's your day going?",
                "required": True,
                "type": "SC",
                # "range_min": 1.0,
                # "range_max": 10.0,
                # "range_default": 5.0,  # default slider value is 5
                # "range_step": 1.0,  # goes in 1 point increments
            },
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_checkboxes_question_additional_nones_are_fine(self):
        """ checkboxes question must have choices """

        # log the user in
        self.client.force_authenticate(self.user)

        # checkboxes question
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            {
                "number": 2,
                "title": "Select all valid statements.",
                "required": False,
                "type": "CB",
                "range_min": None,  # these Nones are ignored
                "range_max": None,
                "range_default": None,
                "range_step": None,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_question_permissions(self):
        """
        authenticated users can add questions to a survey
        """

        question_data = {
            "number": 42,
            "title": "What is the Answer to the Ultimate Question of Life, the Universe, and Everything?",
            "required": True,
            "type": "SA"
        }

        # authenticated users can add questions
        self.client.force_authenticate(self.user)

        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            question_data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)

        # unauthenticated users can't add questions
        self.client.force_authenticate()

        response = self.client.post(
            f'/api/surveys/{self.survey.id}/questions/',
            question_data,
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_question(self):
        """
        GET /surveys/<id>/questions/ lists all questions of that survey
        """

        self.client.force_authenticate(self.user)

        # the survey doesn't have any question yet
        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([], response.data)

        # create 2 questions
        questions = [
            {
                'number': 1,
                'title': 'dummy question 1',
                'type': 'SA',
                'required': False
            },
            {
                'number': 2,
                'title': 'dummy question 2',
                'type': 'SA',
                'required': False
            }
        ]
        for question in questions:
            instance = SurveyQuestion(survey=self.survey, **question)
            instance.save()
            question['id'] = instance.id  # save the id

        # now listing the questions should show the 2 new questions
        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(questions, response.data)

    def test_list_question_permissions(self):
        """
        anyone can list questions,
        """

        # authenticated users can always list questions
        self.client.force_authenticate(self.user)

        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/'
        )
        self.assertEqual(response.status_code, 200)

        # unauthenticated users can also list questions
        self.client.force_authenticate()

        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/'
        )
        self.assertEqual(response.status_code, 200)

    def test_fetch_question(self):
        """
        GET /surveys/<survey_id>/questions/<question_id>/ return the question
        """

        self.client.force_authenticate(self.user)

        question_data = {
            'number': 1,
            'title': 'dummy question 1',
            'type': 'SA',
            'required': False
        }

        # create a questions
        instance = SurveyQuestion(survey=self.survey, **question_data)
        instance.save()
        question_data['id'] = instance.id  # save the id

        # now fetch the question should return the new question
        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/{instance.id }/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(question_data, response.data)

    def test_fetch_question_permissions(self):
        """
        Anyone can fetch questions.
        """

        self.client.force_authenticate(self.user)

        question_data = {
            'number': 1,
            'title': 'dummy question 1',
            'type': 'SA',
            'required': False
        }

        # create questions
        question = SurveyQuestion(survey=self.survey, **question_data)
        question.save()

        # authenticated users can always list questions
        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/'
        )
        self.assertEqual(response.status_code, 200)

        # unauthenticated users can list questions too
        self.client.force_authenticate()

        response = self.client.get(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/'
        )
        self.assertEqual(response.status_code, 200)

    def test_update_question(self):
        """
        PUT or PATCH /surveys/<survey_id>/questions/<question_id>/ edits the question 
        """

        self.client.force_authenticate(self.user)

        question_data = {
            'number': 1,
            'title': 'dummy question 1',
            'type': 'SA',
            'required': False
        }

        # create a question
        instance = SurveyQuestion(survey=self.survey, **question_data)
        instance.save()
        question_data['id'] = instance.id  # save the id

        # now fetch the question should return the new question
        response = self.client.patch(
            f'/api/surveys/{self.survey.id}/questions/{instance.id }/',
            {
                'number': 42,
                'title': 'changed',
                'required': True
            },
            format='json'
        )

        updated_question_data = {**question_data}

        updated_question_data['number'] = 42
        updated_question_data['title'] = 'changed'
        updated_question_data['required'] = True

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(updated_question_data, response.data)

    def test_update_question_choices(self):
        """
        PUT or PATCH /surveys/<survey_id>/questions/<question_id>/ can also be
        used to edit question choices
        """

        self.client.force_authenticate(self.user)

        # create a multiple choice question
        question = SurveyQuestion(
            survey=self.survey,
            number=100,
            title='1 + 1 = ?',
            type='MC',
            required=True
        )
        question.save()

        choiceA = SurveyQuestionChoice(
            question=question,
            value='A',
            description='1'
        )
        choiceA.save()
        choiceB = SurveyQuestionChoice(
            question=question,
            value='B',
            description='2'
        )
        choiceB.save()

        # if you fetch the question now it should be:
        # {
        #     "id": "<unique id>",
        #     "number": 100,
        #     "title": "1 + 1 = ?",
        #     "required": True,
        #     "type": "MC",
        #     "choices": [
        #         {"id": "<unique id>", "value": "A", "description": "1"},
        #         {"id": "<unique id>", "value": "B", "description": "2"}
        #     ]
        # }

        # now fetch the question should return the new question
        response = self.client.patch(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/',
            {
                'choices': [
                    # If you want to keep/update an existing choice, be
                    # sure to include a choice with that id.
                    # This will update that specific choice.
                    {
                        'id': str(choiceA.id),  # <--
                        'value': choiceA.value,
                        'description': '1 + 1 = 1'
                    },
                    # To add a new choice, include a choice without id.
                    {
                        'value': 'C',
                        'description': '1 + 1 = 3'
                    }
                    # To delete an existing choice, just leave it out.
                    # In this case choiceB will be removed.
                ]
            },
            format='json'
        )

        # if you fetch the question now it should be:
        # {
        #     "id": "<unique id>",
        #     "number": 100,
        #     "title": "1 + 1 = ?",
        #     "required": True,
        #     "type": "MC",
        #     "choices": [
        #         {"id": "<unique id>", "value": "A", "description": "1 + 1 = 1"},
        #         {"id": "<unique id>", "value": "C", "description": "1 + 1 = 3"}
        #     ]
        # }

        self.assertEqual(response.status_code, 200)
        # Now there should be 2 choices: A & C
        choices = response.data['choices']
        # Choice A is kept and updated
        self.assertEqual(choiceA.id, choices[0].pop('id'))
        # Choice C is new
        self.assertNotEqual(choiceB.id, choices[1].pop('id'))
        self.assertListEqual(
            choices,
            [
                {"value": "A", "description": "1 + 1 = 1"},
                {"value": "C", "description": "1 + 1 = 3"}
            ]
        )

    def test_update_question_permissions(self):
        """
        only authenticated users can update questions
        """

        self.client.force_authenticate(self.user)

        question_data = {
            'number': 1,
            'title': 'dummy question 1',
            'type': 'SA',
            'required': False
        }

        # create questions
        question = SurveyQuestion(survey=self.survey, **question_data)
        question.save()

        # authenticated users can update questions
        response = self.client.patch(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/',
            {
                'title': 'changed',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)

        # unauthenticated users can't update questions
        self.client.force_authenticate()

        response = self.client.patch(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/',
            {
                'title': 'changed',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_question(self):
        """
        DELETE /surveys/<survey_id>/questions/<question_id>/ removes a question
        """

        self.client.force_authenticate(self.user)

        # create a question
        question_data = {
            'number': 1,
            'title': 'dummy question 1',
            'type': 'SA',
            'required': False
        }

        # create questions
        instance = SurveyQuestion(survey=self.survey, **question_data)
        instance.save()

        self.assertTrue(SurveyQuestion.objects.filter(pk=instance.id).exists())

        # now delete the question
        response = self.client.delete(
            f'/api/surveys/{self.survey.id}/questions/{instance.id}/'
        )

        self.assertEqual(response.status_code, 204)

        # make sure it's deleted
        self.assertFalse(
            SurveyQuestionChoice.objects.filter(pk=instance.id).exists()
        )

    def test_delete_question_permissions(self):
        """
        only authenticated users can delete questions
        """

        self.client.force_authenticate(self.user)

        # create a question
        question_data = {
            'number': 1,
            'title': 'dummy question 1',
            'type': 'SA',
            'required': False
        }

        # create questions
        question = SurveyQuestion(survey=self.survey, **question_data)
        question.save()

        # unauthenticated users can't delete questions
        self.client.force_authenticate()

        response = self.client.delete(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/'
        )
        self.assertEqual(response.status_code, 401)

        # authenticated users can delete questions
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            f'/api/surveys/{self.survey.id}/questions/{question.id}/'
        )
        self.assertEqual(response.status_code, 204)
