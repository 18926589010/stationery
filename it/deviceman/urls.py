from django.urls import path, re_path

from . import views, testdb, pyechart, totalechart, excel, tests

urlpatterns = [
    path('', pyechart.index),
    path('index', pyechart.index),
    path('total', views.total ),
    path('pc_list', views.pc_list, name='pc_list'),
    path('user_list', views.user_list, name='user_list'),
    path('dept_list', views.dept_list, name='dept_list'),
    path('hello', views.hello, name='hello'),
    #path('searchuser', views.searchuser,),
    re_path(r'search', views.search),
    re_path('showusers', views.showusers),
    path('display_pc', testdb.display_pc),
    path('display_user', testdb.display_user),
    #path('get_username_from_pcid', testdb.get_username_from_pcid),
    path('update_pc', testdb.update_pc),
    path('newdevice', testdb.newdevice),
    path('adddevice', testdb.adddevice),
    path('pccreate', testdb.pccreate),
    path('pcedit', testdb.pcedit),
    path('usercreate', testdb.usercreate),
    path('useredit', testdb.useredit),
    path('borrowscreate', testdb.borrowscreate),
    path('borrowsedit', testdb.borrowsedit),
    path('totalchart', totalechart.totalchart),
    path('report', testdb.report),
    path('exportxls', excel.export_xls),
    path('map', testdb.planmap),
    path('gps', testdb.gps),
    path('test',tests.test_update_user),
    path('userid',tests.get_user_id),


]

