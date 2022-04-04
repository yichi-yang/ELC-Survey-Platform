from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone, dateparse
from rest_framework.test import APIClient
from datetime import timedelta
from survey.models import Survey, SurveyQuestion


class SurveyViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_survey(self):
        """only authenticated users can create surveys"""

        user = User.objects.create_user('some user')
        # log the user in
        self.client.force_authenticate(user)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'test_create_survey',
                'description': 'only authenticated users can create surveys'
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
                'draft': True,
                'group_by_question': None
            }
        )

    def test_create_survey_not_logged_in(self):
        """unauthenticated users can't create surveys"""
        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'test_create_survey_not_logged_in',
                'description': "unauthenticated  users can't create surveys"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def get_survey_id_set(self, data):
        return set(survey['id'] for survey in data['results'])

    def test_list_survey(self):
        """
        Anyone can list surveys.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 2 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'survey 1',
                'description': "user1's survey 1",
            },
            format='json'
        )
        survey1_id = response.data['id']

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'survey 2',
                'description': "user1's survey 2",
            },
            format='json'
        )
        survey2_id = response.data['id']

        # user1 should see both surveys
        response = self.client.get('/api/surveys/')
        u1_get_survey_ids = self.get_survey_id_set(response.data)

        self.assertSetEqual(u1_get_survey_ids, {survey1_id, survey2_id})

        # user2 should see both surveys
        self.client.force_authenticate(user2)

        response = self.client.get('/api/surveys/')
        u2_get_survey_ids = self.get_survey_id_set(response.data)

        self.assertSetEqual(u2_get_survey_ids, {survey1_id, survey2_id})

        # unauthenticated user should only both surveys
        self.client.force_authenticate()

        response = self.client.get('/api/surveys/')
        unauthenticated_get_survey_ids = set(
            survey['id'] for survey in response.data['results'])

        self.assertSetEqual(unauthenticated_get_survey_ids,
                            {survey1_id, survey2_id})

    def test_fetch_survey(self):
        """
        Anyone can view surveys.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 1 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'Some survey',
                'description': "user1's survey",
            },
            format='json'
        )
        survey_id = response.data['id']
        survey_data = response.data

        # user1 should be able to fetch the survey
        response = self.client.get(f'/api/surveys/{survey_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, survey_data)

        # user2 should be able to fetch the survey
        self.client.force_authenticate(user2)

        response = self.client.get(f'/api/surveys/{survey_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, survey_data)

        # unauthenticated user should be able to fetch the survey
        self.client.force_authenticate()

        response = self.client.get(f'/api/surveys/{survey_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, survey_data)

    def test_update_survey(self):
        """
        Authenticated users can update any survey.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 1 survey
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'Some survey',
                'description': "user1's survey",
            },
            format='json'
        )
        survey_id = response.data['id']

        # user1 should be able to update the survey
        response = self.client.patch(
            f'/api/surveys/{survey_id}/',
            {'description': "user1's survey updated"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['description'],
            "user1's survey updated"
        )

        # user2 should also able to update user1's surveys
        self.client.force_authenticate(user2)

        response = self.client.patch(
            f'/api/surveys/{survey_id}/',
            {'description': "updated by user 2"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['description'],
            "updated by user 2"
        )

        # unauthenticated user shouldn't be able to update user1's surveys
        self.client.force_authenticate()

        response = self.client.patch(
            f'/api/surveys/{survey_id}/',
            {'description': "this doesn't work"},
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_survey(self):
        """
        Authenticated users can delete any survey.
        """
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')

        # user1 creates 2 surveys
        self.client.force_authenticate(user1)

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'survey 1',
                'description': "blah blah blah"
            },
            format='json'
        )
        survey1_id = response.data['id']

        response = self.client.post(
            '/api/surveys/',
            {
                'title': 'survey 2',
                'description': "blah blah blah"
            },
            format='json'
        )
        survey2_id = response.data['id']

        # user2 should be able to delete user1's surveys
        self.client.force_authenticate(user2)

        response = self.client.delete(f'/api/surveys/{survey1_id}/')
        self.assertEqual(response.status_code, 204)

        # unauthenticated user shouldn't be able to delete user1's surveys
        self.client.force_authenticate()

        response = self.client.delete(f'/api/surveys/{survey2_id}/')
        self.assertEqual(response.status_code, 401)

        # user1 should be able to delete the survey
        self.client.force_authenticate(user1)

        response = self.client.delete(f'/api/surveys/{survey2_id}/')
        self.assertEqual(response.status_code, 204)

    def test_set_group_question(self):
        """
        You can update group by question after a survey is created.
        """
        user = User.objects.create_user('user')

        survey = Survey(
            title='test survey',
            description='test description'
        )
        survey.save()
        mc_question = SurveyQuestion(
            number=1,
            title='test question',
            type='MC',
            required=False,
            survey=survey
        )
        mc_question.save()

        self.client.force_authenticate(user)

        response = self.client.get(f'/api/surveys/{survey.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['group_by_question'], None)

        response = self.client.patch(
            f'/api/surveys/{survey.id}/',
            {'group_by_question': str(mc_question.id)},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['group_by_question'], str(mc_question.id)
        )

        # group_by_question must be a multiple choice or dropdown question

        sa_question = SurveyQuestion(
            number=1,
            title='test question SA',
            type='SA',
            required=False,
            survey=survey
        )
        sa_question.save()

        response = self.client.patch(
            f'/api/surveys/{survey.id}/',
            {'group_by_question': str(sa_question.id)},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

        # you shouldn't be able to mix and match question / survey
        another_survey = Survey(
            title='test survey',
            description='test description'
        )
        another_survey.save()
        another_question = SurveyQuestion(
            number=1,
            title='test question',
            type='MC',
            required=False,
            survey=another_survey
        )
        another_question.save()

        response = self.client.patch(
            f'/api/surveys/{survey.id}/',
            {'group_by_question': str(another_question.id)},
            format='json'
        )
        self.assertEqual(response.status_code, 400)

        # make sure we can also reset it to null
        response = self.client.patch(
            f'/api/surveys/{survey.id}/',
            {'group_by_question': None},
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_list_survey_filter(self):
        """
        You can filter surveys using draft and keywork query parameter.
        """
        survey1 = Survey(
            title='apple survey',
            description='test description',
            draft=True
        )
        survey1.save()

        survey2 = Survey(
            title='banana survey',
            description='test description',
            draft=False
        )
        survey2.save()

        # no filters
        response = self.client.get(f'/api/surveys/')
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            self.get_survey_id_set(response.data),
            {survey1.id, survey2.id}
        )

        # filter by draft
        response = self.client.get(f'/api/surveys/?draft=true')
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            self.get_survey_id_set(response.data), {survey1.id}
        )

        response = self.client.get(f'/api/surveys/?draft=false')
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            self.get_survey_id_set(response.data), {survey2.id}
        )

        # no filter by keyword
        response = self.client.get(f'/api/surveys/?keyword=apple')
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            self.get_survey_id_set(response.data), {survey1.id}
        )

        response = self.client.get(f'/api/surveys/?keyword=banana')
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            self.get_survey_id_set(response.data), {survey2.id}
        )

        # you can also combine both query parameters
        response = self.client.get(f'/api/surveys/?draft=true&keyword=banana')
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            self.get_survey_id_set(response.data), set()
        )