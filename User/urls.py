from django.urls import path

from User import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('homesuper/', views.home_super, name='home_super'),

    path('mine/', views.mine, name='mine'),
    path('minesuper/', views.mine_super, name='mine_super'),
    path('delete/', views.delete, name='delete'),
    path('addition/', views.addition, name='addition'),
    path('search/', views.search, name='search'),
    path('update/', views.update, name='update'),

    path('checkuser/', views.check_user, name='check_user'),
    path('activate/', views.activate, name='activate'),
    path('activatesuper/', views.activate_super, name='activate_super'),
    path('register/', views.register, name='register'),

    # 验证码
    path('getcode/', views.get_code, name='get_code'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]