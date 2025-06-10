from ninja.pagination import LimitOffsetPagination, PaginationBase
from ninja import Schema
from typing import List, Any

class SafePagination(LimitOffsetPagination):
    """
    Custom pagination class that extends LimitOffsetPagination
    to ensure safe pagination behavior with a maximum limit.
    """
    max_limit = 1000

    class Input(Schema):
        limit: int = None
        offset: int = 0

    class Output(Schema):
        items: List[Any]
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        limit = pagination.limit if pagination.limit is not None else self.max_limit
        offset = pagination.offset

        # Ensure limit does not exceed max_limit
        if limit is not None and limit > self.max_limit:
            limit = self.max_limit

        # Calculate the slice of the queryset
        total = queryset.count()
        items = queryset[offset:offset + limit]

        return {
            'items': items,
            'total': total,
            'per_page': limit,
        }