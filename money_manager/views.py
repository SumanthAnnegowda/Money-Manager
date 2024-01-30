from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_access_policy import AccessPolicy, AccessViewSetMixin


class ReadOnlyAccessPolicy(AccessPolicy):
    statements = [
        {
            "action":["<method:post>","<method:put>","<method:delete>"],
            "principal":"admin",
            "effect":"allow",
        },
        {
            "action":["<method:get>"],
            "principal":"authenticated",
            "effect":"allow",
        },
    ]


class IncomeCategoryList(generics.ListCreateAPIView):
    queryset = Income_Category.objects.all()
    serializer_class = IncomeCategorySerializer


class IncomeCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income_Category.objects.all()
    serializer_class = IncomeCategorySerializer


class ExpenseCategoryList(generics.ListCreateAPIView):
    queryset = Expense_Category.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense_Category.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseSubcategoryList(generics.ListCreateAPIView):
    queryset = Expense_Subcategory.objects.all()
    serializer_class = ExpenseSubcategorySerializer


class ExpenseSubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense_Subcategory.objects.all()
    serializer_class = ExpenseSubcategorySerializer


class ExpenseList(AccessViewSetMixin, generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    access_policy  = ReadOnlyAccessPolicy

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Expense.objects.all()
        return Expense.objects.filter(owner=user)
        

class ExpenseDetail(AccessViewSetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    access_policy= ReadOnlyAccessPolicy


class IncomeList(AccessViewSetMixin,generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    access_policy = ReadOnlyAccessPolicy

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Income.objects.all()
        return Income.objects.filter(owner=user)

class IncomeDetail(AccessViewSetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    access_policy = ReadOnlyAccessPolicy
    