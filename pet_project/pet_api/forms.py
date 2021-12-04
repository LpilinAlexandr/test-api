from django import forms

from . import models as api_models


class PetForm(forms.ModelForm):
    """Create the pet."""

    class Meta:
        model = api_models.Pet
        fields = ('name', 'age', 'kind')


class PetListForm(forms.Form):
    """Validation the params for getting pets list."""

    limit = forms.IntegerField(required=False)
    offset = forms.IntegerField(required=False)
    has_photos = forms.BooleanField(required=False)

    def clean_has_photos(self):
        if 'has_photos' in self.data:
            return self.cleaned_data['has_photos']

    def clean(self):
        return {key: value for key, value in self.cleaned_data.items() if value is not None}
