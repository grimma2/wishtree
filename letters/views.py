from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView

from .models import Gift
from .utils import Letter, SearchMethods, FavoritesMixin


def index(request):
    if request.user.is_staff:
        return redirect('usertools:admin_letters', ordering='all')

    letters = Letter.objects.all()
    if request.user.is_authenticated:
        pks = request.user.favorites.values_list('pk', flat=True)
        letters = letters.filter(~Q(pk__in=pks))

    return render(request, 'letters/index.html', {'letters': letters})


class LetterList(FavoritesMixin, ListView):
    model = Letter
    template_name = 'letters/letters.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ordering = self.kwargs['ordering']
        letters = self.exclude_favorite_letters()
        if not ordering == 'all':
            letters = letters.filter(gift__status=Gift.GIFT_STATUS_CHOICES[int(ordering)][0])
        context['letters'] = letters
        context['ordering'] = ordering

        return context


class SearchLettersAdmin(SearchMethods, View):

    def get(self, request, query_text):
        letters_by_user = self.search_by_user(query_text)
        letters_by_child = self.search_by_child(query_text)
        letters_by_gift = self.search_by_gift(query_text)

        return JsonResponse(
            {
                'letters_by_user': letters_by_user,
                'letters_by_child': letters_by_child,
                'letters_by_gift': letters_by_gift
            }
        )

    @staticmethod
    def search_by_user(query_text):
        letters = Letter.objects.filter(
            picked_by__first_name__icontains=query_text
        ).values('pk', 'picked_by__first_name')

        return list(letters)


class SearchLettersUser(SearchMethods, View):

    def get(self, request, query_text):
        letters_by_child = self.search_by_child(query_text)
        letters_by_gift = self.search_by_gift(query_text)

        return JsonResponse(
            {'letters_by_child': letters_by_child, 'letters_by_gift': letters_by_gift, 'letters_by_user': []}
        )


class AdminLetterDetail(DetailView):
    model = Letter
    template_name = 'letters/admin_letter.html'
    context_object_name = 'letter'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse(status=403)
        return super().get(request, *args, **kwargs)


class UserLetterDetail(DetailView):
    model = Letter
    template_name = 'letters/user_letter.html'
    context_object_name = 'letter'

