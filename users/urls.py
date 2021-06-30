from django.urls import path
from . import views

app_name    = "users"
urlpatterns = [ 
    path('<uuid:pk>/', views.single, name="single"),
    path('follow/<uuid:pk>/', views.follow, name="follow"),
    path('block/<uuid:pk>/', views.block, name="block"),
    path('useredit/', views.useredit, name="useredit"),

]
