from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

# based on http://www.djangosnippets.org/snippets/1261/
class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'treepages/jpicker/css/jPicker-1.0.13.min.css',
            )
        }
        js = (
            settings.STATIC_URL + 'treepages/jquery-1.3.2.min.js',
            settings.STATIC_URL + 'treepages/jpicker/jpicker-1.0.13.min.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
$(document).ready(function(){

$('#id_%(name)s').jPicker(
{
window:{title: 'Scegli il colore',position:{y:'center'}},
color:{mode:'h'},
images:{clientPath:'%(STATIC_URL)streepages/jpicker/images/'},
localization:{
    text:
    {
      title: 'Scegli un colore',
      newColor: 'nuovo',
      currentColor: 'attuale',
      ok: 'OK',
      cancel: 'Annulla'
    }
  }
});
/* fix for django-admin */
$('.jPicker_Picker').parent().parent('.form-row').css('overflow', 'visible');
});
</script>''' % {"name":name, "STATIC_URL":settings.STATIC_URL})
