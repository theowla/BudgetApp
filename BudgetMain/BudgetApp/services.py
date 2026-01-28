from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .models import Income, Expenses, Savings, Withdraw_Savings

def withdraw_from_savings(*, amount: int, name: str):
        with transaction.atomic():
            savings_total = Savings.objects.aggregate(total=Sum("amount"))["total"] or 0

            if savings_total < amount:
                raise ValidationError("Not enough savings")
            
            remaining = amount
            savings = Savings.objects.select_for_update().order_by("time")

            for saving in savings:
                if remaining <= 0:
                    break

                if saving.amount <= remaining:
                    remaining -= saving.amount
                    saving.delete()
                else:
                    saving.amount -= remaining
                    saving.save()
                    remaining = 0
            Income.objects.create(name=f"withdraw: {name}",amount=amount,)

def saved(*, amount: int, name: str):
        with transaction.atomic():
            income_total = Income.objects.aggregate(total=Sum("amount"))["total"] or 0

            if income_total < amount:
                raise ValidationError("Not enough income")
            
            remaining = amount
            income = Income.objects.select_for_update().order_by("time")

            for income_item in income:
                if remaining <= 0:
                    break

                if income_item.amount <= remaining:
                    remaining -= income_item.amount
                    income_item.delete()
                else:
                    income_item.amount -= remaining
                    income_item.save()
                    remaining = 0
            Savings.objects.create(name=f"saved: {name}",amount=amount,)

def spent(*, amount: int, name: str):
        with transaction.atomic():
            income_total = Income.objects.aggregate(total=Sum("amount"))["total"] or 0
            expenses_total = Expenses.objects.filter(paid=True).aggregate(total=Sum("amount"))["total"] or 0

            if income_total < amount:
                raise ValidationError("Not enough income")
            
            remaining = amount
            income = Income.objects.select_for_update().order_by("time")
            expenses = Expenses.objects.filter(paid=True).select_for_update().order_by("time")
            
            for expenses_total in expenses:
                if remaining <= 0:
                    break
                if expenses_total.amount <= remaining:
                    remaining -= expenses_total.amount
                    expenses_total.delete()
                else:
                    expenses_total.amount -= remaining

                    expenses_total.save()
                    remaining = 0

            remaining = amount

            for income_item in income:
                if remaining <= 0:
                    break

                if income_item.amount <= remaining:
                    remaining -= income_item.amount

                    income_item.delete()
                else:
                    income_item.amount -= remaining

                    income_item.save()
                    remaining = 0
