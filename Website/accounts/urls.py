from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns =[
    path('signup/',views.user_signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_profile,name='profile'),
    path('update/',views.user_update,name='update'),
    path('change/',views.password_change,name='password_change'),
    path('active/<uidb64>/<toke>/',views.RegisterEmail.as_view(),name='active'),
    path('reset/',views.ResetPassword.as_view(),name='reset'),
    path('reset/done/',views.DonePassword.as_view(),name='reset_done'),
    path('confirm/<uidb64>/<token>/',views.ConfirmPassword.as_view(),name='password_reset_confirm'),
    path('confirm/done/',views.Complete.as_view(),name='complete'),
    path('favorite/',views.favorite,name='favorite'),
    path('history/',views.history,name='history'),
]