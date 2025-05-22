from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home/', views.HomeView, name='home'), 
    path("new/", views.create_expense_payment, name="create_expense_payment"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/success/page/", views.payment_success_page, name="payment_success_page"),  
    path("payment/failed/page/", views.payment_failed_page, name="payment_failed_page"),
    
    
    path('',views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    path('expense/', views.expense_list, name='expense_list'),
    path('update/<int:pk>/', views.update_expense, name='update_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('detail/<int:pk>/', views.expense_detail, name='expense_detail'),
]
