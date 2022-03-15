from .serializers import NestedSurveyQuestionSerializer, SurveySerializer
from statistics import mean, median


class SubmissionSummarizer:

    def __init__(self, session, submission_queryset) -> None:
        survey = session.survey

        summary = dict()

        # general stats
        summary['submission_count'] = submission_queryset.count()

        # include a copy of the survey object
        summary['survey'] = SurveySerializer(survey).data

        # process group question related stuff
        group_by_question = survey.group_by_question
        if group_by_question is not None:
            responses = group_by_question.responses\
                .filter(submission__session=session)\
                .select_related('choice')
            submissions_by_group = {
                c.id: list()
                for c in group_by_question.choices.all()
            }
            for response in responses:
                submissions_by_group[response.choice.id]\
                    .append(response.submission.id)

            # include a copy of group by question in the result
            serializer = NestedSurveyQuestionSerializer(group_by_question)
            summary['group_by_question'] = serializer.data
        else:
            summary['group_by_question'] = None

        # per-question summary
        summary['question_summary'] = list()

        for question in survey.questions.all().prefetch_related('choices'):

            # no need to summarize group_by_question
            if question == group_by_question:
                continue

            responses = question.responses\
                .filter(submission__session=session)\
                .select_related('choice')

            try:
                summarizer = getattr(self, f'summarize_{question.type}')
            except AttributeError:
                raise NotImplementedError(
                    f"Can't summarize question type {question.type}"
                )

            question_summary = dict()

            # include a copy of the question
            question_serializer = NestedSurveyQuestionSerializer(question)
            question_summary['question'] = question_serializer.data

            # summary for all responses
            question_summary['all'] = summarizer(question, responses)

            # per-group summary
            if group_by_question is not None:
                question_summary['by_group'] = dict()
                for g_id, s_ids in submissions_by_group.items():
                    group_responses = responses.filter(submission__in=s_ids)
                    group_summary = summarizer(question, group_responses)
                    question_summary['by_group'][str(g_id)] = group_summary

            summary['question_summary'].append(question_summary)

        self.data = summary

    # Handlers for various questions types

    def summarize_MC(self, question, responses):
        summary = self._summarize_choices(question, responses)
        values = self._choices_to_floats(question, responses)
        if values is not None:
            summary = {**summary, **self._summarize_numeric_values(values)}
        return summary

    def summarize_CB(self, question, responses):
        return self._summarize_choices(question, responses)

    def summarize_DP(self, question, responses):
        return self._summarize_choices(question, responses)

    def summarize_SC(self, question, responses):
        return self._summarize_numeric_values(
            [r.numeric_value for r in responses]
        )

    def summarize_SA(self, question, responses):
        return self._summarize_text(question, responses)

    def summarize_PA(self, question, responses):
        return self._summarize_text(question, responses)

    def summarize_RK(self, question, responses):
        ranking = {
            str(c.id): self._summarize_numeric_values([
                r.numeric_value for r in responses if r.choice == c
            ])
            for c in question.choices.all()
        }
        return {'ranking': ranking}

    # Helpers

    def _summarize_choices(self, question, responses):
        count = {str(c.id): 0 for c in question.choices.all()}
        for response in responses:
            count[str(response.choice.id)] += 1
        return {"count": count}

    def _summarize_text(self, question, responses):
        return {'answers': [r.text for r in responses]}

    def _summarize_numeric_values(self, values):
        # JSON can't serialize NaNs, so we'll just use a None (null)
        NaN = None
        return {
            'min': min(values, default=NaN),
            'max': max(values, default=NaN),
            'mean': mean(values) if len(values) else NaN,
            'median': median(values) if len(values) else NaN
        }

    def _choices_to_floats(self, question, responses):
        """
        Returns a list of floats if all choices can be 
        interpreted as floats. Returns None otherwise.
        """
        try:
            map = {c.id: float(c.description) for c in question.choices.all()}
        except ValueError:
            return None
        return [map[r.choice.id] for r in responses]
