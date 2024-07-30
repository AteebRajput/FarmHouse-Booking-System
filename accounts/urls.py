from django.urls import path
from accounts.views import login_page,register_page,activate_email, my_logout,register_admin,login_admin
urlpatterns = [
    path('login/',login_page,name="login"),
    path('login_admin/',login_admin,name="login_admin"),
    path('logout/',my_logout,name="logout"),
    path('register/',register_page,name="register"),
    path('register_admin/',register_admin,name="register_admin"),
    path('activate/<email_token>/' , activate_email , name="activate_email"),
] 