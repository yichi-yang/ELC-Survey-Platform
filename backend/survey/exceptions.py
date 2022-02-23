from rest_framework.exceptions import APIException

class BadQueryParameter(APIException):
    status_code = 400
    default_detail = 'Query parameter is invalid.'
    default_code = 'bad_query_parameter'