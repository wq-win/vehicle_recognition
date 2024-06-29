from django.urls import path

from Vehicle import views

urlpatterns = [
    path('index/', views.index, name='index'),

    path('search/', views.search, name='search'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('add/', views.add, name='add'),
    path('checkplate/', views.check_plate, name='check_plate'),

    path('addroad/', views.add_road, name='add_road'),
    path('updateroad/', views.update_road, name='update_road'),
    path('saveroad/', views.save_road, name='save_road'),
    path('deleteroad/', views.delete_road, name='delete_road'),
    path('predict/', views.predict, name='predict'),
]