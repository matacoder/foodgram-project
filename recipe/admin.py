from django.contrib import admin

from recipe.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
