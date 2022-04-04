from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from survey.models import Survey, SurveyQuestion, SurveyQuestionChoice


class DuplicateSurveyViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('some user')
        self.survey = Survey(
            title='test survey',
            description='test description'
        )
        self.survey.save()
        self.question = SurveyQuestion(
            survey=self.survey,
            number=100,
            title='1 + 1 = ?',
            type='MC',
            required=True
        )
        self.question.save()
        self.choice = SurveyQuestionChoice(
            question=self.question,
            value='A',
            description='1'
        )
        self.choice.save()

    def tearDown(self):
        # clean up Survey and user objects after each test
        Survey.objects.all().delete()
        User.objects.all().delete()

    def test_duplicate_survey_not_logged_in(self):
        """unauthenticated users can't create sessions"""
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/duplicate/',
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_duplicate_survey(self):
        self.client.force_authenticate(self.user)

        # duplicate a survey
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/duplicate/',
            format='json'
        )
        response_data = response.data

        self.assertEqual(response.status_code, 201)

        survey_id = response_data.pop('id')

        # check that a new survey is made
        self.assertNotEqual(survey_id, self.survey.id)
        self.assertTrue(Survey.objects.filter(pk=survey_id).exists())
        # check that the old survey wasn't overriden
        self.assertTrue(Survey.objects.filter(pk=self.survey.id).exists())

        response_data.pop('created_at')
        # newly created survey should have same fields as original survey
        self.assertDictEqual(
            response_data,
            {
                'title': 'test survey',
                'description': 'test description',
                'draft': True,
                'group_by_question': None
            }
        )
        # check if a new question has been made
        new_question = SurveyQuestion.objects.filter(survey=survey_id)
        self.assertTrue(new_question.exists())
        new_question_id = list(new_question)[0].id
        self.assertNotEqual(new_question_id, self.question.id)
        # check that the old question wasn't overriden
        self.assertTrue(SurveyQuestion.objects.filter(
            survey=self.survey.id).exists())

        # get the original and duplicated question
        question1 = list(SurveyQuestion.objects.filter(
            survey=self.survey.id).values())[0]
        question2 = list(SurveyQuestion.objects.filter(
            survey=survey_id).values())[0]
        question1.pop('id')
        question1.pop('survey_id')
        question2.pop('id')
        question2.pop('survey_id')
        # check if all fields are equal except for id and survey_id
        self.assertDictEqual(question1, question2)

        # check if a new question choice has been made
        new_choice = SurveyQuestionChoice.objects.filter(
            question=new_question_id)
        self.assertTrue(new_choice.exists())
        new_choice_id = list(new_choice)[0].id
        self.assertNotEqual(new_choice_id, self.choice.id)
        # check that the old question wasn't overriden
        self.assertTrue(SurveyQuestion.objects.filter(
            survey=self.choice.id).exists())

        # get the original and duplicated choice
        choice1 = list(SurveyQuestionChoice.objects.filter(
            question=self.choice.id).values())[0]
        choice2 = list(SurveyQuestionChoice.objects.filter(
            question=new_choice_id).values())[0]
        choice1.pop('id')
        choice1.pop('question_id')
        choice2.pop('id')
        choice2.pop('question_id')
        # check if all fields are equal except for id and question_id
        self.assertDictEqual(choice1, choice2)
        
    def test_duplicate_invalid_survey(self):
        self.client.force_authenticate(self.user)

        # duplicate a survey
        response = self.client.post(
            f'/api/surveys/asdasd/duplicate/',
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        detail = response.data.pop('detail')
        self.assertEqual(detail, "Not found.")

    def test_group_by_question(self):
        self.client.force_authenticate(self.user)

        group_question = SurveyQuestion(
            number=1,
            title='Which Group are you in?',
            type='MC',
            required=False,
            survey=self.survey
        )
        group_question.save()

        # add group_by_question to survey
        self.survey.group_by_question = group_question
        self.survey.save()

        response = self.client.post(
            f'/api/surveys/{self.survey.id}/duplicate/',
            format='json'
        )

        response_data = response.data

        self.assertEqual(response.status_code, 201)

        new_group_by_question = response_data.pop('group_by_question')
        # check that the group by question on the new survey !=
        # the group by question on the old survey
        self.assertNotEqual(new_group_by_question, group_question)

        new_group_by_question = SurveyQuestion.objects.filter(id=new_group_by_question)

        # check that the new group by question asks for the group
        self.assertEqual(list(new_group_by_question)[0].title, 'Which Group are you in?')