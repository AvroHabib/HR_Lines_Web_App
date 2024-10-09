# urls.py
from django.urls import path
from .views import add_vessel
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('add-vessel/', views.add_vessel, name='add_vessel'),
    path('cce_table/', views.cce_table, name='cce_table'),
    path('predict/', views.predict_etb, name='predict'),
]
