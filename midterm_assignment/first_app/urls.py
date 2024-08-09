from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name = 'registerpage'),
    path('login/', views.UserLogin.as_view(), name = 'loginpage'),
    path('logout/', views.user_logout, name = 'logoutpage'),
    path('profile/', views.profile, name = 'profilepage'),
    path('profile/edit/', views.edit_profile, name = 'edit_profile'),
    path('profile/edit/pass_change/', views.ChangePasswordView.as_view(), name = 'pass_change'),
    path('detail_view/<int:id>/', views.CarDetailView.as_view(), name = 'detail_view'),
    path('buy/<int:id>/', views.buy_car, name='buy_car'),
]