from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import SurveySubmission, SurveySession


class SurveySubmissionViewSetTests(TestCase):

    fixtures = ['test_submission_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(pk=1)
        self.survey_responses = [
            # multiple choice
            {"question": "yO5lED9", "choice": "m2OkayZ"},
            # checkboxes
            {"question": "R7jNpDG", "choice": "GDOaMOj"},
            {"question": "R7jNpDG", "choice": "LjyRko9"},
            # dropdown
            {"question": "dBjywDL", "choice": "wKoPloR"},
            # scale
            {"question": "Lo5MY5R", "numeric_value": 8.0},
            # short answer
            {"question": "GajwyDE", "text": "apple"},
            # paragraph
            {"question": "O2VeYVd", "text": "Describe the city you live in."},
            # ranking
            {"question": "vQVx1jW", "choice": "eMNVmOD", "numeric_value": 1.0},
            {"question": "vQVx1jW", "choice": "wGo71N5", "numeric_value": 2.0},
            {"question": "vQVx1jW", "choice": "DMNxbo0", "numeric_value": 3.0},
            # not required question
            {"question": "GrjLWV2", "text": "optional"},
        ]

    def test_submit(self):
        """ Wellformed list of response should work. """

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertListEqual(response.data['responses'], self.survey_responses)

    def test_submit_optional(self):
        """ Questions marked required=False can have no response """

        # it's ok if an optional question doesn't have a response
        self.survey_responses.pop()

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertListEqual(response.data['responses'], self.survey_responses)

    def test_submit_missing_question(self):
        """ All questions marked as require must be answered """

        # removes response for question yO5lED9
        self.survey_responses.pop(0)

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("is required", str(response.data))

    def test_submit_duplicate_question(self):
        """ Some question types only allow one response. """

        # two resposes for question yO5lED9
        self.survey_responses.append({
            "question": "yO5lED9",
            "choice": "WKo1dyZ"
        })

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Too many responses for", str(response.data))

    def test_submit_checkboxes_duplicate_choices(self):
        """ Even for ones that allow multiple response choices must be unique. """

        # duplicate choice GDOaMOj
        self.survey_responses.append({
            "question": "R7jNpDG",
            "choice": "GDOaMOj"}
        )

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Selected choices must be unique", str(response.data))

    def test_submit_response_missing_required_field(self):
        """ All required fields must be present. """

        self.survey_responses[0].pop('choice')

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("'choice' is required", str(response.data))

    def test_submit_response_invalid_field(self):
        """ All fields must be valid for the current question type. """

        self.survey_responses[0]['numeric_value'] = 5.0

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("'numeric_value' is invalid", str(response.data))

    def test_submit_response_value_out_of_range(self):
        """ numeric_value must be in the range specified by the question. """

        self.survey_responses[4]['numeric_value'] = 1000.0

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Value must be between", str(response.data))

    def test_submit_ranking_not_enough_responses(self):
        """ For ranking questions their must be a response for each choice. """

        # remove one of ranking responses
        self.survey_responses.pop(7)

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not enough responses", str(response.data))

    def test_create_permissions(self):
        """ Authenticated users should also be able to create submissions. """

        self.client.force_authenticate(self.user)

        response = self.client.post(
            '/api/sessions/Dy07DNq/submissions/',
            {"responses": self.survey_responses},
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_retrieve_permissions(self):
        """ Only authenticated users can fetch submissions. """

        session = SurveySession.objects.get(id='Dy07DNq')
        submission = SurveySubmission.objects.create(session=session)
        submission.save()

        response = self.client.get(
            f'/api/sessions/Dy07DNq/submissions/{submission.id}/'
        )
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(self.user)

        response = self.client.get(
            f'/api/sessions/Dy07DNq/submissions/{submission.id}/'
        )
        self.assertEqual(response.status_code, 200)

    def test_destroy_permissions(self):
        """ Only authenticated users can delete submissions. """

        session = SurveySession.objects.get(id='Dy07DNq')
        submission = SurveySubmission.objects.create(session=session)
        submission.save()

        response = self.client.delete(
            f'/api/sessions/Dy07DNq/submissions/{submission.id}/'
        )
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(self.user)

        response = self.client.delete(
            f'/api/sessions/Dy07DNq/submissions/{submission.id}/'
        )
        self.assertEqual(response.status_code, 204)

    def test_list_permissions(self):
        """ Only authenticated users can list submissions. """

        response = self.client.get('/api/sessions/Dy07DNq/submissions/')
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(self.user)

        response = self.client.get('/api/sessions/Dy07DNq/submissions/')
        self.assertEqual(response.status_code, 200)
