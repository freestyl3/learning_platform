from django import forms

from ..models import Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('name', 'hidden')
