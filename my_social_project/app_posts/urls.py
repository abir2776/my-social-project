from app_posts import views
from django.urls import path

app_name = 'app_posts'

urlpatterns = [
    path("",views.home,name='home'),
    path('liked/<pk>/',views.liked,name='liked'),
    path('unliked/<pk>/',views.unliked,name='unliked'),
    path('comment/<pk>/',views.comment,name='comment'),
]
