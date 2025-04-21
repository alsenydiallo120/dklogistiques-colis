from django import forms

class CustomSelect(forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), modify_choices=()):
        super(CustomSelect, self).__init__(attrs, choices=choices)
        self.modify_choices = modify_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(CustomSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        for a, b,c,d in self.modify_choices:
            if value == a:
                option['attrs']['data-nom'] = b
                option['attrs']['data-telephone'] = c
                option['attrs']['data-email'] = d
        return option