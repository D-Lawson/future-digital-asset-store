from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """ Form customisations """
    class Meta:
        """ Fields to customise """
        model = Order
        fields = ('full_name', 'phone_number',
                  'address_line_1', 'address_line_2',
                  'town_or_city', 'county', 'country', 'postcode', 'email',)

    def __init__(self, *args, **kwargs):
        """
        Apply placeholder text and classes to form.  Remove labels and set the
        autofocus.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'address_line_1': 'Address line 1',
            'address_line_2': 'Address line 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'country': 'Country',
            'postcode': 'Post Code',
            'email': 'Email Address',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-input-style'
            self.fields[field].label = False
