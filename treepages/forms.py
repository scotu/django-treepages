from django import forms
from admin_upload.widgets import WYMEditor, WYMEditorUpload
from treepages.models import Page

class PageAdminModelForm(forms.ModelForm):
    body = forms.CharField(required=False, widget=WYMEditorUpload())

    class Meta:
        model = Page
