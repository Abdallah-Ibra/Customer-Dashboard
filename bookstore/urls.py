from django.urls import path
from bookstore import views

from django.contrib.auth import views as authviews

urlpatterns = [
   
   path('', views.home, name='home'),
   path('books/', views.books, name='books'),
   # path('customer/', views.customer, name='customer'),
   path('customer/<str:pk>', views.customer, name='customer'),
   # path('create/', views.create, name='create'),
   path('create/<str:pk>', views.create, name='create'),
   path('update/<str:pk>', views.update, name='update'),
   path('delete/<str:pk>', views.delete, name='delete'),
   path('register',views.register,name='register'),
   path('login',views.userLogin,name='login'),
   path('logout',views.userLogout,name='logout'),
   path('user',views.userProfile,name='user_profile'),
   path('profile',views.profileInfo,name='profile_info'),
   
   
   
   path('reset_password/', authviews.PasswordResetView.as_view(template_name= "password_reset.html"), name="reset_password"),
   path('reset_password_sent/', authviews.PasswordResetDoneView.as_view(template_name= "password_reset_sent.html"), name="password_reset_done"),
   path('reset/<uidb64>/<token>/', authviews.PasswordResetConfirmView.as_view(template_name= "password_reset_form.html"), name="password_reset_confirm"),
   path('reset_password_complete/', authviews.PasswordResetCompleteView.as_view(template_name= "password_reset_done.html"), name="password_reset_complete"),
   
]


