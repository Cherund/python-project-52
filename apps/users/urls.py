from django.urls import path
from apps.users import views


urlpatterns = [
    path('', views.UserIndexView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='users_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='users_delete'),

]
