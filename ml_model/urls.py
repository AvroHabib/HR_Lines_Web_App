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
    path('edit_record/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
   
    path('item_list/', views.item_list, name='item_list'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('line-chart/', views.line_chart_view, name='line_chart'),
]


