from django import forms
from tinymce.widgets import TinyMCE
from treepages.models import Page

class PageAdminModelForm(forms.ModelForm):
    body = forms.CharField(required=False, widget=TinyMCE())

    class Meta:
        model = Page
