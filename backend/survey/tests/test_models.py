from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from survey.models import Survey


class SurveyViewSetTests(TestCase):

    def test_survey_inactive(self):
        survey = Survey(active=False)
        self.assertFalse(survey.is_active)

    def test_survey_active(self):
        # if no start / end time set, .is_active == be .active
        survey = Survey(active=True)
        self.assertTrue(survey.is_active)

    def test_survey_active_before_start(self):
        survey = Survey(
            active=True,
            # survey starts one day in the future
            start_date_time=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(survey.is_active)

    def test_survey_active_after_end(self):
        survey = Survey(
            active=True,
            # survey has ended 1 day ago
            end_date_time=timezone.now() - timedelta(days=1)
        )
        self.assertFalse(survey.is_active)

    def test_survey_active_after_end(self):
        survey = Survey(
            active=True,
            # survey has ended 1 day ago
            end_date_time=timezone.now() - timedelta(days=1)
        )
        self.assertFalse(survey.is_active)

    def test_survey_active_ongoing(self):
        survey = Survey(
            active=True,
            start_date_time=timezone.now() - timedelta(days=1),
            end_date_time=timezone.now() + timedelta(days=1)
        )
        self.assertTrue(survey.is_active)

    def test_survey_inactive_ongoing(self):
        survey = Survey(
            active=False,
            start_date_time=timezone.now() - timedelta(days=1),
            end_date_time=timezone.now() + timedelta(days=1)
        )
        # even if the survey is ongoing, setting .active = False forces .is_active to False
        self.assertFalse(survey.is_active)
