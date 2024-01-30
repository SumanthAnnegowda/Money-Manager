from django.contrib import admin
from .models import Income_Category, Expense_Category, Expense_Subcategory, Expense, Income

admin.site.register(Income_Category)
admin.site.register(Expense_Category)
admin.site.register(Expense_Subcategory)
admin.site.register(Expense)
admin.site.register(Income)
