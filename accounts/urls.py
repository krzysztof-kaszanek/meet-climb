from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.create_new_user, name='signup'),
]