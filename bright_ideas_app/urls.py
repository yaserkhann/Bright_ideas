from typing import ValuesView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('bright_ideas', views.ideas),
    path('login', views.login),
    path('logout', views.logout),
    path('post_idea', views.post_idea),
    path('add_like/<int:idea_id>', views.add_like),
    path('post/<int:idea_id>', views.detail),
    path('user/<int:user_id>', views.user_detail),
    path('delete/<int:idea_id>', views.delete),
    path('edit/<int:idea_id>', views.edit),
    path('update_idea/<int:idea_id>', views.update_idea),
    path('update_user/<int:user_id>', views.update_user)
]
