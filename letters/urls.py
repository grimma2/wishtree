from django.urls import path

from .views import *

urlpatterns = [
    path('letters/<ordering>/', LetterList.as_view(), name='letter_list'),
    path('search/admin/<query_text>/', SearchLettersAdmin.as_view(), name='admin_search'),
    path('search/user/<query_text>/', SearchLettersUser.as_view(), name='user_search'),
    path('letter/admin/<int:pk>/', AdminLetterDetail.as_view(), name='admin_letter'),
    path('letter/user/<int:pk>/', UserLetterDetail.as_view(), name='user_letter'),
]

app_name = 'letters'
