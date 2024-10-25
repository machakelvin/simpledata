from django.urls import path
from . import views
from .views import SignupView, Dashboard, DeleteItem, edit_entry
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='index'),
    path('add/', views.add_entry, name='add_entry'),
    path('filter/', views.filter_data, name='filter_data'),
    path('register/', SignupView.as_view(), name='register'),
    path('detail/<int:id>/', views.entry_detail, name='entry_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('edit-item/<int:entry_id>/', edit_entry, name='edit_entry'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
]
