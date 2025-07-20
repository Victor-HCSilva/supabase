from django.urls import path
from .import views


urlpatterns = [
    path('users/',views.get_users,name='users'),
    path('add-user/', views.add_user_api,name='add_user'),
    path('delete-user/', views.delete_user,name='delete_user'),
    path('update/<int:user_id>/', views.update_user_api,name='update'),
]
