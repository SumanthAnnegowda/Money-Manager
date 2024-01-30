from django.urls import path, include
from money_manager import views

urlpatterns = [
    path('income/category', views.IncomeCategoryList.as_view()),
    path('income/category/<int:pk>', views.IncomeCategoryDetail.as_view()),
    path('expense/category', views.ExpenseCategoryList.as_view()),
    path('expense/category/<int:pk>', views.ExpenseCategoryDetail.as_view()),
    path('expense/subcategory', views.ExpenseSubcategoryList.as_view()),
    path('expense/subcategory/<int:pk>', views.ExpenseSubcategoryDetail.as_view()),
    path('expense', views.ExpenseList.as_view()),
    path('expense/<int:pk>', views.ExpenseDetail.as_view()),
    path('income', views.IncomeList.as_view()),
    path('income/<int:pk>', views.IncomeDetail.as_view()),
]