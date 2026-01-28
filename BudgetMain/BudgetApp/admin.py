from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Expenses, Income, Savings, Withdraw_Savings
from .services import withdraw_from_savings, saved, spent

# Register your models here.
admin.site.register(Income)

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        
        if change:
            old = Expenses.objects.get(pk=obj.pk)

            if not old.paid and obj.paid:
                print("🔥 paid changed in admin")

                # call the service
                spent(
                    amount=obj.amount,
                    name=obj.name,
                )
        super().save_model(request, obj, form, change)

@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        if change:
            raise ValidationError("Cannot edit transactions")
        
        # save first
        super().save_model(request, obj, form, change)

        # call the service
        saved(
            amount=obj.amount,
            name=obj.name,
        )

@admin.register(Withdraw_Savings)
class WithdrawSavingsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        if change:
            raise ValidationError("Cannot edit transactions")
        
        # save the withdrawal first
        super().save_model(request, obj, form, change)

        # call the service
        withdraw_from_savings(
            amount=obj.amount,
            name=obj.name,
        )
