# Troy swagger template
from drf_yasg import openapi


class DuplicateCheckParamCollection(object):
    nickname = openapi.Parameter(
        'nickname',
        openapi.IN_QUERY,
        description='중복 검사를 수행할 \'nickname\'값을 parameter로 전달해주세요.',
        type=openapi.TYPE_STRING
    )


class CoachListQueryParamCollection(object):
    option = openapi.Parameter(
        'option',
        openapi.IN_QUERY,
        description='검색을 수행할 때 \'search\'값을 parameter로 전달해주세요.',
        type=openapi.TYPE_STRING
    )
    q = openapi.Parameter(
        'q',
        openapi.IN_QUERY,
        description='검색 키워드를 parameter로 전달해주세요.',
        type=openapi.TYPE_STRING
    )
    sorting = openapi.Parameter(
        'sorting',
        openapi.IN_QUERY,
        description='정렬 수행 여부를 boolean 값으로 전달해주세요.',
        type=openapi.TYPE_BOOLEAN
    )
    order_by = openapi.Parameter(
        'order_by',
        openapi.IN_QUERY,
        description='정렬을 수행할 때 \'ascending(오름차순),\', \'descending(내림차순)\'값을 parameter로 전달해주세요.',
        type=openapi.TYPE_STRING
    )
