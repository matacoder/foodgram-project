from django import forms

from recipe.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("name", "tags", "description", "cook_time", "image",)

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
