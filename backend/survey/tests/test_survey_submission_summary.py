from http import client
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import SurveySubmission, SurveySession


class SurveySubmissionSummaryTests(TestCase):

    fixtures = ['test_summary_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(pk=1)

    def test_summary(self):
        """ Make sure generated summary is correct. """

        self.client.force_authenticate(self.user)

        response = self.client.get(
            '/api/sessions/4wNwX6O/submissions/summarize/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                "submission_count": 3,
                "survey": {
                    "id": "Wl95e9L",
                    "title": "Test Survey Summary",
                    "description": "test 123",
                    "draft": False,
                    "group_by_question": "vQVx1jW",
                    "created_at": "2022-04-10T21:41:04.150000Z"
                },
                "group_by_question": {
                    "id": "vQVx1jW",
                    "number": 6,
                    "title": "Which Group are you in?",
                    "required": True,
                    "type": "DP",
                    "choices": [
                        {
                            "id": "anyGzNM",
                            "value": "1",
                            "description": "Group 1"
                        },
                        {
                            "id": "k2Odnya",
                            "value": "2",
                            "description": "Group 2"
                        }
                    ]
                },
                "question_summary": [
                    {
                        "question": {
                            "id": "yO5lED9",
                            "number": 1,
                            "title": "Question 1",
                            "required": False,
                            "type": "MC",
                            "choices": [
                                {
                                    "id": "m2OkayZ",
                                    "value": "1",
                                    "description": "A"
                                },
                                {
                                    "id": "WKo1dyZ",
                                    "value": "2",
                                    "description": "B"
                                },
                                {
                                    "id": "GDOaMOj",
                                    "value": "3",
                                    "description": "C"
                                },
                                {
                                    "id": "LjyRko9",
                                    "value": "4",
                                    "description": "D"
                                }
                            ]
                        },
                        "all": {
                            "count": {
                                "m2OkayZ": 2,
                                "WKo1dyZ": 0,
                                "GDOaMOj": 1,
                                "LjyRko9": 0
                            }
                        },
                        "by_group": {
                            "anyGzNM": {
                                "count": {
                                    "m2OkayZ": 1,
                                    "WKo1dyZ": 0,
                                    "GDOaMOj": 1,
                                    "LjyRko9": 0
                                }
                            },
                            "k2Odnya": {
                                "count": {
                                    "m2OkayZ": 1,
                                    "WKo1dyZ": 0,
                                    "GDOaMOj": 0,
                                    "LjyRko9": 0
                                }
                            }
                        }
                    },
                    {
                        "question": {
                            "id": "R7jNpDG",
                            "number": 2,
                            "title": "Question 2",
                            "required": False,
                            "type": "MC",
                            "choices": [
                                {
                                    "id": "D9NXgO6",
                                    "value": "1",
                                    "description": "1"
                                },
                                {
                                    "id": "M9O2bOA",
                                    "value": "2",
                                    "description": "2"
                                },
                                {
                                    "id": "wKoPloR",
                                    "value": "3",
                                    "description": "3"
                                },
                                {
                                    "id": "MgyreN6",
                                    "value": "4",
                                    "description": "4.0"
                                }
                            ]
                        },
                        "all": {
                            "count": {
                                "D9NXgO6": 1,
                                "M9O2bOA": 2,
                                "wKoPloR": 0,
                                "MgyreN6": 0
                            },
                            "min": 1.0,
                            "max": 2.0,
                            "mean": 1.6666666666666667,
                            "median": 2.0
                        },
                        "by_group": {
                            "anyGzNM": {
                                "count": {
                                    "D9NXgO6": 1,
                                    "M9O2bOA": 1,
                                    "wKoPloR": 0,
                                    "MgyreN6": 0
                                },
                                "min": 1.0,
                                "max": 2.0,
                                "mean": 1.5,
                                "median": 1.5
                            },
                            "k2Odnya": {
                                "count": {
                                    "D9NXgO6": 0,
                                    "M9O2bOA": 1,
                                    "wKoPloR": 0,
                                    "MgyreN6": 0
                                },
                                "min": 2.0,
                                "max": 2.0,
                                "mean": 2.0,
                                "median": 2.0
                            }
                        }
                    },
                    {
                        "question": {
                            "id": "Lo5MY5R",
                            "number": 3,
                            "title": "Question 3",
                            "required": False,
                            "type": "CB",
                            "choices": [
                                {
                                    "id": "B4OBvO2",
                                    "value": "1",
                                    "description": "Apple"
                                },
                                {
                                    "id": "eMNVmOD",
                                    "value": "2",
                                    "description": "Banana"
                                }
                            ]
                        },
                        "all": {
                            "count": {
                                "B4OBvO2": 2,
                                "eMNVmOD": 1
                            }
                        },
                        "by_group": {
                            "anyGzNM": {
                                "count": {
                                    "B4OBvO2": 2,
                                    "eMNVmOD": 1
                                }
                            },
                            "k2Odnya": {
                                "count": {
                                    "B4OBvO2": 0,
                                    "eMNVmOD": 0
                                }
                            }
                        }
                    },
                    {
                        "question": {
                            "id": "GajwyDE",
                            "number": 4,
                            "title": "Question 4",
                            "required": False,
                            "type": "SA"
                        },
                        "all": {
                            "answers": [
                                "answer 1",
                                "answer 2",
                                "answer 3"
                            ]
                        },
                        "by_group": {
                            "anyGzNM": {
                                "answers": [
                                    "answer 1",
                                    "answer 3"
                                ]
                            },
                            "k2Odnya": {
                                "answers": [
                                    "answer 2"
                                ]
                            }
                        }
                    },
                    {
                        "question": {
                            "id": "O2VeYVd",
                            "number": 5,
                            "title": "Question 5",
                            "required": False,
                            "type": "RK",
                            "range_min": 1.0,
                            "range_max": 5.0,
                            "range_default": 1.0,
                            "range_step": 1.0,
                            "choices": [
                                {
                                    "id": "wGo71N5",
                                    "value": "1",
                                    "description": "CEO"
                                },
                                {
                                    "id": "DMNxbo0",
                                    "value": "2",
                                    "description": "COO"
                                },
                                {
                                    "id": "54Only0",
                                    "value": "3",
                                    "description": "CFO"
                                }
                            ]
                        },
                        "all": {
                            "ranking": {
                                "wGo71N5": {
                                    "min": 1.0,
                                    "max": 5.0,
                                    "mean": 3.0,
                                    "median": 3.0
                                },
                                "DMNxbo0": {
                                    "min": 2.0,
                                    "max": 4.0,
                                    "mean": 3.0,
                                    "median": 3.0
                                },
                                "54Only0": {
                                    "min": 2.0,
                                    "max": 5.0,
                                    "mean": 3.6666666666666665,
                                    "median": 4.0
                                }
                            }
                        },
                        "by_group": {
                            "anyGzNM": {
                                "ranking": {
                                    "wGo71N5": {
                                        "min": 1.0,
                                        "max": 5.0,
                                        "mean": 3.0,
                                        "median": 3.0
                                    },
                                    "DMNxbo0": {
                                        "min": 3.0,
                                        "max": 4.0,
                                        "mean": 3.5,
                                        "median": 3.5
                                    },
                                    "54Only0": {
                                        "min": 2.0,
                                        "max": 5.0,
                                        "mean": 3.5,
                                        "median": 3.5
                                    }
                                }
                            },
                            "k2Odnya": {
                                "ranking": {
                                    "wGo71N5": {
                                        "min": 3.0,
                                        "max": 3.0,
                                        "mean": 3.0,
                                        "median": 3.0
                                    },
                                    "DMNxbo0": {
                                        "min": 2.0,
                                        "max": 2.0,
                                        "mean": 2.0,
                                        "median": 2.0
                                    },
                                    "54Only0": {
                                        "min": 4.0,
                                        "max": 4.0,
                                        "mean": 4.0,
                                        "median": 4.0
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        )

    def test_summary_permission(self):
        """ Only authenticated users can view summaries. """

        self.client.force_authenticate()

        response = self.client.get(
            '/api/sessions/4wNwX6O/submissions/summarize/'
        )
        self.assertEqual(response.status_code, 401)
