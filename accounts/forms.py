from django import forms
from .models import UserAccount


class UserAccountForm(forms.ModelForm):
    """ Form customisations """
    class Meta:
        """ Fields to customise """
        model = UserAccount
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Apply placeholder text and classes to form.  Remove labels and set the
        autofocus.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_address_line_1': 'Address line 1',
            'default_address_line_2': 'Address line 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County',
            'default_postcode': 'Post Code',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'account-form-input'
            self.fields[field].label = False
