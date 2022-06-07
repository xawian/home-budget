from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page,name="login"),
    path('register/',views.register_page,name="register"),
    path('logout/',views.logout_user,name="logout"),
    path('elo/',views.get_data,name="get_data"),
    path('elo2/',views.get_data_earnings,name="get_data_earnings"),
    path('', views.budget_view,name="budget_view"),
    path('budget/',views.budget_view,name="budget_view"),
    path('analise/',views.analise,name="analise"),
    path('analise_earnings/',views.analise_earnings,name="analise_earnings"),
    path('create_expense',views.create_expense,name="create_expense"),
    path('create_expense_category',views.create_expense_category,name="create_expense_category"),
    path('create_earning_category',views.create_earning_category,name="create_earning_category"),
    path('create_earning',views.create_earning,name="create_earning"),
    path('update_expense/<str:pk>/',views.update_expense,name="update_expense"),
    path('update_earning/<str:pk>/',views.update_earning,name="update_earning"),
    path('delete_expense/<str:pk>/',views.delete_expense,name="delete_expense"),
    path('delete_earning/<str:pk>/',views.delete_earning,name="delete_earning"),
    path('pdf/',views.pdf,name="pdf"),
]