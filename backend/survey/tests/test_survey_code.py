from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from survey.models import SurveySession, Survey

class CodeToSessionSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('some user')
        self.survey = Survey(
            title='test survey',
            description='test description'
        )
        self.survey.save()
        self.session = SurveySession(survey=self.survey, code=1234, owner=self.user)
        self.session.save()

    def tearDown(self):
        # clean up Session and user objects after each test
        SurveySession.objects.all().delete()
        Survey.objects.all().delete()
        User.objects.all().delete()

    def test_lookup_code(self):
        """authenticated users can search for code"""
        self.client.force_authenticate(self.user)
        response = self.client.get(
            f'/api/codes/{self.session.code}/'
        )
        self.assertEqual(response.status_code, 200)
        survey_id = response.data.pop('survey')
        self.assertEqual(survey_id, self.survey.id)

    def test_lookup_code_not_logged_in(self):
        """unauthenticated users can search for code"""
        response = self.client.get(
            f'/api/codes/{self.session.code}/'
        )
        self.assertEqual(response.status_code, 200)
        survey_id = response.data.pop('survey')
        self.assertEqual(survey_id, self.survey.id)
    
    def test_lookup_invalid_code(self):
        response = self.client.get(
            f'/api/codes/{1789}/'
        )
        self.assertEqual(response.status_code, 404)
        detail = response.data.pop('detail')
        self.assertEqual(detail, "Not found.")

