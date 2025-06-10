from ninja.pagination import LimitOffsetPagination
from ninja.errors import HttpError

class SafePagination(LimitOffsetPagination):
    max_limit = 1000 
    max_offset = 10000 
    def paginate_queryset(self, queryset, request, view=None, **kwargs):
        limit = self.get_limit(request)
        offset = self.get_offset(request)

        if limit is not None:
            if limit <= 0:
                raise HttpError(400, "max_limit must be greater than 0")
            if limit > self.max_limit:
                limit = self.max_limit
        if offset is not None:
            if offset < 0:
                raise HttpError(400, "offset must be greater than or equal to 0")
            if offset > self.max_offset:
                raise HttpError(400, "offset must be less than or equal to max_offset")
        return super().paginate_queryset(queryset, request, view, **kwargs)
               