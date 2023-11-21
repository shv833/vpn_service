from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:site_name>/<path:url>/', views.proxy, name='proxy'),
    path('delete/<int:pk>/', views.delrecord, name='delete'),
    path('add/', views.addrecord, name='add'),

]