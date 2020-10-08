from django.urls import path
from accounts import views 

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signup/check/', views.check, name="check"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('check/', views.check, name="check"),
    # path('useredit/', views.user_edit, name="user_edit"),
    # path('userinfo/', views.user_info, name="user_info"),
    path('notice/', views.notice, name="user_notice"),
    path('chatlist/<int:id>/', views.chatlist, name='chatlist'),
    path('follow_trip/<int:pk>/<int:tid>/<int:num>/', views.follow_trip, name="follow_trip"),
    path('unfollow_trip/<int:pk>/<int:tid>/<int:num>/', views.unfollow_trip, name="unfollow_trip"),

    path('chatroom/<int:rid>/', views.chatroom, name="chatroom"),
    path('chatroom/<int:rid>/<int:id>/', views.send_message, name="send_message"),

]

# <int:pk>/<int:tid>/<int:num>