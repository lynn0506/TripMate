from django.urls import path
from feeds import views 


urlpatterns = [
    path('', views.start, name="start"),
    path('main/', views.main, name="main"),
    path('main/<int:num>/', views.main, name="main"),
    path('mypage/', views.mypage, name="mypage"),
    path('mypage_detail/<str:place>', views.mypage_detail, name="mypage_detail"),
    path('mypage_detail_edit/<str:place>', views.mypage_detail_edit, name="mypage_detail_edit"),
    path('mypage_edit/', views.mypage_edit, name='mypage_edit'),
    path('select/', views.select_place, name="select_place"),
    path('select/<str:place>/', views.select_detail_1, name="select_detail_1"),
]