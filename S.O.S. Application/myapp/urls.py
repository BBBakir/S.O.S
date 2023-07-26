
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path('', views.home, name='sos-home'),
    path('report', views.expense_report, name='expense_report'),
    path('export_percentages/', views.export_percentages, name='export_percentages'),
    path('export_item_costs/', views.export_item_costs, name='export_item_costs'),
    path('export_district_costs/', views.export_district_costs, name='export_district_costs'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),

    path('donations/', views.donation_list_view, name='donations'),
    path('donations/add/', views.donation_create_view, name='donation_add'),
    path('donations/<int:pk>/edit/', views.donation_edit_view, name='donation_edit'),
    path('donations/<int:pk>/delete/', views.donation_delete_view, name='donation_delete'),


    path('logistics/', views.logistics_list_view, name='logistics'),
    path('logistics/<int:pk>/edit/', views.logistics_update_view, name='logistics_edit'),
    path('logistics/<int:pk>/edit/company_edit', views.logistics_edit_company_view, name='company_edit'),
    path('logistics/delete/<int:pk>/', views.logistics_delete, name='logistics_delete'),
    path('delete_request/<int:pk>/', views.delete_request, name='delete_request'),
    path('delete_district/<int:pk>/', views.delete_district, name='delete_district'),
]