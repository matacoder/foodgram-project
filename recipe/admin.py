from django.contrib import admin

from recipe.models import Amount, Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    pass


class AmountAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ("name",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Recipe, RecipeAdmin)
