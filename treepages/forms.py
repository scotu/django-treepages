from django import forms
# TODO: remove unused widgets
from admin_upload.widgets import WYMEditorUpload
#from django_rte_widgets.wmd import WmdTextarea
#from tinymce.widgets import TinyMCE
from treepages.models import Page

class PageAdminModelForm(forms.ModelForm):
    body = forms.CharField(required=False, widget=WYMEditorUpload())

    class Meta:
        model = Page
