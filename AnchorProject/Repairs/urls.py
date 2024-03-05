from django.urls import path
from . import views

# in each usl pass the prefix you want for the rout, the name of the function in the views and the name youll use when you want to render it
urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login_user, name= 'login'),
    path('logout/', views.logout_user, name= 'logout'),
    path('register/', views.register_user, name= 'register'),
    path('mecanic/', views.view_mec, name= 'mecanic'),
    path('userowner/', views.view_owner, name= 'owner'),
    path('userpost/', views.post, name= 'userpost'),
    path('postdetail/<int:id>/', views.post_detail, name= 'postdetail'),



]
