from django.urls import path
from Home.urls import urlpatterns
from . import views

urlpatterns =[
    path('admin_login', views.AdminLoginView.as_view(), name='admin_login'),
    path('admin_logout', views.AdminLogoutView.as_view(), name='admin_logout'),
    path('admin_home', views.AdminHomeView.as_view(), name="admin_home"),
    path('financial_management',views.FinancialManagement.as_view(), name='financial_management'),
    path('user/', views.usr_mng, name="user_management"),
    path('notification_management',views.NotifcationManagement.as_view(),name='notification_management'),
    path('user/add/', views.add_user, name='add_user'),
    path('user/edit/<int:pk>/', views.edit_user, name='edit_user'),
]