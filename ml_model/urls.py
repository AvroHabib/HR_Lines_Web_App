# urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('cce_table/', views.cce_table, name='cce_table'),
    path('predict/', views.predict_etb, name='predict'),
]
