from ninja.pagination import LimitOffsetPagination

class SafePagination(LimitOffsetPagination):
    """
    Custom pagination class that extends LimitOffsetPagination
    to ensure safe pagination behavior.
    """
    def paginate_queryset(self, queryset, request, view=None, **kwargs):
        # Ensure that the limit is not too high
        if self.limit is not None and self.limit > 1000:
            self.limit = 1000
        return super().paginate_queryset(queryset, request, view)