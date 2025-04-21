
from django import forms
class CustomSelect(forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), modify_choices=()):
        super(CustomSelect, self).__init__(attrs, choices=choices)
        self.modify_choices = modify_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(CustomSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        for a, b, c,d, e, f, g, h, i, j in self.modify_choices:
            if value == a:
                option['attrs']['data-telephone'] = b
                option['attrs']['data-adresse'] = c
                option['attrs']['data-rue'] = d
                option['attrs']['data-code_postal'] = e
                option['attrs']['data-ville'] = f
                option['attrs']['data-etage'] = g
                option['attrs']['data-code'] = h
                option['attrs']['data-num_app'] = i
                option['attrs']['data-ascenseur'] = j
        return option