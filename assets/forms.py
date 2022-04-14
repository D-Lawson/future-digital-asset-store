from django import forms
from .models import Asset, Category


class AssetForm(forms.ModelForm):
    """
    Update assets
    """
    class Meta:
        """
        Form for adding assets
        """
        model = Asset
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        display_names = [(c.id, c.get_display_name()) for c in categories]

        self.fields['category'].choices = display_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'