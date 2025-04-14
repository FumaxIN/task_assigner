import random
import string
from django.db.models import Case, When, Value, IntegerField, F, ExpressionWrapper


def get_random_string(length: int) -> str:
    return "".join(random.choices(string.hexdigits, k=length))



def null_if_zero(expression):
    return Case(
        When(expression=0, then=Value(1)),  # avoid zero by setting dummy denominator
        default=expression,
        output_field=IntegerField()
    )