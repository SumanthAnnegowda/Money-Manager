from rest_framework import serializers
from .models import Income_Category, Income, Expense_Category, Expense_Subcategory, Expense


class IncomeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Income_Category
        fields = '__all__'


class ExpenseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense_Category
        fields = '__all__'


class ExpenseSubcategorySerializer(serializers.ModelSerializer):
    #category = ExpenseCategorySerializer()

    class Meta:
        model = Expense_Subcategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    #category = ExpenseCategorySerializer()
    #sub_category = ExpenseSubcategorySerializer()

    class Meta:
        model = Expense
        fields = '__all__'

    def validate_amount(self, attrs):
        if attrs <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return attrs

    def validate(self, attrs):
        if attrs["expense_category"] == 'others' and not attrs["expense_category_detail"]:
            raise serializers.ValidationError("Expense category detail is required for 'Others' category.")
        return attrs
    

class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
