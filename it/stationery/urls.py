from stationery import views
from django.urls import path, re_path

urlpatterns = [
 path('',views.index),
 path('index',views.index),
 path('stat_list',views.stat_list),
 path('stat_apply_index',views.stat_apply_index) ,
 path('order_detail',views.order_detail),
 path('add_to_cart', views.add_to_cart),
 path('clean_cart', views.clean_cart),
 path('submit_cart', views.submit_cart),
 path('complete_order',views.complete_order),
 path('apply_login', views.apply_login),
 path('ajax',views.ajax),

]