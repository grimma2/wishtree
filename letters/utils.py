from django.db.models import QuerySet, Q
from django.views.generic.list import MultipleObjectMixin

from letters.models import Letter


class SearchMethods:

    @staticmethod
    def search_by_child(query_text: str):
        '''
        :return: list Letter instances presented in dict
        '''
        letters = Letter.objects.filter(
            child__name__icontains=query_text
        ).values('pk', 'child__name')

        return list(letters)

    @staticmethod
    def search_by_gift(query_text: str):
        letters = Letter.objects.filter(
            gift__name__icontains=query_text
        ).values('pk', 'gift__name')

        return list(letters)


class FavoritesMixin(MultipleObjectMixin):

    def exclude_favorite_letters(self) -> QuerySet:
        object_list = self.get_queryset()

        if not self.request.user.is_authenticated:
            return object_list

        pks = self.request.user.favorites.values_list('pk', flat=True)
        letters = object_list.filter(~Q(pk__in=pks))

        return letters
