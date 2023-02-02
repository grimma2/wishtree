from django.urls import path

from .views import *


urlpatterns = [
    path('selected/', user_selected, name='user_selected'),

    # admin paths
    path('admin/letters/<ordering>/', AdminPageLetters.as_view(), name='admin_letters'),
    path('admin/users/', AdminPageUsers.as_view(), name='admin_users'),
    path('clear_user_letters/<int:pk>/', clear_user_letters, name='clear_user_letters'),

    # auth paths
    path('logout/', logout_view, name='logout'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/<uidb64>/<token>/', ConfirmEmail.as_view(), name='do_confirm_email'),
    path('info/email_was_send/', email_was_send, name='email_was_send'),

    path('update/gift/<int:gift_id>/<str:status>/', update_gift),
    path('update/letter/picked_by/<int:pk>/', add_favorite, name='pick_letter'),
    path('excel/save/file/', db_to_excel, name='saveexcel'),
    path('favorites/', favorite_page, name='favorites'),
    path('delete/favorites/<str:favorites>/', remove_list_favorites),
    path('favorites_to_selected/<str:favorites>/', favorites_to_selected),
    path('recommend_goods/<int:gift_pk>/', RecommendGoodsView.as_view(), name='recommend_goods'),
    path('get_recommend_goods/<int:pk>/', get_recommend_goods)
]

app_name = 'usertools'
