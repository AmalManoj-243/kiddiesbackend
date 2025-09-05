from .views import leaderboard
from django.urls import path
from .views import register, login_view, profile, reset_password, home, view_ticket, my_gifts, gift_ticket, gift_settings, send_gift, accept_gift, award_share_points, share_and_earn, invite_referral, movie_quiz, emoji_guess, movie_trivia, box_office_prediction, spin_wheel, games
from .views import memory_match
from django.urls import path
from .views import register, login_view, profile, reset_password, home, view_ticket, my_gifts, gift_ticket, gift_settings, send_gift, accept_gift, award_share_points, share_and_earn, invite_referral, dart_throw, update_coins
from django.contrib.auth import views as auth_views
from .views import music_lounge, upload_music
from . import views
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

def kids_logout(request):
     auth_logout(request)
     return redirect('login')

class CustomLogoutView(auth_views.LogoutView):
     def get(self, request, *args, **kwargs):
          return self.post(request, *args, **kwargs)

urlpatterns = [
     path('',home,name='home'),
     path('register/', register, name='register'),
     path('login/', login_view, name='login'),
     path('profile/', profile, name='profile'),
     path('reset-password/', reset_password, name='reset-password'),
     path('logout/', kids_logout, name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('view-ticket/<int:booking_id>/', view_ticket, name='view_ticket'),
    path('gifts/', my_gifts, name='my_gifts'),
    path('gift-ticket/<int:booking_id>/', gift_ticket, name='gift_ticket'),
     path('post_login_redirect/', views.post_login_redirect, name='post_login_redirect'),
    path('gift-settings/', gift_settings, name='gift_settings'),
    path('send-gift/', send_gift, name='send_gift'),
    path('accept-gift/<int:gift_id>/', accept_gift, name='accept_gift'),
     path('award-share-points/', award_share_points, name='award_share_points'),
     path('share-and-earn/', share_and_earn, name='share_and_earn'),
          path('switch-mode/', views.switch_mode, name='switch_mode'),
     path('invite/<str:referral_code>/', invite_referral, name='invite_referral'),
     # Chatbot URLs removed
     path('movie-quiz/', movie_quiz, name='movie_quiz'),
     path('emoji-guess/', emoji_guess, name='emoji_guess'),
     path('movie-trivia/', movie_trivia, name='movie_trivia'),
     path('box-office-prediction/', box_office_prediction, name='box_office_prediction'),
     path('spin-wheel/', spin_wheel, name='spin_wheel'),
     path('games/', games, name='games'),
          path('memory-match/', memory_match, name='memory_match'),
          path('leaderboard/', leaderboard, name='leaderboard'),
          path('dart-throw/', dart_throw, name='dart_throw'),
          path('update_coins/', update_coins, name='update_coins'),
          path('music/', music_lounge, name='music_lounge'),
          path('music/upload/', upload_music, name='music-upload'),
]
