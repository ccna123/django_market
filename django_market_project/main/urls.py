from django.urls import path
from main import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('market/', views.market_page, name='market-page'),
    path('register/', views.register_page, name='register-page'),
    path('login/', views.login_page, name='login-page'),
    path('logout/', views.logout_page, name='logout-page'),
    path('dashboard/', views.dashboard_page, name='dashboard-page'),
    path('info/<str:item_name>/', views.info_page, name='info-page'),
    path('review/<str:item_name>/', views.review, name='review-page'),

]