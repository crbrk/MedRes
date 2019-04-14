from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.formats import localize

from .models import Clinic
from .models import Specialist
from .models import Examination
from .models import File
from django.core.exceptions import ValidationError
import magic


class RegisterForm(UserCreationForm):

    def identify(self):
        return "register"

# class DateInput(forms.DateInput):
#     format = '%Y/%m/%d'
#     input_formats = ('%Y/%m/%d',)
#     input_type = 'date'
    # The widget format attribute sets the display format for the field
    # The input_formats attribute lets you define the acceptable formats for date input.

class ClinicForm(ModelForm):

    class Meta:
        model = Clinic
        exclude = ['owner']
        labels = {
            "name": "*** Nazwa",
            'street': "Ulica",
            "street_number": "Numer budynku",
            'city': "Miasto",
            'postal': "Kod pocztowy",
        }


class SpecialistForm(ModelForm):

    class Meta:
        model = Specialist
        exclude = ['owner']
        labels = {
            'name': "Imię",
            "surname": "Nazwisko",
            "specialisation": "*** Specjalizacja"
        }


class ExaminationForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'id': 'datepicker', 'autocomplete': 'off'}), label='*** Data')
    signer = forms.ModelChoiceField(queryset=None, label="*** Lekarz")
    clinic = forms.ModelChoiceField(queryset=None, label="*** Placówka")

    def __init__(self, user, *args, **kwargs):
        super(ExaminationForm, self).__init__(*args, **kwargs)
        self.fields['signer'].queryset = Specialist.objects.filter(owner=user).order_by('specialisation')
        self.fields['clinic'].queryset = Clinic.objects.filter(owner=user).order_by('name')


    class Meta:
        model = Examination
        exclude = ['owner']
        labels = {
            'name': "*** Nazwa",
        }



class MimetypeValidator(object):
    def __init__(self, mimetypes):
        self.mimetypes = mimetypes

    def __call__(self, value):
        try:
            mime = magic.from_buffer(value.read(1024), mime=True)
            if not mime in self.mimetypes:
                raise ValidationError('%s is not an acceptable file type' % value)
        except AttributeError as e:
            raise ValidationError('This value could not be validated for file type' % value)


class FileForm(ModelForm):
    file = forms.FileField(allow_empty_file=False, validators=[MimetypeValidator('application/pdf')],
                           help_text='tylko pliki PDF', label='*** Plik')
    examination = forms.ModelChoiceField(queryset=None, label='*** Badanie')

    def __init__(self, user, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields['examination'].queryset = Examination.objects.filter(owner=user).order_by('-date')

    class Meta:
        model = File
        exclude = ['owner']

