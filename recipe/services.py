from decimal import Decimal

from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from recipe.models import Ingredient, Amount


def save_form_m2m(request, form):
    # https://docs.djangoproject.com/en/3.1/topics/db/transactions/#controlling-transactions-explicitly
    try:
        with transaction.atomic():
            # prepare Recipe object to save
            form.instance.author = request.user
            form.save()

            # prepare M2M through table Amount to save
            ingredients = get_ingredients_from(request.POST)
            amounts = check_and_convert_to_objects(ingredients, form)
            Amount.objects.bulk_create(amounts)
            form.save_m2m()
            return form
    except IntegrityError:
        raise HttpResponseBadRequest


def get_ingredients_from(post):
    ingredients = {}
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            value = key.replace('name', 'value')
            ingredients[name] = post[value]
    return ingredients


def check_and_convert_to_objects(ingredients, recipe):
    amounts = []
    for name, amount in ingredients:
        amount = Decimal(amount.replace(',', '.'))
        ingredient = get_object_or_404(Ingredient, name=name)
        amounts.append(Amount(recipe=recipe, ingredient=ingredient, amount=amount))
    return amounts
