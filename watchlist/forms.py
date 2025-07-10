from django import forms
from .models import WatchItem

class WatchItemForm(forms.ModelForm):
    class Meta:
        model = WatchItem
        fields = ['title', 'type', 'status', 'year', 'genre', 'rating', 'poster', 'cast']
        widgets = {
                'cast': forms.SelectMultiple(attrs={'class': 'select2'})
        }

    def __init__(self, *args, **kwargs):
        super(WatchItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                # يضيف form-control بدون ما يحذف select2
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'    


 
        