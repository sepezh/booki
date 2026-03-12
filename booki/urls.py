from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('login_register', views.login_register, name='login_register'),
    path('logout', views.logout_user, name='logout'),
    path('categories', views.categories, name='categories'),
    path('categories/<slug:slug>', views.category_detail, name='category_detail'),
    path('authors', views.authors, name='authors'),
    path('authors/<slug:slug>', views.author_detail, name='author_detail'),
    path('books/<slug:slug>', views.book_detail, name='book_detail'),
    path('user/profile/edit', views.user_profile_edit, name='user_profile_edit'),
    path('user/reservation/<str:code>', views.user_reservation, name='user_reservation'),
    path('user/reservations', views.user_reservation_list, name='user_reservation_list'),
    path('user/reservation/action/<str:code>', views.user_reservation_action, name='user_reservation_action'),
    path('reserve', views.reserve, name='reserve'),
    path('submit_review/<slug:book_slug>', views.submit_review, name='submit_review'),
    # Dashboard
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/reservation/<str:code>', views.dashboard_reservation_detail, name='dashboard_reservation_detail'),
    path('dashboard/reservation/action/<str:code>', views.dashboard_reservation_action, name='dashboard_reservation_action'),
    # Ajax calls
    path('ajax/near-libraries', views.ajax_near_libraries, name='ajax_near_libraries'),
    path('ajax/load-more-reviews/<slug:book_slug>', views.ajax_load_more_reviews, name='ajax_load_more_reviews')
]
