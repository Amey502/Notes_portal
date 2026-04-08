from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('create-team/', views.create_team, name='create_team'),
    path('team/<str:team_id>/', views.team_detail, name='team_detail'),
    path('team/<str:team_id>/join/', views.join_team, name='join_team'),
    path('post/delete/<str:post_id>/', views.delete_post, name='delete_post'),
    path('user/toggle-like/<str:post_id>/', views.toggle_like, name='toggle_like'),
    path('post/comment/<str:post_id>/', views.add_comment, name='add_comment'),
    path('post/edit/<str:post_id>/', views.edit_post, name='edit_post'),
    path('search/team/', views.search_team, name='search_team'),
    path('profile/', views.profile, name='profile'),
]