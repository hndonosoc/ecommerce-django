from django import template

register = template.Library()

@register.filter
def pesos(value):
    try:
        valor = f"${value:,.0f}".replace(",", ".")
        return f"{valor} CLP"
    except (ValueError, TypeError):
        return value