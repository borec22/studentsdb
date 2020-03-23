from django import forms
from django.core.urlresolvers import reverse
from .models import StProfile
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Field
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

class PhotoProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = StProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PhotoProfileUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        #import pdb; pdb.set_trace()
        self.helper.form_action = reverse('profile_edit', 
        	kwargs={'pk':kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.form_show_labels = True
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-7'
        self.helper.attrs = {'novalidate': ''}

        #add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('save', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel', _(u'Cancel'), css_class="btn btn-link"),
        ))
	