from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class PaginatedSerializer:
    """ Serializer to perform pagination of queryset according to given
    serializer.
    """

    def __init__(
            self, queryset, page, num, serializer_method=None, context=None,
            **kwargs
    ):
        paginator = Paginator(queryset, num)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        count = paginator.count
        previous = None if not objects.has_previous() else \
            objects.previous_page_number()
        next = None if not objects.has_next() else objects.next_page_number()
        if serializer_method:
            serializer = serializer_method(
                objects, many=True, context=context, **kwargs)
            data = serializer.data
        else:
            data = objects.object_list
        self.pages_count = paginator.num_pages
        self.data = {
            'count': count, 'previous': previous, 'next': next, 'result': data}
