from rest_framework.pagination import PageNumberPagination

class ResultPagination(PageNumberPagination):
    """
    Custom pagination class for API responses.

    Attributes:
    - page_size (int): Defines the default number of items per page (default: 6).
    - page_size_query_param (str): Allows the client to specify a custom page size via query parameters.
    - max_page_size (int): Limits the maximum page size to prevent excessive data requests (default: 10).

    Usage:
    - This pagination class can be used in Django REST Framework views to control response pagination.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10