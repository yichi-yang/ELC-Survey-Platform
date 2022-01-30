from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone, dateparse
from rest_framework.test import APIClient
from datetime import timedelta
from survey.models import Survey, SurveyQuestion, SurveyQuestionChoice


class SurveyViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        # clean up survey and user objects after each test
        Survey.objects.all().delete()
        User.objects.all().delete()

    def test_create_survey(self):
        """only authenticated users can create surveys"""

        user = User.objects.create_user('some user')
        # log the user in
        self.client.force_authenticate(user)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'test_create_survey',
                'description': 'only authenticated users can create surveys',
                'active': True
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        response_data = response.data

        # Sanity check for id and created_at
        survey = Survey.objects.get(pk=response_data.pop('id'))
        self.assertEqual(survey.title, 'test_create_survey')
        created_at = dateparse.parse_datetime(response_data.pop('created_at'))
        now = timezone.now()
        self.assertLess(abs(now - created_at), timedelta(seconds=1))

        # The rest should be the same.
        self.assertDictEqual(
            response_data,
            {
                'title': 'test_create_survey',
                'description': 'only authenticated users can create surveys',
                'active': True,
                'start_date_time': None,
                'end_date_time': None
            }
        )

    def test_create_survey_not_logged_in(self):
        """unauthenticated users can't create surveys"""
        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'test_create_survey_not_logged_in',
                'description': "unauthenticated  users can't create surveys",
                'active': True
            },
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_list_survey(self):
        """
        Authenticated users can list their own + other people's active surveys.
        Unauthenticated users can only list other people's active surveys.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 2 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_active',
                'description': "user1's survey (active)",
                'active': True
            },
            format='json'
        )
        u1_active_id = response.data['id']

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_inactive',
                'description': "user1's survey (not active)",
                'active': False
            },
            format='json'
        )
        u1_inactive_id = response.data['id']

        # user1 should see both surveys
        response = self.client.get('/api/surveys/')
        u1_get_survey_ids = set(survey['id'] for survey in response.data)

        self.assertEqual(u1_get_survey_ids, {u1_active_id, u1_inactive_id})

        # user2 should only see the active one
        self.client.force_authenticate(user2)

        response = self.client.get('/api/surveys/')
        u1_get_survey_ids = set(survey['id'] for survey in response.data)

        self.assertEqual(u1_get_survey_ids, {u1_active_id})

        # unauthenticated user should only see the active one
        self.client.force_authenticate()

        response = self.client.get('/api/surveys/')
        u1_get_survey_ids = set(survey['id'] for survey in response.data)

        self.assertEqual(u1_get_survey_ids, {u1_active_id})

    def test_fetch_survey(self):
        """
        Authenticated users can see their own + other people's active surveys.
        Unauthenticated users can only see other people's active surveys.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 2 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_active',
                'description': "user1's survey (active)",
                'active': True
            },
            format='json'
        )
        u1_active_id = response.data['id']
        active_survey_data = response.data

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_inactive',
                'description': "user1's survey (not active)",
                'active': False
            },
            format='json'
        )
        u1_inactive_id = response.data['id']
        inactive_survey_data = response.data

        # user1 should be able to fetch both surveys
        response = self.client.get(f'/api/surveys/{u1_active_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, active_survey_data)

        response = self.client.get(f'/api/surveys/{u1_inactive_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, inactive_survey_data)

        # user2 should only be able to fetch the active one
        self.client.force_authenticate(user2)

        response = self.client.get(f'/api/surveys/{u1_active_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, active_survey_data)

        response = self.client.get(f'/api/surveys/{u1_inactive_id}/')
        self.assertEqual(response.status_code, 403)

        # unauthenticated user should only see the active one
        self.client.force_authenticate()

        response = self.client.get(f'/api/surveys/{u1_active_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, active_survey_data)

        response = self.client.get(f'/api/surveys/{u1_inactive_id}/')
        self.assertEqual(response.status_code, 403)

    def test_update_survey(self):
        """
        Authenticated users can update their own surveys.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 2 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_active',
                'description': "user1's survey (active)",
                'active': True
            },
            format='json'
        )
        u1_active_id = response.data['id']

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_inactive',
                'description': "user1's survey (not active)",
                'active': False
            },
            format='json'
        )
        u1_inactive_id = response.data['id']

        # user1 should be able to update both surveys
        response = self.client.patch(
            f'/api/surveys/{u1_active_id}/',
            {'description': "user1's survey (active) updated"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['description'],
            "user1's survey (active) updated"
        )

        response = self.client.patch(
            f'/api/surveys/{u1_inactive_id}/',
            {'description': "user1's survey (inactive) updated"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['description'],
            "user1's survey (inactive) updated"
        )

        # user2 shouldn't be able to update user1's surveys
        self.client.force_authenticate(user2)

        response = self.client.patch(
            f'/api/surveys/{u1_active_id}/',
            {'description': "should not work"},
            format='json'
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(
            f'/api/surveys/{u1_inactive_id}/',
            {'description': "should not work"},
            format='json'
        )
        self.assertEqual(response.status_code, 403)

        # unauthenticated user shouldn't be able to update user1's surveys
        self.client.force_authenticate()

        response = self.client.patch(
            f'/api/surveys/{u1_active_id}/',
            {'description': "should not work"},
            format='json'
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(
            f'/api/surveys/{u1_inactive_id}/',
            {'description': "should not work"},
            format='json'
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_survey(self):
        """
        Authenticated users can delete their own surveys.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 2 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_active',
                'description': "user1's survey (active)",
                'active': True
            },
            format='json'
        )
        u1_active_id = response.data['id']

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'u1_inactive',
                'description': "user1's survey (not active)",
                'active': False
            },
            format='json'
        )
        u1_inactive_id = response.data['id']

        # user2 shouldn't be able to delete user1's surveys
        self.client.force_authenticate(user2)

        response = self.client.delete(f'/api/surveys/{u1_active_id}/')
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f'/api/surveys/{u1_inactive_id}/')
        self.assertEqual(response.status_code, 403)

        # unauthenticated user shouldn't be able to delete user1's surveys
        self.client.force_authenticate()

        response = self.client.delete(f'/api/surveys/{u1_active_id}/')
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f'/api/surveys/{u1_inactive_id}/')
        self.assertEqual(response.status_code, 403)

        # user1 should be able to delete both surveys
        self.client.force_authenticate(user1)

        response = self.client.delete(f'/api/surveys/{u1_active_id}/')
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(f'/api/surveys/{u1_inactive_id}/')
        self.assertEqual(response.status_code, 204)


class SurveyQuestionViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('some user')
        self.survey = Survey(
            title='test',
            description='test description',
            active=False,
            owner=self.user
        )
        self.survey.save()

    def tearDown(self):
        # clean up survey and user objects after each test
        # survey questions will also be removed because on_delete=CASCADE
        Survey.objects.all().delete()
        User.objects.all().delete()

    def test_create_question(self):
        """ the owner can add a multiple choice question to the survey """

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
        self.assertTrue(
            SurveyQuestionChoice.objects.filter(pk=choices[0].pop('id'))
            .exists()
        )
        self.assertTrue(
            SurveyQuestionChoice.objects.filter(pk=choices[1].pop('id'))
            .exists()
        )
        # other than the ids, the response should look the same
        self.assertEqual(
            choices,
            [
                {'value': 'A', 'description': 'Star Trek'},
                {'value': 'B', 'description': 'Star Wars'},
            ]
        )
        self.assertEqual(
            question_data,
            {
                'number': 1,
                'title': 'Which is better?',
                'required': True,
                'type': 'MC',
            }
        )

    #     # Sanity check for id and created_at
    #     survey = Survey.objects.get(pk=response_data.pop('id'))
    #     self.assertEqual(survey.title, 'test_create_survey')
    #     created_at = dateparse.parse_datetime(response_data.pop('created_at'))
    #     now = timezone.now()
    #     self.assertLess(abs(now - created_at), timedelta(seconds=1))

    #     # The rest should be the same.
    #     self.assertDictEqual(
    #         response_data,
    #         {
    #             'title': 'test_create_survey',
    #             'description': 'only authenticated users can create surveys',
    #             'active': True,
    #             'start_date_time': None,
    #             'end_date_time': None
    #         }
    #     )

    # def test_create_survey_not_logged_in(self):
    #     """unauthenticated users can't create surveys"""
    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'test_create_survey_not_logged_in',
    #             'description': "unauthenticated  users can't create surveys",
    #             'active': True
    #         }
    #     )
    #     self.assertEqual(response.status_code, 403)

    # def test_list_survey(self):
    #     """
    #     Authenticated users can list their own + other people's active surveys.
    #     Unauthenticated users can only list other people's active surveys.
    #     """
    #     user1 = User.objects.create_user('user1')
    #     user2 = User.objects.create_user('user2')

    #     # user1 creates 2 surveys
    #     self.client.force_authenticate(user1)

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_active',
    #             'description': "user1's survey (active)",
    #             'active': True
    #         }
    #     )
    #     u1_active_id = response.data['id']

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_inactive',
    #             'description': "user1's survey (not active)",
    #             'active': False
    #         }
    #     )
    #     u1_inactive_id = response.data['id']

    #     # user1 should see both surveys
    #     response = self.client.get('/api/surveys/')
    #     u1_get_survey_ids = set(survey['id'] for survey in response.data)

    #     self.assertEqual(u1_get_survey_ids, {u1_active_id, u1_inactive_id})

    #     # user2 should only see the active one
    #     self.client.force_authenticate(user2)

    #     response = self.client.get('/api/surveys/')
    #     u1_get_survey_ids = set(survey['id'] for survey in response.data)

    #     self.assertEqual(u1_get_survey_ids, {u1_active_id})

    #     # unauthenticated user should only see the active one
    #     self.client.force_authenticate()

    #     response = self.client.get('/api/surveys/')
    #     u1_get_survey_ids = set(survey['id'] for survey in response.data)

    #     self.assertEqual(u1_get_survey_ids, {u1_active_id})

    # def test_fetch_survey(self):
    #     """
    #     Authenticated users can see their own + other people's active surveys.
    #     Unauthenticated users can only see other people's active surveys.
    #     """
    #     user1 = User.objects.create_user('user1')
    #     user2 = User.objects.create_user('user2')

    #     # user1 creates 2 surveys
    #     self.client.force_authenticate(user1)

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_active',
    #             'description': "user1's survey (active)",
    #             'active': True
    #         }
    #     )
    #     u1_active_id = response.data['id']
    #     active_survey_data = response.data

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_inactive',
    #             'description': "user1's survey (not active)",
    #             'active': False
    #         }
    #     )
    #     u1_inactive_id = response.data['id']
    #     inactive_survey_data = response.data

    #     # user1 should be able to fetch both surveys
    #     response = self.client.get(f'/api/surveys/{u1_active_id}/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, active_survey_data)

    #     response = self.client.get(f'/api/surveys/{u1_inactive_id}/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, inactive_survey_data)

    #     # user2 should only be able to fetch the active one
    #     self.client.force_authenticate(user2)

    #     response = self.client.get(f'/api/surveys/{u1_active_id}/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, active_survey_data)

    #     response = self.client.get(f'/api/surveys/{u1_inactive_id}/')
    #     self.assertEqual(response.status_code, 403)

    #     # unauthenticated user should only see the active one
    #     self.client.force_authenticate()

    #     response = self.client.get(f'/api/surveys/{u1_active_id}/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, active_survey_data)

    #     response = self.client.get(f'/api/surveys/{u1_inactive_id}/')
    #     self.assertEqual(response.status_code, 403)

    # def test_update_survey(self):
    #     """
    #     Authenticated users can update their own surveys.
    #     """
    #     user1 = User.objects.create_user('user1')
    #     user2 = User.objects.create_user('user2')

    #     # user1 creates 2 surveys
    #     self.client.force_authenticate(user1)

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_active',
    #             'description': "user1's survey (active)",
    #             'active': True
    #         }
    #     )
    #     u1_active_id = response.data['id']

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_inactive',
    #             'description': "user1's survey (not active)",
    #             'active': False
    #         }
    #     )
    #     u1_inactive_id = response.data['id']

    #     # user1 should be able to update both surveys
    #     response = self.client.patch(
    #         f'/api/surveys/{u1_active_id}/',
    #         {'description': "user1's survey (active) updated"}
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.data['description'],
    #         "user1's survey (active) updated"
    #     )

    #     response = self.client.patch(
    #         f'/api/surveys/{u1_inactive_id}/',
    #         {'description': "user1's survey (inactive) updated"}
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.data['description'],
    #         "user1's survey (inactive) updated"
    #     )

    #     # user2 shouldn't be able to update user1's surveys
    #     self.client.force_authenticate(user2)

    #     response = self.client.patch(
    #         f'/api/surveys/{u1_active_id}/',
    #         {'description': "should not work"}
    #     )
    #     self.assertEqual(response.status_code, 403)

    #     response = self.client.patch(
    #         f'/api/surveys/{u1_inactive_id}/',
    #         {'description': "should not work"}
    #     )
    #     self.assertEqual(response.status_code, 403)

    #     # unauthenticated user shouldn't be able to update user1's surveys
    #     self.client.force_authenticate()

    #     response = self.client.patch(
    #         f'/api/surveys/{u1_active_id}/',
    #         {'description': "should not work"}
    #     )
    #     self.assertEqual(response.status_code, 403)

    #     response = self.client.patch(
    #         f'/api/surveys/{u1_inactive_id}/',
    #         {'description': "should not work"}
    #     )
    #     self.assertEqual(response.status_code, 403)

    # def test_delete_survey(self):
    #     """
    #     Authenticated users can delete their own surveys.
    #     """
    #     user1 = User.objects.create_user('user1')
    #     user2 = User.objects.create_user('user2')

    #     # user1 creates 2 surveys
    #     self.client.force_authenticate(user1)

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_active',
    #             'description': "user1's survey (active)",
    #             'active': True
    #         }
    #     )
    #     u1_active_id = response.data['id']

    #     response = self.client.post(
    #         '/api/surveys/',
    #         {
    #             'title': 'u1_inactive',
    #             'description': "user1's survey (not active)",
    #             'active': False
    #         }
    #     )
    #     u1_inactive_id = response.data['id']

    #     # user2 shouldn't be able to delete user1's surveys
    #     self.client.force_authenticate(user2)

    #     response = self.client.delete(f'/api/surveys/{u1_active_id}/')
    #     self.assertEqual(response.status_code, 403)

    #     response = self.client.delete(f'/api/surveys/{u1_inactive_id}/')
    #     self.assertEqual(response.status_code, 403)

    #     # unauthenticated user shouldn't be able to delete user1's surveys
    #     self.client.force_authenticate()

    #     response = self.client.delete(f'/api/surveys/{u1_active_id}/')
    #     self.assertEqual(response.status_code, 403)

    #     response = self.client.delete(f'/api/surveys/{u1_inactive_id}/')
    #     self.assertEqual(response.status_code, 403)

    #     # user1 should be able to delete both surveys
    #     self.client.force_authenticate(user1)

    #     response = self.client.delete(f'/api/surveys/{u1_active_id}/')
    #     self.assertEqual(response.status_code, 204)

    #     response = self.client.delete(f'/api/surveys/{u1_inactive_id}/')
    #     self.assertEqual(response.status_code, 204)
