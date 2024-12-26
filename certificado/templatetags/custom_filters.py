# meu_app/templatetags/custom_filters.py

from django import template
from datetime import timedelta, date

register = template.Library()

@register.filter
def add_days(value, days):
    """Adiciona um número de dias a uma data"""
    if isinstance(value, date):
        return value + timedelta(days=int(days))
    return value
