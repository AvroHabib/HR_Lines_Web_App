# urls.py
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('cce_table/', views.cce_table, name='cce_table'),
    path('predict/', views.predict_etb, name='predict'),
    path('edit_record/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
    path('item_list/', views.item_list, name='item_list'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('line-chart/', views.line_chart_view, name='line_chart'),
    path('histogram/', views.histogram_view, name='histogram_view'),
    path('piechart/', views.pie_chart_view, name='pie_chart_view'),
    path('analytics/', views.chart_view, name='chart_view'),
    path('page/',views.card_list,name='card_list'),
    path('page_filter/',views.page_view,name='card_list_filter'),
    path('add-vessels/', views.add_vessels, name='add_vessels'), 
    path('remove-vessel/',views.remove_vessel,name='remove_vessel'),
    path('update-vessel-service/', views.update_vessel_service, name='update_vessel_service'),
    path('show-cce-vessel/', views.show_cce_vessel, name='show_cce_vessel'),
    path('show-bes-vessel/', views.show_bes_vessel, name='show_bes_vessel'),
    path('set-cce-rv/', views.cce_rv, name='cce_rv'),
    path('set-bes-rv/', views.bes_rv, name='bes_rv'),
    path('show-schedule/', views.show_schedule, name='show_schedule'),
    path('show-bes/', views.show_bes, name='show_bes'),
    path('reset-db/', views.db_reset, name='reset_db'),
    path('generate-schedule/', views.generate_table_n_months, name='generate_table_n_months'),
    path('set-voyage-complete/',views.set_voyage_complete,name='set_voyage_complete'),
]


