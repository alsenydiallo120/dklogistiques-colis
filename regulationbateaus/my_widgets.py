from django import forms

class CustomSelect(forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), modify_choices=()):
        super(CustomSelect, self).__init__(attrs, choices=choices)
        self.modify_choices = modify_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(CustomSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        for a, b, c,d, e, f in self.modify_choices:
            if value == a:
                option['attrs']['data-expeditaire'] = b
                option['attrs']['data-destinataire'] = c
                option['attrs']['data-montant'] = d
                option['attrs']['data-paye'] = e
                option['attrs']['data-reste'] = f
        return option