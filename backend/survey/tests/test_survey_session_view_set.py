from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from survey.models import Survey, SurveyQuestion, SurveyQuestionChoice, SurveySession


class SessionViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('some user')
        self.survey = Survey(
            title='test survey',
            description='test description'
        )
        self.survey.save()

    def tearDown(self):
        # clean up Session and user objects after each test
        SurveySession.objects.all().delete()
        Survey.objects.all().delete()
        User.objects.all().delete()

    def test_create_session(self):
        """only authenticated users can create sessions"""

        # log the user in
        self.client.force_authenticate(self.user)
        response = self.client.post(
            f'/api/sessions/',
            {
                "survey": str(self.survey.id)
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        session_data = response.data
        session_id = session_data.pop('id')
        session_code = session_data.pop('code')
        session_survey = session_data.pop('survey')

        self.assertTrue(SurveySession.objects.filter(
            pk=session_id, code=session_code).exists())
        self.assertEqual(session_survey, self.survey.id)

    def test_create_sessions_not_logged_in(self):
        """unauthenticated users can't create sessions"""
        response = self.client.post(
            '/api/sessions/',
            {
                'survey': str(self.survey.id),
            },
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_session(self):

        self.client.force_authenticate(self.user)

        # the survey doesn't have any question yet
        response = self.client.get(
            f'/api/sessions/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

        # create 2 sessions
        instance = Survey(title='test survey 2')
        instance.save()

        session_data = [
            {
                'code': 1234,
                'survey': str(self.survey.id)
            },
            {
                'code': 1235,
                'survey': str(instance.id)
            }
        ]

        session1 = SurveySession(
            survey=self.survey, code=1234, owner=self.user)
        session1.save()
        session2 = SurveySession(survey=instance, code=1235, owner=self.user)
        session2.save()
        session_data[0]['id'] = session1.id
        session_data[1]['id'] = session2.id

        # now listing the sessions should show the 2 new sessions
        response = self.client.get(
            f'/api/sessions/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(session_data, response.data['results'])

    def test_fetch_session(self):

        self.client.force_authenticate(self.user)

        session_data = {
            'code': 1234,
            'survey': str(self.survey.id)
        }

        # create a session
        instance = SurveySession(
            survey=self.survey, code=1234, owner=self.user)
        instance.save()
        session_data['id'] = instance.id
        # now fetch the session should return the new session
        response = self.client.get(
            f'/api/sessions/{instance.id }/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(session_data, response.data)
    
    def test_fetch_invalid_session(self):

        self.client.force_authenticate(self.user)

        # create a session
        instance = SurveySession(
            survey=self.survey, code=1234, owner=self.user)
        instance.save()
        # now fetch the session should return the new session
        response = self.client.get(
            f'/api/sessions/asdasd/'
        )
        self.assertEqual(response.status_code, 404)
        detail = response.data.pop('detail')
        self.assertEqual(detail, "Not found.")

    def test_delete_sessions(self):

        self.client.force_authenticate(self.user)

        # create a session

        instance = SurveySession(
            survey=self.survey, code=1234, owner=self.user)
        instance.save()

        self.assertTrue(SurveySession.objects.filter(pk=instance.id).exists())

        # now delete the session
        response = self.client.delete(
            f'/api/sessions/{instance.id}/'
        )

        self.assertEqual(response.status_code, 204)

        # make sure it's deleted
        self.assertFalse(
            SurveySession.objects.filter(pk=instance.id).exists()
        )