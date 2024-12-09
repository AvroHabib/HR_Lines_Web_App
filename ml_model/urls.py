# urls.py
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('vessel-schedule/', views.vessel_schedule, name='vessel_schedule'),
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
    path('add-vessels/', views.add_vessels, name='add-vessels'), 
    path('remove-vessel/',views.remove_vessel,name='remove-vessel'),
    path('update-vessel-service/', views.update_vessel_service, name='update-vessel-service'),
    path('show-cce-vessel/', views.show_cce_vessel, name='show_cce_vessel'),
    path('show-bes-vessel/', views.show_bes_vessel, name='show_bes_vessel'),
    path('set-cce-rv/', views.cce_rv, name='set-cce-rv'),
    path('set-bes-rv/', views.bes_rv, name='set-bes-rv'),
    path('show-schedule/', views.show_schedule, name='show_schedule'),
    path('show-cce-complete/', views.show_cce_complete, name='show_cce_complete'),
    path('show-bes/', views.show_bes, name='show_bes'),
    path('show-bes-complete/', views.show_bes_complete, name='show_bes_complete'),
    path('reset-db/', views.db_reset, name='reset_db'),
    path('reset-db-complete/', views.db_reset_complete, name='reset_db_complete'),
    path('generate-schedule/', views.generate_table_n_months, name='generate-schedule'),
    path('set-voyage-complete/',views.set_voyage_complete,name='set_voyage_complete'),
    path('view-bes/',views.bes_view,name='view-bes'),
    path('view-cce/',views.cce_view,name='view-cce'),
    path('get-all-columns-bes/',views.get_all_columns_bes,name='get_all_columns_bes'),
    path('get-all-columns-cce/',views.get_all_columns_cce,name='get_all_columns_cce'),
    path('update-bes-complete/',views.update_bes_complete,name='update_bes_complete'),
    path('update-cce-complete/',views.update_cce_complete,name='update_bes_complete'),
    path('reset-page/',views.reset_page,name='reset-page'),
    path('get-all-vessel/',views.get_all_vessel,name='get_all_vessel'),
    path('remove-page/',views.remove_vessel_page,name='remove-page'),

]


