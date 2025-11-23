from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.current_user, name='current_user'),
    path('auth/google/', views.google_auth, name='google_auth'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    # Settings
    path('settings/change-password/', views.change_password, name='change_password'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
    
    # Dataset operations
    path('upload/', views.upload_dataset, name='upload_dataset'),
    path('datasets/', views.list_datasets, name='list_datasets'),
    path('datasets/<int:dataset_id>/', views.dataset_detail, name='dataset_detail'),
    path('datasets/<int:dataset_id>/summary/', views.dataset_summary, name='dataset_summary'),
    path('datasets/<int:dataset_id>/report/', views.generate_report, name='generate_report'),
    path('datasets/<int:dataset_id>/delete/', views.delete_dataset, name='delete_dataset'),
]