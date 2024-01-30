from django.db import models


class Income_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Income Category"


class Expense_Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Expense Category"


class  Expense_Subcategory(models.Model):
    category = models.ForeignKey(Expense_Category, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Expense Subcategory"


class Expense(models.Model):
    date = models.DateField(auto_now=True)
    amount = models.IntegerField()
    Transaction_mode_status = [
        ('online', 'ONLINE'),
        ('cash', 'CASH'),
        ('credit_card', 'CREDIT_CARD')
    ] 
    transaction_mode = models.CharField(max_length = 15, choices = Transaction_mode_status)
    expense_category = models.ForeignKey(Expense_Category, on_delete = models.CASCADE)
    expense_subcategory = models.ForeignKey(Expense_Subcategory, on_delete = models.CASCADE)
    expense_for_status = [
        ('self', 'SELF'),
        ('spouse', 'SPOUSE'),
        ('childern','CHILDERN'),
        ('parents', 'PARENTS'),
        ('in-laws', 'IN-LAWS'),
        ('siblings', 'SIBLINGS'),
        ('friends', 'FRIENDS'),
        ('others', 'OTHERS')
    ]
    expense_for = models.CharField(max_length = 20, choices = expense_for_status)
    comments = models.CharField(max_length = 100, null = True, blank = True)
    expense_category_detail = models.CharField(max_length = 20, null = True, blank = True)
    expense_subcategory_detail = models.CharField(max_length = 20, null = True, blank = True)

    def __str__(self) -> str:
        return str(self.amount) + '->' + self.transaction_mode

    class Meta:
        verbose_name_plural = "Expense"

class Income(models.Model):
    date = models.DateField(auto_now = True)
    amount = models.IntegerField()
    transaction_mode_status = [
        ('online', 'ONLINE'),
        ('cash', 'CASH')
    ]
    transaction_mode = models.CharField(max_length = 20, choices = transaction_mode_status)
    income_category = models.ForeignKey(Income_Category, on_delete = models.CASCADE)
    comments = models.CharField(max_length = 100, null = True, blank = True)

    def __str__(self):
        return str(self.amount) + '->' + self.transaction_mode + '->' + str(self.income_category.id)

    class Meta:
        verbose_name_plural = "Income"
